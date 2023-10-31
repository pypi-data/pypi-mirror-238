# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : test_tools.py

@Modify Time :  2023/4/19 17:54   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import glob
import os
import sys
import numpy as np
import datetime



def test_RasterAndVector():
    from lb_toolkits.tools import VectorPro
    srcfile = r'D:\thinktanks\shapefile\china\polygon\china_cities_polygon.shp'
    src1 = r'C:\Users\admin\Desktop\test\china.shp'
    src2 = r'C:\Users\admin\Desktop\lc\lc.shp'

    pro = VectorPro()
    # pro.intersect(outname=r'C:\Users\admin\Desktop\test\test.shp',
    #               srcfile=src2, clipfile=srcfile, layername='clip')
    # dstpatialRef = pro.get_spatialref(src2)
    # pro.transform(src1, srcfile, dstpatialRef=dstpatialRef)

    # import tempfile
    # tmp_file = tempfile.NamedTemporaryFile(prefix="tmp_Py6S_input_", delete=False)
    # print(tmp_file.name)
    # exit(0)
    # pro.fishgrid('./data/test_fishgrid.shp', extent=[-180, -85, 175, 90], xRes=10, yRes=10)

    # data = pro.grid(r'E:\XZDYYG\code\parm\stations\stations1.shp', field='dem',
    #                 kind='idw', outputBounds=[70, 25, 100, 35],
    #                 xRes=0.01, yRes=0.01, nodata=-999,
    #          outname=r'E:\XZDYYG\code\parm\stations\test.tif', format='MEM')
    #
    # print(data)
    shplist = glob.glob(r'E:\XZDYYG\code\parm\shapefile\wetland\*\*2021.shp')
    # pro.merge1('./data/xizang_wetland_polygon.shp', shplist=shplist)
    pro.createBuffer('./data/xizang_wetland_buffer_polygon.shp', srcshp='./data/xizang_wetland_polygon.shp',
                     bdistance=0.001)

def test_ftp():
    from lb_toolkits.tools import ftppro

    ip = 'ftp.nsmc.org.cn'
    user = "PNQ"
    pwd = "NSMC_NQ7412"

    # /FY3D_NDVI/20220120/EAST
    startdate = datetime.datetime.strptime('20220101', '%Y%m%d')
    enddate   = datetime.datetime.strptime('20221231', '%Y%m%d')

    mpro = ftppro(ip, user, pwd)

    nowdate = startdate
    while nowdate <= enddate :

        srcdir = os.path.join('/FY3D_NDVI', nowdate.strftime('%Y%m%d'), 'EAST')
        srcdir = srcdir.replace('\\', '/')
        print(srcdir)
        filelist = mpro.listdir(srcdir, pattern='*AOTD*')
        if len(filelist) != 0 :
            print(filelist)

        for filename in filelist :
            srcfile = os.path.join(srcdir, filename)
            srcfile = srcfile.replace('\\', '/')
            mpro.downloadFile(srcfile, r'E:\XZDYYG\data\NDVI')

        nowdate += datetime.timedelta(days=1)





if __name__ == '__main__':
    test_RasterAndVector()

    # test_ftp()

    # test_spider()