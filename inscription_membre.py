# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os
from PyQt5.QtCore import pyqtSignal


class InscriptionMembre(QDialog):
    #Signals
    cancelled = pyqtSignal()
    inscrit = pyqtSignal()

    def __init__(self):
        super(InscriptionMembre, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'inscription_membre.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.cancel)
        self.btn_inscription.clicked.connect(self.inscription)

    def inscription(self):
        """
        Enregistre le status de membre lorsque l'inscritpion est completee
        """
        self.inscrit.emit()
        self.close()

    def cancel(self):
        """
        Annule l'inscription
        """
        self.cancelled.emit()
        self.close()