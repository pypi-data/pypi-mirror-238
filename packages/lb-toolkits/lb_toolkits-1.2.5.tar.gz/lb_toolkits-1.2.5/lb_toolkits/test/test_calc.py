# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : test_calc.py

@Modify Time :  2022/11/10 14:49   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import os
import sys
import numpy as np
import datetime

from lb_toolkits.tools import readtiff, writenc

if __name__ == '__main__':
    srcfile = r'E:\XZDYYG\data\FY3D_MERSI_WHOLE_GLL_L1_20220718_0540_1000M\FY3D_MERSI_WHOLE_GLL_L1_20220718_0540_1000M.tif'

    data, trans, prj = readtiff(srcfile)

    chcnt, line, pixel = data.shape
    lon = trans[0] + trans[1] * np.arange(pixel)
    lat = trans[3] + trans[5] * np.arange(line)

    writenc('test.nc', 'Latitude', lat, overwrite=1)
    writenc('test.nc', 'Longitude', lon, overwrite=0)

    dict_info = {
        'valid_range' : [0, 60000],
        'scale_factor' : 0.1,
        'add_offset' : 0.0,
        'units' : 'K',
        'coordinates' : 'Latitude Longitude',
        'Discriptions' : 'wavelength xxx',
    }
    for bandid in range(1, chcnt+1) :
        writenc('test.nc', 'B%02d' %(bandid), data[bandid],
                dictsdsinfo=dict_info,
                dimension=('Latitude', 'Longitude'), overwrite=0, fill_value=65535)
