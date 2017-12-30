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
        self.btn_add.clicked.connect(self.check_fields)

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

    def check_fields(self):
        """
        Vérifie que tout les champs sont remplis
        :return: True s'ils sont bien remplis
        """
        if self.txt_nom.text() != "":
            self.process()
            return True
        else:
            self.message_box_missing_information("Le nom de la catégorie d'activité doit être remplis")
        return False

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        Implanter dans les sous classes
        """
        pass


class NouvelleCategorieActivite(CategorieActivite):
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
        query.prepare("INSERT INTO categorie_activite (nom, prix_membre, prix_non_membre, participante_minimum, "
                      "participante_maximum, id_responsable, id_type_activite, id_lieu) "
                      "VALUES (:nom, :prix_membre, :prix_non_membre, :participante_minimum, :participante_maximum, "
                      ":id_responsable, :id_type_activite, :id_lieu)")
        query.bindValue(':nom', self.check_string(self.txt_nom.text()))
        query.bindValue(':prix_membre', self.sbx_prix_membre.value())
        query.bindValue(':prix_non_membre', self.sbx_prix_non_membre.value())
        query.bindValue(':participante_minimum', self.sbx_participante_minimum.value())
        query.bindValue(':participante_maximum', self.sbx_participantes_maximum.value())
        query.bindValue(':id_responsable', self.cbx_responsable.currentIndex()+1)
        query.bindValue(':id_type_activite', self.cbx_type_activite.currentIndex()+1)
        query.bindValue(':id_lieu', self.cbx_lieu.currentIndex()+1)
        query.exec_()

        self.accept()


class ModifierCategorieActivite(CategorieActivite):
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
        query.prepare("SELECT nom, prix_membre, prix_non_membre, participante_minimum, participante_maximum, "
                      "id_responsable, id_type_activite, id_lieu "
                      "FROM categorie_activite WHERE id_type_activite = :id_type_activite")
        query.bindValue(':id_type_activite', self.id_categorie_activite)
        query.exec_()

        # Afficher les informations
        query.first()

        self.txt_nom.setText(query.value(0))
        self.sbx_prix_membre.setValue(query.value(1))
        self.sbx_prix_non_membre.setValue(query.value(2))
        self.sbx_participante_minimum.setValue(query.value(3))
        self.sbx_participantes_maximum.setValue(query.value(4))
        self.cbx_responsable.setCurrentIndex(query.value(5)-1)
        self.cbx_type_activite.setCurrentIndex(query.value(6)-1)
        self.cbx_lieu.setCurrentIndex(query.value(7)-1)

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
        query.bindValue(':id_responsable', self.cbx_responsable.currentIndex() + 1)
        query.bindValue(':id_type_activite', self.cbx_type_activite.currentIndex() + 1)
        query.bindValue(':id_lieu', self.cbx_lieu.currentIndex() + 1)
        query.bindValue(':id_categorie_activite', self.id_categorie_activite)
        query.exec_()

        self.accept()
