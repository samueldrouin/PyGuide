# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os


class Responsable(QDialog):
    def __init__(self):
        super(Responsable, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'responsable.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.close)