# -*- coding: UTF-8 -*-

from DataProcess.AdjacentStationsInfo import levelLineSort

if __name__ == "__main__":
    # 1.离散点文件
    ptsfile = r"D:\ResearchProject\GNSS\level_vel-200511.txt"
    # 2.测量路线文件
    stdfile = r"D:\ResearchProject\GNSS\动态平差17-19.xls"
    # 3.输出文件
    outfile = r"D:\ResearchProject\GNSS\series_line_pt.txt"    
    #4.信息文件
    Infofile = r"D:\ResearchProject\GNSS\Info.txt"

    pro = levelLineSort(ptsfile, stdfile, outfile, Infofile)
    # pro.Sortpts()
    # pro.Adjacent('2015', [0, 1, 2, 4, 8, 13])
    pro.sortlines('2015', [0, 1, 2, 4, 8, 13])
