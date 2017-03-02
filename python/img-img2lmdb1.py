import sys, os
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
    maps = []
    for i in t:
        t1, t2 = i.split()
        imgs.append(normpath(join(data_dir, t1)))
        maps.append(normpath(join(data_dir, t2)))

    db_path = os.path.join(lmdb_dir , 'lmdb')
    
    #make images db
    if not os.path.exists(db_path):
        os.makedirs(db_path)
    new_db = lmdb.open(db_path, map_size=int(1e12))
    
    with imgs_db.begin(write=True) as in_txn:
        for idx, img_path in enumerate(imgs):
            datum=caffe.proto.caffe_pb2.Datum()
            datum.channels = X.shape[1]
            datum.channels = X.shape[1]        

if __name__ == '__main__':
    make_lmdb_map(txt_fn, dst_dir, display = True, shuf=True)