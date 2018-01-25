"""Création de nouvelle facture"""

# Python import
import os

# PyQt import
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QMessageBox
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import QTime, QDate
from PyQt5.QtGui import QColor, QBrush
from PyQt5 import uic

# Project import
from form import Form
from script.database import Error
import script.interface.selection
import definitions


class Facture(Form):
    """Fonctions nécessaires pour tous les types de facture"""

    def __init__(self, database):
        super(Facture, self).__init__()

        # Instance variable definition
        self.DATABASE = database
        self.ID_PARTICIPANTE = None

    def set_parsed_phone_number(self, old, new):
        """
        Show parsed phone number
        :param old: Old cursor position
        :param new: New cursor position
        """
        phone_number = self.phone_number_parsing(old, new, self.sender().text())
        self.sender().setText(phone_number)

    def information_participante(self, numero_telephone):
        """
        Obtenir les informations sur une participante
        :return: Informations sur la participante
        """
        # Vérifier si le numéro de téléphone est valide
        if len(numero_telephone) == 12:

            # Preparation du numero de telephone
            phone_number = int(self.check_phone_number(numero_telephone))

            query = QSqlQuery()
            query.prepare("SELECT "
                            "participante.id_participante, "
                            "participante.prenom, "
                            "participante.nom, "
                            "participante.ville, "
                            "membre.actif "
                          "FROM participante "
                          "LEFT JOIN membre ON participante.id_participante = membre.id_participante "
                          "WHERE "
                            "(participante.telephone_1 = :phone) "
                            "OR "
                            "(participante.telephone_2 = :phone)")
            query.bindValue(':phone', phone_number)
            query.exec_()

            # Affichage d'un message d'erreur si la requete echoue
            Error.DatabaseError.sql_error_handler(query.lastError())

            resultat = []

            # Obtenir les informations de la requete
            while query.next():
                informations = {}
                informations["index"] = int(query.value(0))
                self.ID_PARTICIPANTE = int(query.value(0))

                nom = str(query.value(1)) + " " + str(query.value(2))
                informations["nom"] = nom

                informations["ville"] = str(query.value(3))
                informations["actif"] = query.value(4)
                resultat.append(informations)

            # La requête ne contient aucune information
            if not resultat:
                Error.DataError.numero_telephone_inexistant()
            # La requête contient plusieurs comptes
            elif len(resultat) != 1:
                selection = Selection.SelectionParticipante(resultat)
                if selection.exec() == QDialog.Accepted:
                    index = int(selection.get_value())
                    self.activer_facturation()
                    return [element for element in resultat if element["index"] == index][0]
            else:
                self.activer_facturation()
                return resultat[0]
        # Le numéro de téléphone est invalide
        else:
            Error.DataError.numero_telephone_invalide()
        return False

    def activer_facturation(self):
        """
        Active les éléments du dialog qui permettent d'ajouter des articles à une facture
        À implanter dans les sous classes
        """
        pass

    def afficher_liste_activite(self, search, actif, table, annule=False):
        """
        Afficher la liste des activite
        :param search: Texte pour la recherche
        :param table: Tableau dans lequel les données sont affichées
        """
        # Fetch data from database
        query = QSqlQuery()
        sql = "SELECT " \
                "categorie_activite.nom, " \
                "categorie_activite.prix_membre, " \
                "categorie_activite.prix_non_membre, " \
                "activite.date, " \
                "activite.heure_debut, " \
                "activite.heure_fin, " \
                "activite.id_activite, "\
                "("\
                  "SELECT COUNT(inscription.id_inscription) "\
                  "FROM inscription "\
                  "WHERE (inscription.id_activite = activite.id_activite) AND (inscription.status = 1) "\
                ") nombre_participante, "\
                "categorie_activite.participante_maximum "\
              "FROM activite " \
              "INNER JOIN categorie_activite "\
                "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite " \
              "WHERE activite.date_limite_inscription >= {} ".format(int(QDate.currentDate().toString('yyyy-MM-dd')))
        
        # Afficher les activités qui ne sont pas annulées
        if not annule:
            sql = sql + "AND activite.status = 1 "
        else:
            sql = sql + "AND activite.status = 0 "

        # Recherche par nom d'activite
        if search != "":
            sql = sql + "WHERE categorie_activite.nom LIKE '%{}%' ".format(search)

        sql = sql + "ORDER BY categorie_activite.nom ASC, activite.date ASC LIMIT 100"
        query.exec_(sql)

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        table.setRowCount(0)
        while query.next():
            table.insertRow(table.rowCount())
            r = table.rowCount() - 1

            table.setItem(r, 0, QTableWidgetItem(str(query.value(6))))
            table.setItem(r, 2, QTableWidgetItem(str(query.value(0))))

            if actif:
                prix = "{0:.2f}$".format(query.value(1))
            else:
                prix = "{0:.2f}$".format(query.value(2))
            table.setItem(r, 3, QTableWidgetItem(prix))

            date_activite = QDate.fromString(query.value(3), 'yyyy-MM-dd').toString('dd MMM yyyy')
            table.setItem(r, 4, QTableWidgetItem(date_activite))

            heure_debut = QTime.fromString(query.value(4), 'HH:mm').toString('hh:mm')
            heure_fin = QTime.fromString(query.value(5), 'HH:mm').toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            table.setItem(r, 5, QTableWidgetItem(heure))

            # Vérifier si le nombre de participante maximum est atteint
            participante = int(query.value(7))
            maximum = int(query.value(8))
            if participante >= maximum:
                for c in range(0, 6):
                    table.item(r, c).setForeground(QBrush(QColor(175, 0, 0)))
                    table.setItem(r, 1, QTableWidgetItem("1"))
            else:
                table.setItem(r, 1, QTableWidgetItem("0"))

    def inscription(self, actif):
        """Obtenir les inscriptions associetes au compte"""
        # Fetch inscriptions from database
        query = QSqlQuery()
        query.prepare("SELECT "
                        "inscription.id_inscription, "
                        "categorie_activite.nom, "
                        "categorie_activite.prix_membre, "
                        "categorie_activite.prix_non_membre, "
                        "activite.date, "
                        "activite.heure_debut, "
                        "activite.heure_fin, "
                        "activite.id_activite, "
                        "("
                          "SELECT COUNT(inscription.id_inscription) "
                          "FROM inscription "
                          "WHERE (inscription.id_activite = activite.id_activite) AND (inscription.status = 1) "
                        ") nombre_participante, "
                        "categorie_activite.participante_maximum "
                      "FROM inscription "
                      "LEFT JOIN activite "
                        "ON inscription.id_activite = activite.id_activite "
                      "LEFT JOIN categorie_activite "
                        "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite "
                      "WHERE "
                        "(inscription.id_participante = :id_participante) "
                        "AND (activite.date >= :current_date) "
                        "AND (inscription.status = :status) "
                        "AND (activite.status = 1)"
                      "ORDER BY categorie_activite.nom ASC, activite.date ASC")
        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
        query.bindValue(':current_date', QDate.currentDate().toString('yyyy-MM-dd'))
        query.bindValue(':status', self.STATUS_INSCRIPTION)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Préparer les données de la requete
        resultat = []
        while query.next():
            inscription = {}
            inscription["id"] = str(query.value(0))
            inscription["nom"] = str(query.value(1))

            if actif:
                prix = "{0:.2f}$".format(query.value(2))
            else:
                prix = "{0:.2f}$".format(query.value(3))
            inscription["prix"] = prix

            inscription["date"] = QDate.fromString(query.value(4), 'yyyy-MM-dd').toString('dd MMM yyyy')

            heure_debut = QTime.fromString(query.value(5), 'HH:mm').toString('hh:mm')
            heure_fin = QTime.fromString(query.value(6), 'HH:mm').toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            inscription["heure"] = heure
            inscription["id_activite"] = str(query.value(7))

            # Vérifier si le nombre de participante maximum est atteint
            participante = int(query.value(8))
            maximum = int(query.value(9))
            if participante >= maximum:
                inscription["complet"] = str(int(True))
            else:
                inscription["complet"] = str(int(False))
            resultat.append(inscription)
        return resultat

    def liberation_liste_attente(self, id_activite):
        """
        Affiche la disponibilité d'une place de la liste d'attente
        :param id_activite: ID de l'activité pour laquelle une place est libérée
        """
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Liste d'attente")
        msgbox.setText("Libération d'une place")

        # Vérifier l'inscription pour laquelle la place est libérée
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT participante.prenom, participante.nom "
                      "FROM inscription "
                      "LEFT JOIN participante ON participante.id_participante = inscription.id_participante "
                      "WHERE (inscription.status = 1) AND (inscription.id_activite = :id_activite) "
                      "ORDER BY inscription.time")
        query.bindValue(':id_activite', id_activite)
        query.exec_()

        # Affiche un message en cas d'erreur dans la requete
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            return # Empeche de continuer la fonction avec des donnees incompletes

        # Affichage de l'information sur la place libérée
        lst = []
        while query.next():
            lst.append(query.value(0) + " " + query.value(1))

        # Vérifier le nombre total de participantes
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT COUNT(inscription.id_inscription) "
                      "FROM inscription "
                      "WHERE (inscription.id_activite = :id_activite) AND (inscription.status = 1) ")
        query.bindValue(':id_activite', id_activite)
        query.exec_()

        # Affiche un message en cas d'erreur dans la requete
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            return # Empeche de continuer la fonction avec des donnees incompletes

        # Obtenir le nombre de participante
        query.first()
        nombre_participante = query.value(0)

        # Obtenir les informations sur l'activite
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT categorie_activite.nom, categorie_activite.participante_maximum, activite.date "
                      "FROM activite "
                      "LEFT JOIN categorie_activite ON categorie_activite.id_categorie_activite = activite.id_categorie_activite "
                      "WHERE activite.id_activite = :id_activite")
        query.bindValue(':id_activite', id_activite)
        query.exec_()

        # Affiche un message en cas d'erreur dans la requete
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            return # Empeche de continuer la fonction avec des donnees incompletes

        # Preparation des donnees
        query.first()
        nom_activite = str(query.value(0))
        maximum = int(query.value(1))
        date = QDate().fromString(query.value(2), 'yyyy-MM-dd')

        # Continuer seulement s'il y a des participante sur la liste d'attente
        if nombre_participante <= maximum:
            return

        text = "Une place pour {} sera libérée dans l'activitée {} du {} lorsque vous enregistrerez ces inscriptions.".format(lst[maximum], nom_activite, date.toString('dd MMM yyyy'))
        msgbox.setInformativeText(text)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

class Facturation(Facture):
    """Dialog pour la création de nouvelle facture"""
    def __init__(self, database):
        super(Facturation, self).__init__(database)
        ui = os.path.join(definitions.INTERFACE_DIR, 'facturation.ui')
        uic.loadUi(ui, self)

        # Validator
        self.txt_numero.setValidator(self.phone_validator())

        # Table widget parameters
        self.tbl_activite.setColumnHidden(0, True)
        self.tbl_activite.setColumnHidden(1, True)
        self.tbl_inscription.setColumnHidden(0, True)
        self.tbl_article.setColumnHidden(0, True)

        # Afficher la liste des activite
        self.afficher_liste_activite()

        # Afficher le numero de la facture
        self.get_numero_facture()

        # Slots
        self.btn_annuler.clicked.connect(self.close)
        self.txt_numero.cursorPositionChanged.connect(self.set_parsed_phone_number)
        self.txt_numero.returnPressed.connect(self.afficher_information_participante)
        self.txt_activite.textChanged.connect(self.afficher_liste_activite)
        self.btn_ajouter_activite.clicked.connect(self.ajout_activite)
        self.btn_ajouter_inscription.clicked.connect(self.ajout_inscription)
        self.btn_rembourser.clicked.connect(self.ajout_activite)
        self.btn_remove.clicked.connect(self.retirer_activite)
        self.btn_enregistrer.clicked.connect(self.process)
        self.chk_annule.toggled.connect(self.afficher_annule)

    def afficher_annule(self, checked):
        """Afficher les activités annulées seulement"""
        if checked:
            self.btn_ajouter_activite.setEnabled(False)
        else:
            self.btn_ajouter_activite.setEnabled(True)
        self.afficher_liste_activite()

    def afficher_inscriptions(self):
        """Afficher les inscriptions liees au compte"""
        # Effacer les elements existants
        self.tbl_inscription.setRowCount(0)

        resultat = self.inscription(self.chk_actif.isChecked())

        for inscription in resultat:
            # Vérifier si l'inscription est complete
            if int(inscription["complet"]):
                # Obtenir la liste des noms sur la liste d'attente
                query = QSqlQuery(self.DATABASE)
                query.prepare("SELECT participante.id_participante "
                            "FROM inscription "
                            "LEFT JOIN participante ON participante.id_participante = inscription.id_participante "
                            "WHERE (inscription.status = 1) AND (inscription.id_activite = :id_activite) "
                            "ORDER BY inscription.time")
                query.bindValue(':id_activite', inscription["id_activite"])
                query.exec_()

                # Affiche un message en cas d'erreur dans la requete
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    return # Empeche de continuer la fonction avec des donnees incompletes

                # Liste d'attente
                liste_attente = []
                while query.next():
                    liste_attente.append(query.value(0))

                # Obtenir le nombre maximal de participante
                query = QSqlQuery(self.DATABASE)
                query.prepare("SELECT categorie_activite.participante_maximum "
                              "FROM activite "
                              "LEFT JOIN categorie_activite ON categorie_activite.id_categorie_activite = activite.id_categorie_activite "
                              "WHERE activite.id_activite = :id_activite")
                query.bindValue(':id_activite', inscription["id_activite"])
                query.exec_()

                # Affiche un message en cas d'erreur dans la requete
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    return # Empeche de continuer la fonction avec des donnees incompletes

                # Preparation des donnees
                query.first()
                maximum = int(query.value(0))

                index = liste_attente.index(self.ID_PARTICIPANTE)

                # Si la personne est encore sur la liste d'attente
                if index > maximum-1:
                    continue

            # Afficher les informations dans le tableau
            self.tbl_inscription.insertRow(self.tbl_inscription.rowCount())
            r = self.tbl_inscription.rowCount() - 1

            self.tbl_inscription.setItem(r, 0, QTableWidgetItem(inscription["id_activite"]))
            self.tbl_inscription.setItem(r, 1, QTableWidgetItem(inscription["nom"]))
            self.tbl_inscription.setItem(r, 2, QTableWidgetItem(inscription["prix"]))
            self.tbl_inscription.setItem(r, 3, QTableWidgetItem(inscription["date"]))
            self.tbl_inscription.setItem(r, 4, QTableWidgetItem(inscription["heure"]))

    def afficher_total(self, montant):
        """
        Changer le montant du total
        :param montant: Montant de l'article
        """
        total = self.txt_total.text()
        montant = float(montant[:-1])
        if total != "":
            total = float(total[:-1])
            total = total + montant
            self.txt_total.setText("{0:.2f}$".format(total))
        else:
            self.txt_total.setText("{0:.2f}$".format(montant))

    def activer_facturation(self):
        """Permettre l'ajout d'activite lorsqu'un compte est ouvert"""
        self.btn_ajouter_activite.setEnabled(True)
        self.btn_rembourser.setEnabled(True)
        self.btn_ajouter_inscription.setEnabled(True)
        self.btn_remove.setEnabled(True)
        self.afficher_inscriptions()
        self.txt_activite.setText("")
        self.chk_annule.setEnabled(True)
        self.chk_annule.setChecked(False)

    def afficher_information_participante(self):
        """Afficher les informations sur la participante"""
        informations = self.information_participante(self.txt_numero.text())

        # S'il existe dans informations
        if informations:
            # Afficher les informations du membre
            self.txt_nom.setText(informations["nom"])
            self.txt_ville.setText(informations["ville"])

            if informations["actif"]:
                self.chk_actif.setChecked(True)

    def afficher_liste_activite(self):
        """Afficher la liste des activite"""
        search = self.txt_activite.text()
        actif = self.chk_actif.isChecked()
        table = self.tbl_activite
        super().afficher_liste_activite(search, actif, table, annule=self.chk_annule.isChecked())

    def ajout_activite(self):
        """Ajouter une activite à la facture"""
        row = self.tbl_activite.currentRow()

        # Vérifier si l'activité à deja ete facturée
        query = QSqlQuery()
        query.prepare("SELECT COUNT(id_inscription) "
                      "FROM inscription "
                      "WHERE "
                        "(status = :status) AND "
                        "(id_activite = :id_activite) AND "
                        "(id_participante = :id_participante)")
        query.bindValue(':status', self.STATUS_FACTURE)
        query.bindValue(':id_activite' , self.tbl_activite.item(row, 0).text())
        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
        query.exec_()

        # Affiche un message en cas d'erreur dans la requete
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            return # Empeche de continuer la fonction avec des donnees incompletes

        query.first()
        count = int(query.value(0))

        # Valeur de la quantité
        if self.sender() == self.btn_ajouter_activite:
            quantite = "1"

            # Si l'activite a deja ete facturee
            if count:
                msgbox = QMessageBox()
                msgbox.setWindowTitle("Facturation impossible")
                msgbox.setText("Facturation impossible")
                msgbox.setInformativeText("Impossible de facturer une activité qui à déjà été facturée")
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.setDefaultButton(QMessageBox.Ok)
                msgbox.exec()
                return

            # Avertissement si l'activité est complète
            if int(self.tbl_activite.item(row, 1).text()):
                resultat = Error.DataError.activite_complete()
                if resultat == QMessageBox.No:
                    return # Ne pas ajouter l'article

            # Retirer l'activité de la liste d'inscription si elle y est
            id_activite = self.tbl_activite.item(row, 0).text()
            for r in range(self.tbl_inscription.rowCount()):
                if self.tbl_inscription.item(r, 0).text() == id_activite:
                    self.tbl_inscription.setRowHidden(r, True)
        else:
            quantite = "(1)"

            # Si l'activite n'a jamais ete facturee
            if not count:
                msgbox = QMessageBox()
                msgbox.setWindowTitle("Remboursement impossible")
                msgbox.setText("Remboursement impossible")
                msgbox.setInformativeText("Impossible de rembourser une activité qui n'a jamais été facturée")
                msgbox.setIcon(QMessageBox.Information)
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.setDefaultButton(QMessageBox.Ok)
                msgbox.exec()
                return

        if row != -1:
            # Préparation du tableau
            self.tbl_article.insertRow(self.tbl_article.rowCount())
            r = self.tbl_article.rowCount() - 1

            # Ajout de l'article
            self.tbl_article.setItem(r, 0, self.tbl_activite.item(row, 0).clone())
            self.tbl_article.setItem(r, 1, self.tbl_activite.item(row, 2).clone())
            self.tbl_article.setItem(r, 2, self.tbl_activite.item(row, 3).clone())
            self.tbl_article.setItem(r, 3, self.tbl_activite.item(row, 4).clone())
            self.tbl_article.setItem(r, 4, self.tbl_activite.item(row, 5).clone())
            self.tbl_article.setItem(r, 5, QTableWidgetItem(quantite))

            self.afficher_total(self.tbl_activite.item(row, 3).text())

            # Remettre le texte en noir
            for c in range(0, 6):
                self.tbl_article.item(r, c).setForeground(QBrush(QColor(0, 0, 0)))

            # Traitement de la liste d'attente
            if quantite == "(1)":
                self.afficher_total("-" + self.tbl_activite.item(row, 3).text())

                # Vérifier s'il y a une liste d'attente sur l'activité
                if int(self.tbl_activite.item(row, 1).text()):
                    self.liberation_liste_attente(int(self.tbl_activite.item(row, 0).text()))

        else:
            Error.DataError.aucun_article_selectionne()

    def ajout_inscription(self):
        """Ajouter une inscription a la facture"""
        row = self.tbl_inscription.currentRow()

        # Vérifier si l'inscription est sur la liste d'attente
        query = QSqlQuery(self.DATABASE)
        query.prepare("")

        if row != -1:
            # Préparation du tableau
            self.tbl_article.insertRow(self.tbl_article.rowCount())
            r = self.tbl_article.rowCount() - 1

            # Ajout de l'article
            self.tbl_article.setItem(r, 0, self.tbl_inscription.item(row, 0).clone())
            self.tbl_article.setItem(r, 1, self.tbl_inscription.item(row, 1).clone())
            self.tbl_article.setItem(r, 2, self.tbl_inscription.item(row, 2).clone())
            self.tbl_article.setItem(r, 3, self.tbl_inscription.item(row, 3).clone())
            self.tbl_article.setItem(r, 4, self.tbl_inscription.item(row, 4).clone())
            self.tbl_article.setItem(r, 5, QTableWidgetItem("1"))

            self.afficher_total(self.tbl_inscription.item(row, 2).text())
        else:
            Error.DataError.aucun_article_selectionne()

    def retirer_activite(self):
        """Retirer une activite du panier"""
        row = self.tbl_article.currentRow()
        if row != -1:
            # Afficher l'activité de la liste d'inscription si elle y est
            id_activite = self.tbl_article.item(row, 0).text()
            for r in range(self.tbl_inscription.rowCount()):
                if self.tbl_inscription.item(r, 0).text() == id_activite:
                    self.tbl_inscription.setRowHidden(r, False)

            # Effacer l'article de la facture 
            self.tbl_article.removeRow(row)
        else:
            Error.DataError.aucun_article_selectionne()

    def process(self):
        """Traitement des donnees pour la base de données"""
        # Commencer une transaction
        self.DATABASE.transaction()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(self.DATABASE.lastError()):
            return # Empêche la fermeture du dialog

        # Ajouter une facture
        query = QSqlQuery()
        query.prepare("INSERT INTO facture "
                        "(numero_recu, id_participante, total) "
                      "VALUES "
                        "(:numero_recu, :id_participante, :total)")
        query.bindValue(':numero_recu', self.check_string(self.txt_recu.text()))
        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
        query.bindValue(':total', float(self.txt_total.text()[:-1]))
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            self.DATABASE.rollback() # Annuler la transaction
            return # Empêche la fermeture du dialog

        # Obtenir le numero de de la facture
        query = QSqlQuery(self.DATABASE)
        query.exec("SELECT last_insert_rowid()")

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            self.DATABASE.rollback() # Annuler la transaction
            return # Empêche la fermeture du dialog

        query.first()
        id_facture = int(query.value(0))

        # Ajouter les articles à la facture
        for row in range(self.tbl_article.rowCount()):
            # Prix de l'article
            if self.tbl_article.item(row, 5) == "1":
                prix = float(self.tbl_article.item(row, 2))
            else:
                prix = float("-" + str(self.tbl_article.item(row, 2).text()[:-1]))
            query = QSqlQuery(self.DATABASE)
            query.prepare("INSERT INTO article "
                          "(id_facture, prix, description) "
                          "VALUES " 
                          "(:id_facture, :prix, :description)")
            query.bindValue(':id_facture', id_facture)
            query.bindValue(':prix', prix)
            description = str(self.tbl_article.item(row, 1).text()) + "(" + str(self.tbl_article.item(row, 3).text()) + ")"
            query.bindValue(':description', description)
            query.exec_()

            # Affichage d'un message d'erreur si la requete echoue
            if Error.DatabaseError.sql_error_handler(query.lastError()):
                self.DATABASE.rollback() # Annuler la transaction
                return # Empêche la fermeture du dialog

        # Gestion des inscriptions
        for row in range(self.tbl_article.rowCount()):
            if self.tbl_article.item(row, 5).text() == "1":
                # Ajouter les inscriptions

                # Essayer d'ajouter une nouvelle inscription
                query = QSqlQuery()
                query.prepare("INSERT INTO inscription "
                                "(id_inscription, id_participante, id_activite, status) "
                            "VALUES "
                                "((SELECT id_inscription "
                                "FROM inscription "
                                "WHERE (id_participante = :id_participante) "
                                "AND (id_activite = :id_activite)), "
                                ":id_participante, :id_activite, :status)")
                query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                query.bindValue(':id_activite', self.tbl_article.item(row, 0).text())
                query.bindValue(':status', self.STATUS_FACTURE)
                query.exec_()

                # Vérifier s'il y a violation de la contraint de la primary key
                if query.lastError().nativeErrorCode() == str(Error.DatabaseError.SQLITE_CONSTRAINT): 
                    # Vérifier si une transaction a deja ete annulee
                    query = QSqlQuery(self.DATABASE)
                    query.prepare("SELECT status "
                                  "FROM inscription "
                                  "WHERE (id_participante = :id_participante) AND (id_activite = :id_activite)")
                    query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                    query.bindValue(':id_activite', self.tbl_article.item(row, 0).text())
                    query.exec_()

                    # Affichage d'un message d'erreur si la requete echoue
                    if Error.DatabaseError.sql_error_handler(query.lastError()):
                        self.DATABASE.rollback() # Annuler la transaction
                        return # Empêche la fermeture du dialog

                    # Obtenir le status
                    query.first()
                    status = int(query.value(0))

                    if status == 1:
                        # Ajouter les inscriptions
                        query = QSqlQuery(self.DATABASE)
                        query.prepare("UPDATE inscription "
                                      "SET "
                                        "status = :status "
                                      "WHERE "
                                        "id_inscription = (SELECT id_inscription "
                                        "FROM inscription "
                                        "WHERE (id_participante = :id_participante) "
                                        "AND (id_activite = :id_activite))")
                        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                        query.bindValue(':id_activite', self.tbl_article.item(row, 0).text())
                        query.bindValue(':status', self.STATUS_FACTURE)
                        query.exec_()

                        # Affichage d'un message d'erreur si la requete echoue
                        if Error.DatabaseError.sql_error_handler(query.lastError()):
                            self.DATABASE.rollback() # Annuler la transaction
                            return # Empêche la fermeture du dialog
                    else:
                        query = QSqlQuery()
                        query.prepare("INSERT OR IGNORE INTO inscription "
                                        "(id_inscription, id_participante, id_activite, status) "
                                    "VALUES "
                                        "((SELECT id_inscription "
                                        "FROM inscription "
                                        "WHERE (id_participante = :id_participante) "
                                        "AND (id_activite = :id_activite)), "
                                        ":id_participante, :id_activite, :status)")
                        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                        query.bindValue(':id_activite', self.tbl_article.item(row, 0).text())
                        query.bindValue(':status', self.STATUS_FACTURE)
                        query.exec_()

                        # Affichage d'un message d'erreur si la requete echoue
                        if Error.DatabaseError.sql_error_handler(query.lastError()):
                            self.DATABASE.rollback() # Annuler la transaction
                            return # Empêche la fermeture du dialog
                # Affichage d'un message d'erreur
                else:
                    if Error.DatabaseError.sql_error_handler(query.lastError()):
                        self.DATABASE.rollback() # Annuler la transaction
                        return # Empêche la fermeture du dialog

            # Effacer une inscription
            else:
                # La date d'insertion est remise à zéro lorsque l'inscription est effacee
                query = QSqlQuery()
                query.prepare("INSERT OR REPLACE INTO inscription "
                                "(id_inscription, id_participante, id_activite, status) "
                              "VALUES "
                                "((SELECT id_inscription "
                                  "FROM inscription "
                                  "WHERE (id_participante = :id_participante) "
                                  "AND (id_activite = :id_activite)), "
                                ":id_participante, :id_activite, :status)")
                query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                query.bindValue(':id_activite', self.tbl_article.item(row, 0).text())
                query.bindValue(':status', self.STATUS_REMBOURSE)
                query.exec_()

                #Affichage d'un message d'erreur si la requete echoue
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    self.DATABASE.rollback() # Annuler la transaction
                    return # Empêche la fermeture du dialog

        # Terminer la transaction
        self.DATABASE.commit()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(self.DATABASE.lastError()):
            self.DATABASE.rollback() # Annuler la transaction
            return # Empêche la fermeture du dialog

        self.accept()

    def get_numero_facture(self):
        """Recuperer le numero de la facture"""
        query = QSqlQuery()
        query.exec_("SELECT MAX(id_facture) FROM facture")

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())
        query.first()

        # S'il existe deja des facture dans la base de donnees
        if query.value(0) != "":
            self.txt_facture.setText(str(query.value(0)+1))
        # S'il s'agit de la première facture
        else:
            self.txt_facture.setText("1")

class Inscription(Facture):
    """Dialog pour la création de nouvelle inscriptions"""

    # Constante definition
    STATUS_INSCRIPTION_ANNULEE = 0
    STATUS_INSCRIPTION = 1
    STATUS_FACTURE = 2
    STATUS_REMBOURSE = 3

    def __init__(self, database):
        super(Inscription, self).__init__(database)
        ui = os.path.join(definitions.INTERFACE_DIR, 'inscription.ui')
        uic.loadUi(ui, self)

        # Validator
        self.txt_numero.setValidator(self.phone_validator())

        # Table widget parameters
        self.tbl_activite.setColumnHidden(0, True)
        self.tbl_activite.setColumnHidden(1, True)
        self.tbl_panier.setColumnHidden(0, True)
        self.tbl_panier.setColumnHidden(1, True)
        self.tbl_panier.setColumnHidden(2, True)

        # Afficher la liste des activite
        self.afficher_liste_activite()

        # Slots
        self.btn_annuler.clicked.connect(self.reject)
        self.txt_numero.cursorPositionChanged.connect(self.set_parsed_phone_number)
        self.txt_numero.returnPressed.connect(self.afficher_information_participante)
        self.txt_activite.textChanged.connect(self.afficher_liste_activite)
        self.btn_ajouter.clicked.connect(self.ajout_activite)
        self.btn_enregistrer.clicked.connect(self.process)
        self.btn_remove.clicked.connect(self.retirer_activite)

    def activer_facturation(self):
        """Permettre l'ajout d'activite lorsqu'un compte est ouvert"""
        self.btn_ajouter.setEnabled(True)
        self.btn_remove.setEnabled(True)
        self.afficher_inscriptions()
        self.txt_activite.setText("")

    def afficher_information_participante(self):
        """Afficher les informations sur la participante"""
        informations = self.information_participante(self.txt_numero.text())

        # S'il existe dans informations
        if informations:
            # Afficher les informations du membre
            self.txt_nom.setText(informations["nom"])
            self.txt_ville.setText(informations["ville"])

            if informations["actif"]:
                self.chk_actif.setChecked(True)

    def afficher_liste_activite(self):
        """Afficher la liste des activite"""
        search = self.txt_activite.text()
        actif = self.chk_actif.isChecked()
        table = self.tbl_activite
        super().afficher_liste_activite(search, actif, table)

    def ajout_activite(self):
        """
        Ajouter une activite au panier
        """
        activite_row = self.tbl_activite.currentRow()
        # Vérifier si un article est sélectionné
        if activite_row != -1:
            # Avertissement si l'activité est complète
            if int(self.tbl_activite.item(activite_row, 1).text()):
                resultat = Error.DataError.activite_complete()
                if resultat == QMessageBox.No:
                    return # Ne pas ajouter l'article
            
            # Préparation du tableau
            self.tbl_panier.insertRow(self.tbl_panier.rowCount())
            r = self.tbl_panier.rowCount() - 1

            # Ajout de l'article
            self.tbl_panier.setItem(r, 0, self.tbl_activite.item(activite_row, 0).clone())
            self.tbl_panier.setItem(r, 1, QTableWidgetItem("1"))
            self.tbl_panier.setItem(r, 2, self.tbl_activite.item(activite_row, 1).clone())
            self.tbl_panier.setItem(r, 3, self.tbl_activite.item(activite_row, 2).clone())
            self.tbl_panier.setItem(r, 4, self.tbl_activite.item(activite_row, 3).clone())
            self.tbl_panier.setItem(r, 5, self.tbl_activite.item(activite_row, 4).clone())
            self.tbl_panier.setItem(r, 6, self.tbl_activite.item(activite_row, 5).clone())

            self.tbl_panier.resizeColumnsToContents()
        # Avertissement qu'il est nécessaire de choisir un article
        else:
            Error.DataError.aucun_article_selectionne()

    def retirer_activite(self):
        """Retirer une activite du panier"""
        row = self.tbl_panier.currentRow()
        if row != -1:
            # Annulation d'une inscription
            if self.tbl_panier.item(row, 1).text() == "0":
                # Avertissement si une place de la liste d'attente est libérée
                if int(self.tbl_panier.item(row, 2).text()):
                    # Avertissement de perte de priorité
                    msgbox = QMessageBox()
                    msgbox.setWindowTitle("Activité contingentée")
                    msgbox.setText("Activité contingentée")
                    msgbox.setInformativeText("En continuant l'annulation, vous allez retirer à la participante sa priorité sur la liste. Voulez-vous continuer ? ")
                    msgbox.setIcon(QMessageBox.Information)
                    msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
                    msgbox.setDefaultButton(QMessageBox.Yes)
                    if msgbox.exec() == QMessageBox.No:
                        return
                    self.liberation_liste_attente(int(self.tbl_panier.item(row, 0).text()))

                self.tbl_panier.setItem(row, 1, QTableWidgetItem("-1"))
                self.tbl_panier.setRowHidden(row, True)

            # Effacer une inscription qui n'a pas encore été ajoutée
            elif self.tbl_panier.item(row, 1).text() == "1":
                self.tbl_panier.removeRow(row)
        else:
            Error.DataError.aucun_article_selectionne()

    def process(self):
        """Traitement des donnees pour la base de données"""
        # Commencer une transaction
        self.DATABASE.transaction()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(self.DATABASE.lastError()):
            return # Empêche la fermeture du dialog

        for row in range(self.tbl_panier.rowCount()):
            # Ajouter une inscription
            if int(self.tbl_panier.item(row, 1).text()) == 1:
                # Essayer d'ajouter une nouvelle inscription
                query = QSqlQuery()
                query.prepare("INSERT INTO inscription "
                                "(id_inscription, id_participante, id_activite, status) "
                              "VALUES "
                                "((SELECT id_inscription "
                                "FROM inscription "
                                "WHERE (id_participante = :id_participante) "
                                "AND (id_activite = :id_activite)), "
                                ":id_participante, :id_activite, :status)")
                query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                query.bindValue(':id_activite', self.tbl_panier.item(row, 0).text())
                query.bindValue(':status', self.STATUS_INSCRIPTION)
                query.exec_()

                # Vérifier s'il y a violation de la contraint de la primary key
                if query.lastError().nativeErrorCode() == str(Error.DatabaseError.SQLITE_CONSTRAINT):
                    # Vérifier si une transaction a deja ete annulee
                    query = QSqlQuery(self.DATABASE)
                    query.prepare("SELECT status "
                                  "FROM inscription "
                                  "WHERE (id_participante = :id_participante) AND (id_activite = :id_activite)")
                    query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                    query.bindValue(':id_activite', self.tbl_panier.item(row, 0).text())
                    query.exec_()

                    # Affichage d'un message d'erreur si la requete echoue
                    if Error.DatabaseError.sql_error_handler(query.lastError()):
                        self.DATABASE.rollback() # Annuler la transaction
                        return # Empêche la fermeture du dialog

                    # Obtenir le status
                    query.first()
                    status = int(query.value(0))

                    if status == 1:
                        # Ajouter les inscriptions
                        query = QSqlQuery(self.DATABASE)
                        query.prepare("UPDATE inscription "
                                      "SET "
                                        "status = :status, "
                                        "id_facture = :id_facture "
                                      "WHERE "
                                        "id_inscription = (SELECT id_inscription "
                                        "FROM inscription "
                                        "WHERE (id_participante = :id_participante) "
                                        "AND (id_activite = :id_activite))")
                        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                        query.bindValue(':id_activite', self.tbl_panier.item(row, 0).text())
                        query.bindValue(':status', self.STATUS_INSCRIPTION)
                        query.exec_()

                        # Affichage d'un message d'erreur si la requete echoue
                        if Error.DatabaseError.sql_error_handler(query.lastError()):
                            self.DATABASE.rollback() # Annuler la transaction
                            return # Empêche la fermeture du dialog
                    else:
                        query = QSqlQuery()
                        query.prepare("INSERT OR REPLACE INTO inscription "
                                        "(id_inscription, id_participante, id_activite, status) "
                                     "VALUES "
                                        "((SELECT id_inscription "
                                        "FROM inscription "
                                        "WHERE (id_participante = :id_participante) "
                                        "AND (id_activite = :id_activite)), "
                                        ":id_participante, :id_activite, :status)")
                        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                        query.bindValue(':id_activite', self.tbl_panier.item(row, 0).text())
                        query.bindValue(':status', self.STATUS_INSCRIPTION)
                        query.exec_()

                        # Affichage d'un message d'erreur si la requete echoue
                        if Error.DatabaseError.sql_error_handler(query.lastError()):
                            self.DATABASE.rollback() # Annuler la transaction
                            return # Empêche la fermeture du dialog

                # Affichage d'un message d'erreur
                else:
                    if Error.DatabaseError.sql_error_handler(query.lastError()):
                        self.DATABASE.rollback() # Annuler la transaction
                        return # Empêche la fermeture du dialog

            # Effacer une inscription
            elif int(self.tbl_panier.item(row, 1).text()) == -1:
                # La date d'insertion est remise à zéro lorsque l'inscription est effacee
                query = QSqlQuery()
                query.prepare("INSERT OR REPLACE INTO inscription "
                                "(id_inscription, id_participante, id_activite, status) "
                              "VALUES "
                                "((SELECT id_inscription "
                                  "FROM inscription "
                                  "WHERE (id_participante = :id_participante) "
                                  "AND (id_activite = :id_activite)), "
                                ":id_participante, :id_activite, :status)")
                query.bindValue(':id_participante', self.ID_PARTICIPANTE)
                query.bindValue(':id_activite', self.tbl_panier.item(row, 0).text())
                query.bindValue(':status', self.STATUS_INSCRIPTION_ANNULEE)
                query.exec_()

                #Affichage d'un message d'erreur si la requete echoue
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    self.DATABASE.rollback() # Annuler la transaction
                    return # Empêche la fermeture du dialog

        # Terminer la transaction
        self.DATABASE.commit()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(self.DATABASE.lastError()):
            self.DATABASE.rollback() # Annuler la transaction
            return # Empêche la fermeture du dialog

        self.accept()

    def afficher_inscriptions(self):
        """Afficher les inscriptions liees au compte"""
        # Effacer les elements existants
        self.tbl_panier.setRowCount(0)

        resultat = self.inscription(self.chk_actif.isChecked())

        for inscription in resultat:
            self.tbl_panier.insertRow(self.tbl_panier.rowCount())
            r = self.tbl_panier.rowCount() - 1

            self.tbl_panier.setItem(r, 0, QTableWidgetItem(inscription["id_activite"]))
            self.tbl_panier.setItem(r, 1, QTableWidgetItem("0"))
            self.tbl_panier.setItem(r, 2, QTableWidgetItem(inscription["complet"]))
            self.tbl_panier.setItem(r, 3, QTableWidgetItem(inscription["nom"]))
            self.tbl_panier.setItem(r, 4, QTableWidgetItem(inscription["prix"]))
            self.tbl_panier.setItem(r, 5, QTableWidgetItem(inscription["date"]))
            self.tbl_panier.setItem(r, 6, QTableWidgetItem(inscription["heure"]))
