"""Inscription et renouvellement des membres"""

# Python import
import os

# PyQt import
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtCore import QDate, Qt
from PyQt5 import uic
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

# Project import
from form import Form
from Script import Error


class InscriptionMembre(Form):
    """Dialog pour l'inscription ou le renouvellement d'un nouveau membre"""
    def __init__(self, database):
        super(InscriptionMembre, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'inscription_membre.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.id_participante = None
        self.database = database

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

    def ajouter_article_renouvellement(self):
        """
        Ajouter le renouvellement du status à la liste d'article
        """
        # Article
        self.tbl_commande.setItem(0, 0, QTableWidgetItem())
        month = QDate.currentDate().month()
        year = QDate().currentDate().year()
        year = year
        if month > 9:
            year = year + 2
        else:
            year = year + 1
        article = "Renouvellement membre " + str(year)
        self.tbl_commande.setItem(0, 0, QTableWidgetItem(article))

        # Prix
        prix = 5.00
        item = QTableWidgetItem('%.2f' % prix)
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.tbl_commande.setItem(0, 1, item)

        # Afficher le prix total
        self.txt_total.setText('%.2f' % prix)

    def inscription(self):
        """
        Enregistre le status de membre lorsque l'inscritpion est completee
        Definie dans les sous classes
        """
        pass


class NouvelleInscription(InscriptionMembre):
    """Dialog pour l'inscription de nouveau membre"""
    def __init__(self, nom, phone, id_participante, database):
        super(NouvelleInscription, self).__init__(database)

        # Instance variable definition
        self.id_participante = id_participante

        # Affichage de l'interface
        self.txt_nom.setText(nom)
        self.txt_telephone.setText(phone)
        self.get_numero_membre()
        self.ajouter_article_regulier()

    def get_numero_membre(self):
        """
        Recuperer le numero du nouveau membre
        """
        query = QSqlQuery()
        query.exec_("SELECT MAX(numero_membre) FROM membre")

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

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
        QSqlDatabase(self.database).transaction()

        # Active le membre
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO membre "
                        "(actif, "
                        "id_participante, "
                        "numero_membre, "
                        "membre_honoraire, "
                        "date_renouvellement) "
                      "VALUES "
                        "(:actif, "
                        ":id_participante, "
                        ":numero_membre, "
                        ":honoraire, "
                        ":renouvellement)")
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
            year = year
            if month > 9:
                year = year + 1
            date = QDate(year, 9, 1).toJulianDay()
            query.bindValue(':renouvellement', date)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            QSqlDatabase(self.database).rollback() # Annuler la transaction
            return # Empecher la fermeture du dialog

        # Ouvre une facture
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO facture "
                        "("
                          "numero_recu, "
                          "id_participante, "
                          "total "
                        ")"
                      "VALUES "
                        "("
                          ":numero_recu, "
                          ":id_participante, "
                          ":total "
                        ")")
        query.bindValue(':numero_recu', self.check_string(self.txt_recu.text()))
        query.bindValue(':id_participante', self.id_participante)
        query.bindValue(':total', self.tbl_commande.item(0, 1).text())

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            QSqlDatabase(self.database).rollback() # Annuler la transaction
            return# Empecher la fermeture du dialog

        # Ajout des articles à la facture
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO article "
                        "("
                          "id_facture, "
                          "prix, "
                          "description, "
                        ")"
                      "VALUES "
                        "("
                          "(SELECT last_insert_rowid()), "
                          ":prix, "
                          ":description, "
                        ")")
        query.bindValue(':prix', self.tbl_commande.item(0, 1).text())
        query.bindValue(':description', self.tbl_commande.item(0, 0).text())

        #Termine la transation
        QSqlDatabase(self.database).commit()

        self.accept()


class RenouvelerInscription(InscriptionMembre):
    """Dialog pour le renouvellement de l'inscription d'un membre"""
    def __init__(self, nom, phone, id_participante, database):
        super(RenouvelerInscription, self).__init__(database)

        # Instance variable definition
        self.id_participante = id_participante

        # Modifier les labels
        self.lbl_titre.setText("Renouveler une inscription")
        self.btn_inscription.setText("Renouveler")

        # Affichage de l'interface
        self.txt_nom.setText(nom)
        self.txt_telephone.setText(phone)
        self.ajouter_article_renouvellement()

        # Determiner le numero de membre
        self.get_numero_membre()

    def get_numero_membre(self):
        """
        Determiner le numero de membre
        """
        query = QSqlQuery(self.database)
        query.prepare("SELECT "
                        "numero_membre "
                      "FROM "
                        "membre "
                      "WHERE id_participante = :id_participante")
        query.bindValue(':id_participante', self.id_participante)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        query.first()
        self.txt_numero_membre.setText(str(query.value(0)))

    def inscription(self):
        """
        Enregistre le status de membre lorsque l'inscription est completee
        """
        # Ouvre une transation
        QSqlDatabase(self.database).transaction()
        # Active le membre
        query = QSqlQuery(self.database)
        query.prepare("UPDATE membre "
                      "SET membre_honoraire = :honoraire, date_renouvellement = :renouvellement "
                      "WHERE id_participante = :id_participante")

        # Determiner si le membre est honoraire
        if self.chk_honoraire.isChecked():
            query.bindValue(':honoraire', True)

            # Aucune date de renouvellement
            query.bindValue(':renouvellement', 0)
        # Si le membre n'est pas honoraire
        else:
            query.bindValue(':honoraire', False)

            # Determiner la date de renouvellement
            month = QDate.currentDate().month()
            year = QDate().currentDate().year()
            if month > 9:
                year = year + 2
            else:
                year = year + 1
            date = QDate(year, 9, 1).toJulianDay()
            query.bindValue(':renouvellement', date)

        query.bindValue(':id_participante', int(self.id_participante))

        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            QSqlDatabase(self.database).rollback() # Annuler la transaction
            return # Empecher la fermeture du dialog

        # Enregistre la commande
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO inscription_membre "
                        "(id_membre, "
                        "date, "
                        "article, "
                        "prix, "
                        "numero_recu) "
                      "VALUES "
                        "((SELECT id_membre "
                          "FROM membre "
                          "WHERE id_participante = :id_participante), "
                        "(SELECT date('now')), "
                        ":article, "
                        ":prix, "
                        ":numero_recu)")
        query.bindValue(':id_participante', self.id_participante)
        query.bindValue(':article', self.tbl_commande.item(0, 0).text())
        query.bindValue(':prix', self.tbl_commande.item(0, 1).text())
        query.bindValue(':numero_recu', self.check_string(self.txt_recu.text()))
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            QSqlDatabase(self.database).rollback() # Annuler la transaction
            return # Empecher la fermeture du dialog
        #Termine la transation
        QSqlDatabase(self.database).commit()

        self.accept()
