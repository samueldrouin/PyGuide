"""Création ou modification d'un lieu"""

# Python import
import os

# PyQt import
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic

# Project import
from form import Form

class Lieu(Form):
    """Dialog de base pour la création ou la modification des lieux"""
    def __init__(self, database):
        super(Lieu, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'lieu.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.database = database

        # Validator
        self.txt_nom.setValidator(self.address_validator())
        self.txt_adresse1.setValidator(self.address_validator())
        self.txt_adresse2.setValidator(self.address_validator())
        self.txt_ville.setValidator(self.name_validator())
        self.txt_code_postal.setValidator(self.zip_code_validator())

        # Completer
        self.txt_ville.setCompleter(self.ville_completer())

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.check_fields)
        self.txt_code_postal.cursorPositionChanged.connect(self.zip_code_parsing)

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

    def check_fields(self):
        """
        Vérifie que tout les champs sont remplis
        :return: True s'ils sont bien remplis
        """
        if self.txt_nom.text() != "":
            self.process()
        else:
            self.message_box_missing_information("Le nom du lieu doit être remplis")

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        Implanter dans les sous classes
        """
        pass


class NouveauLieu(Lieu):
    """Dialog pour la création de nouveau lieu"""
    def __init__(self, database):
        super(NouveauLieu, self).__init__(database)

        # Interface graphique
        self.setWindowTitle("Nouveau lieu")
        self.lbl_titre.setText("Nouveau lieu")

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        """
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO lieu (nom, adresse_1, adresse_2, ville, province, code_postal) "
                      "VALUES (:nom, :adresse_1, :adresse_2, :ville, :province, :code_postal)")
        query.bindValue(':nom', self.check_string(self.txt_nom.text()))
        query.bindValue(':adresse_1', self.check_string(self.txt_adresse1.text()))
        query.bindValue(':adresse_2', self.check_string(self.txt_adresse2.text()))
        query.bindValue(':ville', self.check_string(self.txt_ville.text()))
        query.bindValue(':province', self.check_string(self.cbx_province.currentText()))
        query.bindValue(':code_postal', self.check_string(self.txt_code_postal.text()))
        query.exec_()

        self.accept()


class ModifierLieu(Lieu):
    """Dialog pour la modification d'un lieu existant"""
    def __init__(self, id_lieu, database):
        super(ModifierLieu, self).__init__(database)

        # Instance variable definition
        self.id_lieu = id_lieu

        # Interface graphique
        self.setWindowTitle("Modifier un lieu")
        self.lbl_titre.setText("Modifier un lieu")
        self.btn_add.setText("Modifier")
        self.show_informations()

    def show_informations(self):
        """
        Afficher les informations sur le lieu
        """
        # Obtenir les informations de la base de donnees
        query = QSqlQuery(self.database)
        query.prepare("SELECT nom, adresse_1, adresse_2, ville, province, code_postal "
                      "FROM lieu WHERE id_lieu = :id_lieu")
        query.bindValue(':id_lieu', self.id_lieu)
        query.exec_()

        # Afficher les informations
        query.first()
        self.txt_nom.setText(query.value(0))
        self.txt_adresse1.setText(query.value(1))
        self.txt_adresse2.setText(query.value(2))
        self.txt_ville.setText(query.value(3))
        self.cbx_province.setCurrentText(query.value(4))
        self.txt_code_postal.setText(query.value(5))

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        """
        query = QSqlQuery(self.database)
        query.prepare("UPDATE lieu "
                      "SET nom = :nom, adresse_1 = :adresse_1, adresse_2 = :adresse_2, ville = :ville, "
                      "province = :province, code_postal = :code_postal "
                      "WHERE id_lieu = :id_lieu")
        query.bindValue(':nom', self.check_string(self.txt_nom.text()))
        query.bindValue(':adresse_1', self.check_string(self.txt_adresse1.text()))
        query.bindValue(':adresse_2', self.check_string(self.txt_adresse2.text()))
        query.bindValue(':ville', self.check_string(self.txt_ville.text()))
        query.bindValue(':province', self.check_string(self.cbx_province.currentText()))
        query.bindValue(':code_postal', self.check_string(self.txt_code_postal.text()))
        query.bindValue(':id_lieu', self.id_lieu)
        query.exec_()
        print(query.lastError().text())

        self.accept()
