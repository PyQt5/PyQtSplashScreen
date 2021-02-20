# PyQtSplashScreen

原本考虑使用C++ Qt编写，但需要编译个版本比较麻烦，这里使用Python编写，并编译为独立的Launcher进程

启动界面采用独立进程（考虑相同进程繁忙时可能导致界面不更新，故分离出来）。并使用`QLocalSocket`来作为通信传递消息

ScreenShot

![Launcher1](ScreenShot/Launcher1.gif)

![Launcher2](ScreenShot/Launcher2.gif)

![Launcher3-1](ScreenShot/Launcher3-1.gif)

![Launcher3-2](ScreenShot/Launcher3-2.gif)