#!/bin/sh

python.exe -m PyInstaller .\main_pyqt5.spec --noconfirm
xcopy data .\dist\soda\data /E /H /I
