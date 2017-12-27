# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os

class Inscription(QDialog):
    def __init__(self):
        super(Inscription,self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'inscription.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_annuler.clicked.connect(self.close)