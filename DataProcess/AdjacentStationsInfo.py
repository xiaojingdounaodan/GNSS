# -*- coding: UTF-8 -*-
# 提取段差信息。依据测量路线文件格式，由离散点信息文件构建系列记录时序文件

import os
import pandas as pd
import numpy as np


class levelLineSort:
    """
    将离散点文件规整为章传银老师程所需文件格式
    """

    def __init__(self, ptsfilepath, stdfilepath, outfilepath, infofilepath):
        self.ptsfile = ptsfilepath  # 所用测点信息文件 txt格式
        self.stdfile = stdfilepath  # 被查找信息文件
        self.outfile = outfilepath  # 输出文件
        self.infofile = infofilepath  # 过程文件
        self.remainfile = r"D:\ResearchProject\GNSS\remain_pts.txt"

    def Sortpts(self):
        """
        整理出相邻测段信息为“序列记录时序文件格式”,测段信息查找可参考
        """
        pts = pd.read_csv(self.ptsfile, delimiter='\t', header=None)
        stdline = pd.read_excel(self.stdfile, '2015_1',
                                usecols=[0, 1, 2, 5, 6])
        print(stdline)
        outdat = []  # 用于存储数据生成的数据文件，最终转换为dataframe保存
        tempdat = []
        num = 0
        nlines = 0  # 测段数
        for index, row in stdline.iterrows():
            startpt = row["起点"]
            endpt = row["终点"]
            # 起点终点能否在平差结果中找到,如果可以查找其索引
            existstart = pts[pts[7] == startpt].index.tolist()
            existend = pts[pts[7] == endpt].index.tolist()
            ns = len(existstart)
            ne = len(existend)
            ntemp = len(tempdat)
            # 查找测段第一个点
            if(ne == 0):
                continue
            if(ne != 0):
                indend = existend[0]
                lone = pts.iat[indend, 0]
                late = pts.iat[indend, 1]
                ptname = row["终点"]
                ptnum = row["终点点号"]
                tempdis = row["距离"]
                tempdat.append(ptname)
                tempdat.append(ptnum+1000)
                tempdat.append(lone)
                tempdat.append(late)
                tempdat.append(tempdis)
                num = num+1
                if(num == 2):
                    num = 0
                    nlines = nlines+1
                    outdat.append(tempdat)
                    # print("测段数为："+str(nlines))
                    # print("数据为：")
                    # print(tempdat)
                    # print("最终数据：", outdat)
                    tempdat = []
        print(len(outdat))
        restemp = np.array(outdat)
        res = pd.DataFrame(restemp)
        print("构造后结果：\n", res)

        res["测段"] = res[1].map(str) + "_" + res[6].map(str)
        print("新结果：\n", res)

    def Adjacent(self, sheetname, usecolslist):
        """
        根据水准路线，构造相邻点相关信息
        sheetname:需要读取的Excel sheet名称
        usecolslist：需要读取那几列
        """
        pts = pd.read_csv(self.ptsfile, delimiter='\t', header=None)
        stdline = pd.read_excel(self.stdfile, sheetname, usecols=usecolslist)
        df = pd.read_excel(self.stdfile, '2015_1', usecols=[0, 5])

        print(pts)
        print(stdline)
        outdata = []
        linenum = 0  # 测线号
        npts = 0  # 测点数
        linedis = 0  # 测段距离
        tempdata = []
        cont = 0
        for index, row in stdline.iterrows():
            ptname = row["点名"]
            ptlon = row["经度"]
            ptlat = row["纬度"]
            ptdis = row["距起算点距离"]
            ptgc = row["改正后高差中数"]
            ptnum = row["测线号"]
            ptexist = pts[pts[7] == ptname].index.tolist()
            nlen = len(ptexist)
            ntemp = 0
            if ((nlen > 0) and (npts == 0)):
                linenum = ptnum
                npts = 1
                linedis = ptdis
                code = self.getPtNum(ptname, df)+1000
                tempdata.extend([ptname, ptlon, ptlat, code])
                ntemp = len(tempdata)
            if (ntemp == 4):
                continue
            if ((nlen > 0) and (npts == 1) and (linenum == ptnum)):
                dis = ptdis - linedis
                code = self.getPtNum(ptname, df)+1000
                tempdata.extend([ptname, ptlon, ptlat, code, dis])
                outdata.append(tempdata)
                # 恢复原始状态
                linenum = 0
                npts = 0
                linedis = 0
                tempdata = []
        print(outdata)

    def sortlines(self, sheetname, usecolslist):
        # 打开过程文件
        finfo = open(self.infofile, 'w')
        finfo.write("测线中有，但平差结果中没有的的点：\n")
        # 1.筛选路线
        pts = pd.read_csv(self.ptsfile, delimiter='\t', header=None)
        stdline = pd.read_excel(self.stdfile, sheetname, usecols=usecolslist)
        df = pd.read_excel(self.stdfile, '2015_1', usecols=[0, 5])
        # pts筛选
        remaninpts = []
        # 2.路线中筛选点
        tempdat = []
        outdat = []
        resdata = []

        for num in range(1, 49):
            linenums = stdline[stdline["线号"] == num].index.tolist()
            ptnames = stdline.ix[linenums, "点名"]
            # print(ptnames)
            for ind, item in enumerate(linenums):
                ptname = ptnames[item]
                ptdis = stdline.ix[item, "距起算点距离"]
                state = pts[pts[7] == ptname].index.tolist()
                ns = len(state)
                if (ns != 0):
                    remaninpts.extend(state)
                    lon = pts.iat[state[0], 0]
                    lat = pts.iat[state[0], 1]
                    adjustment = pts.iat[state[0], 3]
                    code = self.getPtNum(ptname, df) + 1000
                    if (code > 10000):
                        print(ptname + "--在成果中没有！")
                        finfo.write("测线号："+str(item)+"---点名："+ptname+"\n")
                        continue
                    tempdat.extend([ptname, lat, lon, ptdis, code, adjustment])
                if ((ind + 1) == len(linenums)):
                    if (len(tempdat) == 0):
                        continue
                    outdat.append(tempdat)
                    tempdat = []
        # print(outdat)
        # print(remaninpts)

        # 3.1构建测段
        finfo.write("==============================\n")
        nout = len(outdat)
        for i in range(nout):
            lineinfo = outdat[i]
            ni = len(lineinfo)
            if (ni <= 6):
                finfo.write("该测段只有一个点：" + str(lineinfo)+"\n")
                continue

            begdis = lineinfo[3]  # 查找到的第一点与起测点的距离
            # 遍历测段
            nlines = ni/6
            for ip in range(0, 6, ni):
                pt1_ind = ip
                pt2_ind = ip + 6
                if (ip >= ni):
                    break
                ptsname = lineinfo[pt1_ind] + "_" + lineinfo[pt2_ind]
                ptscode = str(lineinfo[pt1_ind+4]) + \
                    "_" + str(lineinfo[pt2_ind+4])
                ptsdis = lineinfo[pt2_ind + 3] - lineinfo[pt2_ind + 3] - begdis
                pt1lat = lineinfo[pt1_ind+1]
                pt1lon = lineinfo[pt1_ind+2]
                pt1adjust = lineinfo[pt1_ind+5]
                pt2lat = lineinfo[pt2_ind+1]
                pt2lon = lineinfo[pt2_ind + 2]
                pt2adjust = lineinfo[pt2_ind + 5]
                adjustdiff = pt2adjust-pt1adjust
                resdata.append([ptscode, pt1lon, pt1lat, pt2lon,
                                pt2lat, adjustdiff, ptsdis, ptsname])
        # print(resdata)

        finfo.close()
        tempres = pd.DataFrame(resdata)
        tempres.to_csv(self.outfile, header=None, index=None,
                       sep=" ", encoding="utf_8_sig")
        # 速率中有，而测信信息表中没有
        remaninptsdf = pts.drop(remaninpts)[7]
        remaninptsdf.to_csv(self.remainfile, encoding="utf_8_sig")

    def getPtNum(self, ptname, df):
        """
        根据点名从DATAFRAME中获取点号
        """
        ind = df[df["起点"] == ptname].index.tolist()
        if (len(ind) == 0):
            return 9999
        row = ind[0]  # 行
        res = df.at[row, '起点点号']
        return res
