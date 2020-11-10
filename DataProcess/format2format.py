# 文件格式转换

#
import os
import pandas as pd


fout = r"D:\ResearchProjects\2020\zw\地下水反演-level\剩余正高变化zc.txt"
fin = r"D:\ResearchProjects\2020\zw\地下水反演-level\剩余正高变化0.txt"

fexist = not(os.path.exists(fout))

if (fexist):
    fd = open(fout, mode="w", encoding="utf-8")
    fd.close()
    # os.mknod(fout)

dt = pd.read_table(fin, header=None,
                   encoding='gb2312', sep=',', index_col=None)
dt.to_csv(fout, sep=" ", float_format='%-9.3f', index=0, header=0)
