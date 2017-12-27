# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os

class Facturation(QDialog):
    def __init__(self):
        super(Facturation,self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'facturation.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_annuler.clicked.connect(self.close)