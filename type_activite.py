# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os


class TypeActivite(QDialog):
    def __init__(self):
        super(TypeActivite, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'type_activite.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.close)