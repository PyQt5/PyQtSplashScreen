cd %~dp0

pyinstaller Launcher1.py -y

pyinstaller Launcher2.py -y

pyinstaller Launcher3.py -y

pyinstaller -y Client.py --add-binary=dist\Launcher1\Launcher1.exe;. --add-binary=dist\Launcher2\Launcher2.exe;. --add-binary=dist\Launcher3\Launcher3.exe;.