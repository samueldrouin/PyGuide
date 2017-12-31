# Python import
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic
import os
from datetime import date

# Project import
from form import Form

class Activite(Form):
    def __init__(self, database):
        super(Activite,self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'activite.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.database = database

        # Afficher les dates et heure par defaut
        current_date = QDate.currentDate()
        self.ded_unique.setDate(current_date)
        self.ded_debut.setDate(current_date)
        self.ded_fin.setDate(current_date)
        self.ded_exclusion.setDate(current_date)

        current_time = QTime.currentTime()
        self.tim_debut.setTime(current_time)
        self.tim_fin.setTime(current_time)

        # Affichage des champs pour les dates
        self.afficher_champs_date()

        # Afficher les categories d'activite
        self.afficher_categorie_activite()

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.rbt_unique.toggled.connect(self.afficher_champs_date)
        self.rbt_recurrente.toggled.connect(self.afficher_champs_date)
        self.btn_ajouter_exclusion.clicked.connect(self.ajout_date_exclusion)
        self.btn_vider.clicked.connect(self.vider_date_exclusion)

    def vider_date_exclusion(self):
        """
        Vide la liste des date d'exclusion
        """
        self.txt_exclusion.clear()

    def ajout_date_exclusion(self):
        """
        Ajouter une date à la liste d'exclusion
        """
        # Formattage de la date
        q_date = self.ded_exclusion.date()
        date_value = date(q_date.year(), q_date.month(), q_date.day())

        # Affichage de la liste
        liste_exclusion = self.txt_exclusion.text()
        if liste_exclusion == "":
            nouvelle_liste_exclusion = str(date_value)
        else:
            nouvelle_liste_exclusion = liste_exclusion + ", " + str(date_value)
        self.txt_exclusion.setText(nouvelle_liste_exclusion)

    def afficher_categorie_activite(self):
        """
        Afficher la liste des categories d'activite dans le combobox
        """
        # Fetch data from database
        query = QSqlQuery(self.database)
        query.exec_("SELECT nom FROM categorie_activite")

        # Ajouter les responsables a la liste
        while query.next():
            self.cbx_category_activite.addItem(str(query.value(0)))

    def afficher_champs_date(self):
        """
        Afficher les champs pour entrer les dates
        """

        # Date unique
        if self.rbt_unique.isChecked():
            self.widget_recurrente.setHidden(True)
            self.widget_unique.setHidden(False)

        # Plusieurs dates
        else:
            self.widget_unique.setHidden(True)
            self.widget_recurrente.setHidden(False)


class NouvelleActivite(Activite):
    def __init__(self, database):
        super(NouvelleActivite, self).__init__(database)


class ModifierActivite(Activite):
    def __init__(self, database):
        super(ModifierActivite, self).__init__(database)