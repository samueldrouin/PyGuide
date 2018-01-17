"""
Module permettant le traitement des types d'activité

Le module est responsable de l'ajout et de la modification des types d'activité dans la base de donnée. 

Classes : 
- TypeActivité : Base des dialog permettant la modification ou la création de type d'activité
- NouveauTypeActivite : Specificité du dialog permettant la création de nouveau type d'activité dans la base de donnée
- ModifierTypeActivite : Spécificité du dialog permettant la modificaton de type d'activité existant dans la base de donnée
"""


# Python import
import os

# PyQt import
from PyQt5 import uic
from PyQt5.QtSql import QSqlQuery

# Project import
from form import Form
from Script import Error


class TypeActivite(Form):
    """
    Base des dialog permettant la modification ou la création de type d'activité. 

    Cette classe est responsable de l'affichage de l'interface et de la connection des slots à l'interface

    Les sous classes doivent override la méthode process qui traite les données dans la base de donnée lorsque le dialog est accepté. 

    Méthodes:
    - check_fields: Vérifie que tout les champs nécessaires sont remplis
    - process : Traitement de donnée dans la base de donnée. Doit être implantée dans les sous classes. 
    """
    def __init__(self, database):
        super(TypeActivite, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'type_activite.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.DATABASE = database

        # Validator
        self.txt_nom.setValidator(self.name_validator())

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_add.clicked.connect(self.check_fields)

    def check_fields(self):
        """
        Vérifie que tout les champs sont remplis
        :return: True s'ils sont bien remplis
        """
        if self.txt_nom.text() != "":
            self.process()
        else:
            self.message_box_missing_information("Le nom du type d'activité doit être remplis")

    def process(self):
        """
        Traitement dans donnes dans la base de données
        Implante dans les sous classes
        """
        pass


class NouveauTypeActivite(TypeActivite):
    """Dialog pour la création de nouveau type d'activité"""
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
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie


class ModifierTypeActivite(TypeActivite):
    """Dialog pour la modification de type d'activité"""
    def __init__(self, database, id_type_activite):
        super(ModifierTypeActivite, self).__init__(database)

        # Instance variable definition
        self.id_type_activite = id_type_activite

        # Interface graphique
        self.lbl_titre.setText("Modifier un type d'activité")
        self.btn_add.setText("Modifier")
        self.show_informations()

    def show_informations(self):
        """Afficher les informations sur le type d'activite"""
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
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Afficher les informations
        query.first()
        self.txt_nom.setText(query.value(0))

    def process(self):
        """Modifier le type d'activite dans la base de donnees"""
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
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            self.accept() # Fermer le dialog seulement si la requete reussie
