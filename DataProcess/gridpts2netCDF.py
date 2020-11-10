# -*- coding: utf-8 -*-

# 格值点转换为NetCDF文件

import netCDF4 as nc
import numpy as np
import os
import pdb
import errno
import sys
import math

inp_dir = "D:\\ResearchProjects\\2020\\zw"
out_dir = "D:\\ResearchProjects\\2020"
# inp_file = '地下水等效水高变化ewh.dat'
# inp_file = '地下水等效水高变化ewh_gps10.dat'
# inp_file = '地下水等效水高变化ewh0908proddg.dat'
# out_nc = os.path.join(inp_dir, 'levelV0908ddg.nc')

# inp_file = 'ewh_1m_Kriging.dat'
# out_nc = os.path.join(inp_dir, 'ewh_1m_Kriging.nc')
inp_file = 'ewh_1m_Kriging_extract.dat'
out_nc = os.path.join(inp_dir, 'ewh_1m_Kriging_extract.nc')
# out_nc = 'ewh_gps10.nc'


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
grddatalist = dtest[6:]
grddata_np = np.array(grddatalist)

# 提取行列数信息
lonstep = (float(infodata[4]))
latstep = (float(infodata[5]))
nlon = math.ceil((float(infodata[1])-float(infodata[0]))/lonstep)
nlat = math.ceil((float(infodata[3])-float(infodata[2]))/latstep)

# 构建 列为经度个数 行为纬度个数的数组
grddata = grddata_np.reshape((nlat, nlon))

# Initialize nc file
# out_nc = out_dir+os.path.basename(inp_dir+inp_file)[:-4]+'.nc'
# out_nc = 'ewh_gps10.nc'
nc_data = nc.Dataset(out_nc, 'w', format='NETCDF4')
nc_data.description = 'ewh data'

# define dimensions
nc_data.createDimension('lat', size=grddata.shape[0])
nc_data.createDimension('lon', size=grddata.shape[1])

# define variables for storing data
# variables
lon = nc_data.createVariable('lon', 'f4', dimensions='lon')
lat = nc_data.createVariable('lat', 'f4', dimensions='lat')
ewh = nc_data.createVariable('ewh', 'f8', ('lat', 'lon'))

# add data to variables . do not use np.arrange .
# if you don't want to use last value,you can use par "endponit=False"
lon_dt = np.linspace(float(infodata[0]), float(infodata[1]), nlon)
lat_dt = np.linspace(float(infodata[2]), float(infodata[3]), nlat)

nc_data.variables['lat'][:] = lat_dt
nc_data.variables['lon'][:] = lon_dt
nc_data.variables['ewh'][:] = grddata


# add attributes
# add global attributes
nc_data.title = 'create NetCDF file using netcdf4-python using grid points'
# add local attributes to variable
lon.description = 'longitude'
lon.units = 'degrees east'

lat.description = 'latitude'
lat.units = 'degrees north'

ewh.description = 'ewh data'
ewh.units = 'mm'


# close file
nc_data.close()
print(out_nc)
