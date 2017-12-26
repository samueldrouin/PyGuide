# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import os

class CategorieActivite(QDialog):
    def __init__(self, type):
        super(CategorieActivite, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'categorie_activite.ui')
        uic.loadUi(ui, self)

