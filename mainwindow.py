from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)

    def open_consult_participantes(self):
        """
        Ouvrir le fenêtre de consultation des participantes
        :return: Aucun
        """
        