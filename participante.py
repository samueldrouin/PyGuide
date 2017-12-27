# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os


class Participante(QDialog):
    def __init__(self, connection):
        super(Participante, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'participante.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.close)