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

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget

import Resource_rc
from SplashScreen import SplashScreen
from UiFiles.Ui_AdobeCenter import Ui_AdobeCenter


class AdobeCenter(QWidget, Ui_AdobeCenter):

    def __init__(self):
        super(AdobeCenter, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    cgitb.enable(format='text')
    Resource_rc.qInitResources()

    executable = 'Client'
    if sys.argv[0].find('.py') > -1:
        # 调试时用
        sys.argv.append(os.path.abspath('Client.py'))
        executable = sys.executable

    SplashScreen.start(
        executable, ':/Resources/Splash2013Background.png',
        AdobeCenter, above=True, color=QColor(43, 204, 249))
