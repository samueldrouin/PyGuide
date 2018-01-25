# PyQt import
from PyQt5.QtWidgets import QWidget

# Project import
from interface.a_propos import Ui_a_propos

class APropos(QWidget, Ui_a_propos):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Slots
        self.btn_close.clicked.connect(self.close)