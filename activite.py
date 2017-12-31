# Python import
from PyQt5.QtWidgets import QWidget
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
        self.rbt_unique.toggled.connect(self.afficher_champs_date)
        self.rbt_recurrente.toggled.connect(self.afficher_champs_date)

        # Affichage des champs pour les dates
        self.afficher_champs_date()

    def afficher_champs_date(self):
        """
        Afficher les champs pour entrer les dates
        """

        # Date unique
        if self.rbt_unique.isChecked():
            self.widget_recurrente.setHidden(True)
            self.widget_unique.setHidden(False)

        # Plusieurs dates
        else:
            self.widget_unique.setHidden(True)
            self.widget_recurrente.setHidden(False)

    def clearLayout(layout, self):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clearLayout(child.layout())

class NouvelleActivite(Activite):
    def __init__(self):
        super(NouvelleActivite, self).__init__()


class ModifierActivite(Activite):
    def __init__(self):
        super(ModifierActivite, self).__init__()