import numpy as np
from scipy.integrate import simps

def iou(box1,box2):
    inter_x1 = max(box1[0],box2[0])
    inter_x2 = min(box1[2],box2[2])
    inter_y1 = max(box1[1],box2[1])
    inter_y2 = min(box1[3],box2[3])
    inter_w = (inter_x2 - inter_x1)
    inter_w = max(inter_w,0)
    inter_h = (inter_y2 - inter_y1)
    inter_h = max(inter_h,0)
    inter_area = inter_w * inter_h
    area1=(box1[2]-box1[0])*(box1[3]-box1[1])
    area2=(box2[2]-box2[0])*(box2[3]-box2[1])
    union_area = (area1+area2) - inter_area
    return inter_area / union_area

def get_precision_recall(gt, pred, iou_thresh=0.8):
    """
    gt,pred: x,y,x,y format
    """
    gt = np.array(gt, dtype=np.float32).reshape([-1, 4])
    pred = np.array(pred, dtype=np.float32).reshape([-1, 4])
    if len(pred) == 0:
        return 0, 0
    gt_area = (gt[:, 2]-gt[:, 0]) * (gt[:, 3]-gt[:, 1])
    pred_area = (pred[:, 2]-pred[:, 0]) * (pred[:, 3]-pred[:, 1])
    inter_x1 = np.maximum(gt[:, 0].reshape([-1, 1]), pred[:, 0])
    inter_x2 = np.minimum(gt[:, 2].reshape([-1, 1]), pred[:, 2])
    inter_y1 = np.maximum(gt[:, 1].reshape([-1, 1]), pred[:, 1])
    inter_y2 = np.minimum(gt[:, 3].reshape([-1, 1]), pred[:, 3])
    inter_w = (inter_x2 - inter_x1)
    inter_w = np.clip(inter_w, 0, inter_w.max())
    inter_h = (inter_y2 - inter_y1)
    inter_h = np.clip(inter_h, 0, inter_h.max())
    inter_area = inter_w * inter_h
    union_area = (gt_area.reshape([-1, 1]) + pred_area) - inter_area
    iou_matrix = inter_area / union_area
#     print(iou_matrix)

#     pred_max = np.max(iou_matrix,axis=0)
#     pred_max=np.tile(pred_max,[iou_matrix.shape[0],1]).reshape([iou_matrix.shape[0],iou_matrix.shape[1]])
#     iou_matrix=np.where(iou_matrix==pred_max,iou_matrix,0)

    iou_mask = np.where(iou_matrix > iou_thresh, np.ones_like(iou_matrix), np.zeros_like(iou_matrix))

    num_tp = np.sum(iou_mask,axis=0)
#     num_tp = np.where(num_tp >= 1, np.ones_like(num_tp), np.zeros_like(num_tp))
    num_tp = np.sum(num_tp)
    
    precision = num_tp / len(pred)
    recall = num_tp / len(gt)
    return precision, recall
def get_iou_matrix(boxes1,boxes2):
    gt = np.array(boxes1, dtype=np.float32).reshape([-1, 4])
    pred = np.array(boxes2, dtype=np.float32).reshape([-1, 4])
    if len(pred) == 0 or len(gt)==0:
        return None
    gt_area = (gt[:, 2]-gt[:, 0]) * (gt[:, 3]-gt[:, 1])
    pred_area = (pred[:, 2]-pred[:, 0]) * (pred[:, 3]-pred[:, 1])
    inter_x1 = np.maximum(gt[:, 0].reshape([-1, 1]), pred[:, 0])
    inter_x2 = np.minimum(gt[:, 2].reshape([-1, 1]), pred[:, 2])
    inter_y1 = np.maximum(gt[:, 1].reshape([-1, 1]), pred[:, 1])
    inter_y2 = np.minimum(gt[:, 3].reshape([-1, 1]), pred[:, 3])
    inter_w = (inter_x2 - inter_x1)
    inter_w = np.clip(inter_w, 0, inter_w.max())
    inter_h = (inter_y2 - inter_y1)
    inter_h = np.clip(inter_h, 0, inter_h.max())
    inter_area = inter_w * inter_h
    union_area = (gt_area.reshape([-1, 1]) + pred_area) - inter_area
    iou_matrix = inter_area / union_area
    return iou_matrix
def compute_nme(preds, gts):
    N=len(preds)
    rmse=np.zeros(N)
    for i in range(len(preds)):
        pts_gt = np.array(gts[i]).reshape([-1,2])
        pts_pred=np.array(preds[i]).reshape([-1,2])
        L=len(pts_gt)
        if L == 19:  # aflw
            interocular = meta['box_size'][i]
        elif L == 29:  # cofw
            interocular = np.linalg.norm(pts_gt[8, ] - pts_gt[9, ])
        elif L == 68:  # 300w
            # interocular
            interocular = np.linalg.norm(pts_gt[36, ] - pts_gt[45, ])
        elif L == 98:
            interocular = np.linalg.norm(pts_gt[60, ] - pts_gt[72, ])
        elif L == 5:  # cofw
            interocular = np.linalg.norm(pts_gt[0, ] - pts_gt[1, ])
        else:
            raise ValueError('Number of landmarks is wrong')
        rmse[i] = np.sum(np.linalg.norm(pts_pred - pts_gt, axis=1)) / (interocular * L)

    return rmse


def auc(errors, threshold=0.08, step=0.0001, show=False):
    nErrors = len(errors)
    xAxis = list(np.arange(0., threshold + step, step))
    ced = [float(np.count_nonzero([errors <= x])) / nErrors for x in xAxis]
    AUC = simps(ced, x=xAxis) / threshold
    if show:
        plt.plot(xAxis, ced)
        plt.show()
    return AUC
def match_iou(boxes1,boxes2):
    gt = np.array(boxes1, dtype=np.float32).reshape([-1, 4])
    pred = np.array(boxes2, dtype=np.float32).reshape([-1, 4])
    if len(pred) == 0 or len(gt)==0:
        return np.zeros([len(gt),len(pred)])
    gt_area = (gt[:, 2]-gt[:, 0]) * (gt[:, 3]-gt[:, 1])
    pred_area = (pred[:, 2]-pred[:, 0]) * (pred[:, 3]-pred[:, 1])
    inter_x1 = np.maximum(gt[:, 0].reshape([-1, 1]), pred[:, 0])
    inter_x2 = np.minimum(gt[:, 2].reshape([-1, 1]), pred[:, 2])
    inter_y1 = np.maximum(gt[:, 1].reshape([-1, 1]), pred[:, 1])
    inter_y2 = np.minimum(gt[:, 3].reshape([-1, 1]), pred[:, 3])
    inter_w = (inter_x2 - inter_x1)
    inter_w = np.clip(inter_w, 0, inter_w.max())
    inter_h = (inter_y2 - inter_y1)
    inter_h = np.clip(inter_h, 0, inter_h.max())
    inter_area = inter_w * inter_h
    union_area = (gt_area.reshape([-1, 1]) + pred_area) - inter_area
    iou_matrix = inter_area / union_area
    return iou_matrix
def get_match_num(gt, pred, iou_thresh=0.8):
    gt = np.array(gt, dtype=np.float32).reshape([-1, 4])
    pred = np.array(pred, dtype=np.float32).reshape([-1, 4])
    if len(pred) == 0 or len(gt)==0:
        return 0
    iou_matrix = match_iou(gt,pred)
    iou_mask = np.where(iou_matrix > iou_thresh, 1, 0)
    num_tp = np.sum(iou_mask)
    return num_tp