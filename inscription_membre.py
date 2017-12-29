# Python import
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
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
        self.ajouter_article_regulier()

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_inscription.clicked.connect(self.inscription)
        self.chk_honoraire.toggled.connect(self.membre_honoraire)

    def membre_honoraire(self, checked):
        """
        Ajoute les articles d'un membre honoraire
        :param checked: CheckBox Honoraire
        """
        self.tbl_commande.removeRow(0)
        self.tbl_commande.setRowCount(1)
        if checked:
            # Confirme l'inscription d'un membre honoraire
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Inscription d'un membre honoraire")
            msgbox.setText("Inscription d'un membre honoraire")
            msgbox.setInformativeText("Êtes-vous certain de vouloir inscrire ce membre comme honoraire")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            msgbox.setDefaultButton(QMessageBox.Yes)
            ret = msgbox.exec()

            # Annulation du nouveau status
            if ret == QMessageBox.No:
                self.chk_honoraire.setChecked(False)
            # Ajout du status honoraire
            else:
                self.ajouter_article_honoraire()
        else:
            self.ajouter_article_regulier()

    def ajouter_article_honoraire(self):
        """
        Ajouter le status de membre honoraire à la liste d'articles
        """
        # Article
        article = "Membre honoraire"
        self.tbl_commande.setItem(0, 0, QTableWidgetItem(article))

        # Prix
        prix = 0.00
        item = QTableWidgetItem('%.2f' % prix)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.tbl_commande.setItem(0, 1, item)

        # Afficher le prix total
        self.txt_total.setText('%.2f' % prix)

    def ajouter_article_regulier(self):
        """
        Ajouter le status à la liste d'article
        """
        # Article
        self.tbl_commande.setItem(0, 0, QTableWidgetItem())
        month = QDate.currentDate().month()
        year = QDate().currentDate().year()
        if month > 9:
            year = year + 1
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
        """
        Recuperer le numero du nouveau membre
        """
        query = QSqlQuery()
        query.exec_("SELECT MAX(numero_membre) FROM membre")

        query.first()

        # S'il existe deja des membres dans la base de donnees
        if query.value(0) != "":
            self.txt_numero_membre.setText(str(query.value(0)+1))
        # Si le membre est le premier
        else:
            self.txt_numero_membre.setText("1")

    def inscription(self):
        """
        Enregistre le status de membre lorsque l'inscritpion est completee
        """
        # Ouvre une transation
        QSqlDatabase.transaction(self.database)
        # Active le membre
        query = QSqlQuery()
        query.prepare("INSERT INTO membre (actif, id_participante, numero_membre, membre_honoraire, date_renouvellement) "
                      "VALUES (:actif, :id_participante, :numero_membre, :honoraire, :renouvellement)")
        query.bindValue(':actif', True)
        query.bindValue(':id_participante', int(self.id_participante))
        query.bindValue(':numero_membre', self.txt_numero_membre.text())

        # Determiner si le membre est honoraire
        if self.chk_honoraire.isChecked():
            query.bindValue(':honoraire', True)

            # Aucune date de renouvellement
            query.bindValue(':renouvellement', 0)
        else:
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
        query.prepare("INSERT INTO inscription_membre (id_membre, date, article, prix, numero_recu) "
                      "VALUES ((SELECT last_insert_rowid()), (SELECT date('now')), :article, :prix, "
                      ":numero_recu)")
        query.bindValue(':article', self.tbl_commande.item(0, 0).text())
        query.bindValue(':prix', self.tbl_commande.item(0, 1).text())
        query.bindValue(':numero_recu', self.check_string(self.txt_recu.text()))
        query.exec_()
        #Termine la transation
        QSqlDatabase.commit(self.database)

        self.accept()