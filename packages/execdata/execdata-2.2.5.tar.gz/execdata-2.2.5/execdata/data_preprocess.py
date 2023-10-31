'''
Date         : 2023-10-11 13:39:36
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-10-12 10:30:41
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\data_preprocess.py
Copyright (c) 2023 by BDFD, All Rights Reserved. 
'''

import numpy as np
import pandas as pd


def drop_columns(df, del_columns_list):
    if isinstance(del_columns_list, str):
        del_columns_list = [del_columns_list]
    elif isinstance(del_columns_list, list):
        del_columns_list = del_columns_list
    else:
        return print("input is not list or str! please redo the function with correct parameter.")
    for column in del_columns_list:
        df = df.drop(column, axis=1)
    return df
