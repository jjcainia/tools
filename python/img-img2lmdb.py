import sys, os, time
from os.path import normpath, join, split
from random import shuffle
import Image
import numpy as np
from scipy import io
import lmdb
import argparse
parser = argparse.ArgumentParser(description='split data to training and testing subset.')
parser.add_argument('--caffe_root', type=str, help='caffe root folder', default='~/caffe/')
parser.add_argument('--txt', type=str, help='txt list file', default='train.txt')
parser.add_argument('--dst', type=str, help='destination dir to save lmdb', default='./lmdb')
args = parser.parse_args()
caffe_root = args.caffe_root
txt_fn = args.txt
dst_dir = args.dst
sys.path.insert(0, join(caffe_root, 'python'))
import caffe

def str_time(sec):
    sec=float(sec)
    if sec>60 and sec<3600:
        return str(sec/60)+'min'
    if sec>3600:
        return str(sec/3600)+'h'
    return str(sec)+'sec'

def make_lmdb_map(txt_list, lmdb_dir = './', mat_field = 'map', shuf = True, mean = None, display = False):
    NUM_IDX_DIGITS = 10
    IDX_FMT = '{:0>%d' % NUM_IDX_DIGITS + 'd}'
    data_dir = os.path.split(txt_list)[0]
    with open(txt_list) as f:
        t = f.readlines()
    if len(t) == 0:
    	print 'empty in', txt_list
    	return
    if shuf:
        print 'shuffling data...'
        shuffle(t)
    imgs = []
    labels = []
    for i in t:
        t1, t2 = i.split()
        imgs.append(normpath(join(data_dir, t1)))
        labels.append(normpath(join(data_dir, t2)))

    lmdb_imgs_dir = os.path.join(lmdb_dir , 'lmdb_imgs')
    lmdb_labels_dir = os.path.join(lmdb_dir , 'lmdb_labels')
    
    # make images db
    if not os.path.exists(lmdb_imgs_dir):
        os.makedirs(lmdb_imgs_dir)
    imgs_db = lmdb.open(lmdb_imgs_dir, map_size=int(1e12))
    print 'converting images to lmdb...'
    t0 = time.time()
    with imgs_db.begin(write=True) as in_txn:
        for idx, img_path in enumerate(imgs):
            if display and (idx+1) % 5 == 0:
                elp = time.time()-t0
                remain = float(elp)/float(idx+1) * float(len(imgs)-idx-1)
                print "%s of %s, %s elapsed, remaining %s, %s per image"%(str(idx+1), str(len(imgs)), str_time(elp), str_time(remain), str_time(elp/(idx+1)))
            img = Image.open(img_path)
            if img is None:
                IOError(img_path + 'not found')
            img = np.array(img, dtype=np.float32)
            if mean is not None:
                img -= mean
            img = img.astype(np.float)
            #rgb to bgr
            if img.ndim == 3:
                img = img.transpose([2, 0, 1])
            else:
                AttributeError("No. of dimensions (%d) not supported." % img.ndim)
            img_data = caffe.io.array_to_datum(img)
            in_txn.put(IDX_FMT.format(idx), img_data.SerializeToString())
    imgs_db.close()

    #now make labels_db
    if not os.path.exists(lmdb_labels_dir):
        os.makedirs(lmdb_labels_dir)
    labels_db = lmdb.open(lmdb_labels_dir, map_size=int(1e12))
    print 'converting label to lmdb...'
    t0 = time.time()
    with labels_db.begin(write=True) as in_txn:
        for idx, label_path in enumerate(labels):
            if display: #and (idx+1) % 5 == 0:
                elp = time.time()-t0
                remain = float(elp)/float(idx+1) * float(len(imgs)-idx-1)
                print "%s of %s, %s elapsed, remaining %s, %s per image"%(str(idx+1), str(len(imgs)), str_time(elp), str_time(remain), str_time(elp/(idx+1)))
            label_img = Image.open(label_path)
            if label_img is None:
                IOError(label_path+' not found!')
            label_data = np.array(label_img, dtype=np.float)
            assert((label_data[:,:,0]-label_data[:,:,1]).sum()==0)
            if label_data.shape[2]>1:
                label_data = label_data[:,:,0]
            while label_data.ndim!=3:
                label_data = np.expand_dims(label_data, axis=0)
            # max_label = label_data.max()
            # label_data[label_data<max_label/2] = np.float(0)
            # label_data[label_data!=0]=np.float(1)
            assert(label_data.ndim==3)
            label_data = caffe.io.array_to_datum(label_data)
            in_txn.put(IDX_FMT.format(idx), label_data.SerializeToString())
    labels_db.close()

if __name__ == '__main__':
    make_lmdb_map(txt_fn, dst_dir, display = True, shuf=True)