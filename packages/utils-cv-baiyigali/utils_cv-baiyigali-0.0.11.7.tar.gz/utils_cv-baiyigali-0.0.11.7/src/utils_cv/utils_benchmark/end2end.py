import pandas as pd
from nltk import edit_distance
import numpy as np
from utils_cv.utils_box import get_iou


def get_match_info(texts_gt, texts_pd, boxes_gt, boxes_pd, ed_thresh=0, iou_thresh=0):
    """
    texts_gt: [text1, text2], ground truth texts on one page
    texts_pd: [text1, text2], predicted texts on one page
    boxes_gt: [box1, box2], ground truth boxes on one page
    boxes_pd: [box1, box2], predicted boxes on one page
    """
    boxes_gt = np.array(boxes_gt, dtype=np.int32).reshape([-1, 4]).copy().tolist()
    boxes_pd = np.array(boxes_pd, dtype=np.int32).reshape([-1, 4]).copy().tolist()
    texts_gt = list(texts_gt)  # copy
    texts_pd = list(texts_pd)
    assert len(texts_gt) == len(boxes_gt)
    assert len(texts_pd) == len(boxes_pd)

    num_tp = 0
    pop_list = []
    unmatch_idxs_gt = list(range(len(texts_gt)))
    unmatch_idxs_pd = list(range(len(texts_pd)))

    i = 0
    while i < len(unmatch_idxs_gt):
        j = 0
        gti = unmatch_idxs_gt[i]
        box_gt = boxes_gt[gti]
        text_gt = texts_gt[gti]
        is_matched = False
        while j < len(unmatch_idxs_pd):
            pdj = unmatch_idxs_pd[j]
            box_pd = boxes_pd[pdj]
            text_pd = texts_pd[pdj]
            if text_gt == text_pd and get_iou(box_gt, box_pd) > iou_thresh:
                unmatch_idxs_gt.pop(i)
                unmatch_idxs_pd.pop(j)
                num_tp += 1
                is_matched = True
                break
            j += 1
        if not is_matched:
            i += 1

    i = 0
    while i < len(unmatch_idxs_gt):
        j = 0
        gti = unmatch_idxs_gt[i]
        box_gt = boxes_gt[gti]
        text_gt = texts_gt[gti]
        is_matched = False
        while j < len(unmatch_idxs_pd):
            pdj = unmatch_idxs_pd[j]
            box_pd = boxes_pd[pdj]
            text_pd = texts_pd[pdj]
            if (
                edit_distance(text_gt, text_pd) <= ed_thresh
                and get_iou(box_gt, box_pd) > iou_thresh
            ):
                unmatch_idxs_gt.pop(i)
                unmatch_idxs_pd.pop(j)
                num_tp += 1
                is_matched = True
                break
            j += 1
        if not is_matched:
            i += 1

    unmatch_list = []
    for i in unmatch_idxs_gt:
        pds = []
        for j in unmatch_idxs_pd:
            iou = get_iou(boxes_gt[i], boxes_pd[j])
            if iou > iou_thresh:
                pds.append([boxes_pd[j], texts_pd[j], iou])
        pds = sorted(pds, key=lambda x: x[2])

        row_dict = {
            "gt": [boxes_gt[i], texts_gt[i]],
            "pds": pds,
        }

        unmatch_list.append(row_dict)

    result = {"match_num": num_tp, "unmatch_list": unmatch_list}
    return result


def get_prf(texts_gt, texts_pd, ed_thresh=0):
    """
    texts_gt: [texts1, texts2], texts1 is ground truth texts on page1
    texts_pd: [texts1, texts2], texts1 is predicted texts on page1
    """
    assert len(texts_gt) == len(texts_pd)

    def prf(gt_n, pd_n, match_n):
        p = pd_n / match_n
        r = gt_n / match_n
        f = p * r * 2 / (p + r)
        return p, r, f

    # per page prf
    gt_n = [len(texts) for texts in texts_gt]
    pd_n = [len(texts) for texts in texts_pd]
    match_n = [
        get_match_num(texts_gt[i], texts_pd[i], ed_thresh=ed_thresh)
        for i in range(len(texts_gt))
    ]
    per_page_prf = [prf(gt_n[i], pd_n[i], match_n[i]) for i in range(len(gt_n))]

    # total average prf
    total_match_n = sum(match_n)
    total_gt_n = sum(gt_n)
    total_pd_n = sum(pd_n)
    precision, recall, fscore = prf(total_gt_n, total_pd_n, total_match_n)

    results = {
        "precision": precision,
        "recall": recall,
        "fscore": fscore,
        "per_page_gt_n": gt_n,
        "per_page_pd_n": pd_n,
        "per_page_match_n": match_n,
        "per_page_prf": per_page_prf,
    }

    return results


def benchmark(df, ed_thresh=0, iou_thresh=0.01):
    """
    df: dataframe must include keys, texts_gt and texts_pd, each row of them represents ground truth and prediction texts in one page
    """
    eps = 1e-12
    df = df.copy()

    def split_and_flat(texts, boxes):
        texts = list(texts)
        boxes = list(boxes)
        texts = [text.split() for text in texts]
        boxes = [[box] * len(texts[i]) for (i, box) in enumerate(boxes)]
        texts = list([text for texts_ in texts for text in texts_])
        boxes = list([box for boxes_ in boxes for box in boxes_])
        return texts, boxes

    assert df["texts_gt"].apply(len).sum() == df["boxes_gt"].apply(len).sum()
    assert df["texts_pd"].apply(len).sum() == df["boxes_pd"].apply(len).sum()

    for i, row in df.iterrows():
        row["texts_gt"], row["boxes_gt"] = split_and_flat(
            row["texts_gt"], row["boxes_gt"]
        )
        row["texts_pd"], row["boxes_pd"] = split_and_flat(
            row["texts_pd"], row["boxes_pd"]
        )

    assert df["texts_gt"].apply(len).sum() == df["boxes_gt"].apply(len).sum()
    assert df["texts_pd"].apply(len).sum() == df["boxes_pd"].apply(len).sum()

    df["match_info"] = df.apply(
        lambda row: get_match_info(
            row["texts_gt"],
            row["texts_pd"],
            row["boxes_gt"],
            row["boxes_pd"],
            ed_thresh=ed_thresh,
            iou_thresh=iou_thresh,
        ),
        axis=1,
    )
    df["match_num"] = df["match_info"].apply(lambda x: x["match_num"])
    df["unmatch_list"] = df["match_info"].apply(lambda x: x["unmatch_list"])
    df["num_pd"] = df["texts_pd"].apply(len)
    df["num_gt"] = df["texts_gt"].apply(len)
    df["precision"] = df["match_num"] / (df[f"num_pd"] + eps)
    df["recall"] = df["match_num"] / (df[f"num_gt"] + eps)
    df["fmeasure"] = (
        2 * df["precision"] * df["recall"] / (df["precision"] + df["recall"] + eps)
    )

    precision_ = df["match_num"].sum() / (df["num_pd"].sum() + eps)
    recall_ = df["match_num"].sum() / (df["num_gt"].sum() + eps)
    fmeasure_ = precision_ * recall_ * 2 / (precision_ + recall_ + eps)

    return precision_, recall_, fmeasure_, df
