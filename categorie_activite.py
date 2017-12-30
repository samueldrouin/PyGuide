# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os

# Projet import
from form import Form

class CategorieActivite(Form):
    def __init__(self):
        super(CategorieActivite, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'categorie_activite.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.reject)


class NouvelleCategorieActivite(CategorieActivite):
    def __init__(self):
        super(NouvelleCategorieActivite, self).__init__()


class ModifierCategorieActivite(CategorieActivite):
    def __init__(self):
        super(ModifierCategorieActivite, self).__init__()