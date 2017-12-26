# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
import os

# Project import
from responsable import Responsable
from type_activite import TypeActivite

class Consultation(QDialog):
    def __init__(self, type):
        """
        :param type:
            1 : Type d'activite
            2 : Responsables
        """
        super(Consultation, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'consultation.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_close.clicked.connect(self.close) # Close windows on "Close" button clicked
        self.cbx_search.currentIndexChanged.connect(self.update_search_placeholder_text)

        if type == 1:
            self.lbl_title.setText("Consultation des types d'activité")
            self.window().setWindowTitle("Consultation des types d'activité")
            self.cbx_search.addItems(["Nom"])
            self.cbx_sort.addItems(["Nom"])
            self.btn_add.clicked.connect(self.nouveau_type_activite)

            # Tablewidget characteristics
            self.tbl_result.setColumnCount(2)
            self.tbl_result.setColumnHidden(0, True)
            headers = ["Index", "Nom"]
            self.tbl_result.setHorizontalHeaderLabels(headers)

        elif type == 2:
            self.lbl_title.setText("Consultation des responsables")
            self.window().setWindowTitle("Consultation des responsables")
            self.cbx_search.addItems(["Nom", "Prénom"])
            self.cbx_sort.addItems(["Nom", "Prénom"])
            self.btn_add.clicked.connect(self.nouveau_responsable)

            # Tablewidget characteristics
            self.tbl_result.setColumnCount(3)
            self.tbl_result.setColumnHidden(0, True)
            headers = ["Index", "Nom", "Prénom"]
            self.tbl_result.setHorizontalHeaderLabels(headers)

    def update_search_placeholder_text(self):
        """
        Update search placeholder text with current item from combo box
        DO NOT UPDATE this function unless you know EXACTLY what you are doing
        :return: None
        """
        s = self.cbx_search.currentText()
        self.txt_search.setPlaceholderText(s)

    """
    Les fonctions suivantes ouvrent un dialog pour créer un nouvel élément dans le type actif
    """
    def nouveau_responsable(self):
        responsable = Responsable()
        responsable.exec()

    def nouveau_type_activite(self):
        type_activite = TypeActivite()
        type_activite.exec()
