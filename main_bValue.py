# %

import os
import pandas as pd
from SeisMethod import bvalue as b

if __name__ == "__main__":
    # 读取震例文件
    fullfilepath = r"F:\GNSS\earthquakedata.xlsx"
    dat = pd.read_excel(fullfilepath, header=2, usecols=[5])
    Mlist = dat.values.tolist()
    result = []
    for s_li in Mlist:
        result.append(s_li[0])

    # 计算b值
    bobject = b.bvalue(result, 0, 2)
    bobject.CalculateB()
