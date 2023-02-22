import datetime
import logging
import sys

from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from ViewsPyQT5.main_view import MainWindow

logging.basicConfig(filename="soda.log", filemode="w", level=logging.INFO)

if __name__ == "__main__":
    logging.log(logging.INFO, "Starting SODA at {}".format(datetime.datetime.now()))

    app = QApplication(sys.argv)
    file = QFile("data/img/pyqt5/themes/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    window = MainWindow()
    window.showMaximized()
    window.setWindowIcon(QIcon('data/img/icons/logo_w_trans.png'))
    app.exec()
    logging.log(logging.INFO, "SODA ended normally at {}".format(datetime.datetime.now()))
