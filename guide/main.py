"""Script de lancement du programme GUIDE-CFR"""

# Python import
import os
import sys

# PyQt import
from PyQt5.QtWidgets import QApplication

# Project import
from mainwindow import MainWindow

# Screen scaling on HiDPI
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

if __name__ == "__main__":
    APP = QApplication(sys.argv)
    MAIN_WINDOW = MainWindow()
    MAIN_WINDOW.show()
    sys.exit(APP.exec_())
