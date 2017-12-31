# Python import
from PyQt5 import uic
import os

# Project import
from form import Form

class Activite(Form):
    def __init__(self):
        super(Activite,self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'activite.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.reject)


class NouvelleActivite(Activite):
    def __init__(self):
        super(NouvelleActivite, self).__init__()


class ModifierActivite(Activite):
    def __init__(self):
        super(ModifierActivite, self).__init__()