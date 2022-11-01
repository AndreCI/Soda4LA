#!/bin/sh

python.exe -m PyInstaller .\main_pyqt5.spec --noconfirm
xcopy data .\dist\main_pyqt5\data /E /H /I
