"""Création de nouvelle facture"""

# Python import
import os

# PyQt import
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import QTime, QDate
from PyQt5 import uic

# Project import
from form import Form
from Script import Error


class Facture(Form):
    """Fonctions nécessaires pour tous les types de facture"""
    def __init__(self, database):
        return super(Facture, self).__init__()
   
        # Instance variable definition
        self.database = database
        self.id_participante = None

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
                self.id_participante = int(query.value(0))
                
                nom = str(query.value(1)) + " " + str(query.value(2))
                informations["nom"] = nom

                informations["ville"] = str(query.value(3))
                informations["actif"] = query.value(4)
                resultat.append(informations)

            # La requête ne contient aucune information
            if len(resultat) == 0:
                Error.DataError.numero_telephone_inexistant()
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

    def afficher_liste_activite(self, search, actif, table):
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
                "activite.id_activite "\
              "FROM activite " \
              "INNER JOIN categorie_activite "\
                "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite " \
              "WHERE activite.date_limite_inscription >= {} ".format(int(QDate.currentDate().toJulianDay()))

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
            table.setItem(r, 1, QTableWidgetItem(str(query.value(0)))) 
 
            if actif: 
                prix = "{0:.2f}$".format(query.value(1)) 
            else: 
                prix = "{0:.2f}$".format(query.value(2)) 
            table.setItem(r, 2, QTableWidgetItem(prix)) 
 
            date_activite = QDate.fromJulianDay(query.value(3)).toString('dd MMM yyyy') 
            table.setItem(r, 3, QTableWidgetItem(date_activite)) 
 
            heure_debut = QTime.fromMSecsSinceStartOfDay(query.value(4)).toString('hh:mm') 
            heure_fin = QTime.fromMSecsSinceStartOfDay(query.value(5)).toString('hh:mm') 
            heure = heure_debut + " à " + heure_fin 
            table.setItem(r, 4, QTableWidgetItem(heure)) 

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
                        "activite.id_activite "
                      "FROM inscription "
                      "LEFT JOIN activite "
                        "ON inscription.id_activite = activite.id_activite "
                      "LEFT JOIN categorie_activite "
                        "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite "
                      "WHERE "
                        "(inscription.id_participante = :id_participante) "
                        "AND (activite.date >= :current_date) "
                        "AND (inscription.status = :status) "
                      "ORDER BY categorie_activite.nom ASC, activite.date ASC")
        query.bindValue(':id_participante', self.id_participante)
        query.bindValue(':current_date', QDate.currentDate().toJulianDay())
        query.bindValue(':status', True)
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

            inscription["date"] = QDate.fromJulianDay(query.value(4)).toString('dd MMM yyyy')

            heure_debut = QTime.fromMSecsSinceStartOfDay(query.value(5)).toString('hh:mm')
            heure_fin = QTime.fromMSecsSinceStartOfDay(query.value(6)).toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            inscription["heure"] = heure
            inscription["id_activite"] = str(query.value(7))
            resultat.append(inscription)
        return resultat

class Facturation(Facture):
    """Dialog pour la création de nouvelle facture"""
    def __init__(self, database):
        super(Facturation, self).__init__(database)
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'facturation.ui')
        uic.loadUi(ui, self)

        # Validator
        self.txt_numero.setValidator(self.phone_validator())

        # Table widget parameters
        self.tbl_activite.setColumnHidden(0, True)
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

    def afficher_inscriptions(self):
        """Afficher les inscriptions liees au compte"""
        # Effacer les elements existants
        self.tbl_inscription.setRowCount(0)

        """Afficher les inscriptions"""
        resultat = self.inscription(self.chk_actif.isChecked())

        for inscription in resultat:
            self.tbl_inscription.insertRow(self.tbl_inscription.rowCount())
            r = self.tbl_inscription.rowCount() - 1

            self.tbl_inscription.setItem(r, 0, QTableWidgetItem(inscription["id"]))
            self.tbl_inscription.setItem(r, 1, QTableWidgetItem(inscription["nom"]))
            self.tbl_inscription.setItem(r, 2, QTableWidgetItem(inscription["prix"]))
            self.tbl_inscription.setItem(r, 3, QTableWidgetItem(inscription["date"]))
            self.tbl_inscription.setItem(r, 4, QTableWidgetItem(inscription["heure"]))

    def ajouter_article(self, table, quantite):
        """
        Ajouter un article à la commande
        :param table: Table à partir de laquelle l'article est ajoute
        :param quantite: Quantite de l'article a ajouter
        """
        row = table.currentRow()

        if row != -1:
            # Préparation du tableau
            self.tbl_article.insertRow(self.tbl_article.rowCount())
            r = self.tbl_article.rowCount() - 1

            # Ajout de l'article
            self.tbl_article.setItem(r, 0, table.item(row, 0).clone())
            self.tbl_article.setItem(r, 1, table.item(row, 1).clone())
            self.tbl_article.setItem(r, 2, table.item(row, 2).clone())
            self.tbl_article.setItem(r, 3, table.item(row, 3).clone())
            self.tbl_article.setItem(r, 4, table.item(row, 4).clone())
            self.tbl_article.setItem(r, 5, QTableWidgetItem(quantite))

            # Calcul du total
            if quantite == "(1)":
                self.afficher_total("-" + table.item(row, 2).text())
            else:
                self.afficher_total(table.item(row, 2).text())
        else:
            Error.DataError.aucun_article_selectionne()

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
        """Ajouter une activite à la facture"""
        # Prépration des paramètres
        table = self.tbl_activite
        if self.sender() == self.btn_ajouter_activite:
            quantite = "1"
        else:
            quantite = "(1)"

        # Ajout de l'article
        self.ajouter_article(table, quantite)

    def ajout_inscription(self):
        """Ajouter une inscription a la facture"""
        # Prépration des paramètres
        table = self.tbl_inscription
        quantite = "1"

        # Ajout de l'article
        self.ajouter_article(table, quantite)

    def retirer_activite(self):
        """Retirer une activite du panier"""
        row = self.tbl_article.currentRow()
        if row != -1:
            self.tbl_article.removeRow(row)
        else:
            Error.DataError.aucun_article_selectionne()

    def process(self):
        """Traitement des donnees pour la base de données"""
        for row in range(self.tbl_article.rowCount()):
            # Commencer une transaction
            QSqlDatabase(self.database).transaction()

            # Ajouter une facture
            query = QSqlQuery()
            query.prepare("INSERT INTO facture "
                            "(numero_recu, id_participante) "
                          "VALUES "
                            "(:numero_recu, :id_participante)")
            query.bindValue(':numero_recu', self.check_string(self.txt_recu.text()))
            query.bindValue(':id_participante', self.id_participante)
            query.exec_()

            # Affichage d'un message d'erreur si la requete echoue
            if Error.DatabaseError.sql_error_handler(query.lastError()):
                QSqlDatabase(self.database).rollback() # Annuler la transaction
                return # Empêche la fermeture du dialog

            # Ajouter les inscriptions
            query = QSqlQuery()
            query.prepare("INSERT OR REPLACE INTO inscription "
                            "(id_inscription, id_participante, id_activite, status, id_facture) "
                          "VALUES "
                            "((SELECT id_inscription "
                              "FROM inscription "
                              "WHERE (id_participante = :id_participante) "
                              "AND (id_activite = :id_activite)), "
                            ":id_participante, :id_activite, :status, "
                            "(SELECT last_insert_rowid()))")
            query.bindValue(':id_participante', self.id_participante)
            query.bindValue(':id_activite', self.tbl_article.item(row, 0).text())
            query.bindValue(':status', True)
            query.exec_()

            # Affichage d'un message d'erreur si la requete echoue
            if Error.DatabaseError.sql_error_handler(query.lastError()):
                QSqlDatabase(self.database).rollback() # Annuler la transaction
                return # Empêche la fermeture du dialog

            # Termer la transaction
            QSqlDatabase(self.database).commit()
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
    def __init__(self, database):
        super(Inscription, self).__init__(database)
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'inscription.ui')
        uic.loadUi(ui, self)

        # Validator
        self.txt_numero.setValidator(self.phone_validator())

        # Table widget parameters
        self.tbl_activite.setColumnHidden(0, True)
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
        if activite_row != -1:
            self.tbl_panier.insertRow(self.tbl_panier.rowCount())
            r = self.tbl_panier.rowCount() - 1

            self.tbl_panier.setItem(r, 0, self.tbl_activite.item(activite_row, 0).clone())
            self.tbl_panier.setItem(r, 2, QTableWidgetItem("1"))
            self.tbl_panier.setItem(r, 3, self.tbl_activite.item(activite_row, 1).clone())
            self.tbl_panier.setItem(r, 4, self.tbl_activite.item(activite_row, 2).clone())
            self.tbl_panier.setItem(r, 5, self.tbl_activite.item(activite_row, 3).clone())
            self.tbl_panier.setItem(r, 6, self.tbl_activite.item(activite_row, 4).clone())

            self.tbl_panier.resizeColumnsToContents()
        else:
            Error.DataError.aucun_article_selectionne()

    def retirer_activite(self):
        """
        Retirer une activite du panier
        """
        row = self.tbl_panier.currentRow()
        if row != -1:
            if self.tbl_panier.item(row, 1) != "0":
                self.tbl_panier.setItem(row, 1, QTableWidgetItem("-1"))
                self.tbl_panier.setRowHidden(row, True)
            else:
                self.tbl_panier.removeRow(row)
        else:
            Error.DataError.aucun_article_selectionne()

    def process(self):
        """
        Traitement des donnees pour la base de données
        """
        for row in range(self.tbl_panier.rowCount()):
            # Ajouter une inscription
            if int(self.tbl_panier.item(row, 1).text()) == 1:
                query = QSqlQuery()
                query.prepare("INSERT OR REPLACE INTO inscription "
                                "(id_inscription, id_participante, id_activite, status) "
                              "VALUES "
                                "((SELECT id_inscription "
                                  "FROM inscription "
                                  "WHERE (id_participante = :id_participante) "
                                "AND (id_activite = :id_activite)), "
                                ":id_participante, :id_activite, :status)")
                query.bindValue(':id_participante', self.id_participante)
                query.bindValue(':id_activite', self.tbl_panier.item(row, 0).text())
                query.bindValue(':status', True)
                query.exec_()

                # Affichage d'un message d'erreur si la requete echoue
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    return # Empêche la fermeture du dialog

            # Effacer une inscription
            elif int(self.tbl_panier.item(row, 1).text()) == -1:
                query = QSqlQuery()
                query.prepare("UPDATE inscription "
                              "SET status = :status "
                              "WHERE id_inscription = :id_inscription ")
                query.bindValue(':status', False)
                query.bindValue(':id_inscription', self.tbl_panier.item(row, 2).text())
                query.exec_()

                # Affichage d'un message d'erreur si la requete echoue
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    return # Empêche la fermeture du dialog

        self.accept()
    
    def afficher_inscriptions(self):
        """Afficher les inscriptions liees au compte"""
        # Effacer les elements existants
        self.tbl_panier.setRowCount(0)

        """Afficher les inscriptions"""
        resultat = self.inscription(self.chk_actif.isChecked())

        for inscription in resultat:
            self.tbl_panier.insertRow(self.tbl_panier.rowCount())
            r = self.tbl_panier.rowCount() - 1

            self.tbl_panier.setItem(r, 0, QTableWidgetItem(inscription["id_activite"])) 
            self.tbl_panier.setItem(r, 1, QTableWidgetItem(inscription["id"]))
            self.tbl_panier.setItem(r, 2, QTableWidgetItem(True)) 
            self.tbl_panier.setItem(r, 3, QTableWidgetItem(inscription["nom"]))
            self.tbl_panier.setItem(r, 4, QTableWidgetItem(inscription["prix"]))
            self.tbl_panier.setItem(r, 5, QTableWidgetItem(inscription["date"]))
            self.tbl_panier.setItem(r, 6, QTableWidgetItem(inscription["heure"]))
