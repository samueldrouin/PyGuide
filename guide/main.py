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
