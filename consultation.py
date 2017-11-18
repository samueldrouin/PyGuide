# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
import os

# Project import
import place
from Scripts import query

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
        Set window characteristics according to type
        DO NOT EDIT THE PATTERN of this section unless you know EXACTLY what you are doing
        
        Follow this pattern to add a new type (edit only when instructed to) :
        if type == 3:
            self.lbl_title.setText(g_view_place_title)
            self.window().setWindowTitle(g_view_place_title)
            self.cbx_search.addItems(g_search_fields)
            self.cbx_sort.addItems(g_sort_fields)
            self.btn_add.clicked.connect(self.open_add_place) # Use new type function
            
            # Tablewidget characteristics
            self.tbl_result.setColumnCount() # Define column count
            self.tbl_result.setColumnHidden(0, True)
            headers = [] # Define headers label 
            self.tbl_result.setHorizontalHeadersItems(headers)
            self.place_query() # Use new type query
        """
        if type == 3:
            self.lbl_title.setText(g_view_place_title)
            self.window().setWindowTitle(g_view_place_title)
            self.cbx_search.addItems(g_search_fields)
            self.cbx_sort.addItems(g_sort_fields)
            self.btn_add.clicked.connect(self.open_add_place)

            # Tablewidget characteristics
            self.tbl_result.setColumnCount(4)
            self.tbl_result.setColumnHidden(0, True)
            headers = ["Index","Nom","Rue","Ville"]
            self.tbl_result.setHorizontalHeaderLabels(headers)
            self.place_query()
            self.tbl_result.cellClicked.connect(self.edit_place)

    def update_search_placeholder_text(self):
        """
        Update search placeholder text with current item from combo box
        DO NOT UPDATE this function unless you know EXACTLY what you are doing
        :return: None
        """
        s = self.cbx_search.currentText()
        self.txt_search.setPlaceholderText(s)

    """
    Following functions open the create dialog of the current type
    
    If a new type is added create a new function for this type
    """
    def open_add_place(self):
        self.create_place = place.CreatePlace()
        self.create_place.show()

    """
    Following functions open the edit dialog of the current type
    
    If a new type is added create a new function for this type
    """
    def edit_place(self, row, column):
        place_id = self.tbl_result.item(row, 0).text()
        edit_place = place.EditPlace(place_id)
        edit_place.exec()

    """
    Change the following code to update query
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
        if self.chk_desc.isChecked():
            sql += " DESC"
        places = query.execute_query_return_all(sql)
        self.tbl_result.setRowCount(len(places))

        r = 0
        for place in places:
            self.tbl_result.setItem(r, 0, QTableWidgetItem(str(place["idplaces"])))
            self.tbl_result.setItem(r, 1, QTableWidgetItem(place["name"]))
            self.tbl_result.setItem(r, 2, QTableWidgetItem(place["road"]))
            self.tbl_result.setItem(r, 3, QTableWidgetItem(place["city"]))
            r = r + 1
