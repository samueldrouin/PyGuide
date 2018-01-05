"""Création de nouvelle facture"""

# Python import
import os

# PyQt import
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtCore import QTime, QDate
from PyQt5 import uic

# Project import
from form import Form

class Facture(Form):
    """Fonctions nécessaires pour tous les types de facture"""
    def __init__(self, database):
        return super(Facture, self).__init__()
   
        # Instance variable definition
        self.database = database
        self.id_participante = None

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

    def set_parsed_phone_number(self, old, new):
        """
        Show parsed phone number
        :param old: Old cursor position
        :param new: New cursor position
        """
        phone_number = self.phone_number_parsing(old, new, self.sender().text())
        self.sender().setText(phone_number)

    def afficher_information_participante(self):
        """
        Afficher les informations sur la participante
        """

        if len(self.txt_numero.text()) == 12:

            # Preparation du numero de telephone
            phone_number = int(self.check_phone_number(self.txt_numero.text()))

            query = QSqlQuery()
            query.prepare("SELECT participante.id_participante, participante.prenom, participante.nom, "
                          "participante.ville, membre.actif FROM participante "
                          "LEFT JOIN membre ON participante.id_participante = membre.id_participante "
                          "WHERE (participante.telephone_1 = :phone) OR (participante.telephone_2 = :phone)")
            query.bindValue(':phone', phone_number)
            query.exec_()

            if query.first():
                # Afficher les informations du membre
                self.id_participante = int(query.value(0))

                nom = str(query.value(1)) + " " + str(query.value(2))
                self.txt_nom.setText(nom)

                self.txt_ville.setText(str(query.value(3)))

                if query.value(4):
                    self.chk_actif.setChecked(True)

                # Permettre l'ajout d'activite
                self.btn_ajouter_activite.setEnabled(True)
                self.btn_rembourser.setEnabled(True)
                self.btn_ajouter_inscription.setEnabled(True)
                self.btn_remove.setEnabled(True)
                self.afficher_inscriptions()
                self.txt_activite.setText("")
            else:
                # Indiquer à l'utilisateur qu'il n'existe pas de compte avec ce numero
                msgbox = QMessageBox()
                msgbox.setWindowTitle("Aucune compte")
                msgbox.setText("Aucune compte")
                msgbox.setInformativeText("Il n'existe aucun compte à ce numéro de téléphone. Vérifiez que le "
                                          "numéro est entré correctement.")
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.setDefaultButton(QMessageBox.Ok)
                msgbox.exec()

        # Indiquer que le numéro est invalide
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Numéro de téléphone invalide")
            msgbox.setText("Numéro de téléphone invalide")
            msgbox.setInformativeText("Veuillez entrer un numéro de téléphone valide")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.exec()

    def afficher_liste_activite(self):
        """
        Afficher la liste des activite
        """

        # Fetch data from database
        query = QSqlQuery()
        sql = "SELECT categorie_activite.nom, categorie_activite.prix_membre, categorie_activite.prix_non_membre, "\
              "activite.date, activite.heure_debut, activite.heure_fin, activite.id_activite "\
              "FROM activite "\
              "INNER JOIN categorie_activite ON activite.id_categorie_activite = categorie_activite.id_categorie_activite " \
              "WHERE activite.date_limite_inscription >= {} ".format(int(QDate.currentDate().toJulianDay()))

        # Recherche par nom d'activite
        if self.txt_activite.text() != "":
            sql = sql + "WHERE categorie_activite.nom LIKE '%{}%' ".format(self.txt_activite.text())

        sql = sql + "LIMIT 100"
        query.exec_(sql)

        self.tbl_activite.setRowCount(0)
        while query.next():
            self.tbl_activite.insertRow(self.tbl_activite.rowCount())
            r = self.tbl_activite.rowCount() - 1

            self.tbl_activite.setItem(r, 0, QTableWidgetItem(str(query.value(6))))
            self.tbl_activite.setItem(r, 1, QTableWidgetItem(str(query.value(0))))

            if self.chk_actif.isChecked():
                prix = "{0:.2f}$".format(query.value(1))
            else:
                prix = "{0:.2f}$".format(query.value(2))
            self.tbl_activite.setItem(r, 2, QTableWidgetItem(prix))

            date_activite = QDate.fromJulianDay(query.value(3)).toString('dd MMM yyyy')
            self.tbl_activite.setItem(r, 3, QTableWidgetItem(date_activite))

            heure_debut = QTime.fromMSecsSinceStartOfDay(query.value(4)).toString('hh:mm')
            heure_fin = QTime.fromMSecsSinceStartOfDay(query.value(5)).toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.tbl_activite.setItem(r, 4, QTableWidgetItem(heure))

        self.tbl_activite.resizeColumnsToContents()

    def ajout_activite(self):
        """
        Ajouter une activite à la facture
        """
        activite_row = self.tbl_activite.currentRow()
        if activite_row != -1:
            self.tbl_article.insertRow(self.tbl_article.rowCount())
            r = self.tbl_article.rowCount() - 1

            self.tbl_article.setItem(r, 0, self.tbl_activite.item(activite_row, 0).clone())
            self.tbl_article.setItem(r, 1, self.tbl_activite.item(activite_row, 1).clone())
            self.tbl_article.setItem(r, 2, self.tbl_activite.item(activite_row, 2).clone())
            self.tbl_article.setItem(r, 3, self.tbl_activite.item(activite_row, 3).clone())
            self.tbl_article.setItem(r, 4, self.tbl_activite.item(activite_row, 4).clone())

            if self.sender() == self.btn_ajouter_activite:
                self.tbl_article.setItem(r, 5, QTableWidgetItem("1"))
                self.changer_total(self.tbl_activite.item(activite_row, 2).text())
            else:
                self.tbl_article.setItem(r, 5, QTableWidgetItem("(1)"))
                self.changer_total("-" + self.tbl_activite.item(activite_row, 2).text())
            self.tbl_article.resizeColumnsToContents()
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Aucune activité sélectionnée")
            msgbox.setText("Aucune activité sélectionnée")
            msgbox.setInformativeText("Veuillez sélectionner une activité à ajouter.")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.exec()

    def ajout_inscription(self):
        """
        Ajouter une inscription a la facture
        """
        tbl_inscription = self.tbl_inscription.currentRow()
        if tbl_inscription != -1:
            self.tbl_article.insertRow(self.tbl_article.rowCount())
            r = self.tbl_article.rowCount() - 1

            self.tbl_article.setItem(r, 0, self.tbl_activite.item(tbl_inscription, 0).clone())
            self.tbl_article.setItem(r, 1, self.tbl_activite.item(tbl_inscription, 1).clone())
            self.tbl_article.setItem(r, 2, self.tbl_activite.item(tbl_inscription, 2).clone())
            self.tbl_article.setItem(r, 3, self.tbl_activite.item(tbl_inscription, 3).clone())
            self.tbl_article.setItem(r, 4, self.tbl_activite.item(tbl_inscription, 4).clone())
            self.tbl_article.setItem(r, 5, QTableWidgetItem("1"))

            self.changer_total(self.tbl_activite.item(tbl_inscription, 2).text())
            self.tbl_article.resizeColumnsToContents()
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Aucune activité sélectionnée")
            msgbox.setText("Aucune activité sélectionnée")
            msgbox.setInformativeText("Veuillez sélectionner une activité à ajouter.")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.exec()

    def retirer_activite(self):
        """
        Retirer une activite du panier
        """
        row = self.tbl_article.currentRow()
        if row != -1:
            self.tbl_article.removeRow(row)
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Aucune activité sélectionnée")
            msgbox.setText("Aucune activité sélectionnée")
            msgbox.setInformativeText("Veuillez sélectionner une activité à retirer.")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.exec()

    def changer_total(self, montant):
        """
        Changer le montant du total
        :param montant: Montant de l'article
        """
        total = self.txt_total.text()
        montant = float(montant[:-1])
        if total != "":
            print(montant)
            total = float((self.txt_total.text())[:-1])
            total = total + montant
            print(total)
            self.txt_total.setText("{0:.2f}$".format(total))
        else:
            print(montant)
            self.txt_total.setText("{0:.2f}$".format(montant))

    def afficher_inscriptions(self):
        """
        Afficher les inscriptions associetes au compte
        """

        # Effacer les elements existants
        self.tbl_inscription.setRowCount(0)

        # Fetch inscriptions from database
        query = QSqlQuery()
        query.prepare("SELECT inscription.id_inscription, categorie_activite.nom, categorie_activite.prix_membre, "
                      "categorie_activite.prix_non_membre, activite.date, activite.heure_debut, activite.heure_fin "
                      "FROM inscription "
                      "LEFT JOIN activite ON inscription.id_activite = activite.id_activite "
                      "LEFT JOIN categorie_activite ON activite.id_categorie_activite = categorie_activite.id_categorie_activite "
                      "WHERE (inscription.id_participante = :id_participante) AND (activite.date >= :current_date) AND (inscription.status = :status)")
        query.bindValue(':id_participante', self.id_participante)
        query.bindValue(':current_date', QDate.currentDate().toJulianDay())
        query.bindValue(':status', True)
        query.exec_()

        # Afficher la liste des activites dans le panier
        while query.next():
            self.tbl_inscription.insertRow(self.tbl_inscription.rowCount())
            r = self.tbl_inscription.rowCount() - 1

            self.tbl_inscription.setItem(r, 0, QTableWidgetItem(str(query.value(0))))
            self.tbl_inscription.setItem(r, 1, QTableWidgetItem(str(query.value(1))))

            if self.chk_actif.isChecked():
                prix = "{0:.2f}$".format(query.value(2))
            else:
                prix = "{0:.2f}$".format(query.value(3))
            self.tbl_inscription.setItem(r, 2, QTableWidgetItem(prix))

            date_activite = QDate.fromJulianDay(query.value(4)).toString('dd MMM yyyy')
            self.tbl_inscription.setItem(r, 3, QTableWidgetItem(date_activite))

            heure_debut = QTime.fromMSecsSinceStartOfDay(query.value(5)).toString('hh:mm')
            heure_fin = QTime.fromMSecsSinceStartOfDay(query.value(6)).toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.tbl_inscription.setItem(r, 4, QTableWidgetItem(heure))

    def process(self):
        """
        Traitement des donnees pour la base de données
        """
        for row in range(self.tbl_article.rowCount()):
            # Commencer une transaction
            QSqlDatabase(self.database).transaction()

            # Ajouter une facture
            query = QSqlQuery()
            query.prepare("INSERT INTO facture (numero_recu, id_participante) "
                          "VALUES (:numero_recu, :id_participante)")
            query.bindValue(':numero_recu', self.check_string(self.txt_recu.text()))
            query.bindValue(':id_participante', self.id_participante)
            query.exec_()

            # Ajouter les inscriptions
            query = QSqlQuery()
            query.prepare("INSERT OR REPLACE INTO inscription (id_inscription, id_participante, id_activite, status, id_facture) "
                          "VALUES "
                          "((SELECT id_inscription FROM inscription WHERE (id_participante = :id_participante) "
                          "AND (id_activite = :id_activite)), :id_participante, :id_activite, :status, (SELECT last_insert_rowid()))")
            query.bindValue(':id_participante', self.id_participante)
            query.bindValue(':id_activite', self.tbl_article.item(row, 0).text())
            query.bindValue(':status', True)
            query.exec_()

            # Termer la transaction
            QSqlDatabase(self.database).commit()
        self.accept()

    def get_numero_facture(self):
        """
        Recuperer le numero de la facture
        """
        query = QSqlQuery()
        query.exec_("SELECT MAX(id_facture) FROM facture")

        query.first()

        # S'il existe deja des facture dans la base de donnees
        if query.value(0) != "":
            self.txt_facture.setText(str(query.value(0)+1))
        # S'il s'agit de la première facture
        else:
            self.txt_facture.setText("1")
