"""Statistiques"""
# Python import
import os

# PyQt import
from PyQt5 import uic

# Project import
from form import Form

class Statistiques(Form):
    """Dialog des statistiques"""
    def __init__(self, database):
        super(Statistiques, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'statistique.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.DATABASE = database
