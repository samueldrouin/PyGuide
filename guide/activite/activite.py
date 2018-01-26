"""
Module permettant la création et l'affichage des activités

Le module est responsable de l'ajout et de la modification des activité dans la base de donnée. Contrairement à la majorité des modules, 
se module ne comporte pas de classe de base puis les besoins pour la création et l'affichage des activités sont très différents. 

Classes
    NouvelleActivite : Dialog permettant la création d'une nouvelle activité dans la base de données
    AfficherActivite : Dialog permettant l'affichage des informations sur une activité
"""


# Python import
import os
from datetime import date, timedelta, datetime
import tempfile
import uuid

# PyQt import
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QDialog
from PyQt5.QtCore import QDate, QTime, Qt, QDateTime
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

# PyLaTeX import
from pylatex import Document, Command, PageStyle, simple_page_number, MiniPage, LineBreak, MediumText, LargeText, Head, LongTabu
from pylatex.utils import bold

# Project import
from script.database import Error
from facturation import facturation

# Interface import
from interface.nouvelle_activite import Ui_NouvelleActivite
from interface.afficher_activite import Ui_AfficherActivite


class NouvelleActivite(QDialog, Ui_NouvelleActivite):
    """
    Dialog permettant la création d'une nouvelle activité dans la base de données
    
    Méthodes
        vider_date_exclusion : Vide la liste des date d'exclusion
        ajout_date_exclusion : Ajouter une date à la liste d'exclusion
        afficher_categorie_activite : Afficher la liste des categories d'activite dans le combobox
        afficher_champs_date : Afficher les champs pour entrer les date selon la fréquence de l'activité
        process : Traitement de l'ajout de l'activité dans la base de données
    """
    def __init__(self, database):
        super(NouvelleActivite, self).__init__()
        self.setupUi(self)

        # Instance variable definition
        self.DATABASE= database

        # Afficher les dates et heure par defaut
        current_date = QDate.currentDate()
        self.ded_unique.setDate(current_date)
        self.ded_debut.setDate(current_date)
        self.ded_fin.setDate(current_date)
        self.ded_exclusion.setDate(current_date)

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
        query = QSqlQuery(self.DATABASE)
        query.exec_("SELECT "
                      "id_categorie_activite, nom "
                    "FROM "
                      "categorie_activite")

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Ajouter les responsables a la liste
        while query.next():
            self.cbx_category_activite.addItem(str(query.value(1)), userData=query.value(0))

    def afficher_champs_date(self):
        """
        Afficher les champs pour entrer les date selon la fréquence de l'activité
            - Activité unique : un seul champ est affiché pour entrer la date
            - Activité hebdomadaire : les champs pour afficher les date de début, fin et exlcusion sotn affichés
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
        Traitement de l'ajout de l'activité dans la base de données
        """
        if self.rbt_unique.isChecked():
            query = QSqlQuery(self.DATABASE)
            query.prepare("INSERT INTO activite "
                            "(id_categorie_activite, "
                            "date, "
                            "heure_debut, "
                            "heure_fin, "
                            "date_limite_inscription) "
                          "VALUES "
                            "(:id_categorie_activite, "
                            ":date, "
                            ":heure_debut, "
                            ":heure_fin, "
                            ":date_limite_inscription)")
            query.bindValue(':id_categorie_activite',
                            self.cbx_category_activite.itemData(self.cbx_category_activite.currentIndex()))
            query.bindValue(':date', self.ded_unique.date().toString('yyyy-MM-dd'))
            query.bindValue(':heure_debut', self.tim_debut.time().toString('HH:mm'))
            query.bindValue(':heure_fin', self.tim_fin.time().toString('HH:mm'))

            # Date limite inscription
            value_date = self.ded_unique.date().toString('yyyy-MM-dd') - self.sbx_fin_inscription.value()
            query.bindValue(':date_limite_inscription', value_date)

            query.exec_()
            # Affichage d'un message d'erreur si la requete echoue
            if not Error.DatabaseError.sql_error_handler(query.lastError()):
                self.accept() # Fermer le dialog seulement si la requete est réussie
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
            
            QSqlDatabase(self.DATABASE).transaction()
            for date_activite in liste_date:
                query = QSqlQuery(self.DATABASE)
                query.prepare("INSERT INTO activite "
                                "(id_categorie_activite, "
                                "date, "
                                "heure_debut, "
                                "heure_fin, "
                                "date_limite_inscription) "
                              "VALUES "
                                "(:id_categorie_activite, "
                                ":date_activite, "
                                ":heure_debut, "
                                ":heure_fin, "
                                ":date_limite_inscription)")
                query.bindValue(':id_categorie_activite',
                                self.cbx_category_activite.itemData(self.cbx_category_activite.currentIndex()))
                query.bindValue(':date_activite', QDate(date_activite.year, date_activite.month,
                                                        date_activite.day).toString('yyyy-MM-dd'))
                query.bindValue(':heure_debut', self.tim_debut.time().toString('HH:mm'))
                query.bindValue(':heure_fin', self.tim_fin.time().toString('HH:mm'))

                # Date limite inscription
                value_date = QDate(date_activite.year, date_activite.month,
                                   date_activite.day).toString('yyyy-MM-dd') - self.sbx_fin_inscription.value()
                query.bindValue(':date_limite_inscription', value_date)
                query.exec_()

                # Affichage d'un message d'erreur si la requete echoue
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    QSqlDatabase(self.DATABASE).rollback() # Annuler la transaction
                    return # Empêche la fermeture du dialog
            QSqlDatabase(self.DATABASE).commit()
        self.accept()

class AfficherActivite(QDialog, Ui_AfficherActivite):
    """
    Dialog permettant l'affichage des informations sur une activité
    """
    def __init__(self, database, id_activite):
        super(AfficherActivite, self).__init__()
        self.setupUi(self)

        # Instance variable definition
        self.DATABASE= database
        self.ID_ACTIVITE = id_activite

        # Afficher les informations sur l'activite
        self.afficher_informations()
        self.afficher_inscription()

        # Affichage des dates
        self.ded_date.setMinimumDate(QDate().currentDate())
        self.ded_limite.setMinimumDate(QDate().currentDate())
        
        # Parametres du table widget
        self.tbl_inscriptions.setColumnHidden(0, True)

        # Slots
        self.btn_fermer.clicked.connect(self.accept)
        self.btn_annuler.clicked.connect(self.annuler_activite)
        self.btn_modifier.clicked.connect(self.modifier_activite)
        self.btn_liste.clicked.connect(self.liste_presence)
        self.btn_presence.clicked.connect(self.enregistrer_presences)

    def enregistrer_presences(self):
        """Enregistrer la liste des présences"""
        for row in range(self.tbl_inscriptions.rowCount()):
            # Entrer la personne comme présente
            print(self.tbl_inscriptions.item(row, 5).checkState())
            if self.tbl_inscriptions.item(row, 5).checkState() == Qt.Checked:
                query = QSqlQuery(self.DATABASE)
                query.prepare("UPDATE inscription "
                              "SET "
                                "present = 1 "
                              "WHERE id_inscription = :id_inscription")
                query.bindValue(':id_inscription', self.tbl_inscriptions.item(row, 0).text())
                query.exec_()

                # Affichage d'un message d'erreur si la requete echoue
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    return # Ne pas continuer si la requete échoue
            # Entrer la personne comme abscente
            else:
                query = QSqlQuery(self.DATABASE)
                query.prepare("UPDATE inscription "
                              "SET "
                                "present = 0 "
                              "WHERE id_inscription = :id_inscription")
                query.bindValue(':id_inscription', self.tbl_inscriptions.item(row, 0).text())
                query.exec_()

                # Affichage d'un message d'erreur si la requete echoue
                if Error.DatabaseError.sql_error_handler(query.lastError()):
                    return # Ne pas continuer si la requete échoue
    
    def liste_presence(self):
        """Afficher la liste des présences"""
        geometry_options = {"margin": "1in"}
        doc = Document(page_numbers=True, geometry_options=geometry_options)

        # Document header
        header = PageStyle("header")
        # Left header
        with header.create(Head("L")):
            header.append("Liste de présences")
        # Right header
        with header.create(Head("R")):
            header.append("Centre femmes du Haut-Richelieu")

        doc.preamble.append(header)
        doc.change_document_style("header")

        # Titre du document
        with doc.create(MiniPage(align='c')):
            doc.append(LargeText(bold("Liste de présences")))
            doc.append(LineBreak())
            doc.append(MediumText("{}".format(self.txt_nom.text())))
            doc.append(LineBreak())
            doc.append(MediumText("{}".format(self.ded_date.date().toString('dd MMMM yyyy'))))

        # Generer le tableau
        with doc.create(LongTabu("X[l] X[l]")) as data_table:
            header_row1 = ["Nom de la participante", "Signature"]
            data_table.add_row(header_row1, mapper=[bold])
            data_table.add_hline()
            data_table.end_table_header()
            for r in range(self.tbl_inscriptions.rowCount()):
                data_table.add_empty_row()
                row = [self.tbl_inscriptions.item(r, 1).text(), ""]
                data_table.add_row(row)
                data_table.add_empty_row()
                data_table.add_empty_row()
                data_table.add_hline()

        temp_dir = tempfile.mkdtemp()
        file = str(uuid.uuid4())
        filename = os.path.join(temp_dir, file)

        doc.generate_pdf(filename, compiler="pdflatex")

        file_ext = file + ".pdf"
        filename_ext = os.path.join(temp_dir, file_ext)
        os.startfile(os.path.normpath(filename_ext))

    def afficher_inscription(self):
        """Afficher la liste des inscriptions"""
        # Obtenir les informations dans la base de donnees
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                          "inscription.id_inscription, "
                          "participante.prenom, "
                          "participante.nom, "
                          "participante.telephone_1, "
                          "participante.poste_telephone_1, "
                          "inscription.status, "
                          "membre.actif, "
                          "inscription.present "
                      "FROM inscription "
                      "INNER JOIN participante ON participante.id_participante = inscription.id_participante "
                      "LEFT JOIN membre ON membre.id_participante = inscription.id_participante "
                      "WHERE (inscription.id_activite = :id_activite) AND ((inscription.status = :inscription) OR (inscription.status = :facture))")
        query.bindValue(':id_activite', self.ID_ACTIVITE)
        query.bindValue(':inscription', facturation.STATUS_INSCRIPTION)
        query.bindValue(':facture', facturation.STATUS_FACTURE)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        while query.next():
            # Préparation du tableau
            self.tbl_inscriptions.insertRow(self.tbl_inscriptions.rowCount())
            r = self.tbl_inscriptions.rowCount() - 1

            # Affichage des donnees
            self.tbl_inscriptions.setItem(r, 0, QTableWidgetItem(str(query.value(0))))

            nom = str(query.value(1)) + " " + str(query.value(2))
            self.tbl_inscriptions.setItem(r, 1, QTableWidgetItem(nom))

            phone_number_string = str(query.value(3))
            phone_number = phone_number_string[:3] + " " + phone_number_string[3:6] + "-" + phone_number_string[6:]
            print(query.value(4))
            if query.value(4) == " ":
                phone_number = phone_number + " p. " + str(query.value(4))
            self.tbl_inscriptions.setItem(r, 2, QTableWidgetItem(phone_number))

            if int(query.value(5)) == facturation.STATUS_FACTURE:
                item = QTableWidgetItem()
                item.setCheckState(Qt.Checked)
                item.setFlags(item.flags() ^ Qt.ItemIsUserCheckable)
                item.setText("")
                self.tbl_inscriptions.setItem(r, 4, item)

            if str(query.value(6)) == "1":
                item = QTableWidgetItem()
                item.setCheckState(Qt.Checked)
                item.setFlags(item.flags() ^ Qt.ItemIsUserCheckable)
                item.setText("")
                self.tbl_inscriptions.setItem(r, 3, item)

            if str(query.value(7)) == "1":
                item = QTableWidgetItem()
                item.setCheckState(Qt.Checked)
                item.setFlags(item.flags() ^ Qt.ItemIsUserCheckable)
                item.setText("")
                self.tbl_inscriptions.setItem(r, 5, item)
            elif str(query.value(7)) == "0":
                item = QTableWidgetItem()
                item.setCheckState(Qt.Unchecked)
                item.setFlags(item.flags() ^ Qt.ItemIsUserCheckable)
                item.setText("")
                self.tbl_inscriptions.setItem(r, 5, item)
            else:
                # Afficher les boutons de présence si l'activité est passée seulement
                date = self.ded_date.date()
                time = self.ted_heure_fin.time()

                datetime = QDateTime(date, time)
                if datetime <= QDateTime.currentDateTime():
                    item = QTableWidgetItem()
                    item.setCheckState(Qt.Unchecked)
                    item.setText("")
                    self.tbl_inscriptions.setItem(r, 5, item)

    def afficher_informations(self):
        """Afficher les informations sur l'activite lieu"""
        # Obtenir les informations de la base de donnees
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                        "categorie_activite.nom, "
                        "lieu.nom, "
                        "activite.date, "
                        "activite.heure_debut, "
                        "activite.heure_fin, "
                        "activite.date_limite_inscription, "
                        "responsable.prenom, "
                        "responsable.nom "
                      "FROM activite "
                      "LEFT JOIN categorie_activite "
                        "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite "
                      "LEFT JOIN lieu ON "
                        "categorie_activite.id_lieu = lieu.id_lieu "
                      "LEFT JOIN responsable ON "
                         "responsable.id_responsable = categorie_activite.id_responsable "
                      "WHERE (activite.id_activite = :id_activite)")
        query.bindValue(':id_activite', self.ID_ACTIVITE)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        # Afficher les informations
        query.first()
        self.txt_nom.setText(str(query.value(0)))
        self.txt_lieu.setText(str(query.value(1)))
        self.ded_date.setDate(QDate().fromString(query.value(2), 'yyyy-MM-dd'))
        self.ted_heure_debut.setTime(QTime().fromString(query.value(3), 'HH:mm'))
        self.ted_heure_fin.setTime(QTime().fromString(query.value(4), 'HH:mm'))
        self.ded_limite.setDate(QDate().fromString(query.value(5), 'yyyy-MM-dd'))

        nom = str(query.value(6)) + " " + str(query.value(7))
        self.txt_responsable.setText(nom)

        # Disabled le bouton de présence si l'activité n'est pas passée
        date = self.ded_date.date()
        time = self.ted_heure_fin.time()

        datetime = QDateTime(date, time)

        if datetime >= QDateTime.currentDateTime():
            self.btn_presence.setEnabled(False)

    def modifier_activite(self):
        """Modifier une activite"""
        query = QSqlQuery(self.DATABASE)
        query.prepare("UPDATE activite "
                      "SET "
                        "date = :date, "
                        "heure_debut = :heure_debut, "
                        "heure_fin = :heure_fin, "
                        "date_limite_inscription = :date_limite_inscription "
                      "WHERE "
                        "id_activite = :id_activite")
        query.bindValue(':date', self.ded_date.date().toString('yyyy-MM-dd'))
        query.bindValue(':heure_debut', self.ted_heure_debut.time().toString('HH:mm'))
        query.bindValue(':heure_fin', self.ted_heure_fin.time().toString('HH:mm'))
        query.bindValue(':date_limite_inscription', self.ded_limite.date().toString('yyyy-MM-dd'))
        query.bindValue(':id_activite', self.ID_ACTIVITE)
        query.exec_()

        Error.DatabaseError.sql_error_handler(query.lastError())

    def annuler_activite(self):
        """Annuler une activite"""

        # Affiche un message pour confirmer l'annulation
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Annulation d'une activité")
        msgbox.setText("Annulation d'une activité")
        msgbox.setInformativeText("Êtes-vous sur de vouloir continuer à annuler cette activité ?")
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgbox.setDefaultButton(QMessageBox.No)
        
        # L'annulation est confirmée
        if msgbox.exec() == QMessageBox.Yes:
            query = QSqlQuery(self.DATABASE)
            query.prepare("UPDATE activite "
                          "SET "
                            "status = :status "
                          "WHERE "
                            "id_activite = :id_activite")
            query.bindValue(':status', False)
            query.bindValue(':id_activite', self.ID_ACTIVITE)
            query.exec_()

            Error.DatabaseError.sql_error_handler(query.lastError())

            self.accept()
