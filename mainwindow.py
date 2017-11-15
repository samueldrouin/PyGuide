# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
import os
import pymysql.cursors

# Project import
from consultation import Consultation
from place import Place

# Variable
g_host = 'localhost'
g_user = 'samueldrouin'
g_password = 'XqB4ao9yj2c9NPsKaWz2qTR1C9hLtU4e'
g_db = 'Memory'
g_charset = 'utf8'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui = os.path.join(os.path.dirname(__file__),'UI','mainwindow.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_consult_participantes.clicked.connect(self.open_consult_participantes)
        self.btn_consult_activites.clicked.connect(self.open_consult_activite)
        self.btn_consult_lieux.clicked.connect(self.open_consult_lieux)
        self.btn_consult_membres.clicked.connect(self.open_consult_membres)
        self.btn_consult_type_activite.clicked.connect(self.open_consult_type_activite)
        self.btn_gest_lieux.clicked.connect(self.open_gest_lieux)

        # Actions
        self.act_consult_membres.triggered.connect(self.open_consult_membres)
        self.act_consult_activites.triggered.connect(self.open_consult_activite)
        self.act_consult_lieux.triggered.connect(self.open_consult_lieux)
        self.act_consult_participantes.triggered.connect(self.open_consult_participantes)
        self.act_consult_type_activite.triggered.connect(self.open_consult_type_activite)

    def open_consult_participantes(self):
        """
        Ouvrir la fenêtre de consultation des participantes
        :return: Aucun
        """
        self.consultation = Consultation(4)
        self.consultation.exec()

    def open_consult_membres(self):
        """
        Ouvrir la fenêtre de consultation des membres
        :return: Aucun
        """
        self.consultation = Consultation(1)
        self.consultation.exec()

    def open_consult_activite(self):
        """
        Ouvrir la fenêtre de consultation des activites
        :return: Aucun
        """
        self.consultation = Consultation(2)
        self.consultation.exec()

    def open_consult_lieux(self):
        """
        Ouvrir la fenêtre de consultation des lieux
        :return: Aucun
        """
        self.consultation = Consultation(3)
        self.consultation.exec()

    def open_consult_type_activite(self):
        """
        Ouvrir la fenêtre de consultation des types d'activite
        :return: Aucun
        """
        self.consultation = Consultation(5)
        self.consultation.show()

    def open_gest_lieux(self):
        """
        Ouvrir la fenêtre de gestion des lieux
        :return: Aucune
        """
        self.place = Place()
        self.place.show()