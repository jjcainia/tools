#remove fucking bad images
#images with single channel(gray scale image) will be removed as well. 
import shutil, os
from PIL import Image
import numpy as np
import os
import argparse
parser = argparse.ArgumentParser(description='remove bad images in specified folder')
parser.add_argument('--dir', type=str, default='.')
args = parser.parse_args()
txt = open('/tmp/removed_imgs.txt', 'w');
img_dir = os.path.abspath(args.dir)
imgs = [i for i in os.listdir(img_dir) if '.jpg' in i]
n_rm = 0
for idx,i in enumerate(imgs):
    fn = os.path.join(img_dir, i)
    try:
        im = Image.open(fn)
    except IOError:
        os.remove(fn)
        txt.writelines(fn+os.linesep)
        n_rm = n_rm + 1
        print "remove file: "+i+" for bad image file, "+str(n_rm)+'/'+str(idx)
        continue
    try:
        im = np.array(im, dtype=np.float32)
    except SystemError:
        os.remove(fn)
        txt.writelines(fn+os.linesep)
        n_rm = n_rm + 1
        print "remove file: "+i+" for unknown fuck tricks, "+str(n_rm)+'/'+str(idx)
        continue
    if len(im.shape) != 3:
        os.remove(fn)
        txt.writelines(fn+os.linesep)
        n_rm = n_rm + 1
        print "remove file: "+i+" for bad unvalid channel, "+str(n_rm)+'/'+str(idx)

