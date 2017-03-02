from scipy.io import savemat, loadmat
import h5py
mat = 'data/data.mat'
h5 = 'data/data.h5'
mat = loadmat(mat)
fields = [k for k in mat.keys() if '__' not in k]
h5f = h5py.File(h5, 'w')
for f in fields:
	h5f.create_dataset(f, data=mat[f])
h5f.close()