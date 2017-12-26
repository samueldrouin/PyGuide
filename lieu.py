# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os

class Lieu(QDialog):
    def __init__(self, type):
        super(Lieu, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'lieu.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.close)