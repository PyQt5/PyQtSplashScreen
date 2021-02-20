#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/2/18
@author: Irony
@site: https://github.com/PyQt5
@email: 892768447@qq.com
@file: Client
@description: 
"""
import cgitb
import json
import sys
from random import randint
from threading import Thread
from time import sleep

from PyQt5.QtWidgets import QApplication, QWidget

from SplashScreen import SplashScreen

UseHtml = randint(0, 10) % 2


def formatText(text, color, progress=0):
    text = '<font color={0}>{1}</font>'.format(color, text) if UseHtml else text
    return json.dumps({'text': text, 'progress': progress}) + '\n'


def initData():
    # 模拟后台初始化其他数据
    SplashScreen.sendMessage(formatText('初始化其他数据', 'red'))
    sleep(2)

    for i in range(1, 101):
        SplashScreen.sendMessage(
            formatText('加载模型中...{0}%'.format(i), 'green', i))
        sleep(0.1)


class Window(QWidget):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        # 模拟界面初始化
        sleep(2)
        SplashScreen.sendMessage(formatText('UI初始化完成', 'white'))
        sleep(2)

        # 模拟加载其它数据
        t = Thread(target=initData, daemon=True)
        t.start()
        t.join()

        # 加载完成发送退出
        SplashScreen.sendMessage(
            json.dumps({'text': 'exit', 'progress': 0}) + '\n')
        SplashScreen.disconnect()


if __name__ == '__main__':
    cgitb.enable(format='text')

    SplashScreen.connect(True)
    SplashScreen.sendMessage(formatText('初始化中...', 'white'))

    app = QApplication(sys.argv)

    # 创建界面
    w = Window()
    w.show()

    sys.exit(app.exec_())
