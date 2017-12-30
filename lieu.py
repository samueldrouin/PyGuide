# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os

# Project import
from form import Form

class Lieu(Form):
    def __init__(self):
        super(Lieu, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'lieu.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.database = None

        # Slots
        self.btn_cancel.clicked.connect(self.reject)


class NouveauLieu(Lieu):
    def __init__(self, database):
        super(NouveauLieu, self).__init__()

        # Instance variable definition
        self.database = database


class ModifierLieu(Lieu):
    def __init__(self, database):
        super(ModifierLieu, self).__init__()

        # Instance variable definition
        self.database = database