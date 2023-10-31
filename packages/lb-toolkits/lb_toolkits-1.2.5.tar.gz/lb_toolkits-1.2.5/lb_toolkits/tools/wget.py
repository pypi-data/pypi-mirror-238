# -*- coding:utf-8 -*-
'''
@Project     : lb_toolkits

@File        : wget.py

@Modify Time :  2023/10/30 14:19   

@Author      : Lee    

@Version     : 1.0   

@Description :

'''
import os
import sys
import numpy as np
import datetime
import shutil
import platform

from lb_toolkits import parm

exedir = os.path.abspath(list(parm.__path__)[0])
from lb_toolkits.downloadcentre import downwgetfromgithub

if platform.system().lower() == 'windows' :
    WGET = os.path.join(exedir, 'bin', 'windows', 'wget.exe')
    if not os.path.isfile(WGET) :
        downwgetfromgithub(WGET)
        if not os.path.isfile(WGET) :
            raise Exception('wget工具不可用')
else:
    WGET = os.path.join(exedir, 'bin', 'linux', 'wget')
    if not os.path.isfile(WGET) :
        downwgetfromgithub(WGET)
        if not os.path.isfile(WGET) :
            raise Exception('wget工具不可用')


def wget(outdir, url, username=None, password=None, token=None,
         tries=3, skip=False, cover=False, options=None):
    ''' 通过wget方式进行数据下载 '''

    local_filename = os.path.basename(url)
    local_filename = os.path.join(outdir, local_filename)
    if skip :
        return local_filename

    if os.path.isfile(local_filename) :
        if cover :
            print('文件已存在，将执行删除文件【%s】' %(local_filename))
            os.remove(local_filename)
        else:
            print('文件已存在，跳过下载【%s】' %(local_filename))
            return local_filename

    tempfile = local_filename + '.download'

    cmd = [f'{WGET}']
    if username is not None and password is not None :
        cmd.append(f'--http-user={username} --http-passwd={password}')

    if tries is not None :
        cmd.append(f'--tries={tries}')
    cmd.append('--no-check-certificate -e robots=off -c -np -R .html,.tmp -nH --cut-dirs=10')
    if options is not None :
        if isinstance(options, str) :
            cmd.append(options)
        elif isinstance(options, list) :
            cmd.extend(options)
    cmd.append(f'{url}')
    if token is not None :
        cmd.append(f'--header "Authorization: Bearer {token}"')
    cmd.append(f'-O {tempfile}')

    command = ' '.join(cmd)
    print('执行下载命令: 【%s】' %(command))
    os.system(command)

    if os.path.isfile(local_filename) :
        os.remove(local_filename)

    if os.path.isfile(tempfile) :
        shutil.move(tempfile, local_filename)

    if os.path.isfile(local_filename) and os.stat(local_filename).st_size == 0 :
        os.remove(local_filename)

    return local_filename



