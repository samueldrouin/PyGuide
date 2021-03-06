# This file is part of PyGuide.
#
# PyGuide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyGuide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyGuide.  If not, see <http://www.gnu.org/licenses/>.

"""Création ou modification d'un lieu"""


# PyQt import
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog

# Project import
from guide.script.database import database_error
from guide.script.interface import validator
from guide.script.interface import completer
from guide.script.database import data_processing
from guide.script.data import data_error
from guide.script.data import parsing

# Interface import
from guide.interface.ui_lieu import Ui_Lieu


class Lieu(QDialog, Ui_Lieu):
    """Dialog de base pour la création ou la modification des lieux"""
    def __init__(self, database):
        super(Lieu, self).__init__()
        self.setupUi(self)

        # Instance variable definition
        self.DATABASE = database

        # Validator
        self.txt_nom.setValidator(validator.name_validator())
        self.txt_adresse1.setValidator(validator.address_validator())
        self.txt_adresse2.setValidator(validator.address_validator())
        self.txt_ville.setValidator(validator.name_validator())
        self.txt_code_postal.setValidator(validator.zip_code_validator())

        # Completer
        self.txt_ville.setCompleter(completer.ville_completer())

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.check_fields)
        self.txt_code_postal.cursorPositionChanged.connect(self.afficher_code_postal)

    def afficher_code_postal(self, old, new):
        """
        Affiche le code postal formatté
        :param old: Old cursor position
        :param new: New cursor position
        """
        code_postal = parsing.zip_code_parsing(old, new, self.sender().text())
        self.sender().setText(code_postal)

    def check_fields(self):
        """
        Vérifie que tout les champs sont remplis
        :return: True s'ils sont bien remplis
        """
        if self.txt_nom.text() != "":
            self.process()
        else:
            data_error.message_box_missing_information("Le nom du lieu doit être remplis")

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
        query = QSqlQuery(self.DATABASE)
        query.prepare("INSERT INTO lieu (nom, adresse_1, adresse_2, ville, province, code_postal) "
                      "VALUES (:nom, :adresse_1, :adresse_2, :ville, :province, :code_postal)")
        query.bindValue(':nom', data_processing.check_string(self.txt_nom.text()))
        query.bindValue(':adresse_1', data_processing.check_string(self.txt_adresse1.text()))
        query.bindValue(':adresse_2', data_processing.check_string(self.txt_adresse2.text()))
        query.bindValue(':ville', data_processing.check_string(self.txt_ville.text()))
        query.bindValue(':province', data_processing.check_string(self.cbx_province.currentText()))
        query.bindValue(':code_postal', data_processing.check_string(self.txt_code_postal.text()))
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not database_error.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie


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
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                        "nom, "
                        "adresse_1, "
                        "adresse_2, "
                        "ville, "
                        "province, "
                        "code_postal "
                      "FROM "
                        "lieu "
                      "WHERE "
                        "id_lieu = :id_lieu")
        query.bindValue(':id_lieu', self.id_lieu)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        database_error.sql_error_handler(query.lastError())

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
        query = QSqlQuery(self.DATABASE)
        query.prepare("UPDATE "
                        "lieu "
                      "SET "
                        "nom = :nom, "
                        "adresse_1 = :adresse_1, "
                        "adresse_2 = :adresse_2, "
                        "ville = :ville, "
                        "province = :province, "
                        "code_postal = :code_postal "
                      "WHERE "
                        "id_lieu = :id_lieu")
        query.bindValue(':nom', data_processing.check_string(self.txt_nom.text()))
        query.bindValue(':adresse_1', data_processing.check_string(self.txt_adresse1.text()))
        query.bindValue(':adresse_2', data_processing.check_string(self.txt_adresse2.text()))
        query.bindValue(':ville', data_processing.check_string(self.txt_ville.text()))
        query.bindValue(':province', data_processing.check_string(self.cbx_province.currentText()))
        query.bindValue(':code_postal', data_processing.check_string(self.txt_code_postal.text()))
        query.bindValue(':id_lieu', self.id_lieu)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not database_error.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie
