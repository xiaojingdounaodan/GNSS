# -*- coding: utf-8 -*-
# 获取离散相邻点属性值之差

import os
import pandas as pd
import numpy as np

# 离散点值文件
ptsfile = r"D:\ResearchProjects\2020\zw\地下水反演-level\level_average0.pts"
data = []  # 每一行一个列表
nHeaders = 1  # 文件头行数
# 打开的文件除了文件头行数，其他行规格相同
with open(ptsfile, 'r', encoding='utf8') as f:
    for i in f:
        data.append([j for j in i.split()])  # 可用于每行列数相同的情况

infodata = data[nHeaders]  # 头文件，数据信息
ptsInof = data[nHeaders:]  # 点位信息

ptsLines = np.array(ptsInof)  # 将list转为numpy的array
pts = pd.DataFrame(ptsLines)  # 将numpy的array与pandas的DataFrame
print(pts)
