"""Script de lancement du programme GUIDE-CFR"""

# Python import
import os
import sys

# PyQt import
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5 import QtCore
#from PyQt5.QtGui import QStyleFactory

# Project import
from mainwindow import MainWindow

# Enable High DPI display with PyQt5
QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps)

if __name__ == "__main__":
    APP = QApplication(sys.argv)
    MAIN_WINDOW = MainWindow()
    MAIN_WINDOW.show()
    sys.exit(APP.exec_())
