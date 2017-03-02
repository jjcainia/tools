import numpy as np
from scipy.io import savemat, loadmat
def pr(pred, gt, w=0.5):
    assert(pred.size == gt.size)
    recall = np.float32(0)
    precision = recall
    threshold = recall
    fmeasure = recall
    ap = recall
    n_ground = gt.sum()
    n_correct = recall
    n_predict = recall
    order = pred.argsort()[::-1]
    pred1 = pred[order]

    if n_ground == 0:
        recall = recall
        precision = recall
        threshold = recall
        fmeasure = recall
        ap = recall
        return np.array((recall, precision, threshold, fmeasure, ap))
    for i in range(pred.size):
        thr = pred1[i]
        n_predict = n_predict + 1
        if gt[order[i]]:
            n_correct = n_correct + 1
            ap = ap + n_correct / (i+1)
        rec = n_correct / n_ground
        pre = n_correct / n_predict
        fmea = 2 * n_correct / (w * n_ground + (1 - w) * n_predict)
        if fmea > fmeasure:
            fmeasure = fmea
            precision = pre
            recall = rec
            threshold = thr
    ap = ap / n_ground
    return np.array((recall, precision, threshold, fmeasure, ap))

def thres_at_recall(pred, gt, recall):
    """
    get threshold to satisfy specified recall
    """
    assert(gt.size == pred.size)
    num_sample = gt.size
    pos_idx = np.where(gt != 0)#index of these positive samples
    gt = gt[pos_idx]
    pred = pred[pos_idx].sort()
    return pred[int(num_sample * recall)]

def thres_at_precision(pred, gt, precision)
    """
    get threshold to satisfy specified precision
    """
    assert(gt.size == pred.size)
    num_sample = gt.size
    order = pred.argsort()#ascend order
    pred = pred[order]
    gt = gt[order]
    for s in range(num_sample):
        pred1 = pred[s::]
        gt1 = gt[s::]
        tp = np.count_nonzero(gt1)#true positive
        fp = gt1.size - tp #false positive
        p = np.float32(tp) / gt1.size
        if p >= precision:
            return pred1[s]
    ValueError('?')

def multi_pr(pred, gt, w=0.5):
    assert(pred.shape == gt.shape)
    num_label = pred.shape[1]
    num_sample = pred.shape[0]
    analysis = np.zeros((num_label, 5), np.float32)
    mAP = 0;
    for l in range(num_label):
        analysis[l, :] = pr(pred[:, l], gt[:, l], w)
        mAP = mAP + analysis[l,4] * gt[:,l].sum()
    return analysis

def thres_at_recall(pred, gt, recall):
    assert(pred.shape == gt.shap)
    num_label, num_sample = pred.shape[1], pred.shape[0]
    thres = np.zeros((num_label), dtype=np.float32)
    for l in range(num_label):
        pred1 = pred[:, l]
        gt1 = gt[:, l]
        pos_idx = np.where(gt1 == 1)#index of those positive samples
        gt1 = gt1[pos_idx]
        pred1 = pred1[pos_idx]
        pred1 = pred1.sort()
        thres[l] = pred1[num_sample * (1 - recall)]
    return thres

def thres_at_precision(pred, gt, precision):
    assert(pred.shape == gt.shape)
    num_sample, num_label = pred.shape
    for l in range(num_label):
        pred1 = pred[:, l]
        gt1 = gt[:, l]
        order = pred1.argsort()[::-1]#descend order
        pred1 = pred1[order]
        gt1 = gt1[order]
        thres = np.zeros(num_label, dtype=np.float32)
        for s in range(num_sample):
            tp = np.float32(np.count_nonzero(gt1[0:s+1]))
            fp = np.float32(s+1 - np.count_nonzero(gt1[o:s+1]))
            if tp / np.float32(s) < precision:
                thres[l] = pred1[s]
                continue


