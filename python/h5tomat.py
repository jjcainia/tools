from scipy.io import savemat, loadmat
import h5py
mat = 'data/data1.mat'
h5 = 'data/data.h5'
h5f = h5py.File(h5, 'r')
D = dict()
for k in h5f.keys():
	D[k] = h5f[k][...]
	#print mat[k].shape
savemat(mat, D)