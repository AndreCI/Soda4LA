import datetime
import sys
import time


import os
import logging

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication

from ViewsPyQT5.main_view import MainWindow

logging.basicConfig(filename="soda.log", filemode="w", level=logging.DEBUG)


#
# from Utils import m_fluidsynth
# synth = m_fluidsynth.Synth()
# sequencer = m_fluidsynth.Sequencer(time_scale=1000)
# registeredSynth = sequencer.register_fluidsynth(synth)
# sfpath = "D:/visiteur/Documents/Github/sodaMidi/data/soundfonts/Clean_Guitar.sf2"
# synth.start()
# lo = synth.sfload(sfpath)
# synth.program_select(0, lo, 0, 0)
# synth.noteon(0, 100, 100)
# time.sleep(5)
#
# exit()
#
# for f in os.listdir():
#     print(f)
#     if(os.path.isdir(f)):
#         for ff in os.listdir(f):
#             print("   {}".format(ff))

import Views.main_view


if __name__ == "__main__":
    print("starting soda at {}".format(datetime.datetime.now()))

    app = QApplication(sys.argv)
    file = QFile("data/img/pyqt5/themes/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    window = MainWindow()
    window.showMaximized()

    app.exec()

