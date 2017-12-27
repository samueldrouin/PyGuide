# Python import
from PyQt5.QtWidgets import QDialog, QCompleter
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp, Qt, QDate
from PyQt5 import uic
import os


class Participante(QDialog):
    def __init__(self, connection):
        super(Participante, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'participante.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.connection = connection

        # Validator definition
        name_validator = QRegExpValidator(QRegExp("^[a-zA-ZÀ-ÿ -]{0,45}$"))
        address_validator = QRegExpValidator(QRegExp("^[0-9a-zA-ZÀ-ÿ -.]{0,45}$"))
        zip_code_validator = QRegExpValidator(QRegExp("^[A-Z]{1}[0-9]{1}[A-Z]{1}[0-9 ]{1}[0-9]{1}[A-Z]{1}[0-9]{1}$"))
        telephone_validator = QRegExpValidator(QRegExp("^[0-9]{3}[0-9 ]{1}[0-9]{3}[0-9-]{1}[0-9]{4}$"))
        poste_validator = QRegExpValidator(QRegExp("^[0-9]{0,5}$"))
        numero_membre_validator = QRegExpValidator(QRegExp("^[0-9]{0,10}$"))

        # Validator
        self.txt_prenom.setValidator(name_validator)
        self.txt_nom.setValidator(name_validator)
        self.txt_adresse1.setValidator(address_validator)
        self.txt_adresse2.setValidator(address_validator)
        self.txt_ville.setValidator(name_validator)
        self.txt_code_postal.setValidator(zip_code_validator)
        self.txt_telephone1.setValidator(telephone_validator)
        self.txt_poste1.setValidator(poste_validator)
        self.txt_telephone2.setValidator(telephone_validator)
        self.txt_poste2.setValidator(poste_validator)
        self.txt_numero_membre.setValidator(numero_membre_validator)

        # Completer
        liste_ville = ["Saint-Jean-sur-Richelieu", "Saint-Blaire-sur-Richelieu", "Saint-Paul-de-l'Île-aux-Noix",
                       "Saint-Valentin", "Lacolle", "Noyan", "Saint-Sébastien", "Henryville", "Saint-Alexandre",
                       "Sainte-Anne-de-Sabrevois", "Sainte-Brigide-d'Iberville","Mont-Saint-Grégoire",
                       "Venise-en-Québec", "Saint-Georges-de-Clarenceville"]
        completer = QCompleter(liste_ville)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.txt_ville.setCompleter(completer)

        # Default values
        current_date = QDate.currentDate()
        self.ded_date_naissance.setDate(current_date)

        if QDate.currentDate().month() > 9:
            annee_renouvellement = QDate.currentDate().year()+1
        else:
            annee_renouvellement = QDate.currentDate().year()

        date_renouvellement = QDate(annee_renouvellement,9,1)
        self.ded_renouvellement.setDate(date_renouvellement)

        # Slots
        self.btn_cancel.clicked.connect(self.close)
        self.txt_code_postal.cursorPositionChanged.connect(self.zip_code_parsing)
        self.txt_telephone1.cursorPositionChanged.connect(self.phone_number_parsing)

    def zip_code_parsing(self, old, new):
        """
        Parsing zip code
        :param old: Old cursor position
        :param new: New cursor position
        """
        if new == 4 and old == 3:
            zip_code = self.txt_code_postal.text()
            if zip_code[3] != " ":
                zip_code = zip_code[:3] + " " + zip_code[3:]
                self.txt_code_postal.setText(zip_code)

    def phone_number_parsing(self, old, new):
        """
        Parsing phone number
        :param old: Old cursor position
        :param new: New cursor position
        """
        phone_number = self.sender().text()
        if new == 4 and old == 3:
            if phone_number[3] != " ":
                phone_number = phone_number[:3] + " " + phone_number[3:]
                self.sender().setText(phone_number)
        if new == 8 and old == 7:
            if phone_number[7] != "-":
                phone_number = phone_number[:7] + "-" + phone_number[7:]
                self.sender().setText(phone_number)