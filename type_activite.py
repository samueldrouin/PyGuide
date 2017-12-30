# Python import
from PyQt5 import uic
from PyQt5.QtSql import QSqlQuery
import os

# Project import
from form import Form


class TypeActivite(Form):
    def __init__(self):
        super(TypeActivite, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'type_activite.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.database = None

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
    def __init__(self, database):
        super(NouveauTypeActivite, self).__init__()

        # Instance variable definition
        self.database = database

        # Interface graphique
        self.lbl_titre.setText("Nouveau type d'activité")

    def process(self):
        """
        Ajouter le nouveau type d'activite a la base de donnees
        """
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO type_activite (nom) VALUES (:nom)")
        query.bindValue(':nom', self.txt_nom.text())
        query.exec_()
        self.accept()


class ModifierTypeActivite(TypeActivite):
    def __init__(self, database, id_type_activite):
        super(ModifierTypeActivite, self).__init__()

        # Instance variable definition
        self.database = database
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
        query = QSqlQuery(self.database)
        query.prepare("SELECT nom FROM type_activite WHERE id_type_activite = :id_type_activite")
        query.bindValue(':id_type_activite', self.id_type_activite)
        query.exec_()

        # Afficher les informations
        query.first()
        self.txt_nom.setText(query.value(0))

    def process(self):
        """
        Modifier le type d'activite dans la base de donnees
        """
        query = QSqlQuery(self.database)
        query.prepare("UPDATE type_activite SET nom=:nom WHERE id_type_activite=:id_type_activite")
        query.bindValue(':nom', self.txt_nom.text())
        query.bindValue(':id_type_activite', self.id_type_activite)
        query.exec_()
        self.accept()