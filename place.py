# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import os

# Project import
from form import Form


class Place(Form):
    """
    Parent of CreatePlace and EditPlace classes
    """
    def __init__(self):
        super(Place, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'lieux.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.close)

        # Validator
        self.txt_road.setValidator(self.address_validator())
        self.txt_name.setValidator(self.name_validator())
        self.txt_city.setValidator(self.name_validator())


class CreatePlace(Place):
    def __init__(self):
        super(CreatePlace, self).__init__()

        # Slots
        self.btn_add.clicked.connect(self.create_place)

        # Label
        self.window().setWindowTitle("Créer un lieu")

    def create_place(self):
        name = self.txt_name.text()
        road = self.txt_road.text()
        city = self.txt_city.text()
        Scripts.query.create_place(name, road, city)


class EditPlace(Place):
    def __init__(self, place_id):
        super(EditPlace, self).__init__()
        self.place_id = place_id
        self.get_current_record()

        # Slots
        self.btn_add.clicked.connect(self.edit_place)

        # Label
        self.window().setWindowTitle("Modifier un lieu")
        self.btn_add.setText("Modifier")

    def get_current_record(self):
        sql = "SELECT * FROM places WHERE idplaces = %s" % self.place_id
        place = Scripts.query.execute_query_return_all(sql)
        if place:
            self.txt_name.setText(place[0]["name"])
            self.txt_road.setText(place[0]["road"])
            self.txt_city.setText(place[0]["city"])

    def edit_place(self):
        name = self.txt_name.text()
        road = self.txt_road.text()
        city = self.txt_city.text()
        Scripts.query.edit_place(name, road, city, self.place_id)
        self.close()