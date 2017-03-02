# convert multi-label annotated data to lmdb
# code written by zk
caffe_root = '~/caffe/'
import sys, os
import Image
from os.path import normpath, join, split
from random import shuffle
import numpy as np
from scipy import io
import lmdb
sys.path.insert(0, join(caffe_root, 'python'))
import caffe
NUM_IDX_DIGITS = 10
IDX_FMT = '{:0>%d' % NUM_IDX_DIGITS + 'd}'
N_LABEL = 198
#options 
txt_fn = 'train_List_v2.txt'
lmdb_dir = '.'
img_root = '.'
mean_val = np.float(125)
with open(txt_fn, 'r') as f:
    t = f.readlines()
n_samples = len(t)
if not os.path.exists(join(lmdb_dir, 'label')):
    os.makedirs(join(lmdb_dir, 'label'))
if not os.path.exists(join(lmdb_dir, 'image')):
    os.makedirs(join(lmdb_dir, 'image'))

label_db = lmdb.open(join(lmdb_dir, 'label'), map_size=int(1e12))
with label_db.begin(write=True) as in_txn:
    label_np = np.zeros([1,1,N_LABEL], dtype=np.float)
    for idx, lb in enumerate(t):
        print 'making labels lmdb, sample ' + str(idx+1) + 'of', str(n_samples)
        labels = t[idx].split()
        for i in range(N_LABEL):
            label_np[0,0,i] = np.float(labels[i + 1])
        label_data = caffe.io.array_to_datum(label_np)
        in_txn.put(IDX_FMT.format(idx), label_data.SerializeToString())
label_db.close()

img_db = lmdb.open(join(lmdb_dir, 'image'), map_size=int(1e12))
with img_db.begin(write=True) as in_txn:
    for idx, img in enumerate(t):
        print 'making images lmdb, sample ' + str(idx+1) + 'of', str(n_samples)
        img_fn = t[idx].split()
        img_fn = img_fn[-1]
        img = Image.open(join(img_root, img_fn))
        if not img:
            IOError('image file'+' '+join(img_root, img_fn)+ 'not found')
        img = np.array(img, dtype=np.float)
        #minus mean
        img -= mean_val
        if img.ndim == 3:
            img = img.transpose([2,0,1])
        else:
            IOError('image'+ ' ' + join(img_root, img_fn) + ': requires ndim=3')
        img_data = caffe.io.array_to_datum(img)
        in_txn.put(IDX_FMT.format(idx), img_data.SerializeToString())
img_db.close()
