"""Création ou modification des responsables"""

# Python import
import os

# PyQt import
from PyQt5 import uic
from PyQt5.QtSql import QSqlQuery

# Project import
from form import Form
from script.database import Error

# Interface import
from interface.responsable import Ui_Responsable


class Responsable(Form, Ui_Responsable):
    """Dialog pour la créaction ou la modification des responsables"""
    def __init__(self, database):
        super(Responsable, self).__init__()
        self.setupUi(self)

        # Instance variable definition
        self.DATABASE = database

        # Validator
        self.txt_prenom.setValidator(self.name_validator())
        self.txt_nom.setValidator(self.name_validator())

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.check_fields)

    def check_fields(self):
        """
        Vérifie que tout les champs sont remplis
        :return: True s'ils sont bien remplis
        """
        if self.txt_prenom.text() != "":
            self.process()
        else:
            self.message_box_missing_information("Le prénom du responsable doit être remplis")

    def process(self):
        """
        Traitement dans donnes dans la base de données
        Implante dans les sous classes
        """
        pass


class NouveauResponsable(Responsable):
    """Dialog pour la créaction de nouveau responsables"""
    def __init__(self, database):
        super(NouveauResponsable, self).__init__(database)

        # Interface graphique
        self.lbl_titre.setText("Nouveau responsable")

    def process(self):
        """
        Ajouter le nouveau responsable a la base de donnees
        """
        query = QSqlQuery(self.DATABASE)
        query.prepare("INSERT INTO responsable "
                        "(prenom, nom) "
                      "VALUES "
                        "(:prenom, :nom)")
        query.bindValue(':prenom', self.txt_prenom.text())
        query.bindValue(':nom', self.txt_nom.text())
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie


class ModifierResponsable(Responsable):
    """Dialog pour la modification de responsable"""
    def __init__(self, database, id_responsable):
        super(ModifierResponsable, self).__init__(database)

        # Instance variable definition
        self.id_responsable = id_responsable

        # Interface graphique
        self.lbl_titre.setText("Nouveau type d'activité")
        self.btn_add.setText("Modifier")
        self.show_informations()

    def show_informations(self):
        """
        Afficher les informations sur le type d'activite
        """
        # Obtenir les informations de la base de donnees
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                        "prenom, "
                        "nom "
                      "FROM "
                        "responsable "
                      "WHERE "
                        "id_responsable = :id_responsable")
        query.bindValue(':id_responsable', self.id_responsable)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Afficher les informations
        query.first()
        self.txt_prenom.setText(query.value(0))
        self.txt_nom.setText(query.value(1))

    def process(self):
        """
        Modifier le responsable dans la base de donnees
        """
        query = QSqlQuery(self.DATABASE)
        query.prepare("UPDATE responsable "
                      "SET "
                        "prenom = :prenom, "
                        "nom = :nom "
                      "WHERE "
                        "id_responsable=:id_responsable")
        query.bindValue(':prenom', self.txt_prenom.text())
        query.bindValue(':nom', self.txt_nom.text())
        query.bindValue(':id_responsable', self.id_responsable)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie
