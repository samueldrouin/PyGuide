# Python import
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
import os

# Project import
from form import Form


class InscriptionMembre(Form):
    def __init__(self, nom, phone, id_participante, database):
        super(InscriptionMembre, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'inscription_membre.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.id_participante = id_participante
        self.database = database

        # Affichage de l'interface
        self.txt_nom.setText(nom)
        self.txt_telephone.setText(phone)
        self.get_numero_membre()

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_inscription.clicked.connect(self.inscription)

        # Ajouter le status à la liste d'article

        # Article
        self.tbl_commande.setItem(0, 0, QTableWidgetItem())
        month = QDate.currentDate().month()
        year = QDate().currentDate().year()
        if month > 9:
            year = year+1
        article = "Membre " + str(year)
        self.tbl_commande.setItem(0, 0, QTableWidgetItem(article))

        # Prix
        prix = 5.00
        item = QTableWidgetItem('%.2f' % prix)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.tbl_commande.setItem(0, 1, item)

        # Afficher le prix total
        self.txt_total.setText('%.2f' % prix)

    def get_numero_membre(self):
        query = QSqlQuery()
        query.exec_("SELECT MAX(numero_membre) FROM membre")
        query.first()
        self.txt_numero_membre.setText(str(query.value(0)+1))

    def inscription(self):
        """
        Enregistre le status de membre lorsque l'inscritpion est completee
        """
        # Ouvre une transation
        QSqlDatabase.transaction(self.database)
        # Active le membre
        query = QSqlQuery()
        query.prepare("INSERT INTO membre (actif, id_participante, numero_membre, membre_honoraire, date_renouvellement) "
                      "VALUES (:actif, :id_participante, (SELECT MAX(numero_membre) FROM membre)+1, "
                      ":honoraire, :renouvellement)")
        query.bindValue(':actif', True)
        query.bindValue(':id_participante', int(self.id_participante))
        query.bindValue(':honoraire', False)

        # Determiner la date de renouvellement
        month = QDate.currentDate().month()
        year = QDate().currentDate().year()
        if month > 9:
            year = year + 1
        date = QDate(year, 9, 1).toJulianDay()
        query.bindValue(':renouvellement', date)
        query.exec_()

        # Enregistre la commande
        query = QSqlQuery()
        query.prepare("INSERT INTO inscription_membre (id_membre, date, article, prix) "
                      "VALUES ((SELECT numero_membre FROM membre WHERE id_membre = last_insert_rowid()), "
                      "(SELECT date('now')), :article, :prix)")
        print(self.tbl_commande.item(0, 0).text())
        query.bindValue(':article', self.tbl_commande.item(0, 0).text())
        query.bindValue(':prix', self.tbl_commande.item(0, 1).text())
        query.exec_()
        #Termine la transation
        QSqlDatabase.commit(self.database)

        self.accept()