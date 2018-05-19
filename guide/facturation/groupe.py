"""Création de nouveau groupe"""

# Python import
import os

# PyQt import
from PyQt5.QtWidgets import QTableWidgetItem, QDialog
from PyQt5.QtCore import QTime, QDate

from PyQt5.QtSql import QSqlQuery

# Project import
from script.database import database_error

# Interface import
from interface.groupe import Ui_Groupe

class Groupe(QDialog, Ui_Groupe):
    """Dialog pour la création de l'inscription d'un nouveau groupe"""
    def __init__(self, database):
        super(Groupe, self).__init__()
        self.setupUi(self)

        # Instance variable definition
        self.DATABASE = database

        # Table widget parameters
        self.tbl_activite.setColumnHidden(0, True)

        # Afficher la liste des activite
        self.afficher_liste_activite()

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.txt_activite.textChanged.connect(self.afficher_liste_activite)
        self.btn_add.clicked.connect(self.process)

    def process(self):
        """
        Ajout du groupe dans la base de donnees
        """
        activite_row = self.tbl_activite.currentRow()
        if activite_row != -1:
            query = QSqlQuery(self.DATABASE)
            query.prepare("INSERT OR REPLACE INTO groupe "
                            "(id_groupe, "
                            "id_activite, "
                            "f_0_4, "
                            "f_5_11, "
                            "f_12_17, "
                            "f_18_34, "
                            "f_35_64, "
                            "f_65, "
                            "h_0_4, "
                            "h_5_11, "
                            "h_12_17, "
                            "h_18_34, "
                            "h_35_64, "
                            "h_65) "
                          "VALUES "
                            "((SELECT id_groupe "
                              "FROM groupe "
                              "WHERE id_activite = "
                              ":id_activite), "
                            ":id_activite, "
                            ":f_0_4, "
                            ":f_5_11, "
                            ":f_12_17, "
                            ":f_18_34, "
                            ":f_35_64, "
                            ":f_65, "
                            ":h_0_4, "
                            ":h_5_11, "
                            ":h_12_17, "
                            ":h_18_34, "
                            ":h_35_64, "
                            ":h_65) ")
            query.bindValue(':id_activite', self.tbl_activite.item(activite_row, 0).text())
            query.bindValue(':f_0_4', self.sbx_f_0_4.value())
            query.bindValue(':f_5_11', self.sbx_f_5_11.value())
            query.bindValue(':f_12_17', self.sbx_f_12_17.value())
            query.bindValue(':f_18_34', self.sbx_f_18_34.value())
            query.bindValue(':f_35_64', self.sbx_f_35_64.value())
            query.bindValue(':f_65', self.sbx_f_65.value())
            query.bindValue(':h_0_4', self.sbx_h_0_4.value())
            query.bindValue(':h_5_11', self.sbx_h_5_11.value())
            query.bindValue(':h_12_17', self.sbx_h_12_17.value())
            query.bindValue(':h_18_34', self.sbx_h_18_34.value())
            query.bindValue(':h_35_64', self.sbx_h_35_64.value())
            query.bindValue(':h_65', self.sbx_h_65.value())
            query.exec_()

            # Affichage d'un message d'erreur si la requete echoue
            if not database_error.sql_error_handler(query.lastError()):
                self.accept() # Fermer le dialog seulement si la requete reussie
        else:
            Error.DataError.aucun_article_selectionne()

    def afficher_liste_activite(self):
        """
        Afficher la liste des activite
        """

        # Fetch data from database
        query = QSqlQuery()
        sql = "SELECT "\
                "categorie_activite.nom, "\
                "activite.date, "\
                "activite.heure_debut, "\
                "activite.heure_fin, "\
                "activite.id_activite "\
              "FROM activite "\
              "INNER JOIN categorie_activite "\
                "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite " \
              "WHERE activite.date_limite_inscription >= {} ".format(QDate.currentDate().toString('yyyy-MM-dd'))

        # Recherche par nom d'activite
        if self.txt_activite.text() != "":
            sql = sql + "AND categorie_activite.nom LIKE '%{}%' ".format(self.txt_activite.text())

        sql = sql + "LIMIT 100"
        query.exec_(sql)

        # Affichage d'un message d'erreur si la requete echoue
        database_error.sql_error_handler(query.lastError())

        self.tbl_activite.setRowCount(0)
        while query.next():
            self.tbl_activite.insertRow(self.tbl_activite.rowCount())
            r = self.tbl_activite.rowCount() - 1

            self.tbl_activite.setItem(r, 0, QTableWidgetItem(str(query.value(4))))
            self.tbl_activite.setItem(r, 1, QTableWidgetItem(str(query.value(0))))

            date_activite = QDate.fromString(query.value(1), 'yyyy-MM-dd').toString('dd MMM yyyy')
            self.tbl_activite.setItem(r, 2, QTableWidgetItem(date_activite))

            heure_debut = QTime.fromString(query.value(2), 'HH:mm').toString('hh:mm')
            heure_fin = QTime.fromString(query.value(3), 'HH:mm').toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.tbl_activite.setItem(r, 3, QTableWidgetItem(heure))

        self.tbl_activite.resizeColumnsToContents()
