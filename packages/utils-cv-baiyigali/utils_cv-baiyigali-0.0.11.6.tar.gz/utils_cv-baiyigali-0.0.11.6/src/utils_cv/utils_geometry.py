import numpy as np

def pts_to_box(pts):
    pts=np.array(pts).reshape([-1,2])
    box=np.array([np.min(pts,axis=0),np.max(pts,axis=0)]).reshape([4])
    return box

def box_to_pts(box,mode='xyxy'):
    if mode=='xyxy':
        pts = np.array([[box[0], box[1]],[box[2], box[1]],[box[2], box[3]],[box[0], box[3]]])
    else:
        pts = np.array([[box[0], box[1]],[box[2], box[1]],[box[2], box[3]],[box[0], box[3]]])

    return pts
