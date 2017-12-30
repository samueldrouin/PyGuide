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

        # Validator
        self.txt_nom.setValidator(self.address_validator())
        self.txt_adresse1.setValidator(self.address_validator())
        self.txt_adresse2.setValidator(self.address_validator())
        self.txt_ville.setValidator(self.name_validator())
        self.txt_code_postal.setValidator(self.zip_code_validator())

        # Completer
        self.txt_ville.setCompleter(self.ville_completer())

        # Slots
        self.btn_cancel.clicked.connect(self.reject)


class NouveauLieu(Lieu):
    def __init__(self, database):
        super(NouveauLieu, self).__init__()

        # Instance variable definition
        self.database = database

        # Interface graphique
        self.setWindowTitle("Nouveau lieu")
        self.lbl_titre.setText("Nouveau lieu")


class ModifierLieu(Lieu):
    def __init__(self, database, id_lieu):
        super(ModifierLieu, self).__init__()

        # Instance variable definition
        self.database = database

        # Interface graphique
        self.setWindowTitle("Modifier un lieu")
        self.lbl_titre.setText("Modifier un lieu")