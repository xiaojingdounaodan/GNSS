# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2020-08-31 11:59:18
# @Last Modified by:   Your name
# @Last Modified time: 2020-08-31 11:59:18

import os
import math
import numpy as np
import pandas as pd


class bvalue:
    '''
    功能：b值计算
    所需数据：通过输入的所有的地震大小数据，通过整理，计算b值
    作者：张超 2020年8月6日
    '''

    def __init__(self, M, M0=0, method=1):
        '''
        M：输出的地震列表,格式为list
        M0:起算震级
        method:计算b值得方法，1代表最大似然估计(Aki,1965)；2代表线性最小二乘（Sandri et al.,2006)
        '''
        self.M = M
        self.M0 = M0          # 起算震级
        self.method = method
        self.N = len(self.M)  # 地震总个数

    def SortM(self):
        '''
        整理地震目录：
        将输入的地震按照震级归类，以二维数组的方式，['震级'，'个数']，[2,50]...
        返回值：DataFrame格式，第一列为震例
        '''
        Mlist = []
        Mnum = []
        nM = len(self.M)
        df_res = pd.DataFrame(
            data=Noe, columns=['M', 'total'])  # 定义空结果dataframe
        # 将地震列表数据转换为dataframe，方便数据筛选
        df_M = pd.DataFrame(np.array(self.M).T, columns=['M'])
        for i in range(0, 9):
            temp = df_M.loc[(df_M["M"] >= i) & (
                df_M["M"] < (i + 1)), ["M"]].head()
            nt = len(temp)
            Mlist.append(i)
            Mnum.append(nt)
        # Res = pd.DataFrame{'M': pd.Series(Mlist), 'Num': pd.Series(Mnum)}

    def CalculateB(self):
        '''计算B值'''
        # 最大似然估计法
        M = self.M
        N = self.N
        M0 = self.M0

        if self.method == 1:
            tM = 0
            for m in M:
                tM = tM + (m - M0)
            b = N * math.log10(math.e) / tM
            return b
        # 线性最小二乘法
        if self.method == 2:
            Mnew = []  # 筛选后的地震，该地震缺少最大震级的地震，因为比最大地震大的地震为0，对数计算时，自变量必须＞0，否则公式无法使用
            Ni = []  # 震级＞Mi的震例数目
            logNi = []
            Mc = {'M': M}
            df = pd.DataFrame(Mc)
            print(df)
            for mi in M:
                temp = df[(df['M'] > mi)]  # 构建震级大于mi的dataframe
                n = temp.shape[0]
                # 保证Ni中没有为0的数据
                if n <= 0:
                    continue
                Mnew.append(mi)
                Ni.append(n)
                logNi.append(math.log10(n))
            totalM2 = sum(Mnew) * sum(Mnew)  # (∑Mi)²
            total = 0  # n*∑（Mi)²
            member1 = sum(Mnew)*sum(logNi)
            member2 = 0  # n*∑(Mi*[lg(Ni)])
            nM = len(Mnew)
            for i in range(0, nM):
                total = total + Mnew[i] * Mnew[i]
                member2 = Mnew[i] * math.log10(Ni[i])
            member2 = nM*member2
            denominator = totalM2 - nM * total  # 分母
            b = (member1 - member2) / denominator
            return b
