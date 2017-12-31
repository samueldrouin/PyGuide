# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QMessageBox, QTableWidgetItem, \
    QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSettings, QDate, QTime
from PyQt5.Qt import QApplication
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import os
import pathlib
import datetime

# Projet import
from participante import NouvelleParticipante, ModifierParticipante
from lieu import NouveauLieu, ModifierLieu
from activite import NouvelleActivite, ModifierActivite
from categorie_activite import NouvelleCategorieActivite, ModifierCategorieActivite
from a_propos import APropos
from settings import Settings
from consultation import Consultation
from facturation import Facturation
from inscription import Inscription


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui = os.path.join(os.path.dirname(__file__),'GUI','mainwindow.ui')
        uic.loadUi(ui, self)

        # Connection à la base de données
        self.database = self.check_database_status()

        # Charger l'interface graphique
        self.set_participantes_central_widget()

        # Actions
        self.act_consult_participantes.triggered.connect(self.set_participantes_central_widget)
        self.act_consult_activites.triggered.connect(self.set_activite_central_widget)
        self.act_consult_lieux.triggered.connect(self.set_lieux_central_widget)
        self.act_consult_categorie_activite.triggered.connect(self.set_categorie_activite_central_widget)
        self.act_about.triggered.connect(self.a_propos)
        self.act_about_qt.triggered.connect(QApplication.aboutQt)
        self.act_reglage.triggered.connect(self.reglage)
        self.act_type_activite.triggered.connect(self.consultation_type_activite)
        self.act_responsables.triggered.connect(self.consultation_responsables)
        self.act_inscription.triggered.connect(self.inscription)
        self.act_facturation.triggered.connect(self.facturation)

    def check_database_status(self):
        """
        Lecture des réglages
        Vérifier si une base de donnée est enregistrée
        :return: Path to database
        """
        settings = QSettings("Samuel Drouin", "GUIDE-CFR")
        database = settings.value("Database")

        # Demander le chemin de la base de donnée tant qu'un chemin n'est pas entré
        while database is None:
            msgbox = QMessageBox()
            msgbox.setText("Aucune base de donnée")
            msgbox.setInformativeText("Vous devez sélectionner la base de donnée dans les réglages avant de pouvoir "
                                      "utiliser le programme. ")
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            ret = msgbox.exec()

            if ret == QMessageBox.Ok:
                self.reglage()
                settings = QSettings("Samuel Drouin", "GUIDE-CFR")
                database = settings.value("Database")
        # Demander le chemin vers la base de données tant qu'un chemin valide n'est pas entré
        while not pathlib.Path(database).is_file():
            msgbox = QMessageBox()
            msgbox.setText("Base de donnée inexistante")
            msgbox.setInformativeText("Vous devez sélectionner la base de donnée existante dans les réglages avant de "
                                      "pouvoir utiliser le programme. ")
            msgbox.setIcon(QMessageBox.Critical)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            ret = msgbox.exec()

            if ret == QMessageBox.Ok:
                self.reglage()
                settings = QSettings("Samuel Drouin", "GUIDE-CFR")
                database = settings.value("Database")

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(database)

        dbopen = False
        while not dbopen:
            dbopen = db.open()

            if not dbopen:
                msgbox = QMessageBox()
                msgbox.setText("Erreur de connection")
                msgbox.setInformativeText(
                    "Une erreur lors de la connection à la base de données empêche l'ouverture du programme. Appuyez "
                    "sur annuler pour fermer le programme")
                msgbox.setDetailedText(db.lastError().text())
                msgbox.setIcon(QMessageBox.Critical)
                msgbox.setStandardButtons(QMessageBox.Cancel)
                msgbox.setDefaultButton(QMessageBox.Cancel)
                msgbox.exec()
                self.close()

        return db

    def inscription(self):
        """
        Ouvre une fenetre pour une nouvelle inscription
        """
        inscription = Inscription()
        inscription.exec()

    def facturation(self):
        """
        Ouvre une fenetre pour une nouvelle facture
        """
        facturation = Facturation()
        facturation.exec()

    def consultation_responsables(self):
        """
        Ouvre la fenetre de consultation des responsables
        """
        consultation = Consultation(2, self.database)
        consultation.exec()

    def consultation_type_activite(self):
        """
        Ouvrir la fenetre de consultation des types d'activite
        """
        consultation = Consultation(1, self.database)
        consultation.exec()

    def reglage(self):
        """
        Ouvre la fenetre des reglages
        """
        settings = Settings()
        settings.exec()

    @staticmethod
    def a_propos(self):
        """
        Affiche les informations sur l'application
        """
        a_propos = APropos()
        a_propos.exec()

    def set_participantes_central_widget(self):
        """
        Affichage de la liste des participantes et des options de tri
        """
        central_widget = CentralWidgetParticipantes(self.database)
        self.setCentralWidget(central_widget)

    def set_activite_central_widget(self):
        """
        Affichage de la liste des activites et des options de tri
        """
        central_widget = CentralWidgetActivite(self.database)
        self.setCentralWidget(central_widget)

    def set_categorie_activite_central_widget(self):
        """
        Affichage de la liste des type d'activite et des options de tri
        """
        central_widget = CentralWidgetCategorieActivite(self.database)
        self.setCentralWidget(central_widget)

    def set_lieux_central_widget(self):
        """
        Affichage des lieux et des options de tri
        """
        central_widget = CentralWidgetLieux(self.database)
        self.setCentralWidget(central_widget)


"""
Classe principale pour les CentralWidget
Contient les fonction communes à tout les CentralWidget
"""


class CentralWidget(QWidget):
    def __init__(self):
        super(CentralWidget, self).__init__()
        self.layout = QVBoxLayout(self)


"""
CentralWidget spécifiques :
- Options de tri spécifique
- Tableau avec les informations à afficher
"""


class CentralWidgetParticipantes(CentralWidget):
    def __init__(self, database):
        super(CentralWidgetParticipantes, self).__init__()

        # GUI setup
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_participantes.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Instance variable definition
        self.database = database

        # Table widget parameters
        self.table_widget.setColumnCount(6)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Ville", "Courriel", "Telephone", "Numéro de membre"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_participante)
        self.table_widget.clicked.connect(self.edit_participante)
        self.top_widget.cbx_search.currentTextChanged.connect(self.update_search_placeholder)
        self.top_widget.txt_search.textEdited.connect(self.update_list)
        self.top_widget.cbx_sort.currentIndexChanged.connect(self.update_list)
        self.top_widget.chk_membre.toggled.connect(self.update_list)
        self.top_widget.chk_desc.toggled.connect(self.update_list)

        # Update GUI elements
        self.update_list()
        self.update_search_placeholder(self.top_widget.cbx_search.currentText())

    def update_search_placeholder(self, text):
        """
        Update search placeholder text when combo box item is changed
        :param text:
        """
        self.top_widget.txt_search.clear()
        self.top_widget.txt_search.setPlaceholderText(text)

    def edit_participante(self, index):
        """
        Ouvre le dialog pour modifier une participante
        :param index: Index de la colonne
        """
        participante_id = self.table_widget.item(index.row(), 0).text()
        modifier_participante = ModifierParticipante(participante_id, self.database)
        modifier_participante.accepted.connect(self.update_list)
        modifier_participante.exec()

    def nouvelle_participante(self):
        """
        Ouvrir le dialog pour creer une nouvelle participante
        """
        nouvelle_participante = NouvelleParticipante(self.database)
        nouvelle_participante.accepted.connect(self.update_list)
        nouvelle_participante.exec()

    def update_list(self):
        """
        Update participante list in table widget
        """
        # Fetch data from database
        query = QSqlQuery(self.database)
        if self.top_widget.chk_membre.isChecked():
            sql = "SELECT participante.id_participante, participante.prenom, participante.nom, " \
                  "participante.ville, participante.courriel, participante.telephone_1, " \
                  "participante.poste_telephone_1, membre.numero_membre FROM participante " \
                  "INNER JOIN membre ON membre.id_participante = participante.id_participante "
        else:
            sql = "SELECT participante.id_participante, participante.prenom, participante.nom, " \
                  "participante.ville, participante.courriel, participante.telephone_1, " \
                  "participante.poste_telephone_1, membre.numero_membre FROM participante " \
                  "LEFT JOIN membre ON membre.id_participante = participante.id_participante "

        # Ajout des options de recherche
        search = self.top_widget.txt_search.text()
        if search != "":
            if self.top_widget.cbx_search.currentText() == "Prénom":
                sql = sql + "WHERE participante.prenom LIKE '%{}%' ".format(search)
            elif self.top_widget.cbx_search.currentText() == "Nom":
                sql = sql + "WHERE participante.nom LIKE '%{}%' ".format(search)
            elif self.top_widget.cbx_search.currentText() == "Ville":
                sql = sql + "WHERE participante.ville LIKE '%{}%' ".format(search)
            else:
                sql = sql + "WHERE participante.telephone_1 LIKE '%{}%' ".format(search)

        # Ajouter les options de tri
        if self.top_widget.cbx_sort.currentText() == "Prénom":
            sql = sql + "ORDER BY participante.prenom "
        elif self.top_widget.cbx_sort.currentText() == "Nom":
            sql = sql + "ORDER BY participante.nom "
        elif self.top_widget.cbx_sort.currentText() == "Ville":
            sql = sql + "ORDER BY participante.ville "
        elif self.top_widget.cbx_sort.currentText() == "Numéro de téléphone":
            sql = sql + "ORDER BY participante.telephone_1 "
        else:
            sql = sql + "ORDER BY membre.numero_membre "

        # Order du tri
        if self.top_widget.chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "
        query.exec_(sql)

        # Show data in table widget
        self.table_widget.setRowCount(0)

        while query.next():
            self.table_widget.insertRow(self.table_widget.rowCount())
            r = self.table_widget.rowCount()-1

            self.table_widget.setItem(r, 0, QTableWidgetItem(str(query.value(0))))

            if not query.value(2) is None:
                nom = "{} {}".format(str(query.value(1)), str(query.value(2)))
            else:
                nom = str(query.value(1))
            self.table_widget.setItem(r, 1, QTableWidgetItem(nom))

            self.table_widget.setItem(r, 2, QTableWidgetItem(str(query.value(3))))
            self.table_widget.setItem(r, 3, QTableWidgetItem(str(query.value(4))))
            phone_number_string = str(query.value(5))
            phone_number = phone_number_string[:3] + " " + phone_number_string[3:6] + "-" + phone_number_string[6:]
            if query.value(6) is None:
                phone_number = phone_number + " p. " + str(query.value(6))
            self.table_widget.setItem(r, 4, QTableWidgetItem(phone_number))
            self.table_widget.setItem(r, 5, QTableWidgetItem(str(query.value(7))))

        self.table_widget.resizeColumnsToContents()

class CentralWidgetActivite(CentralWidget):
    def __init__(self, database):
        super(CentralWidgetActivite, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_activite)

        # Instance variable definition
        self.database = database

        # Table widget parameters
        self.table_widget.setColumnCount(7)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Lieu", "Prix", "Date", "Heure", "Date limite d'inscription"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Affichage de la date par defaut
        self.top_widget.ded_start.setDate(QDate.currentDate())
        self.top_widget.ded_end.setDate(QDate(QDate.currentDate().year()+1, QDate.currentDate().month(),
                                              QDate.currentDate().day()))

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_activite)
        self.table_widget.clicked.connect(self.modifier_activite)
        self.top_widget.cbx_search.currentTextChanged.connect(self.update_search_placeholder)
        self.top_widget.txt_search.textEdited.connect(self.update_list)
        self.top_widget.cbx_sort.currentIndexChanged.connect(self.update_list)
        self.top_widget.chk_desc.toggled.connect(self.update_list)
        self.top_widget.ded_start.dateChanged.connect(self.update_list)
        self.top_widget.ded_end.dateChanged.connect(self.update_list)

        # Update GUI elements
        self.update_list()
        self.update_search_placeholder(self.top_widget.cbx_search.currentText())

    def update_list(self):
        """
        Affichage de la liste des activites
        """
        print("UPDATE LISTE")
        # Fetch data from database
        query = QSqlQuery(self.database)

        sql = "SELECT activite.id_activite, activite.date, activite.heure_debut, activite.heure_fin, " \
              "activite.date_limite_inscription, categorie_activite.nom, lieu.nom, categorie_activite.prix_membre, " \
              "categorie_activite.prix_non_membre " \
              "FROM activite " \
              "LEFT JOIN categorie_activite ON activite.id_categorie_activite = categorie_activite.id_categorie_activite " \
              "LEFT JOIN lieu ON categorie_activite.id_lieu = lieu.id_lieu "

        # Ajout des options de recherche
        search = self.top_widget.txt_search.text()
        if search != "":
            if self.top_widget.cbx_search.currentText() == "Nom de l'activité":
                sql = sql + "WHERE categorie_activite.nom LIKE '%{}%' ".format(search)
            else:
                sql = sql + "WHERE lieu.nom LIKE '%{}%' ".format(search)

            sql = sql + "AND activite.date >= " + str(self.top_widget.ded_start.date().toJulianDay()) + \
                        " AND activite.date <= " + str(self.top_widget.ded_end.date().toJulianDay()) + " "
        else:
            sql = sql + "WHERE activite.date >= " + str(self.top_widget.ded_start.date().toJulianDay()) + \
                        " AND activite.date <= " + str(self.top_widget.ded_end.date().toJulianDay()) + " "


        # Ajouter les options de tri
        if self.top_widget.cbx_sort.currentText() == "Nom de l'activité":
            sql = sql + "ORDER BY categorie_activite.nom "
        elif self.top_widget.cbx_sort.currentText() == "Lieu" :
            sql = sql + "ORDER BY lieu.nom "
        elif self.top_widget.cbx_sort.currentText() == "Prix régulier":
            sql = sql + "ORDER BY categorie_activite.prix_non_membre "
        elif self.top_widget.cbx_sort.currentText() == "Prix membre":
            sql = sql + "ORDER BY categorie_activite.prix_membre "
        elif self.top_widget.cbx_sort.currentText() == "Date":
            sql = sql + "ORDER BY activite.date "

        # Order du tri
        if self.top_widget.chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "

        query.exec_(sql)

        # Show data in table widget
        self.table_widget.setRowCount(0)

        while query.next():
            self.table_widget.insertRow(self.table_widget.rowCount())
            r = self.table_widget.rowCount() - 1

            self.table_widget.setItem(r, 0, QTableWidgetItem(str(query.value(0))))
            self.table_widget.setItem(r, 1, QTableWidgetItem(str(query.value(5))))
            self.table_widget.setItem(r, 2, QTableWidgetItem(str(query.value(6))))

            prix = "Membre : {0:.2f}$".format(query.value(7)) + "\n" \
                   + "Régulier : {0:.2f}$".format(query.value(8))
            self.table_widget.setItem(r, 3, QTableWidgetItem(prix))

            date_activite = QDate.fromJulianDay(query.value(1)).toString('dd MMM yyyy')
            self.table_widget.setItem(r, 4, QTableWidgetItem(date_activite))

            heure_debut = QTime.fromMSecsSinceStartOfDay(query.value(2)).toString('hh:mm')
            heure_fin = QTime.fromMSecsSinceStartOfDay(query.value(3)).toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.table_widget.setItem(r, 5, QTableWidgetItem(heure))

            date_limite = QDate.fromJulianDay(query.value(4)).toString('dd MMM yyyy')
            self.table_widget.setItem(r, 6, QTableWidgetItem(date_limite))


        self.table_widget.resizeColumnsToContents()

    def modifier_activite(self, index):
        """
        Ouvre le dialog pour modifier une activite
        :param index: Index de la colonne
        """
        id_activite = self.table_widget.item(index.row(), 0).text()
        modifier_activite = ModifierActivite(id_activite, self.database)
        modifier_activite.accepted.connect(self.update_list)
        modifier_activite.exec()

    def update_search_placeholder(self, text):
        """
        Update search placeholder text when combo box item is changed
        :param text:
        """
        self.top_widget.txt_search.clear()
        self.top_widget.txt_search.setPlaceholderText(text)

    def nouvelle_activite(self):
        """
        Ouvrir le dialog pour creer une nouvelle activite
        :return:
        """
        nouvelle_activite = NouvelleActivite(self.database)
        nouvelle_activite.exec()


class CentralWidgetLieux(CentralWidget):
    def __init__(self, database):
        super(CentralWidgetLieux, self).__init__()
        # GUI setup
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_lieux.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Instance variable definition
        self.database = database

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouveau_lieu)

        # Table widget parameters
        self.table_widget.setColumnCount(5)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Adresse", "Ville", "Code Postal"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouveau_lieu)
        self.table_widget.clicked.connect(self.modifier_lieu)
        self.top_widget.cbx_search.currentTextChanged.connect(self.update_search_placeholder)
        self.top_widget.txt_search.textEdited.connect(self.update_list)
        self.top_widget.cbx_sort.currentIndexChanged.connect(self.update_list)
        self.top_widget.chk_desc.toggled.connect(self.update_list)

        # Update GUI elements
        self.update_list()
        self.update_search_placeholder(self.top_widget.cbx_search.currentText())

    def update_search_placeholder(self, text):
        """
        Update search placeholder text when combo box item is changed
        :param text:
        """
        self.top_widget.txt_search.clear()
        self.top_widget.txt_search.setPlaceholderText(text)

    def nouveau_lieu(self):
        """
        Ouvrir le dialog pour créer un nouveau lieu
        """
        lieu = NouveauLieu(self.database)
        lieu.accepted.connect(self.update_list)
        lieu.exec()

    def modifier_lieu(self, index):
        """
        Ouvre le dialog pour modifier un lieu
        :param index: Index de la colonne
        """
        id_lieu = self.table_widget.item(index.row(), 0).text()
        modifier_lieu = ModifierLieu(id_lieu, self.database)
        modifier_lieu.accepted.connect(self.update_list)
        modifier_lieu.exec()

    def update_list(self):
        """
        Affichage de la liste des lieux
        """
        # Fetch data from database
        query = QSqlQuery(self.database)
        sql = "SELECT id_lieu, nom, adresse_1, ville, code_postal from lieu "

        # Ajout des options de recherche
        search = self.top_widget.txt_search.text()
        if search != "":
            if self.top_widget.cbx_search.currentText() == "Nom du lieu":
                sql = sql + "WHERE nom LIKE '%{}%' ".format(search)
            else:
                sql = sql + "WHERE ville LIKE '%{}%' ".format(search)

        # Ajouter les options de tri
        if self.top_widget.cbx_sort.currentText() == "Nom du lieu":
            sql = sql + "ORDER BY nom "
        else:
            sql = sql + "ORDER BY ville "

        # Order du tri
        if self.top_widget.chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "
        query.exec_(sql)

        # Show data in table widget
        self.table_widget.setRowCount(0)

        while query.next():
            self.table_widget.insertRow(self.table_widget.rowCount())
            r = self.table_widget.rowCount() - 1

            self.table_widget.setItem(r, 0, QTableWidgetItem(str(query.value(0))))
            self.table_widget.setItem(r, 1, QTableWidgetItem(str(query.value(1))))
            self.table_widget.setItem(r, 2, QTableWidgetItem(str(query.value(2))))
            self.table_widget.setItem(r, 3, QTableWidgetItem(str(query.value(3))))
            self.table_widget.setItem(r, 4, QTableWidgetItem(str(query.value(4))))

        self.table_widget.resizeColumnsToContents()


class CentralWidgetCategorieActivite(CentralWidget):
    def __init__(self, database):
        super(CentralWidgetCategorieActivite, self).__init__()

        # Instance variable definition
        self.database = database

        # GUI setup
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_categorie_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Table widget parameters
        self.table_widget.setColumnCount(7)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Prix", "Participante", "Responsable", "Type d'activité", "Lieu"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_categorie_activite)
        self.table_widget.clicked.connect(self.modifier_categorie_activite)
        self.top_widget.cbx_search.currentTextChanged.connect(self.update_search_placeholder)
        self.top_widget.txt_search.textEdited.connect(self.update_list)
        self.top_widget.cbx_sort.currentIndexChanged.connect(self.update_list)
        self.top_widget.chk_desc.toggled.connect(self.update_list)

        # Update GUI elements
        self.update_list()
        self.update_search_placeholder(self.top_widget.cbx_search.currentText())

    def update_list(self):
        """
        Affichage de la liste des categories d'activite
        """
        query = QSqlQuery(self.database)

        sql = "SELECT categorie_activite.id_categorie_activite, categorie_activite.nom, categorie_activite.prix_membre, " \
              "categorie_activite.prix_non_membre, " \
              "categorie_activite.participante_minimum, categorie_activite.participante_maximum, " \
              "responsable.prenom, responsable.nom, lieu.nom, type_activite.nom " \
              "FROM categorie_activite " \
              "LEFT JOIN responsable ON categorie_activite.id_responsable = responsable.id_responsable " \
              "LEFT JOIN lieu ON categorie_activite.id_lieu = lieu.id_lieu " \
              "LEFT JOIN type_activite  ON categorie_activite.id_type_activite = type_activite.id_type_activite "
        query.exec_(sql)

        # Ajout des options de recherche
        search = self.top_widget.txt_search.text()
        if search != "":
            if self.top_widget.cbx_search.currentText() == "Nom de la catégorie":
                sql = sql + "WHERE categorie_activite.nom LIKE '%{}%' ".format(search)
            elif self.top_widget.cbx_search.currentText() == "Responsable":
                sql = sql + "WHERE responsable.prenom LIKE '%{0}%' OR responsable.nom LIKE '%{0}%' ".format(search)
            else:
                sql = sql + "WHERE lieu.nom LIKE '%{}%' ".format(search)

        # Ajouter les options de tri
        if self.top_widget.cbx_sort.currentText() == "Nom de la catégorie":
            sql = sql + "ORDER BY categorie_activite.nom "
        elif self.top_widget.cbx_sort.currentText() == "Responsable":
            sql = sql + "ORDER BY responsable.prenom "
        elif self.top_widget.cbx_sort.currentText() == "Lieu":
            sql = sql + "ORDER BY lieu.nom "
        elif self.top_widget.cbx_sort.currentText() == "Prix membre":
            sql = sql + "ORDER BY categorie_activite.prix_membre "
        else:
            sql = sql + "ORDER BY categorie_activite.prix_non_membre "

        # Order du tri
        if self.top_widget.chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "
        query.exec_(sql)

        # Show data in table widget
        self.table_widget.setRowCount(0)

        while query.next():
            self.table_widget.insertRow(self.table_widget.rowCount())
            r = self.table_widget.rowCount() - 1

            self.table_widget.setItem(r, 0, QTableWidgetItem(str(query.value(0))))
            self.table_widget.setItem(r, 1, QTableWidgetItem(str(query.value(1))))

            prix = "Prix membre {0:.2f}: ".format(query.value(2)) + "$" + "\n" \
                   + "Prix non membre : {0:.2f}".format(query.value(3)) + "$"
            self.table_widget.setItem(r, 2, QTableWidgetItem(prix))

            participante = str(query.value(4)) + " - " + str(query.value(5))
            self.table_widget.setItem(r, 3, QTableWidgetItem(participante))

            responsable = str(query.value(6)) + " " + str(query.value(7))
            self.table_widget.setItem(r, 4, QTableWidgetItem(responsable))

            self.table_widget.setItem(r, 5, QTableWidgetItem(str(query.value(8))))
            self.table_widget.setItem(r, 6, QTableWidgetItem(str(query.value(9))))

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

    def update_search_placeholder(self, text):
        """
        Update search placeholder text when combo box item is changed
        :param text:
        """
        self.top_widget.txt_search.clear()
        self.top_widget.txt_search.setPlaceholderText(text)

    def nouvelle_categorie_activite(self):
        """
        Ouvrir le dialog pour créer une nouvelle categorie d'activite
        :return:
        """
        categorie_activite = NouvelleCategorieActivite(self.database)
        categorie_activite.exec()

    def modifier_categorie_activite(self, index):
        """
        Ouvre le dialog pour modifier une categorie d'activite
        :param index: Index de la ligne du tableau
        """
        id_categorie_activite = self.table_widget.item(index.row(), 0).text()
        modifier_categorie_activite = ModifierCategorieActivite(id_categorie_activite, self.database)
        modifier_categorie_activite.accepted.connect(self.update_list)
        modifier_categorie_activite.exec()
