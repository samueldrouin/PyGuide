# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
import os

# Project import
import Scripts.validator
import Scripts.query


class Place(QDialog):
    def __init__(self):
        super(Place, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'lieux.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.close)
        self.btn_add.clicked.connect(self.create_place)

        # Validator
        self.txt_road.setValidator(Scripts.validator.address_validator())
        self.txt_name.setValidator(Scripts.validator.name_validator())
        self.txt_city.setValidator(Scripts.validator.city_validator())

    def create_place(self):
        name = self.txt_name.text()
        road = self.txt_road.text()
        city = self.txt_city.text()
        Scripts.query.create_place(name, road, city)
