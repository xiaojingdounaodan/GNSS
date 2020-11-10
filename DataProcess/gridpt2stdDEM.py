# -*- coding: utf-8 -*-

# 格网文件 修改正为标准DEM文件

import netCDF4 as nc
import numpy as np
import os
import pdb
import errno
import sys
import math

inp_dir = r'D:\ResearchProjects\2020\zw\地下水反演-level'
out_dir = r'D:\ResearchProjects\2020\zw\地下水反演-level'
# out_dir = "D:\\ResearchProjects\\2020"
# inp_file = '计算区域零值格网模型（数字高程模型）5m_nearest.dat'
# out_file = os.path.join(inp_dir, '计算区域0值dem.dat')
inp_file = 'dem0.dat'
out_file = os.path.join(inp_dir, 'dem.dat')


def make_dir_if_missing(d):
    try:
        os.makedirs(d)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


make_dir_if_missing(out_dir)

# Read ASCII File
fl_name = os.path.join(inp_dir, inp_file)
data = []
with open(fl_name, 'r', encoding='utf8') as f:
    for i in f:
        data.append([j for j in i.split()])  # 可用于每行列数相同的情况
dtest = []  # 所有数据
[dtest.extend(li) for li in data]
infodata = dtest[0:6]
grddatalist = dtest[7:]
grddata_np = np.array(grddatalist)

# 提取行列数信息
lonstep = (float(infodata[4]))
latstep = (float(infodata[5]))
nlon = math.ceil((float(infodata[1])-float(infodata[0]))/lonstep)
nlat = math.ceil((float(infodata[3])-float(infodata[2]))/latstep)

# 构建 列为经度个数 行为纬度个数的数组
grddata = grddata_np.reshape((nlat, nlon))

# 写入文件

np.savetxt(out_file, grddata, fmt='%s', delimiter="      ")
