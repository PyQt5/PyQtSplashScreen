#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/2/20
@author: Irony
@site: https://github.com/PyQt5
@email: 892768447@qq.com
@file: Launcher1
@description: 
"""

import cgitb
import os
import sys
from random import randint

import Resource_rc
from SplashScreen import SplashScreen


if __name__ == '__main__':
    cgitb.enable(format='text')
    Resource_rc.qInitResources()

    executable = 'Client'
    if sys.argv[0].find('.py') > -1:
        # 调试时用
        sys.argv.append(os.path.abspath('Client.py'))
        executable = sys.executable

    SplashScreen.start(
        executable,
        ':/Resources/Splash{0}.gif'.format(randint(1, 2)),
        single=True, above=True)
