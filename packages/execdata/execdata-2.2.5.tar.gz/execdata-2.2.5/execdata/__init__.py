'''
Date         : 2022-10-25 15:44:41
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-10-30 13:18:28
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\__init__.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''

from execdata.templateproj import add_one, add_two
from execdata.data_conversion import convint, convfloat
from execdata.data_mining import filtered_value_count, filtered_value_list, column_identify, majority_target_variable
from execdata.data_preprocess import drop_columns
from execdata.standardization import encode, sep, split, sep_split, strat_split
from execdata.model_evaluate import sample_comparsion, model_evaluate, algo_accuracy, result_comparision
