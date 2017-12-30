# Python import
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic
import os

# Projet import
from form import Form


class CategorieActivite(Form):
    def __init__(self, database):
        super(CategorieActivite, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'categorie_activite.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.database = database

        # Validator
        self.txt_nom.setValidator(self.address_validator())

        # Elements des ComboBox
        self.afficher_lieu()
        self.afficher_responsable()
        self.afficher_type_activite()

        # Slots
        self.btn_cancel.clicked.connect(self.reject)

    def afficher_responsable(self):
        """
        Afficher la liste des responsables dans le combobox
        """
        # Fetch data from database
        query = QSqlQuery(self.database)
        query.exec_("SELECT prenom, nom FROM responsable")

        # Ajouter les responsables a la liste
        while query.next():
            nom = str(query.value(0)) + " " + str(query.value(1))
            self.cbx_responsable.addItem(nom)

    def afficher_type_activite(self):
        """
        Afficher la liste des types d'activite dans le ComboBox
        """

        # Fetch data from database
        query = QSqlQuery(self.database)
        query.exec_("SELECT nom FROM type_activite")

        # Ajouter les types d'activite a la liste
        while query.next():
            self.cbx_type_activite.addItem(str(query.value(0)))

    def afficher_lieu(self):
        """
        Afficher la liste des lieux dans le ComboBox
        """

        # Fetch data from database
        query = QSqlQuery(self.database)
        query.exec_("SELECT nom FROM lieu")

        # Ajouter les types d'activite a la liste
        while query.next():
            self.cbx_lieu.addItem(str(query.value(0)))


class NouvelleCategorieActivite(CategorieActivite):
    def __init__(self, database):
        super(NouvelleCategorieActivite, self).__init__(database)


class ModifierCategorieActivite(CategorieActivite):
    def __init__(self, database):
        super(ModifierCategorieActivite, self).__init__(database)