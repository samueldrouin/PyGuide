# PyQt import
from PyQt5.QtWidgets import QDialog

# Project import
from interface.a_propos import Ui_APropos

class APropos(QDialog, Ui_APropos):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Slots
        self.btn_close.clicked.connect(self.close)