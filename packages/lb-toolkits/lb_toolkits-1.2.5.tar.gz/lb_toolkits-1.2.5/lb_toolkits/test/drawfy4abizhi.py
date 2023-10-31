# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : drawfy4abizhi.py

@Modify Time :  2022/12/26 18:01   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import os
import sys
import numpy as np
import datetime

from lb_toolkits.draw.fy4.fy4l1image import DrawFY4AL1Image

def drawbizhi(outname, l1name, geoname, nowdate):
    if not os.path.isfile(l1name) :
        print('文件不存在【%s】' %(l1name))
        return None

    if not os.path.isfile(geoname) :
        print('文件不存在【%s】' %(geoname))
        return None

    mydraw = DrawFY4AL1Image()

    refr = mydraw.getL1Data(l1name, 2)
    refg = mydraw.getL1Data(l1name, 3)
    refb = mydraw.getL1Data(l1name, 1)

    bt8 = mydraw.getL1Data(l1name, 8)
    bt12 = mydraw.getL1Data(l1name, 12)
    #
    satz = mydraw.getGEOData(geoname, 'NOMSatelliteZenith')
    sunz = mydraw.getGEOData(geoname, 'NOMSunZenith')

    mydraw.drawGeoColor(outname, refr, refg, refb,
                        bt8,bt12,
                        sunz, satz,
                        nightlight=True, title=nowdate.strftime('%Y-%m-%d %H:%M:%S(BTC)'))

    # shapename = './parm/China_prov.shp'
    # from drawshape import drawshape
    # draw = drawshape()
    #
    # draw.DrawShape(outname, shapename, s_lat=area_latmax, s_lon=area_lonmin,
    #                resolution=area_resolution, OL_WIDTH=2, OL_COLOR='#FF0000', outputfile=outname)

def downloadL1(outdir, nowdate):
    from lb_toolkits.downloadcentre import downloadFY

    mdown = downloadFY()
    # mdown.download_fy_order('./data', orderID='A202211060030029326')


    # mdown.download_fy_order('./data', './data/A202211030312815913.txt')


    mdown = downloadFY(username='guoxuexingNRT', password='iEkEsMCXL9XSGYeC')
    # nowdate = datetime.datetime.strptime('20221103 0000', '%Y%m%d %H%M')
    return mdown.download_fy_l1(dstpath=outdir, starttime=nowdate, geoflag=True)

if __name__ == '__main__':

    # startdate = datetime.datetime.strptime('20221220', '%Y%m%d')
    # enddate   = datetime.datetime.strptime('20230110', '%Y%m%d')

    startdate = datetime.datetime.strptime(datetime.datetime.utcnow().strftime('%Y%m%d'), '%Y%m%d')
    enddate   = datetime.datetime.strptime(datetime.datetime.utcnow().strftime('%Y%m%d'), '%Y%m%d') \
                - datetime.timedelta(days=30)

    while startdate >= enddate :
        # nowdate = datetime.datetime.strptime('20221225 0400', '%Y%m%d %H%M')
        nowdate = startdate + datetime.timedelta(hours=4)
        outdir = os.path.join(r'D:\DATA\FY4A\L1', nowdate.strftime('%Y%m%d'))
        bjdate = nowdate + datetime.timedelta(hours=8)
        outname = os.path.join(r'D:\bizhi', 'FY4A_%s.JPG' %(bjdate.strftime('%Y%m%d%H%M%S')))
        if os.path.isfile(outname) :
            startdate -= datetime.timedelta(days=1)
            continue

        filelist = downloadL1(outdir, nowdate)
        if len(filelist) == 2:

            drawbizhi(outname, filelist[0], filelist[1], bjdate)

        startdate -= datetime.timedelta(days=1)