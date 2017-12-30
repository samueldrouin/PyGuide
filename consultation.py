# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QHeaderView, QTableWidgetItem
from PyQt5.QtSql import QSqlQuery
import os

# Project import
from responsable import NouveauResponsable, ModifierResponsable
from type_activite import NouveauTypeActivite, ModifierTypeActivite


class Consultation(QDialog):
    def __init__(self, type, database):
        """
        :param type:
            1 : Type d'activite
            2 : Responsables
        """
        # Instance variable definition
        self.database = database

        super(Consultation, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'consultation.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_close.clicked.connect(self.close) # Close windows on "Close" button clicked

        # Table widget
        self.tbl_resultat.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_resultat.setColumnHidden(0, True)

        # Type d'activite
        if type == 1:
            # Interface
            self.lbl_title.setText("Consultation des types d'activité")
            self.window().setWindowTitle("Consultation des types d'activité")

            # Slots
            self.btn_add.clicked.connect(self.nouveau_type_activite)
            self.tbl_resultat.clicked.connect(self.modifier_type_activite)
            self.txt_search.textEdited.connect(self.update_liste_type_activite)

            # Afficher la liste
            self.update_liste_type_activite()

        # Responsable
        elif type == 2:
            # Interface
            self.lbl_title.setText("Consultation des responsables")
            self.window().setWindowTitle("Consultation des responsables")

            # Slots
            self.btn_add.clicked.connect(self.nouveau_responsable)
            self.tbl_resultat.clicked.connect(self.modifier_responsable)
            self.txt_search.textEdited.connect(self.update_liste_responsables)

            # Afficher la liste
            self.update_liste_responsables()

    """
    Fonctions pour la consultation des responsables
    """
    def update_liste_responsables(self):
        """
        Affiche la liste des responsable selon les options de tri
        """
        # Effacer la liste des reponsables
        self.tbl_resultat.setRowCount(0)

        # Obtenir la liste des responsables de la base de donnees
        query = QSqlQuery(self.database)

        sql = "SELECT * FROM responsable "
        if self.txt_search.text() != "":
            sql = sql + "WHERE prenom LIKE '%{0}%' OR nom LIKE '%{0}%'".format(self.txt_search.text())
        query.exec_(sql)

        # Afficher la liste des reponsables dans le tableau
        while query.next():
            self.tbl_resultat.insertRow(self.tbl_resultat.rowCount())
            r = self.tbl_resultat.rowCount() - 1
            self.tbl_resultat.setItem(r, 0, QTableWidgetItem(str(query.value(0))))

            # Format du nom
            nom = query.value(1) + " " + query.value(2)
            self.tbl_resultat.setItem(r, 1, QTableWidgetItem(nom))

    def nouveau_responsable(self):
        """
        Ouvre une fenetre pour creer un nouveau responsable
        """
        responsable = NouveauResponsable(self.database)
        responsable.accepted.connect(self.update_liste_responsables)
        responsable.exec()

    def modifier_responsable(self, index):
        """
        Ouvre le dialog pour modifier un responsable
        :param index: Index de la ligne
        """
        id_responsable = self.tbl_resultat.item(index.row(), 0).text()
        modifier_participante = ModifierResponsable(self.database, id_responsable)
        modifier_participante.accepted.connect(self.update_liste_responsables)
        modifier_participante.exec()

    """
    Fonctions pour la consultation des types d'activité
    """
    def update_liste_type_activite(self):
        """
        Affiche les responsables selon les options de tri
        """
        # Effacer la liste des types d'activite
        self.tbl_resultat.setRowCount(0)

        # Obtenir la liste des types d'activite de la base de donnees
        query = QSqlQuery(self.database)

        sql = "SELECT * FROM type_activite "

        if self.txt_search.text() != "":
            sql = sql + "WHERE nom LIKE '%{}%'".format(self.txt_search.text())
        query.exec_(sql)

        # Afficher la liste des types d'activite
        while query.next():
            self.tbl_resultat.insertRow(self.tbl_resultat.rowCount())
            r = self.tbl_resultat.rowCount() - 1
            self.tbl_resultat.setItem(r, 0, QTableWidgetItem(str(query.value(0))))
            self.tbl_resultat.setItem(r, 1, QTableWidgetItem(query.value(1)))

    def nouveau_type_activite(self):
        """
        Ouvre une fenetre pour ajouter un nouveau type d'activite
        """
        nouveau_type_activite = NouveauTypeActivite(self.database)
        nouveau_type_activite.accepted.connect(self.update_liste_type_activite)
        nouveau_type_activite.exec()

    def modifier_type_activite(self, index):
        """
        Ouvre le dialog pour modifier un responsable
        :param index: Index de la ligne
        """
        id_type_activite = self.tbl_resultat.item(index.row(), 0).text()
        modifier_participante = ModifierTypeActivite(self.database, id_type_activite)
        modifier_participante.accepted.connect(self.update_liste_type_activite)
        modifier_participante.exec()
