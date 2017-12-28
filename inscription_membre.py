# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import os
from PyQt5.QtCore import pyqtSignal

# Project import
from form import Form


class InscriptionMembre(Form):
    def __init__(self, nom, phone):
        super(InscriptionMembre, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'inscription_membre.ui')
        uic.loadUi(ui, self)

        # Affichage de l'interface
        self.txt_nom.setText(nom)
        self.txt_telephone.setText(phone)

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_inscription.clicked.connect(self.inscription)

    def get_numero_membre(self):
        query = QSqlQuery()
        query.exec_("SELECT MAX(numero_membre) FROM membre")
        query.first()
        self.txt_numero_membre.setText(query.value(0))

    def inscription(self):
        """
        Enregistre le status de membre lorsque l'inscritpion est completee
        """
        self.accept()