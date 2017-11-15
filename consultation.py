# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import os

# Project import
from place import Place

"""
GUI text for each type
May need to be updated after an update to database fields
"""
# Consultation d'un lieu
g_view_place_title = "Consultation d'un lieu" # Window title
g_search_fields = ["Nom du lieu","Rue","Ville"] # Search fields name list
g_sort_fields = ["Nom du lieu","Rue","Ville"] # Sort fields name list

class Consultation(QDialog):
    def __init__(self, type):
        """
        :param type:
            1 : Membre
            2 : Activite
            3 : Lieux
            4 : Participantes
            5 : Type d'activité
        """
        super(Consultation, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'consultation.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_close.clicked.connect(self.close) # Close windows on "Close" button clicked
        self.cbx_search.currentIndexChanged.connect(self.update_search_placeholder_text)

        """
        Set window caracteristics from global variable
        DO NOT edit the pattern of this section unless you know EXACTLY what you are doing
        
        To add new type follow the pattern of any other type and increment the number
        of the last type by 1 for type number
        """
        if type == 3:
            self.lbl_title.setText(g_view_place_title)
            self.window().setWindowTitle(g_view_place_title)
            self.cbx_search.addItems(g_search_fields)
            self.cbx_sort.addItems(g_sort_fields)
            self.btn_add.clicked.connect(self.open_add_place)

    def update_search_placeholder_text(self):
        """
        Update search placeholder text with current item from combo box
        DO NOT UPDATE this function unless you know EXACTLY what you are doing
        :return: None
        """
        s = self.cbx_search.currentText()
        self.txt_search.setPlaceholderText(s)

    """
    Following function open a window to create a new instance of the current type
    Name are self explanatory
    """
    def open_add_place(self):
        self.place = Place()
        self.place.show()

    """
    Pour changer les requêtes changer le code suivant
    This code MUST be updated after an update to the database fields
    """
    def place_query(self):
        sql = "SELECT * FROM places"

        # Check if the search field is not empty
        if self.cbx_search.currentIndex() == 0:
            if self.txt_search.text():
               sql += " WHERE name = %s"%self.txt_search.text()
        elif self.cbx_search.currentIndex() == 1:
            if self.txt_search.text():
               sql += " WHERE road = %s"%self.txt_search.text()
        elif self.cbx_search.currentIndex() == 2:
            if self.txt_search.text():
               sql += " WHERE city = %s"%self.txt_search.text()

        # Check if a sort is active
        if self.cbx_sort.currentIndex() == 0:
            sql += " ORDER BY name"
        elif self.cbx_sort.currentIndex() == 1:
            sql += " ORDER BY road"
        elif self.cbx_sort.currentIndex() == 2:
            sql += " ORDER BY city"

        # Sort by descending order
        if self.chk_desk.isChecked():
            sql += " DESC"