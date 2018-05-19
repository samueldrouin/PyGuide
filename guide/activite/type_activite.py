"""
Module permettant le traitement des types d'activité

Le module est responsable de l'ajout et de la modification des types d'activité dans la base de donnée. 

Classes
    TypeActivité : Base des dialog permettant la modification ou la création de type d'activité
    NouveauTypeActivite : Specificité du dialog permettant la création de nouveau type d'activité dans la base de donnée
    ModifierTypeActivite : Spécificité du dialog permettant la modificaton de type d'activité existant dans la base de donnée
"""


# Python import
import os

# PyQt import
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QDialog

# Project import
from script.database import database_error
from script.interface import validator
from script.data import data_error

# Interface import
from interface.type_activite import Ui_TypeActivite


class TypeActivite(QDialog, Ui_TypeActivite):
    """
    Base des dialog permettant la modification ou la création de type d'activité. 
    
    Cette classe est responsable de l'affichage de l'interface et de la connection des slots à l'interface. 
    Les sous classes doivent override la méthode process qui traite les données dans la base de donnée lorsque le dialog est accepté. 

    Méthodes
        check_fields: Vérifie que tout les champs nécessaires sont remplis
        process : Traitement de donnée dans la base de donnée. Doit être implantée dans les sous classes. 
    """
    def __init__(self, database):
        super(TypeActivite, self).__init__()
        # Affichage de l'interface graphique
        self.setupUi(self)

        # Instance variable definition
        self.DATABASE = database

        # Validator
        self.txt_nom.setValidator(Validator.name_validator())

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.check_fields)

    def check_fields(self):
        """
        Vérifie que tout les champs nécessaires sont remplis

        Return
            True s'ils sont bien remplis
        """
        if self.txt_nom.text():
            self.process()
        else:
            DataError.message_box_missing_information("Le nom du type d'activité doit être remplis")

    def process(self):
        """
        Traitement dans donnes dans la base de données

        La fonction doit être implante dans les sous classes
        """
        pass


class NouveauTypeActivite(TypeActivite):
    """
    Specificité du dialog permettant la création de nouveau type d'activité dans la base de donnée
    
    Méthodes
        process : Traitement de l'ajout du type d'activité dans la base de données
    """
    def __init__(self, database):
        super(NouveauTypeActivite, self).__init__(database)

        # Interface graphique
        self.lbl_titre.setText("Nouveau type d'activité")

    def process(self):
        """
        Ajouter le nouveau type d'activite a la base de donnees
        """
        query = QSqlQuery(self.DATABASE)
        query.prepare("INSERT INTO type_activite "
                        "(nom) "
                      "VALUES "
                        "(:nom)")
        query.bindValue(':nom', self.txt_nom.text())
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not database_error.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie


class ModifierTypeActivite(TypeActivite):
    """
    Spécificité du dialog permettant la modificaton de type d'activité existant dans la base de donnée
    
    Méthodes
        show_informations : Affiche les informations sur le type d'activité
        process : Modifier le type d'activite dans la base de donnees
    """
    def __init__(self, database, id_type_activite):
        super(ModifierTypeActivite, self).__init__(database)

        # Instance variable definition
        self.id_type_activite = id_type_activite

        # Interface graphique
        self.lbl_titre.setText("Modifier un type d'activité")
        self.btn_add.setText("Modifier")
        self.show_informations()

    def show_informations(self):
        """
        Afficher les informations sur le type d'activite
        """
        # Obtenir les informations de la base de donnees
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                        "nom "
                      "FROM "
                        "type_activite "
                      "WHERE "
                        "id_type_activite = :id_type_activite")
        query.bindValue(':id_type_activite', self.id_type_activite)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        database_error.sql_error_handler(query.lastError())

        # Afficher les informations
        query.first()
        self.txt_nom.setText(query.value(0))

    def process(self):
        """
        Modifier le type d'activite dans la base de donnees
        """
        query = QSqlQuery(self.DATABASE)
        query.prepare("UPDATE type_activite "
                      "SET "
                        "nom=:nom "
                      "WHERE "
                        "id_type_activite=:id_type_activite")
        query.bindValue(':nom', self.txt_nom.text())
        query.bindValue(':id_type_activite', self.id_type_activite)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not database_error.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie
