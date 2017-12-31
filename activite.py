# Python import
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic
import os
from datetime import date, timedelta, datetime

# Project import
from form import Form

class NouvelleActivite(Form):
    def __init__(self, database):
        super(NouvelleActivite,self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'nouvelle_activite.ui')
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
        self.rbt_hebdomadaire.toggled.connect(self.afficher_champs_date)
        self.btn_ajouter_exclusion.clicked.connect(self.ajout_date_exclusion)
        self.btn_vider.clicked.connect(self.vider_date_exclusion)
        self.btn_add.clicked.connect(self.process)

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
            nouvelle_liste_exclusion = str(date_value.strftime('%d-%m-%Y'))

        else:
            nouvelle_liste_exclusion = liste_exclusion + ", " + str(date_value.strftime('%d-%m-%Y'))

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

    def process(self):
        """
        Traitement des donnees dans la base de donnee
        """
        if self.rbt_unique.isChecked():
            query = QSqlQuery(self.database)
            query.prepare("INSERT INTO activite (id_categorie_activite, date, heure_debut, heure_fin, "
                      "date_limite_inscription) "
                      "VALUES (:id_categorie_activite, :date, :heure_debut, :heure_fin, "
                      ":date_limite_inscription)")
            query.bindValue(':id_categorie_activite', self.cbx_category_activite.currentIndex() + 1)
            query.bindValue(':date', self.ded_unique.date().toJulianDay())
            query.bindValue(':heure_debut', self.tim_debut.time().msecsSinceStartOfDay())
            query.bindValue(':heure_fin', self.tim_fin.time().msecsSinceStartOfDay())

            # Date limite inscription
            value_date = self.ded_unique.date().toJulianDay() - self.sbx_fin_inscription.value()
            query.bindValue(':date_limite_inscription', value_date)

            query.exec_()
        else:
            # Lecture des informations du formulaire
            q_date_debut = self.ded_debut.date()
            debut = date(q_date_debut.year(), q_date_debut.month(), q_date_debut.day())

            q_date_fin = self.ded_fin.date()
            fin = date(q_date_fin.year(), q_date_fin.month(), q_date_fin.day())

            # Preparation de la liste des exclusions
            exclusion_liste = self.txt_exclusion.text().split(', ')
            if exclusion_liste != ['']:
                r = 0
                for exclusion in exclusion_liste:
                    date_value = datetime.strptime(exclusion, '%Y-%m-%d').date()
                    exclusion_liste[r] = date_value
                    r = r + 1

            # Preparation de la liste des dates
            liste_date = []

            current_date = debut
            while current_date <= fin:
                # Ne pas ajouter une date exclue
                if not current_date in exclusion_liste:
                    liste_date.append(current_date)

                current_date = current_date + timedelta(weeks=1)

            # Ajouter les informations a la base de donnees
            for date_activite in liste_date:
                query = QSqlQuery(self.database)
                query.prepare("INSERT INTO activite (id_categorie_activite, date, heure_debut, heure_fin, "
                              "date_limite_inscription) "
                              "VALUES (:id_categorie_activite, :date_activite, :heure_debut, :heure_fin, "
                              ":date_limite_inscription)")
                query.bindValue(':id_categorie_activite', self.cbx_category_activite.currentIndex() + 1)
                query.bindValue(':date_activite', QDate(date_activite.year, date_activite.month, date_activite.day)
                                .toJulianDay())
                query.bindValue(':heure_debut', self.tim_debut.time().msecsSinceStartOfDay())
                query.bindValue(':heure_fin', self.tim_fin.time().msecsSinceStartOfDay())

                # Date limite inscription
                value_date = QDate(date_activite.year, date_activite.month, date_activite.day).toJulianDay() - \
                             self.sbx_fin_inscription.value()
                query.bindValue(':date_limite_inscription', value_date)
                query.exec_()

        self.accept()


class ModifierActivite(Form):
    def __init__(self, id_activite, database):
        super(ModifierActivite, self).__init__()