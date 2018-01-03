# Python import
from PyQt5.QtWidgets import QMessageBox, QAbstractItemView, QTableWidgetItem
from PyQt5.QtCore import QDate, QTime
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic
import os

# Project import
from form import Form


class Inscription(Form):
    def __init__(self, database):
        super(Inscription,self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'inscription.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.database = database
        self.id_participante = None

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
        self.txt_numero.cursorPositionChanged.connect(self.phone_number_parsing)
        self.txt_numero.returnPressed.connect(self.afficher_information_participante)
        self.txt_activite.textChanged.connect(self.afficher_liste_activite)
        self.btn_ajouter.clicked.connect(self.ajouter_activite)
        self.btn_enregistrer.clicked.connect(self.process)
        self.btn_remove.clicked.connect(self.retirer_activite)

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
                self.btn_ajouter.setEnabled(True)
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

    def phone_number_parsing(self, old, new):
        """
        Parsing phone number
        :param old: Old cursor position
        :param new: New cursor position
        """
        phone_number = self.sender().text()
        if new == 4 and old == 3:
            if phone_number[3] != " ":
                phone_number = phone_number[:3] + " " + phone_number[3:]
                self.sender().setText(phone_number)
        if new == 8 and old == 7:
            if phone_number[7] != "-":
                phone_number = phone_number[:7] + "-" + phone_number[7:]
                self.sender().setText(phone_number)

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

    def ajouter_activite(self):
        """
        Ajouter une activite au panier
        """
        activite_row = self.tbl_activite.currentRow()
        if activite_row != -1:
            self.tbl_panier.insertRow(self.tbl_panier.rowCount())
            r = self.tbl_panier.rowCount() - 1

            self.tbl_panier.setItem(r, 0, self.tbl_activite.item(activite_row, 0).clone())
            self.tbl_panier.setItem(r, 1, QTableWidgetItem("1"))
            self.tbl_panier.setItem(r, 3, self.tbl_activite.item(activite_row, 1).clone())
            self.tbl_panier.setItem(r, 4, self.tbl_activite.item(activite_row, 2).clone())
            self.tbl_panier.setItem(r, 5, self.tbl_activite.item(activite_row, 3).clone())
            self.tbl_panier.setItem(r, 6, self.tbl_activite.item(activite_row, 4).clone())

            self.tbl_panier.resizeColumnsToContents()
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
        row = self.tbl_panier.currentRow()
        if row != -1:
            if self.tbl_panier.item(row, 1) != "0":
                self.tbl_panier.setItem(row, 1, QTableWidgetItem("-1"))
                self.tbl_panier.setRowHidden(row, True)
            else:
                self.tbl_panier.removeRow(row)
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Aucune activité sélectionnée")
            msgbox.setText("Aucune activité sélectionnée")
            msgbox.setInformativeText("Veuillez sélectionner une activité à retirer.")
            msgbox.setIcon(QMessageBox.Information)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.exec()

    def process(self):
        """
        Traitement des donnees pour la base de données
        """
        for row in range(self.tbl_panier.rowCount()):
            # Ajouter une inscription
            if int(self.tbl_panier.item(row, 1).text()) == 1:
                query = QSqlQuery()
                query.prepare("INSERT OR REPLACE INTO inscription (id_inscription, id_participante, id_activite, status)   VALUES "
                              "((SELECT id_inscription FROM inscription WHERE (id_participante = :id_participante) "
                              "AND (id_activite = :id_activite)), :id_participante, :id_activite, :status)")
                query.bindValue(':id_participante', self.id_participante)
                query.bindValue(':id_activite', self.tbl_panier.item(row, 0).text())
                query.bindValue(':status', True)
                query.exec_()

            # Effacer une inscription
            elif int(self.tbl_panier.item(row, 1).text()) == -1:
                query = QSqlQuery()
                query.prepare("UPDATE inscription "
                              "SET status = :status "
                              "WHERE id_inscription = :id_inscription ")
                query.bindValue(':status', False)
                query.bindValue(':id_inscription', self.tbl_panier.item(row, 2).text())
                query.exec_()

        self.accept()

    def afficher_inscriptions(self):
        """
        Afficher les inscriptions associetes au compte
        """

        # Effacer les elements existants
        self.tbl_panier.setRowCount(0)

        # Fetch inscriptions from database
        query = QSqlQuery()
        query.prepare("SELECT inscription.id_inscription, categorie_activite.nom, categorie_activite.prix_membre, "
                      "categorie_activite.prix_non_membre, activite.date, activite.heure_debut, activite.heure_fin, "
                      "activite.id_activite FROM inscription "
                      "LEFT JOIN activite ON inscription.id_activite = activite.id_activite "
                      "LEFT JOIN categorie_activite ON activite.id_categorie_activite = categorie_activite.id_categorie_activite "
                      "WHERE (inscription.id_participante = :id_participante) AND (activite.date >= :current_date) AND (inscription.status = :status)")
        query.bindValue(':id_participante', self.id_participante)
        query.bindValue(':current_date', QDate.currentDate().toJulianDay())
        query.bindValue(':status', True)
        query.exec_()

        # Afficher la liste des activites dans le panier
        while query.next():
            self.tbl_panier.insertRow(self.tbl_panier.rowCount())
            r = self.tbl_panier.rowCount() - 1

            self.tbl_panier.setItem(r, 0, QTableWidgetItem(str(query.value(7))))
            self.tbl_panier.setItem(r, 1, QTableWidgetItem(str(query.value(0))))
            self.tbl_panier.setItem(r, 2, QTableWidgetItem(True))
            self.tbl_panier.setItem(r, 3, QTableWidgetItem(str(query.value(1))))

            if self.chk_actif.isChecked():
                prix = "{0:.2f}$".format(query.value(2))
            else:
                prix = "{0:.2f}$".format(query.value(3))
            self.tbl_panier.setItem(r, 4, QTableWidgetItem(prix))

            date_activite = QDate.fromJulianDay(query.value(4)).toString('dd MMM yyyy')
            self.tbl_panier.setItem(r, 5, QTableWidgetItem(date_activite))

            heure_debut = QTime.fromMSecsSinceStartOfDay(query.value(5)).toString('hh:mm')
            heure_fin = QTime.fromMSecsSinceStartOfDay(query.value(6)).toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.tbl_panier.setItem(r, 6, QTableWidgetItem(heure))