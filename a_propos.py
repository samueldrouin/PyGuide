# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os


class APropos(QDialog):
    def __init__(self):
        super(APropos, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'about.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_close.clicked.connect(self.close)