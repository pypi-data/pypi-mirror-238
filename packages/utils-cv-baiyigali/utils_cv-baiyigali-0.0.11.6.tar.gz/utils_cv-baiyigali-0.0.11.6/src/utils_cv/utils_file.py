import os
import pandas as pd
import numpy as np

def split_csv(csv_path):
    prefix,ext=os.path.splitext(csv_path)
    csv_path_trainval='{}-trainval.csv'.format(prefix)
    csv_path_test='{}-test.csv'.format(prefix)
    
    df=pd.read_csv(csv_path)
    
    im_path_list=list(set(list(df.path)))
    im_path_list=sorted(im_path_list)
    np.random.seed(101)
    np.random.shuffle(im_path_list)

    test_len=int(len(im_path_list)*0.1)
    im_path_list_trainval=im_path_list[test_len:]
    im_path_list_test=im_path_list[:test_len]

    print(csv_path)
    print(len(im_path_list))
    df_test=df[df.path.isin(im_path_list_test)]
    df_test.to_csv(csv_path_test,index=False)
    print(csv_path_test)
    print(len(im_path_list_test))
    df_trainval=df[df.path.isin(im_path_list_trainval)]
    df_trainval.to_csv(csv_path_trainval,index=False)
    print(csv_path_trainval)
    print(len(im_path_list_trainval))
