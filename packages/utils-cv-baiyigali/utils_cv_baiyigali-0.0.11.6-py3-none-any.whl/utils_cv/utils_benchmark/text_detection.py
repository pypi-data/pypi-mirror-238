import pandas as pd
import numpy as np
from utils_cv.utils_box import get_match_num


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


def benchmark(df, iou_thresh=0.5):
    df = df.copy()
    df["match_num"] = df.apply(
        lambda row: get_match_num(
            row["boxes_gt"], row["boxes_pd"], iou_thresh=iou_thresh
        ),
        axis=1,
    )
    df["pd_num"] = df["boxes_pd"].apply(lambda x: len(x))
    df["gt_num"] = df["boxes_gt"].apply(lambda x: len(x))

    df["precision"] = df["match_num"] / df["pd_num"]
    df["recall"] = df["match_num"] / df["gt_num"]
    df["fscore"] = 2 * df["precision"] * df["recall"] / (df["precision"] + df["recall"])

    precision = df["match_num"].sum() / df["pd_num"].sum()
    recall = df["match_num"].sum() / df["gt_num"].sum()
    fscore = precision * recall * 2 / (precision + recall)

    return precision, recall, fscore, df
