# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QMessageBox
from PyQt5.QtCore import QSettings
from PyQt5.Qt import QApplication
import os
import sqlite3
import pathlib

# Projet import
from participante import NouvelleParticipante
from lieu import Lieu
from activite import Activite
from categorie_activite import CategorieActivite
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
        database = self.check_database_status()
        self.connection = sqlite3.connect(database)

        # Charger l'interface graphique
        self.set_participantes_central_widget()

        # Actions
        self.act_consult_participantes.triggered.connect(self.set_participantes_central_widget)
        self.act_consult_activites.triggered.connect(self.set_activite_central_widget)
        self.act_consult_lieux.triggered.connect(self.set_lieux_central_widget)
        self.act_consult_type_activite.triggered.connect(self.set_categorie_activite_central_widget)
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

        return database

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
        consultation = Consultation(2)
        consultation.exec()

    def consultation_type_activite(self):
        """
        Ouvrir la fenetre de consultation des types d'activite
        """
        consultation = Consultation(1)
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
        central_widget = CentralWidgetParticipantes(self.connection)
        self.setCentralWidget(central_widget)

    def set_activite_central_widget(self):
        """
        Affichage de la liste des activites et des options de tri
        """
        central_widget = CentralWidgetActivite(self.connection)
        self.setCentralWidget(central_widget)

    def set_categorie_activite_central_widget(self):
        """
        Affichage de la liste des type d'activite et des options de tri
        """
        central_widget = CentralWidgetCategorieActivite(self.connection)
        self.setCentralWidget(central_widget)

    def set_lieux_central_widget(self):
        """
        Affichage des lieux et des options de tri
        """
        central_widget = CentralWidgetLieux(self.connection)
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
    def __init__(self, connection):
        super(CentralWidgetParticipantes, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_participantes.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_participante)

        # Instance variable definition
        self.connection = connection

    def nouvelle_participante(self):
        """
        Ouvrir le dialog pour creer une nouvelle participante
        :return:
        """
        nouvelle_participante = NouvelleParticipante(self.connection)
        nouvelle_participante.exec()


class CentralWidgetActivite(CentralWidget):
    def __init__(self, connection):
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
        self.connection = connection

    def nouvelle_activite(self):
        """
        Ouvrir le dialog pour creer une nouvelle activite
        :return:
        """
        activite = Activite()
        activite.setWindowTitle("Nouvelle activité")
        activite.exec()


class CentralWidgetLieux(CentralWidget):
    def __init__(self, connection):
        super(CentralWidgetLieux, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_lieux.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouveau_lieu)

        # Instance variable definition
        self.connection = connection

    def nouveau_lieu(self):
        """
        Ouvrir le dialog pour créer un nouveau lieu
        :return:
        """
        lieu = Lieu()
        lieu.setWindowTitle("Nouveau lieu")
        lieu.exec()


class CentralWidgetCategorieActivite(CentralWidget):
    def __init__(self, connection):
        super(CentralWidgetCategorieActivite, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_categorie_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_categorie_activite)

        # Instance variable definition
        self.connection = connection

    def nouvelle_categorie_activite(self):
        """
        Ouvrir le dialog pour créer une nouvelle categorie d'activite
        :return:
        """
        categorie_activite = CategorieActivite()
        categorie_activite.setWindowTitle("Nouvelle catégorie d'activité")
        categorie_activite.exec()
