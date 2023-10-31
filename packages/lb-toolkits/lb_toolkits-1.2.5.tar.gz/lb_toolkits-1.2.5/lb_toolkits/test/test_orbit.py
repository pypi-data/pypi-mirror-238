# coding:utf-8
'''
@Project  : CalOrbit
@File     : test_orbit.py
@Modify Time      @Author    @Version    @Desciption
--------------    -------    --------    -----------
2022/1/21 18:01      Lee       1.0         
 
'''

import itertools

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import datetime
import time
from pyorbital import orbital
from lb_toolkits.orbital import Orbital

def draw(outname, x, y) :
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 8))

    plt.plot(x, y, 'r.')

    plt.savefig(outname, dpi=300)

from lb_toolkits.orbital import orbit
if __name__ == '__main__':

    from lb_toolkits.orbital.orbit import orbit

    x1 = []
    y1 = []
    x2 = []
    y2 = []


    t_start = datetime.datetime.strptime('20230625', '%Y%m%d')
    t_stop = t_start + datetime.timedelta(minutes=100)

    timelist = [t_start + datetime.timedelta(minutes=float(x)) for x in np.arange(0, 60, 1)]

    mpro = orbit(satellite="FY-3D")
    orbt = Orbital(satellite="FY-3D")
    while True :
        nowdate = datetime.datetime.now()
        print('#'*100)
        lon, lat, alt = orbt.get_lonlatalt(nowdate)
        print(lon, lat)
        FLONG1, FLAT1, FLONG2, FLAT2 = mpro.calorbit(nowdate)
        x1.append(FLONG1)
        x2.append(FLONG2)
        y1.append(FLAT1)
        y2.append(FLAT2)

        print(FLONG1, FLAT1, FLONG2, FLAT2)
        time.sleep(10)

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(10, 8))

    plt.plot(x1, y1, 'r.')
    plt.plot(x2, y2, 'b.')

    plt.savefig('./data/test.png', dpi=300)


    # FY3D
    # 1 43010U 17072A   21069.05644449  .00000000  00000-0  00000-0 0  0000
    # 2 43010  98.7816  11.7283 0002004  39.0461 321.0937 14.19750111171890

    # dOrbitNum = 14.1975011117
    # dOrbitT = 24.0 / dOrbitNum * 60 * 60
    #
    # dOrbitSemiAxis = np.power(((398613.52 * dOrbitT * dOrbitT) / (4 * np.pi * np.pi)), 1.0/3.0)
    # # dSatHeight = dOrbitSemiAxis - AE
    # tleinfo = {
    #     'dOrbitSemiAxis' : dOrbitSemiAxis,                # 轨道半长轴
    #     'dOrbitEccentricity': 0.0002004,            # 轨道偏心率
    #     'dOrbitInclination': 98.7816,         # 轨道倾角
    #     'dAscendLongitude' : 11.7283,         # 升交点赤道经度
    #     'dPerigeeDegree'  :39.0461,          # 近地点俯角
    #     'dMeanPerigee' :321.0937,         # 平近地点
    #     'dOrbitT' :   dOrbitT,                # 每圈周期时间
    #     # 'dSatHeight' :dSatHeight,         # 卫星高度
    #     'TotalOrbit' :  189,         # 卫星高度
    # }
    # TPixel = 2048
    #
    # StpAng = 0.0541
    # StpTim = 0.000025
    #
    # nowdate = datetime.datetime.utcnow()
    # TimeCal = orbit.TIMEZ(nowdate.year, nowdate.month, nowdate.day, nowdate.hour, nowdate.minute, nowdate.second)
    #
    # print(TimeCal)
    # PIXEL = 1
    # #!调用程序SatAEL 计算第一个象元点（PIXEL=1）所对应的经纬度
    # FLAT1, FLONG1 = orbit.TNLOC(TimeCal, PIXEL, StpAng, StpTim, TPixel, tleinfo, nowdate)
    #
    # #!调用程序SatAEL 计算最后一个象元点（PIXEL=TPixel）所对应的经纬度
    # PIXEL = TPixel
    # FLAT2, FLONG2 = orbit.TNLOC(TimeCal, PIXEL, StpAng, StpTim, TPixel, tleinfo, nowdate)
    #
    # import matplotlib.pyplot as plt
    # fig = plt.figure(figsize=(10, 8))
    #
    # plt.plot(FLONG1, FLAT1, 'r.')
    # plt.plot(FLONG2, FLAT2, 'b.')
    #
    # plt.savefig('./data/test.png', dpi=300)


#
# if __name__ == "__main__":
#     # obs_lon, obs_lat = 12.4143, 55.9065
#     # obs_alt = 0.02
#     orbt = Orbital(satellite="FY-3D")
#
#     t_start = datetime.datetime.strptime('20230625', '%Y%m%d')
#     t_stop = t_start + datetime.timedelta(minutes=100)
#
#     timelist = [t_start + datetime.timedelta(minutes=float(x)) for x in np.arange(0, 24*60, 1)]
#
#     # for item in timelist :
#     #     print(item)
#     lon, lat, alt = orbt.get_lonlatalt(np.array(timelist))
#     # for x, y in zip(lon, lat) :
#     #     print(y, x)
#
#     draw('./data/test.png', lon, lat)

    # t = t_start
    # while True:
        # t += timedelta(seconds=15)

        # t = datetime.datetime.utcnow()

        # lon, lat = np.rad2deg((lon, lat))
        # az, el = o.get_observer_look(t, obs_lon, obs_lat, obs_alt)
        # ob = o.get_orbit_number(t, tbus_style=True)
        # print(lon, lat, az, el, ob)
        # time.sleep(5)



