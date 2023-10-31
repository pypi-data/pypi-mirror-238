# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : sftpdownload.py

@Modify Time :  2023/1/3 9:57   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import os
import sys
import numpy as np
import datetime
from lb_toolkits.tools import sftppro
if __name__ == '__main__':

    down = sftppro('159.138.23.60', username='grapes', password='shinetek_MODIS!')
    down.download(remotepath='/data/era5/m2/oco3', localpath=r'D:\DATA\OCO3\src')
    down.download(remotepath='/data/era5/m2/oco2', localpath=r'D:\DATA\OCO2\src')
    down.download(remotepath='/data/era5/m2/tccon.latest.public.tgz', localpath=r'D:\DATA')