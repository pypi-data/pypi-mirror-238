import numpy as np


def get_area(box):
    if box[0] > box[2] or box[1] > box[3]:
        print("invalid box encountered, get_area returning 0")
        return 0
    area = (box[2] - box[0] + 1) * (box[3] - box[1] + 1)
    return area


def get_iou(box1, box2):
    box1 = np.array(box1)
    box2 = np.array(box2)

    area1 = get_area(box1)
    area2 = get_area(box2)

    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    if x1 <= x2 and y1 <= y2:
        area_inter = get_area([x1, y1, x2, y2])
    else:
        area_inter = 0

    area_union = area1 + area2 - area_inter

    return area_inter / area_union


def get_match_num(boxes1, boxes2, iou_thresh=0.8):
    boxes1 = np.array(boxes1, dtype=np.float32).reshape([-1, 4]).tolist()
    boxes2 = np.array(boxes2, dtype=np.float32).reshape([-1, 4]).tolist()
    boxes1 = sorted(boxes1, key=lambda x: get_area(x))
    boxes2 = sorted(boxes2, key=lambda x: get_area(x))

    match_n = 0
    while len(boxes1) > 0 and len(boxes2) > 0:
        box1 = boxes1.pop(0)
        j = 0
        while len(boxes2) > j:
            if get_iou(box1, boxes2[j]) > iou_thresh:
                boxes2.pop(j)
                match_n += 1
                break
            j += 1

    return match_n


def get_prf(boxes_gt, boxes_pd, iou_thresh=0.5):
    match_n = get_match_num(boxes_gt, boxes_pd)
    precision_ = match_n / len(boxes_pd)
    recall_ = match_n / len(boxes_gt)
    fmeasure_ = precision_ * recall_ * 2 / (precision_ + recall_)
    return precision_, recall_, fmeasure_


# def get_match_num(gt, pred, iou_thresh=0.8):
#     gt = np.array(gt, dtype=np.float32).reshape([-1, 4])
#     pred = np.array(pred, dtype=np.float32).reshape([-1, 4])
#     gt_idxs = list(range(len(gt)))
#     pd_idxs = list(range(len(pred)))
#     iou_matrix = get_iou_matrix(gt, pred)

#     num_tp = 0
#     while len(gt_idxs) > 0 and len(pd_idxs) > 0:
#         i = gt_idxs.pop()
#         j = 0
#         while len(pd_idxs)>j:
#             if iou_matrix[i, pd_idxs[j]]>iou_thresh:
#                 pd_idxs.pop(j)
#                 num_tp+=1
#                 break
#             j+=1
#     return num_tp


def get_iou_matrix(boxes1, boxes2):
    boxes1 = np.array(boxes1, dtype=np.float32).reshape([-1, 4])
    boxes2 = np.array(boxes2, dtype=np.float32).reshape([-1, 4])
    if len(boxes1) == 0 or len(boxes2) == 0:
        return np.zeros([len(boxes1), len(boxes2)])
    boxes1_area = (boxes1[:, 2] - boxes1[:, 0]) * (boxes1[:, 3] - boxes1[:, 1])
    boxes2_area = (boxes2[:, 2] - boxes2[:, 0]) * (boxes2[:, 3] - boxes2[:, 1])
    inter_x1 = np.maximum(boxes1[:, 0].reshape([-1, 1]), boxes2[:, 0])
    inter_x2 = np.minimum(boxes1[:, 2].reshape([-1, 1]), boxes2[:, 2])
    inter_y1 = np.maximum(boxes1[:, 1].reshape([-1, 1]), boxes2[:, 1])
    inter_y2 = np.minimum(boxes1[:, 3].reshape([-1, 1]), boxes2[:, 3])
    inter_w = inter_x2 - inter_x1
    inter_w = np.clip(inter_w, 0, inter_w.max())
    inter_h = inter_y2 - inter_y1
    inter_h = np.clip(inter_h, 0, inter_h.max())
    inter_area = inter_w * inter_h
    union_area = (boxes1_area.reshape([-1, 1]) + boxes2_area) - inter_area
    iou_matrix = inter_area / union_area
    return iou_matrix


def box2poly(box):
    x1, y1, x2, y2 = box
    poly = [x1, y1, x2, y1, x2, y2, x1, y2]
    return poly


def poly2box(poly):
    poly = np.reshape(poly, [-1, 2])
    box = np.concatenate([np.min(poly, axis=0), np.max(poly, axis=0)])
    return box


def boxes2bbox(boxes):
    boxes = np.array(boxes).reshape([-1, 2])
    return poly2box(boxes)


def nms(dets, scores, thresh):
    dets = np.array(dets).reshape([-1, 4])
    scores = np.array(scores).reshape([-1])
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]

    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    order = scores.argsort()[::-1]

    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])

        w = np.maximum(0.0, xx2 - xx1 + 1)
        h = np.maximum(0.0, yy2 - yy1 + 1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)

        inds = np.where(ovr <= thresh)[0]
        order = order[inds + 1]

    return keep
