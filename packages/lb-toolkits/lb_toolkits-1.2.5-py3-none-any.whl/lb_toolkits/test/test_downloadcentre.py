# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : test_downloadcentre.py

@Modify Time :  2022/9/29 9:57   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import datetime
import os.path
import shutil
import sys

import numpy as np

username_nasa = 'libindd'
password_nasa = 'Libin043'



def xco21():
    import cdsapi
    import calendar
    import datetime
    import numpy as np
    c = cdsapi.Client()
    start=datetime.datetime(2015,1,1)
    end=datetime.datetime(2016,12,1)
    while start <= end:
        times=datetime.datetime.strftime(start,'%Y%m%d')
        year=start.strftime('%Y')
        month=start.strftime('%m')
        monthRange = calendar.monthrange(start.year,start.month)[1]
        d=np.arange(monthRange)
        d=d+1
        day=['%02d'%x for x in d]
        print('month=',month)
        c.retrieve(
            'satellite-carbon-dioxide',
            {
                'format': 'tgz',
                'processing_level': 'level_2',
                'variable': 'xco2',
                'sensor_and_algorithm': 'tanso_fts_ocfp',
                'year': year,
                'month': month,
                'day': day,
                'version': '7.3',
            },
            times+'_download.tar.gz')
        start+=datetime.timedelta(days=monthRange)


def xco2():
    import cdsapi

    c = cdsapi.Client()

    c.retrieve(
        'satellite-carbon-dioxide',
        {
            'processing_level': 'level_2',
            'variable': 'xco2',
            'sensor_and_algorithm': 'tanso_fts_ocfp',
            'year': '2017',
            'month': [
                '12',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'version': '7.3',
            'format': 'tgz',
        },
        '2017_12_download.tar.gz')


def test_downloadLandcover():
    from lb_toolkits.downloadcentre import downloadLandcover

    down = downloadLandcover()
    # fils = down.from_tsinghua(outdir='./data/landcover', minX=100, maxX=110, minY=25, maxY=35)

    urllist = down.from_esri(r'./data/landcover',
                             datetime.datetime.strptime('2022', '%Y'),
                             # extent=(70, 15, 135, 55),
                             shapename=r'E:\XZDYYG\code\parm\shapefile\xizang\xizang_sheng_polygon.shp',
                             skip=True)

    print(urllist)
    for filename in urllist :
        basename = os.path.basename(filename)
        srcfile = os.path.join(r'./data/landcover', basename)
        dstfile = os.path.join(r'./data/xz', basename)
        shutil.copy(srcfile, dstfile)
    # down.download()


def test_downloadDEM():
    from lb_toolkits.downloadcentre import downloadDEM

    down = downloadDEM(username=username_nasa, password=password_nasa)

    # 通过CMR查询数据
    # fils = down.searchfile( prodversion='ASTGTM_NC')

    fils = down.searchDEM30M(minX=100, maxX=110, minY=25, maxY=35)

    for file in fils :
        print(file)
        down.download(r'./data/dem', file)


def test_downloadCALIPSO():
    from lb_toolkits.downloadcentre import downloadCALIPSO

    down = downloadCALIPSO(username=username_nasa, password=password_nasa)
    nowdate = datetime.datetime.strptime('20180311 170458', '%Y%m%d %H%M%S')
    fils = down.searchfile(nowdate, endtime=nowdate+datetime.timedelta(hours=2),
                           shortname='CAL_LID_L1-Standard-V4-10')
    # print(fils)
    for file in fils :
        print(file)
        down.download(r'H:\calipso\L1B\2018\2018_03_11', file)

def test_downloadERA5():
    from lb_toolkits.downloadcentre import download_era5_profile, download_era5_surface
    # from test.data.configforera5 import prof_info, surf_info

    nowdate = datetime.datetime.strptime('20210102', '%Y%m%d')
    # 下载廓线数据
    download_era5_profile( outname='prof.nc', nowtime=nowdate,
                           variable=prof_info['variable'],
                           pressure=prof_info['pressure_level'])

    # 下载地面数据
    download_era5_surface(outname='surf.nc', nowtime=nowdate,
                          variable=surf_info['variable'])


def test_downloadFY():
    # from lb_toolkits.downloadcentre import downloadFY
    #
    # mdown = downloadFY(username='guoxuexingNRT', password='iEkEsMCXL9XSGYeC')
    # startdate = datetime.datetime.strptime('20230701', '%Y%m%d')
    # enddate = datetime.datetime.strptime('20230731', '%Y%m%d')
    # nowdate = startdate
    #
    # while nowdate <= enddate :
    #     stime = nowdate + datetime.timedelta(hours=3)
    #     etime = nowdate + datetime.timedelta(hours=9)
    #     mdown.download_fy_l1(dstpath='./data', starttime=stime, endtime=etime, geoflag=True)

    from lb_toolkits.downloadcentre import downloadFY

    mdown = downloadFY(username='FY3D_MERSI', password='Hjx5P_S1')
    startdate = datetime.datetime.strptime('20230701', '%Y%m%d')
    enddate = datetime.datetime.strptime('20230731', '%Y%m%d')
    nowdate = startdate

    while nowdate <= enddate :
        stime = nowdate + datetime.timedelta(hours=3)
        etime = nowdate + datetime.timedelta(hours=9)
        mdown.download_fy_l1(dstpath=r'./FY3D', starttime=stime, endtime=etime, geoflag=True,
                             satid='FY3D', instid='MERSI', resolution=0.01)

        nowdate += datetime.timedelta(days=1)
    # nowdate = datetime.datetime.strptime('20230110 0000', '%Y%m%d %H%M')
    # mdown.download_fy_l1(dstpath=r'D:\DATA\FY3D\MERSI', starttime=nowdate, geoflag=True,
    #                      satid='FY3D', instid='MERSI', resolution=0.01)

    mdown = downloadFY()
    # mdown.download_fy_order('./data', orderID='A202211060030029326')


    # mdown.download_fy_order('./data', './data/A202211030312815913.txt')

    #
    # mdown = downloadFY(username='guoxuexingNRT', password='iEkEsMCXL9XSGYeC')
    # nowdate = datetime.datetime.strptime('20221103 0000', '%Y%m%d %H%M')
    # mdown.download_fy_l1(dstpath='./data', starttime=nowdate, geoflag=True)

    #
    # mdown = downloadFY(username='guoxuexingNRT', password='iEkEsMCXL9XSGYeC')
    # nowdate = datetime.datetime.strptime('20220923 0000', '%Y%m%d %H%M')
    # mdown.download_fy_l2(dstpath='./data', satid='FY4B', instid='AGRI', starttime=nowdate, prodid='CTH')
    #
    #
    mdown = downloadFY(username='FY3D_MERSI', password='Hjx5P_S1')
    nowdate = datetime.datetime.strptime('20230110 0000', '%Y%m%d %H%M')
    # mdown.download_fy_l1(dstpath=r'D:\DATA\FY3D\MERSI', starttime=nowdate, geoflag=True,
    #                      satid='FY3D', instid='MERSI', resolution=0.01)
    #
    # mdown = downloadFY(username='FY3D_MERSI', password='Hjx5P_S1')
    # nowdate = datetime.datetime.strptime('20220803 0000', '%Y%m%d %H%M')

    # seachfile('/L2L3')
    #
    filelist = mdown.download_fy_l2(dstpath=r'D:\DATA\FY3D\MERSI\NDVI', starttime=nowdate, prodid='NVI',
                         satid='FY3D', instid='MERSI', resolution=0.01,
                         extent=[70, 18, 135, 55], FY3Block10Flag=True,
                         shpname=r'C:\Users\admin\Desktop\test\china1.shp')

    print(len(filelist))

def test_downloadGFS():
    from lb_toolkits.downloadcentre import downloadGFS

    downloadGFS('./data', datetime.datetime.utcnow())


def test_downloadH8():
    from lb_toolkits.downloadcentre import downloadH8

    nowdate = datetime.datetime.strptime('202301150400', '%Y%m%d%H%M')
    FTP_HOST = 'ftp.ptree.jaxa.jp'
    FTP_USER = 'libin033_163.com'
    FTP_PAWD = 'SP+wari8'
    down = downloadH8(username=FTP_USER, password=FTP_PAWD)
    # filelist = down.search_ahi8_l1_netcdf(nowdate)
    # down.download('./data', filelist)
    filelist = down.search_ahi8_l1_hsd(starttime=nowdate, endtime=nowdate, pattern=['B03', 'FLDK'])
    down.download(r'D:\DATA\H8', filelist)

def test_downloadHY():
    from lb_toolkits.downloadcentre import downloadHY

    mdown = downloadHY(username='libin033', password='Libin1234!@#$')

    startdate = datetime.datetime.strptime('20230209 0000', '%Y%m%d %H%M')
    enddate = datetime.datetime.strptime('20230225 0000', '%Y%m%d %H%M')
    searchfile = mdown.search(starttime=startdate, endtime=enddate, satid='HY2B', instid='SCA', prodid='L2B')

    mdown.download('./data/HY', searchfile)

def test_downloadLandsat():
    from lb_toolkits.downloadcentre import downloadLandsat

    product = 'landsat_ot_c2_l1'
    lat = 29.65
    lon = 91.13
    start_date=datetime.datetime.strptime('2020-06-01', '%Y-%m-%d')
    end_date=datetime.datetime.strptime('2023-08-01', '%Y-%m-%d')
    cloud_max = 20
    output_dir = './data'

    username = "nieweilimuhan"
    password = "Nw119530"
    username = "luguozhenghpu@163.com"
    password = "luGUOzheng123"

    # dataset = 'LANDSAT_8_C1'
    # lat = 30.75
    # lon = 120.75
    # start_date = '2020-01-01'
    # end_date = '2020-05-01'
    # cloud_max = 30

    down = downloadLandsat(username, password)
    Landsat_name = down.searchfile(product, latitude=lat, longitude=lon,
                                   startdate=start_date, enddate=end_date, cloud_cover_max=cloud_max)
    down.download(Landsat_name, output_dir)

    # down = downloadLandsat(username_nasa, password_nasa)
    # urllist = down.searchfileByCMR(starttime=start_date, endtime=end_date,
    #                                cloud_cover=20,point=[91.2, 29.2])
    #
    # for url in urllist :
    #     down.downloadByCMR(output_dir, url, skip=True)

def test_downloadMODIS():

    from lb_toolkits.downloadcentre import downloadMODIS
    down = downloadMODIS(username='yliang2323', password='Liangyun1306.')
    startdate = datetime.datetime.strptime('20220101', '%Y%m%d')
    enddate = datetime.datetime.strptime('20221231', '%Y%m%d')
    fils = down.searchfile(startdate, enddate,
                           shortname='MOD04_3K', version='6.1', provider='LAADS',
                           bounding_box=[73.5, 3.5, 135.1, 53.6])

    for file in fils :
        print(file)
        down.download(r'./data', file)
    exit()


    from lb_toolkits.downloadcentre import downloadMODIS
    down = downloadMODIS(username=username_nasa, password=password_nasa)
    startdate = datetime.datetime.strptime('20180101', '%Y%m%d')
    enddate = datetime.datetime.strptime('20180103', '%Y%m%d')
    fils = down.searchfile(startdate, enddate,
                           shortname='MOD35_L2', version='6.1',
                           bounding_box=[100.0, 30.0, 110.0, 50.0])

    for file in fils :
        print(file)
        down.download(r'./data', file)

def test_downloadOCO():
    from lb_toolkits.downloadcentre import downloadOCO

    argv = sys.argv
    if len(argv) == 3 :
        starttime=datetime.datetime.strptime(argv[1], '%Y%m%d')
        endtime=datetime.datetime.strptime(argv[2], '%Y%m%d')
    else:
        starttime = datetime.datetime.strptime('20230101', '%Y%m%d')
        endtime   = datetime.datetime.strptime('20230103', '%Y%m%d')

    down = downloadOCO(username='cuitao', password='CUItao1234')
    urllist = down.searchfile(starttime=starttime,
                              endtime=endtime,
                              shortname='OCO2_L2_Lite_FP',
                              version='11.1r')

    count = len(urllist)
    for url in urllist :
        count -= 1
        print(count, url)
        # down.download('./data/', url)


def test_downloadSentinel():

    from lb_toolkits.downloadcentre import downloadSentinel
    username = "niewei_sentinel2"
    password= "Nw119105"

    # username = "s5pguest"
    # password= "s5pguest"
    down = downloadSentinel(username, password)
    starttime=datetime.datetime.strptime('20230101', '%Y%m%d')
    endtime=datetime.datetime.strptime('20231201', '%Y%m%d')
    # endtime=starttime+datetime.timedelta(days=1, seconds=-1)

    urllist = down.searchfile(starttime=starttime, endtime=endtime,
                              platformname='Sentinel-2', producttype='S2MSI2A',
                              # geojson=r'D:\gz.geojson', cloudcoverpercentage=[0,10])
                              geojson=r'./data/st.geojson', cloudcoverpercentage=[0,10])
    for url in urllist :
        print(len(urllist), url)
        down.download('./data', url, skip=True)

def test_downloadGOSAT():

    from lb_toolkits.downloadcentre import downloadGOSAT
    from dateutil.relativedelta import relativedelta
    startdate = datetime.datetime.strptime('20090101', '%Y%m%d')
    enddate = datetime.datetime.strptime('20231201', '%Y%m%d')
    for item in ['CO2', 'CH4'] :
        nowdate = startdate
        while nowdate <= enddate :
            # nowdate = datetime.datetime.strptime('20220101', '%Y%m%d')
            outdir = os.path.join(r'D:\DATA\GOSAT', item)
            downloadGOSAT(outdir=outdir, nowdate=nowdate, prod=item, level='L2',
                          username='libin033@126.com', password='libin033')
            nowdate += relativedelta(months=1)

def test_downloadTANSAT():
    from lb_toolkits.downloadcentre import downloadTANSAT
    down  = downloadTANSAT()
    startdate = datetime.datetime.strptime('20170101', '%Y%m%d')
    enddate = datetime.datetime.strptime('20200601', '%Y%m%d')
    filelist = down.searchfile(startdate, enddate, obstype='ND')
    for item in filelist :
        down.download(r'D:\DATA\TANSAT', item)

def test_downloadEarthdata():

    from lb_toolkits.downloadcentre import downloadEarthdata
    down = downloadEarthdata(username=username_nasa, password=password_nasa)
    startdate = datetime.datetime.strptime('20180101', '%Y%m%d')
    enddate = datetime.datetime.strptime('20180103', '%Y%m%d')
    fils = down.searchfile(startdate, enddate,
                           shortname='MOD35_L2',
                           provider='LAADS',
                           # version='6.1',
                           bounding_box=[100.0, 30.0, 110.0, 50.0])
    for file in fils :
        print(file)
        down.download(r'./data', file)



datetime.datetime.utcnow()
if __name__ == '__main__':

    # test_downloadTANSAT()

    # test_downloadGOSAT()

    # test_downloadLandcover()

    # test_downloadDEM()

    # test_downloadCALIPSO()

    # test_downloadERA5()

    # test_downloadFY()

    # test_downloadHY()

    # test_downloadGFS()

    # test_downloadH8()

    # test_downloadLandsat()

    # test_downloadMODIS()

    # test_downloadEarthdata()

    test_downloadOCO()

    # test_downloadSentinel()

    # import pandas as pd
    #
    # filename = r'C:\Users\admin\Desktop\index.csv'
    # data = pd.read_csv(filename, nrows=10)
    # head = data.head(1)
    # print(head)
    # print(head)
    # s3_scenes = pd.read_csv('http://landsat-pds.s3.amazonaws.com/c1/L8/scene_list.gz', compression='gzip')
    exit(0)

    from lb_toolkits.downloadcentre import downloadSentinel


    argv = sys.argv
    if len(argv) == 3 :
        starttime=datetime.datetime.strptime(argv[1], '%Y%m%d')
        endtime=datetime.datetime.strptime(argv[2], '%Y%m%d')
    else:
        starttime=datetime.datetime.strptime('20181201', '%Y%m%d')
        endtime=datetime.datetime.strptime('20221201', '%Y%m%d')
        # endtime=starttime+datetime.timedelta(days=1, seconds=-1)

    username = "s5pguest"
    password= "s5pguest"
    down = downloadSentinel(username, password)
    dt = endtime
    while dt >= starttime :
        print(dt)
        urllist = down.searchfile(starttime=dt, platformname='Sentinel-5P',
                                  producttype='L2__CH4___', processingmode='Offline')
        count = len(urllist)
        for url in urllist :
            count -= 1
            print(count, url)
            down.download('./data/S5P', url)

        dt += datetime.timedelta(days=-1)