# ECMWF数据下载
from ecmwfapi import ECMWFDataServer

# server = ECMWFService("mars", url="https://api.ecmwf.int/v1",
#   key = "95d22ad529ab2a72cfacf101d016b6b3", email = "zhangchao@fmac.ac.cn")
server = ECMWFDataServer()
server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "20190101/20190201/20190301/20190401/20190501/20190601/20190701/20190801",
    "expver": "1",
    "grid": "0.75/0.75",
    "levtype": "sfc",
    "param": "134.128",
    "stream": "moda",
    "type": "an",
    "target": "output",
    "format":"netcdf",
})
