import numpy as np
import cv2
from matplotlib import pyplot as plt
import pandas as pd
import re
from . import utils_image

def show_boxes(im,boxes,size=None,thickness=2):
    im_draw=np.copy(im)
    for box in boxes:
        im_draw=draw_rect(im_draw,box,thickness=thickness)
    if size is not None:
        plt.figure(figsize=size)
    show_image(im_draw)
def show_polys(im,polys,size=None,thickness=2):
    for poly in polys:
        im=draw_poly(im,poly,thickness=thickness)
    if size is not None:
        plt.figure(figsize=(15,15))
    show_image(im)

def show_image(img,title='title',size=None):
    if size is not None:
        plt.figure(figsize=size)
    if len(img.shape)==2 or (len(img.shape)==3 and img.shape[2]==1):
        img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    plt.imshow(img, interpolation='none')
    plt.title(title)
    plt.show()

def draw_rect(im, rect, color=None,thickness=4):
    if color is None:
        color = [255, 0, 0]
    rect = np.array(rect, np.int16).reshape([4])
    cv2.rectangle(im, (rect[0], rect[1]), (rect[2], rect[3]), color, thickness)
    return im

def draw_boxes(im, box, color=None, thickness=4):
    for box in boxes:
        im=draw_box(im,box,color,thickness)
    return im

def draw_box(im, box, color=None, thickness=4):
    if color is None:
        color = [255, 0, 0]
    box = np.array(box).reshape([4])
    rect = np.array([box[0], box[1], box[0] + box[2], box[1] + box[3]], dtype=np.int16)
    cv2.rectangle(im, (rect[0], rect[1]), (rect[2], rect[3]), color, thickness=thickness)
    return im

def draw_poly(im, poly, color=None,thickness=2):
    poly = np.array(poly, dtype=np.int32).reshape([1, -1, 2])
    im = cv2.polylines(im, poly, True, color, thickness)
    return im

def viz_landmark(im, preds, gts, color=None,thickness=2):
#     im=(im*255).astype(np.uint8)
    preds=np.array(preds,dtype=np.int32)
    gts=np.array(gts,dtype=np.int32)
    for i in range(len(preds)):
        im=cv2.circle(im,tuple(gts[i]),4,(0,0,255),-1)
        im = cv2.putText(im, str(i), tuple(gts[i]), cv2.FONT_HERSHEY_SIMPLEX ,1, (0,0,255), 2, cv2.LINE_AA)
        im=cv2.circle(im,tuple(preds[i]),3,(255,0,0),-1)
    return im

def visualize_field_bbox(df,test_n=1,log=False,field=None,path=None,is_pts=False,size=None,thickness=4,resize=512):
    try:
        df['field_bbox']=df['field_bbox'].apply(lambda x:np.array(str(x)[1:-1].strip().split(),dtype=np.float32))
    except:
        pass
    try:
        df['field_pts']=df['field_pts'].apply(lambda x:np.array(re.sub('[\[\]\,]',' ',x).strip().split(),dtype=np.float32))
    except:
        pass
    if field is not None:
        df=df[lambda x:x.field==field]
    if path is not None:
        df=df[lambda x:x.path==path]

    im_path_list=list(set(list(df.path)))
    im_path_list=sorted(im_path_list)
#     np.random.seed(101)
    np.random.shuffle(im_path_list)
    for i,path in enumerate(im_path_list[:test_n]):
        if log:
            print(path)
        im=cv2.imread(path)
        if resize>0:
            h,w=im.shape[:2]
            f=resize/max(h,w)
            if f<1:
                im=cv2.resize(im,None,fx=f,fy=f)
            else:
                f=1

        df_of_path=df[lambda x:x.path==path]
        field_bbox=list(df_of_path.field_bbox)
        field_bbox=np.array(field_bbox,dtype=np.int32)
        field_bbox=(f*field_bbox).astype(np.int32)
        if is_pts:
            field_pts=list(df_of_path.field_pts)
            field_pts=np.array(field_pts)
            field_pts=(f*field_pts)
        field_list=list(df_of_path.field)
        field_text_list=list(df_of_path.field_text)
        color=(255,0,0)
        if is_pts:
            for box in field_pts:
                im=utils_image.draw_poly(im,box,thickness=thickness,color=color)
        else:
            for box in field_bbox:
                im=utils_image.draw_rect(im,box,thickness=thickness,color=color)

        show_image(im,'im',size=size)

def vis_diff(str1,str2):
    from visedit import StringEdit

    str1 = re.sub('\s', '^', str1).strip()   
    str2 = re.sub('\s', '^', str2).strip()   
    se = StringEdit(str1,str2,text_color_settings={
        "wrong": "RED",
        "correct": "GREEN",
        "base": "BLUE",
        })
    text = se.generate_text()
    print(text)
    # also available html as well as text
    html = se.generate_html()