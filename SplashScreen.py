#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 2021/2/18
@author: Irony
@site: https://github.com/PyQt5
@email: 892768447@qq.com
@file: SplashScreen
@description: 
"""

import hashlib
import json
import os
import sys

from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import QMovie, QColor, QGradient, QPixmap
from PyQt5.QtNetwork import QLocalSocket, QLocalServer
from PyQt5.QtWidgets import QSplashScreen, QApplication, QWidget, QVBoxLayout


class SplashScreen(QSplashScreen):
    """PyQt 启动界面"""

    def __init__(self, name, image='', widget=None, above=False):
        super(SplashScreen, self).__init__()
        self.m_clients = set()
        self.m_movie = None
        self.m_server = None
        self.m_image = image
        self.m_widget = widget
        self.m_alignment = Qt.AlignHCenter | Qt.AlignBottom
        self.m_color = Qt.black
        self.initSplash(name, above)
        self.initPixmap()
        self.initWidget()

    def setAlignment(self, alignment):
        """设置文本位置
        :param alignment: Qt.AlignmentFlag
        """
        if isinstance(alignment, Qt.AlignmentFlag):
            self.m_alignment = alignment

    def setColor(self, color):
        """设置文本颜色
        :param color: Qt.GlobalColor, QColor, QGradient
        """
        if isinstance(color, (Qt.GlobalColor, QColor, QGradient)):
            self.m_color = color

    def showMessage(self, message, progress=0, alignment=None, color=None):
        """设置进度文本
        :param message: 纯文本或html文本
        :param progress: 进度条值
        :param alignment: 对齐方式
        :param color: 文字颜色
        """
        if self.m_widget and hasattr(self.m_widget, 'labelMessage'):
            label = getattr(self.m_widget, 'labelMessage', None)
            progressbar = getattr(self.m_widget, 'labelProgress', None)
            if progressbar and isinstance(progress, int):
                progressbar.setValue(progress)

            if message is not None:
                if hasattr(label, 'setHtml'):
                    label.setHtml(message)
                    return
                elif hasattr(label, 'setText'):
                    label.setText(message)
                    return

        elif message is not None:
            super(SplashScreen, self).showMessage(message,
                                                  alignment or self.m_alignment,
                                                  color or self.m_color)

    def mousePressEvent(self, event):
        """取消默认的鼠标点击隐藏
        :param event: QMouseEvent
        """
        event.ignore()

    def initSplash(self, name, above=False):
        """初始化启动画面
        :param name: local server name
        :param above: stays on top
        """
        # 鼠标
        self.setCursor(Qt.WaitCursor)

        # 是否置顶
        if above:
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowStaysOnTopHint)

        # 创建本地server
        self.m_server = QLocalServer(self)
        if self.m_server.listen(self.getName(name)):
            self.m_server.newConnection.connect(self.slotNewConnection)

    def initPixmap(self):
        """加载背景图"""
        if self.m_image.endswith('.gif'):
            self.m_movie = QMovie(self.m_image, b'gif', self)
            self.m_movie.frameChanged.connect(
                lambda _: self.setPixmap(self.m_movie.currentPixmap()))
            self.m_movie.start()
        else:
            self.setPixmap(QPixmap(self.m_image))

    def initWidget(self):
        if self.m_widget and callable(self.m_widget):
            self.m_widget = self.m_widget()
        if not isinstance(self.m_widget, QWidget):
            return
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.m_widget)

    def slotNewConnection(self):
        """新客户端连接"""
        socket = self.m_server.nextPendingConnection()
        socket.readyRead.connect(self.slotReadyRead)
        socket.disconnected.connect(self.slotDisconnected)
        self.m_clients.add(socket)

    def slotReadyRead(self):
        """收到数据"""
        socket = self.sender()
        if not socket:
            return
        while 1:
            message = socket.readLine().data()
            if not (message and message.endswith(b'\n')):
                break
            message = message.strip(b'\n').decode('utf-8', errors='ignore')
            try:
                message = json.loads(message)
                print('recv:', message)
                text = message.get('text', None)
                progress = message.get('progress', None)
            except Exception as e:
                print(e)
                break
            if text == 'exit':
                self.close()
                QApplication.instance().quit()
                break
            elif text == progress is None:
                break
            else:
                self.showMessage(text, progress)

    def slotDisconnected(self):
        """客户端断开连接"""
        socket = self.sender()
        if socket:
            socket.deleteLater()
        if socket in self.m_clients:
            self.m_clients.remove(socket)

        if len(self.m_clients) == 0:
            self.close()
            QApplication.instance().quit()

    @classmethod
    def getName(cls, name=None):
        if not name or len(str(name)) == 0:
            name = hashlib.md5(
                os.path.dirname(sys.argv[0]).encode()).hexdigest()
        return str(name)

    @classmethod
    def connect(cls, single=False):
        """连接启动器
        :param single: 如果是单实例则客户端必须由启动器启动
        """
        name = os.environ.get('SplashConnectName', None)
        if not name:
            if single:
                # 单实例客户端必须由启动器启动
                sys.exit(-1)
            return
        cls.client = QLocalSocket()
        cls.client.connectToServer(name)

    @classmethod
    def disconnect(cls):
        if hasattr(cls, 'client'):
            cls.client.close()

    @classmethod
    def sendMessage(cls, message):
        """发送json消息
        :param message: json消息，必须\n结尾
        """
        if not hasattr(cls, 'client'):
            return
        if not message.endswith('\n'):
            message += '\n'
        print('send:', message)
        cls.client.write(message.encode())
        cls.client.flush()

    @classmethod
    def start(cls, path, image, widget=None, single=False, name=None,
              above=False, alignment=None, color=None):
        """
        :param path: 客户端路径
        :param image: 背景图片
        :param widget: 自定义的UI层
        :param single: 是否单实例，默认 False
        :param name: 单实例唯一名
        :param above: 是否置顶
        :param alignment: 文字对齐位置
        :param color: 文本颜色
        """
        name = cls.getName(name)
        os.environ['SplashConnectName'] = name

        # 单实例检测
        if single:
            s = QLocalSocket()
            s.connectToServer(name)
            if s.waitForConnected():
                # 应用已经启动则退出
                s.close()
                s.deleteLater()
                print('application is already running')
                sys.exit(0)

        app = QApplication(sys.argv)
        # 启动客户端并将参数传递
        QProcess.startDetached(path, sys.argv[1:])

        # 显示启动界面
        w = SplashScreen(name, image, widget, above)
        w.setAlignment(alignment)
        w.setColor(color)
        w.show()

        sys.exit(app.exec_())
