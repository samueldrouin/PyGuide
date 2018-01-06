"""Créaction et la modification de catégorie d'activité"""

# Python import
import os

# PyQt import
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic

# Projet import
from form import Form
from Script import Error


class CategorieActivite(Form):
    """Classe de bases des dialogs de création et de modification des catégories d'activité"""
    def __init__(self, database):
        super(CategorieActivite, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'categorie_activite.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.database = database

        # Validator
        self.txt_nom.setValidator(self.address_validator())

        # Affiche le contenu des combobox
        self.afficher_responsable()
        self.afficher_type_activite()
        self.afficher_lieu()

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.check_fields)

    def afficher_responsable(self):
        """
        Afficher la liste des responsables dans le combobox
        """
        # Fetch data from database
        query = QSqlQuery(self.database)
        query.exec_("SELECT id_responsable, prenom, nom FROM responsable ORDER BY nom ASC")

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Ajouter les responsables a la liste
        while query.next():
            nom = str(query.value(2)) + ", " + str(query.value(1))
            self.cbx_responsable.addItem(nom, userData = query.value(0))

    def afficher_type_activite(self):
        """
        Afficher la liste des types d'activite dans le ComboBox
        """

        # Fetch data from database
        query = QSqlQuery(self.database)
        query.exec_("SELECT id_type_activite, nom FROM type_activite ORDER BY nom ASC")

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Ajouter les types d'activite a la liste
        while query.next():
            self.cbx_type_activite.addItem(str(query.value(1)), userData = query.value(0))

    def afficher_lieu(self):
        """
        Afficher la liste des lieux dans le ComboBox
        """

        # Fetch data from database
        query = QSqlQuery(self.database)
        query.exec_("SELECT id_lieu, nom FROM lieu")

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Ajouter les types d'activite a la liste
        while query.next():
            self.cbx_lieu.addItem(str(query.value(1)), userData = query.value(0))

    def check_fields(self):
        """
        Vérifie que tout les champs sont remplis
        :return: True s'ils sont bien remplis
        """
        if self.txt_nom.text() != "":
            self.process()
            return True
        else:
            self.message_box_missing_information("Le nom de la catégorie d'activité "\
                                                 "doit être remplis")
        return False

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        Implanter dans les sous classes
        """
        pass


class NouvelleCategorieActivite(CategorieActivite):
    """Dialog pour la création de nouvelle catégorie d'activité"""
    def __init__(self, database):
        super(NouvelleCategorieActivite, self).__init__(database)

        # Interface graphique
        self.setWindowTitle("Nouvelle catégorie d'activité")
        self.lbl_titre.setText("Nouvelle catégorie d'activité")

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        """
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO categorie_activite (nom, prix_membre, prix_non_membre, "
                      "participante_minimum, participante_maximum, id_responsable, id_type_activite, id_lieu) "
                      "VALUES (:nom, :prix_membre, :prix_non_membre, :participante_minimum, :participante_maximum, "
                      ":id_responsable, :id_type_activite, :id_lieu)")
        query.bindValue(':nom', self.check_string(self.txt_nom.text()))
        query.bindValue(':prix_membre', self.sbx_prix_membre.value())
        query.bindValue(':prix_non_membre', self.sbx_prix_non_membre.value())
        query.bindValue(':participante_minimum', self.sbx_participante_minimum.value())
        query.bindValue(':participante_maximum', self.sbx_participantes_maximum.value())
        query.bindValue(':id_responsable', self.cbx_responsable.itemData(self.cbx_responsable.currentIndex()))
        query.bindValue(':id_type_activite', self.cbx_type_activite.itemData(self.cbx_type_activite.currentIndex()))
        query.bindValue(':id_lieu', self.cbx_lieu.itemData(self.cbx_lieu.currentIndex()))
        query.exec_()
        # Affichage d'un message d'erreur si la requete echoue
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            self.accept() # Fermer si dialog seulement si la requete reussie


class ModifierCategorieActivite(CategorieActivite):
    """Dialog pour la modification de categorie d'activité"""
    def __init__(self, id_categorie_activite, database):
        super(ModifierCategorieActivite, self).__init__(database)

        # Instance variable definition
        self.id_categorie_activite = id_categorie_activite

        # Interface graphique
        self.setWindowTitle("Modifier une catégorie d'activité")
        self.lbl_titre.setText("Modifier une catégorie d'activité")
        self.btn_add.setText("Modifier")
        self.show_informations()

    def show_informations(self):
        """
        Afficher les informations sur le lieu
        """
        # Obtenir les informations de la base de donnees
        query = QSqlQuery(self.database)
        query.prepare("SELECT nom, prix_membre, prix_non_membre, participante_minimum, "
                      "participante_maximum, id_responsable, id_type_activite, id_lieu "
                      "FROM categorie_activite WHERE (id_categorie_activite = "
                      ":id_categorie_activite)")
        query.bindValue(':id_categorie_activite', self.id_categorie_activite)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Afficher les informations
        query.first()

        self.txt_nom.setText(query.value(0))
        self.sbx_prix_membre.setValue(query.value(1))
        self.sbx_prix_non_membre.setValue(query.value(2))
        self.sbx_participante_minimum.setValue(query.value(3))
        self.sbx_participantes_maximum.setValue(query.value(4))
        index_responsable = self.cbx_responsable.findData(query.value(5))
        self.cbx_responsable.setCurrentIndex(index_responsable)
        index_type_activite = self.cbx_type_activite.findData(query.value(6))
        self.cbx_type_activite.setCurrentIndex(index_type_activite)
        index_lieu = self.cbx_lieu.findData(query.value(7))
        self.cbx_lieu.setCurrentIndex(index_lieu)

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        """
        query = QSqlQuery(self.database)
        query.prepare("UPDATE categorie_activite "
                      "SET nom = :nom, prix_membre = :prix_membre, prix_non_membre = :prix_non_membre, "
                      "participante_minimum = :participante_minimum, participante_maximum = :participante_maximum, "
                      "id_responsable = :id_responsable, id_type_activite = :id_type_activite, id_lieu = :id_lieu "
                      "WHERE id_categorie_activite = :id_categorie_activite")
        query.bindValue(':nom', self.check_string(self.txt_nom.text()))
        query.bindValue(':prix_membre', self.sbx_prix_membre.value())
        query.bindValue(':prix_non_membre', self.sbx_prix_non_membre.value())
        query.bindValue(':participante_minimum', self.sbx_participante_minimum.value())
        query.bindValue(':participante_maximum', self.sbx_participantes_maximum.value())
        query.bindValue(':id_responsable', self.cbx_responsable.itemData(self.cbx_responsable.currentIndex()))
        query.bindValue(':id_type_activite', self.cbx_type_activite.itemData(self.cbx_type_activite.currentIndex()))
        query.bindValue(':id_lieu', self.cbx_lieu.itemData(self.cbx_lieu.currentIndex()))
        query.bindValue(':id_categorie_activite', self.id_categorie_activite)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie
