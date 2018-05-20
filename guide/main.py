#This file is part of PyGuide.
#
#PyGuide is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#PyGuide is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with PyGuide.  If not, see <http://www.gnu.org/licenses/>.

"""Script de lancement du programme GUIDE-CFR"""

# Python import
import os
import sys
import time

# PyQt import
from PyQt5.QtWidgets import QApplication, QStyleFactory, QSplashScreen
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

# Project import
from mainwindow import MainWindow
from script.launch.check_database import check_database_created

# Permettre les écrans High DPI avec PyQt5
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Ajouter l'icon de l'application
    app.setWindowIcon(QIcon(":/global/Logo.png"))

    # Vérifier l'état de la base de données
    db = check_database_created()

    # Afficher la fenêtre principale
    main_window = MainWindow(db)
    main_window.show()
    sys.exit(app.exec_())
