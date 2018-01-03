# Screen scaling on HiDPI
import os
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

from mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())