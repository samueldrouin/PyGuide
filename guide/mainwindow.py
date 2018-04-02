"""
Module responsable de l'affichage de la fenêtre principale du programme

Les classes de ce module peuvent afficher les informations de la base de donnée et afficher les
fenêtre responsable de les modifier. Elle ne devrait pas pouvoir modifier la base de donnée directement. 

Classes
    MainWindow : Interface de la fenêtre principale
    DockWidgetParticipante : Affichage du DockWidget pour les participantes
    DockWidgetActivite : Affichage du DockWidget pour les activités
    DockWidgetLieu : Affichage du DockWidget pour les lieux
    DockWidgetCategorieActivite :  Affichage du DockWidget pour les catégories d'activité
"""

# Python import
import os
import pathlib
import xml.etree.ElementTree as ET

# PyQt import

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget, QMessageBox, QTableWidgetItem, \
    QAbstractItemView, QHeaderView, QAction, QMenu
from PyQt5.QtCore import QSettings, QDate, QTime
from PyQt5.Qt import QApplication, QDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Projet import
from membre.participante import NouvelleParticipante, ModifierParticipante
from activite.lieu import NouveauLieu, ModifierLieu
from activite.activite import NouvelleActivite, AfficherActivite
from activite.categorie_activite import NouvelleCategorieActivite, ModifierCategorieActivite
from setting import Setting
from consultation import Consultation
from facturation.facturation import Facturation, Inscription
from statistique.statistiques import Statistiques, StatistiquesDialog
from script.interface.selection import SelectionStatistique
from facturation.groupe import Groupe
from script.database import DatabaseError
from script.database import DataProcessing
from script.interface.a_propos import APropos

# Interface import
from interface.mainwindow import Ui_MainWindow
from interface.central_widget.widget_activite import Ui_WidgetActivite
from interface.central_widget.widget_categorie_activite import Ui_WidgetTypeActivite
from interface.central_widget.widget_lieu import Ui_WidgetLieu
from interface.central_widget.widget_participante import Ui_WidgetParticipante

# Resource import 
import resources

# Global constante definition

# Élément affiché
ACTIVITE = 0
CATEGORY_ACTIVITE = 1
LIEU = 2
PARTICIPANTE = 3

# Largeur relative des colonnes des tableaux
FACTOR_COL_NOM = 0.23
FACTOR_COL_ADRESSE = 0.2
FACTOR_COL_COURRIEL = 0.2
FACTOR_COL_TELEPHONE = 0.2

FACTOR_COL_NOM_ACTIVITE = 0.2
FACTOR_COL_LIEU = 0.2
FACTOR_COL_PRIX = 0.15
FACTOR_COL_DATE = 0.15
FACTOR_COL_HEURE = 0.15

FACTOR_COL_PARTICIPANTE = 0.15
FACTOR_COL_RESPONSABLE = 0.15
FACTOR_COL_TYPE_ACTIVITE = 0.15

FACTOR_COL_NOM_LIEU = 0.3
FACTOR_COL_ADRESSE_LIEU = 0.25
FACTOR_COL_VILLE = 0.25


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Interface de la fenêtre principale

    L'interface de la fenêtre principale est généré par une combinaison de trois classes :
                               _                                     _
                               |   --------------                     |
                               |   |            | <- Top Widget       |
                MainWindow ->  |   |------------|    (option de       | <- CentralWidget
                (élément de    |   |            |     tri)            |    (option de tri et
                 QMainWindow)  |_  --------------                    _|     table)
    
    Le CentralWidget varie selon le type d'élément qui doit être affiché

    La connection à la base de donnée est effectuée dans cette classe. La connection n'est pas vérifiée 
    automatiquement ailleur.

    Methodes : 
        read_settings : Lecture des réglages et affichage de l'interface enregistrée dans les réglages
        closeEvent : Enregistre l'état de la fenêtre principale à la fermeture
        afficher_liste_statistique : Afficher la liste des statistiques enregistrées dans une fenêtre de sélection
        ouvrir_statistique : Exécuter un fichier de statistique et afficher le résultat
        verifier_path_statistique : Obtenir le chemin vers le folder contenant les statistiques
        check_database_status : Obtient le chemin vers la base de donnée à partir des réglages
        statistiques : Ouvre le dialog des statistiques
        inscription : Ouvre un dialog pour entrer une nouvelle inscription
        facturation : Ouvre un dialog pour entrer une nouvelle facture
        consultation_responsables : Ouvre le dialog pour consulter les responsables
        consultation_type_activite : Ouvrir le dialog pour consulter les types d'activite
        reglage : Ouvre le dialog des réglages
        groupe : Ouvre le dialog pour entrer un groupe à une activité
        a_propos : Ouvre le dialog qui affiche les informations sur l'application
        resizeEvent : Appelle la fonction responsable de modifier la taille des colonnes lorsque la taille de la fenêtre est modifiée
        resize_table : Ajuster la taille des colonnes à la taille du tableau
        showEvent : Appelle la fonction responsable de modifier la taille des colonnes du tableau lorsque la programme apparait

        afficher_participante : Affichage de la liste des participantes et des options de tri dans la fenêtre principale
        edit_participante : Ouvre le dialog pour modifier une participante
        nouvelle_participante : Ouvre le dialog pour creer une nouvelle participante
        update_liste_participante : Met à jour la liste des participantes lorsque les options de tri sont modifiées

        afficher_activite : Affichage de la liste des activites et des options de tri dans la fenêtre principale
        nouvelle_activite : Ouvre le dialog pour creer une nouvelle activité
        afficher_activite : Ouvre le dialog pour afficher une activité
        update_liste_activite : Met à jour la liste des activités lorsque les options de tri sont modifiées

        afficher_categorie_activite : Affichage de la liste des type d'activite et des options de tri dans la fenêtre principale
        nouvelle_categorie_activite : Affichage de la liste des type d'activite et des options de tri dans la fenêtre principale
        modifier_categorie_activite : Ouvre le dialog pour modifier une catégorie d'activité
        update_liste_categorie_activite : Met à jour la liste des catégories d'activité lorsque les options de tri sont modifiées

        afficher_lieu : Affichage des lieux et des options de tri dans la fenêtre principale
        nouveau_lieu : Ouvre le dialog pour créer un nouveau lieu
        modifier_lieu : Ouvre le dialog pour modifier un lieu
        update_liste_lieu : Met à jour la liste des lieux lorsque les options de tri sont modifiées
    """

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # Connection à la base de données
        self.DATABASE = self.check_database_status()

        # Charger les réglages
        self.read_settings()

        # Enlever la barre de titre du DockWidget
        self.dock_widget.setTitleBarWidget(QWidget())

        # Paramètres du tableau
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Afficher les images des boutons
        self.act_consult_participante.setIcon(QIcon(":/mainwindow/Participante.png"))
        self.act_consult_activite.setIcon(QIcon(":/mainwindow/Activite.png"))
        self.act_consult_lieu.setIcon(QIcon(":/mainwindow/Lieu.png"))
        self.act_consult_categorie_activite.setIcon(QIcon(":/mainwindow/CategorieActivite.png"))
        self.act_inscription.setIcon(QIcon(":/mainwindow/Inscription.png"))
        self.act_facturation.setIcon(QIcon(":/mainwindow/Facture.png"))
        self.act_groupe.setIcon(QIcon(":/mainwindow/Groupe.png"))

        # Actions
        self.act_consult_participante.triggered.connect(self.afficher_participante)
        self.act_consult_activite.triggered.connect(self.afficher_activite)
        self.act_consult_lieu.triggered.connect(self.afficher_lieu)
        self.act_consult_categorie_activite.triggered.connect(self.afficher_categorie_activite)
        self.act_about.triggered.connect(self.a_propos)
        self.act_about_qt.triggered.connect(QApplication.aboutQt)
        self.act_reglage.triggered.connect(self.reglage)
        self.act_type_activite.triggered.connect(self.consultation_type_activite)
        self.act_responsables.triggered.connect(self.consultation_responsables)
        self.act_inscription.triggered.connect(self.inscription)
        self.act_facturation.triggered.connect(self.facturation)
        self.act_groupe.triggered.connect(self.groupe)
        self.act_statistiques.triggered.connect(self.statistiques)
        self.act_enregistre.triggered.connect(self.afficher_liste_statistique)

    def read_settings(self):
        """
        Lecture des réglages et affichage de l'interface enregistrée dans les réglages
        """
        # Restaurer la taille de la fenêtre
        settings = QSettings("Samuel Drouin", "GUIDE-CFR")
        self.restoreGeometry(settings.value("MainWindow/Geometry"))

        # Restaurer le central widget
        if settings.value("MainWindow/CentralWidget") == ACTIVITE:
            self.afficher_activite()
        elif settings.value("MainWindow/CentralWidget") == CATEGORY_ACTIVITE:
            self.afficher_categorie_activite()
        elif settings.value("MainWindow/CentralWidget") == LIEU:
            self.afficher_lieu()
        else:
            self.afficher_participante()

    def closeEvent(self, QCloseEvent):
        """
        Enregistre l'état de la fenêtre principale à la fermeture
        """
        settings = QSettings("Samuel Drouin", "GUIDE-CFR")
        settings.setValue("MainWindow/Geometry", self.saveGeometry())

        if isinstance(self.dock_widget.widget(), DockWidgetActivite):
            settings.setValue("MainWindow/CentralWidget", ACTIVITE)
        elif isinstance(self.dock_widget.widget(), DockWidgetCategorieActivite):
            settings.setValue("MainWindow/CentralWidget", CATEGORY_ACTIVITE)
        elif isinstance(self.dock_widget.widget(), DockWidgetLieu):
            settings.setValue("MainWindow/CentralWidget", LIEU)
        elif isinstance(self.dock_widget.widget(), DockWidgetParticipante):
            settings.setValue("MainWindow/CentralWidget", PARTICIPANTE)
        
        return super().closeEvent(QCloseEvent)

    def resizeEvent(self, event):
        """
        Appelle la fonction responsable de modifier la taille des colonnes du tableau lorsque la taille de
        la fenêtre est modifiée
        """
        self.resize_table()
        return super().resizeEvent(event)

    def showEvent(self, QShowEvent):
        """
        Appelle la fonction responsable de modifier la taille des colonnes du tableau lorsque la programme apparait

        Cette fonction est nécessaire pour que l'affichage de la taille des colonnes soit optimale à l'ouverture. 
        """
        self.resize_table()
        return super().showEvent(QShowEvent)

    def resize_table(self):
        """
        Ajuster la taille des colonnes à la taille du tableau
        """
        # Taille du tableau
        width = self.table_widget.width()

        # Régler la taille des colonnes
        if isinstance(self.dock_widget.widget(), DockWidgetActivite):
            self.table_widget.setColumnWidth(1, FACTOR_COL_NOM_ACTIVITE*width)
            self.table_widget.setColumnWidth(2, FACTOR_COL_LIEU*width)
            self.table_widget.setColumnWidth(3, FACTOR_COL_PRIX*width)
            self.table_widget.setColumnWidth(4, FACTOR_COL_DATE*width)
            self.table_widget.setColumnWidth(5, FACTOR_COL_HEURE*width)
        elif isinstance(self.dock_widget.widget(), DockWidgetCategorieActivite):
            self.table_widget.setColumnWidth(1, FACTOR_COL_NOM_ACTIVITE*width)
            self.table_widget.setColumnWidth(2, FACTOR_COL_PRIX*width)
            self.table_widget.setColumnWidth(3, FACTOR_COL_PARTICIPANTE*width)
            self.table_widget.setColumnWidth(4, FACTOR_COL_RESPONSABLE*width)
            self.table_widget.setColumnWidth(5, FACTOR_COL_TYPE_ACTIVITE*width)
        elif isinstance(self.dock_widget.widget(), DockWidgetLieu):
            self.table_widget.setColumnWidth(1, FACTOR_COL_NOM_LIEU*width)
            self.table_widget.setColumnWidth(2, FACTOR_COL_ADRESSE_LIEU*width)
            self.table_widget.setColumnWidth(3, FACTOR_COL_VILLE*width)
        elif isinstance(self.dock_widget.widget(), DockWidgetParticipante):
            self.table_widget.setColumnWidth(1, FACTOR_COL_NOM*width)
            self.table_widget.setColumnWidth(2, FACTOR_COL_ADRESSE*width)
            self.table_widget.setColumnWidth(3, FACTOR_COL_COURRIEL*width)
            self.table_widget.setColumnWidth(4, FACTOR_COL_TELEPHONE*width)

        # Ajouter la dernier colonne pour prendre tout l'espace restant
        self.table_widget.horizontalHeader().setStretchLastSection(True)

    def afficher_liste_statistique(self):
        """
        Afficher la liste des statistiques enregistrées dans une fenêtre de sélection
        """
        # Obtenir le dossier ou les fichiers statistique sont enregistrée
        statistique = self.verifier_path_statistique()

        # Obtenir la liste des fichiers statistique
        liste_statistique = []
        for file in os.listdir(statistique):
            statname = os.path.splitext(file)[0]

            dict_stat = {}
            dict_stat['fichier'] = file
            dict_stat['nom'] = statname

            liste_statistique.append(dict_stat)

        # Afficher la liste des statistiques à l'utilisation
        selection = SelectionStatistique(liste_statistique)
        selection.setWindowTitle("Statistique")
        if selection.exec() == QDialog.Accepted:
            nom = selection.get_value()
            path = os.path.join(statistique, nom)
            self.ouvrir_statistique(path)

    def ouvrir_statistique(self, path):
        """
        Exécuter un fichier de statistique et afficher le résultat

        Argument :
            path : Chemin du fichier de statistique sélectionné
        """
        # Préparer le contenu du fichier XML
        tree = ET.parse(path)
        stat = tree.getroot()

        sql = stat.find('sql').text
        type = stat.find('output').text

        # Exécuter la statistique
        statistiques = Statistiques(self.DATABASE)
        if type == "csv":
            statistiques.afficher_csv(sql)
        else:
            statistiques.afficher_pdf(sql)

    def verifier_path_statistique(self):
        """
        Obtenir le chemin vers le folder contenant les statistiques

        S'il n'en existe pas, le créer et enregistrer le chemin dans les réglages

        Return :
            Chemin vers la folder des statistiques
        """
        # Obtenir le chemin dans les réglages
        settings = QSettings("Samuel Drouin", "GUIDE-CFR")
        statistique = settings.value("Statistique")

        # Vérifier s'il existe une valeur
        if not statistique:
            # Créer le dossier et l'ajouter aux statistiques si aucune valeur n'est entrée
            statistique = str(os.path.join(pathlib.Path.home(), 'Documents', 'GUIDE-CFR', 'Statistiques'))
            settings.setValue("Statistique", statistique)
        else:
            # Vérifier si le dossier existe
            if not pathlib.Path(statistique).is_dir():
                # Créer le dossier et l'ajouter aux statistiques s'il n'existe pas
                statistique = str(os.path.join(pathlib.Path.home(), 'Documents', 'GUIDE-CFR', 'Statistiques'))
                settings.setValue("Statistique", statistique)

        return statistique

    def check_database_status(self):
        """
        Obtient le chemin vers la base de donnée à partir des réglages

        Return :
            Path to database
        """
        settings = QSettings("Samuel Drouin", "GUIDE-CFR")
        database = settings.value("Database")

        # Vérifier si le chemin vers la base de donnée existe 
        # et si le fichier existe
        if not database or not pathlib.Path(database).is_file():
            # Indique à l'utilisateur que la base de donnée n'existe pas et
            # qu'elle doit être créée
            ret = DatabaseError.aucune_database()

            # Ouvre les réglages pour entrer le chemin vers la base de donnée
            if ret == QMessageBox.Ok:
                setting = Setting()
                setting.accepted.connect(self.check_database_status)
                setting.exec()
        else:
            # Ajouter la base de donnée
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName(database)

            # Vérifier si la base de donnée ouvre
            if not db.open():
                # Avertit l'utilisateur d'une erreur de connection et ferme le programme
                DatabaseError.sql_error_handler(db.lastError())
                self.close()
            else:
                # Si la base de donnée est ouverte, retourne le chemin vers la base de donnée
                return db

    def statistiques(self):
        """
        Ouvre le dialog des statistiques
        """
        statistiques = StatistiquesDialog(self.DATABASE)
        statistiques.exec()

    def inscription(self):
        """
        Ouvre un dialog pour entrer une nouvelle inscription
        """
        inscription = Inscription(self.DATABASE)
        inscription.exec()

    def facturation(self):
        """
        Ouvre un dialog pour entrer une nouvelle facture
        """
        facturation = Facturation(self.DATABASE)
        facturation.exec()

    def consultation_responsables(self):
        """
        Ouvre le dialog pour consulter les responsables
        """
        consultation = Consultation(2, self.DATABASE)
        consultation.exec()

    def consultation_type_activite(self):
        """
        Ouvrir le dialog pour consulter les types d'activite
        """
        consultation = Consultation(1, self.DATABASE)
        consultation.exec()

    def reglage(self):
        """
        Ouvre le dialog des réglages
        """
        setting = Setting()
        setting.exec()

    def groupe(self):
        """
        Ouvre le dialog pour entrer un groupe à une activité
        """
        groupe = Groupe(self.DATABASE)
        groupe.exec()

    def a_propos(self):
        """
        Ouvre le dialog qui affiche les informations sur l'application
        """
        a_propos = APropos()
        a_propos.exec()

    def afficher_participante(self):
        """
        Affichage de la liste des participantes et des options de tri dans la fenêtre principale

        Toutes les connections entre le DockWidget et le tableau sont effectuées dans cette fonction
        """
        # Affichage du DockWidget
        self.dock_widget.setWidget(DockWidgetParticipante())

        # Vider le table widget
        self.table_widget.setRowCount(0)

        # Afficher l'interface du table widget
        self.table_widget.setColumnCount(6)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Ville", "Courriel", "Téléphone", "Numéro \n de membre"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.NoSelection)
        self.table_widget.setAlternatingRowColors(True)

        # Slots
        self.dock_widget.widget().btn_add.clicked.connect(self.nouvelle_participante)
        self.table_widget.clicked.connect(self.edit_participante)
        self.dock_widget.widget().txt_search.textEdited.connect(self.update_liste_participante)
        self.dock_widget.widget().cbx_sort.currentIndexChanged.connect(self.update_liste_participante)
        self.dock_widget.widget().chk_membre.toggled.connect(self.update_liste_participante)
        self.dock_widget.widget().chk_desc.toggled.connect(self.update_liste_participante)

        # Afficher la liste
        self.update_liste_participante()
        self.resize_table()

    def edit_participante(self, index):
        """
        Ouvre le dialog pour modifier une participante

        Argument :
            index : Index de la colonne
        """
        participante_id = self.table_widget.item(index.row(), 0).text()
        modifier_participante = ModifierParticipante(participante_id, self.DATABASE)
        modifier_participante.accepted.connect(self.update_liste_participante)
        modifier_participante.exec()

    def nouvelle_participante(self):
        """
        Ouvre le dialog pour creer une nouvelle participante
        """
        nouvelle_participante = NouvelleParticipante(self.DATABASE)
        nouvelle_participante.accepted.connect(self.update_liste_participante)
        nouvelle_participante.exec()

    def update_liste_participante(self):
        """
        Met à jour la liste des participantes lorsque les options de tri sont modifiées
        """
        # Obtenir la liste des participantes dans la base de donnée

        # Requête principale
        sql = "SELECT "\
                "participante.id_participante, "\
                "participante.prenom, participante.nom, " \
                "participante.ville, "\
                "participante.courriel, "\
                "participante.telephone_1, " \
                "participante.poste_telephone_1, "\
                "membre.numero_membre "\
                "FROM "\
                "participante " \

        # Sélection des membres seulement
        if self.dock_widget.widget().chk_membre.isChecked():
            sql = sql + "INNER JOIN membre "\
                            "ON membre.id_participante = participante.id_participante "
        # Sélection de tout les membres et les participantes
        else:
            sql = sql + "LEFT JOIN membre "\
                            "ON membre.id_participante = participante.id_participante "

        # Ajout des options de recherche
        search = self.dock_widget.widget().txt_search.text()
        if search != "":
            if self.dock_widget.widget().cbx_search.currentText() == "Prénom":
                sql = sql + "WHERE participante.prenom LIKE '{}%' ".format(search)
            elif self.dock_widget.widget().cbx_search.currentText() == "Nom":
                sql = sql + "WHERE participante.nom LIKE '{}%' ".format(search)
            elif self.dock_widget.widget().cbx_search.currentText() == "Ville":
                sql = sql + "WHERE participante.ville LIKE '{}%' ".format(search)
            else:
                sql = sql + "WHERE participante.telephone_1 LIKE '{}%' ".format(DataProcessing.check_phone_number(search))

        # Ajouter les options de tri
        if self.dock_widget.widget().cbx_sort.currentText() == "Prénom":
            sql = sql + "ORDER BY participante.prenom "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Nom":
            sql = sql + "ORDER BY participante.nom "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Ville":
            sql = sql + "ORDER BY participante.ville "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Numéro de téléphone":
            sql = sql + "ORDER BY participante.telephone_1 "
        else:
            sql = sql + "ORDER BY membre.numero_membre "

        # Order du tri
        if self.dock_widget.widget().chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "

        # Exécution de la requête
        query = QSqlQuery(self.DATABASE)
        query.exec_(sql)

        # Affichage d'un message d'erreur si la requete echoue
        DatabaseError.sql_error_handler(query.lastError())

        # Vider la table des éléments existants
        self.table_widget.setRowCount(0)

        # Ajouter les éléments de la requête à la table des participantes
        while query.next():
            self.table_widget.insertRow(self.table_widget.rowCount())
            r = self.table_widget.rowCount() - 1

            self.table_widget.setItem(r, 0, QTableWidgetItem(str(query.value(0))))

            if self.dock_widget.widget().cbx_sort.currentText() == "Prénom":
                if not query.value(2) == "":
                    nom = str(query.value(1)) + " " + str(query.value(2))
                else:
                    nom = str(query.value(1))
            else:
                if not query.value(2) == "":
                    nom = str(query.value(2)) + ", " + str(query.value(1))
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

    def afficher_activite(self):
        """
        Affichage de la liste des activites et des options de tri dans la fenêtre principale

        Toutes les connections entre le DockWidget et le tableau sont effectuées dans cette fonction
        """
        # Affichage du DockWidget
        self.dock_widget.setWidget(DockWidgetActivite())

        # Vider le table widget
        self.table_widget.setRowCount(0)

        # Table widget parameters
        self.table_widget.setColumnCount(7)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Lieu", "Prix", "Date", "Heure", "Date limite \n d'inscription"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # Slots
        self.dock_widget.widget().btn_add.clicked.connect(self.nouvelle_activite)
        self.dock_widget.widget().txt_search.textEdited.connect(self.update_liste_activite)
        self.dock_widget.widget().cbx_sort.currentIndexChanged.connect(self.update_liste_activite)
        self.dock_widget.widget().chk_desc.toggled.connect(self.update_liste_activite)
        self.dock_widget.widget().ded_start.dateChanged.connect(self.update_liste_activite)
        self.dock_widget.widget().ded_end.dateChanged.connect(self.update_liste_activite)
        self.table_widget.clicked.connect(self.informations_activite)

        # Update GUI elements
        self.update_liste_activite()
        self.resize_table()

    def nouvelle_activite(self):
        """
        Ouvre le dialog pour creer une nouvelle activité
        """
        nouvelle_activite = NouvelleActivite(self.DATABASE)
        nouvelle_activite.accepted.connect(self.update_liste_activite)
        nouvelle_activite.exec()

    def informations_activite(self, index):
        """
        Ouvre le dialog pour afficher une activité

        Argument :
            index : Index de la colonne
        """
        id_activite = self.table_widget.item(index.row(), 0).text()
        afficher = AfficherActivite(self.DATABASE, id_activite)
        afficher.accepted.connect(self.update_liste_activite)
        afficher.exec()

    def update_liste_activite(self):
        """
        Met à jour la liste des activités lorsque les options de tri sont modifiées
        """
        # Fetch data from database
        query = QSqlQuery(self.DATABASE)

        sql = "SELECT "\
                "activite.id_activite, "\
                "activite.date, "\
                "activite.heure_debut, "\
                "activite.heure_fin, " \
                "activite.date_limite_inscription, "\
                "categorie_activite.nom, "\
                "lieu.nom, " \
                "categorie_activite.prix_membre, "\
                "categorie_activite.prix_non_membre " \
              "FROM activite " \
              "LEFT JOIN categorie_activite "\
                "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite " \
              "LEFT JOIN lieu ON "\
                "categorie_activite.id_lieu = lieu.id_lieu "

        # Ajout des options de recherche
        search = self.dock_widget.widget().txt_search.text()
        if search != "":
            if self.dock_widget.widget().cbx_search.currentText() == "Nom de l'activité":
                sql = sql + "WHERE categorie_activite.nom LIKE '%{}%' ".format(search)
            else:
                sql = sql + "WHERE lieu.nom LIKE '%{}%' ".format(search)

            sql = sql + "AND activite.date >= " + \
                        str(self.dock_widget.widget().ded_start.date().toString('yyyy-MM-dd')) + \
                        " AND activite.date <= " + \
                        str(self.dock_widget.widget().ded_end.date().toString('yyyy-MM-dd')) + " " + \
                        " AND activite.status = 1 "
        else:
            sql = sql + "WHERE activite.date >= " + \
                        str(self.dock_widget.widget().ded_start.date().toString('yyyy-MM-dd')) + \
                        " AND activite.date <= " + \
                        str(self.dock_widget.widget().ded_end.date().toString('yyyy-MM-dd')) + " " + \
                        " AND activite.status = 1 "

        # Ajouter les options de tri
        if self.dock_widget.widget().cbx_sort.currentText() == "Nom de l'activité":
            sql = sql + "ORDER BY categorie_activite.nom "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Lieu":
            sql = sql + "ORDER BY lieu.nom "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Prix régulier":
            sql = sql + "ORDER BY categorie_activite.prix_non_membre "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Prix membre":
            sql = sql + "ORDER BY categorie_activite.prix_membre "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Date":
            sql = sql + "ORDER BY activite.date "

        # Order du tri
        if self.dock_widget.widget().chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "

        query.exec_(sql)

        # Affichage d'un message d'erreur si la requete echoue
        DatabaseError.sql_error_handler(query.lastError())

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

            date_activite = QDate.fromString(query.value(1), 'yyyy-MM-dd').toString('dd MMM yyyy')
            self.table_widget.setItem(r, 4, QTableWidgetItem(date_activite))

            heure_debut = QTime.fromString(query.value(2), 'HH:mm').toString('hh:mm')
            heure_fin = QTime.fromString(query.value(3), 'HH:mm').toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.table_widget.setItem(r, 5, QTableWidgetItem(heure))

            date_limite = QDate.fromString(query.value(4), 'yyyy-MM-dd').toString('dd MMM yyyy')
            self.table_widget.setItem(r, 6, QTableWidgetItem(date_limite))

    def afficher_categorie_activite(self):
        """
        Affichage de la liste des type d'activite et des options de tri dans la fenêtre principale
        """
        # Affichage du DockWidget
        self.dock_widget.setWidget(DockWidgetCategorieActivite())

        # Table widget parameters
        self.table_widget.setColumnCount(7)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Prix", "Participante", "Responsable", "Type d'activité", "Lieu"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        # Slots
        self.dock_widget.widget().btn_add.clicked.connect(self.nouvelle_categorie_activite)
        self.table_widget.clicked.connect(self.modifier_categorie_activite)
        self.dock_widget.widget().txt_search.textEdited.connect(self.update_liste_categorie_activite)
        self.dock_widget.widget().cbx_sort.currentIndexChanged.connect(self.update_liste_categorie_activite)
        self.dock_widget.widget().chk_desc.toggled.connect(self.update_liste_categorie_activite)

        # Update GUI elements
        self.update_liste_categorie_activite()
        self.resize_table()

    def nouvelle_categorie_activite(self):
        """
        Ouvre le dialog pour créer une nouvelle catégorie d'activité
        """
        categorie_activite = NouvelleCategorieActivite(self.DATABASE)
        categorie_activite.accepted.connect(self.update_liste_categorie_activite)
        categorie_activite.exec()

    def modifier_categorie_activite(self, index):
        """
        Ouvre le dialog pour modifier une catégorie d'activité

        Argument :
            index : Index de la colonne
        """
        id_categorie_activite = self.table_widget.item(index.row(), 0).text()
        modifier_categorie_activite = ModifierCategorieActivite(id_categorie_activite, 
                                                                self.DATABASE)
        modifier_categorie_activite.accepted.connect(self.update_liste_categorie_activite)
        modifier_categorie_activite.exec()

    def update_liste_categorie_activite(self):
        """
        Met à jour la liste des catégories d'activité lorsque les options de tri sont modifiées
        """
        query = QSqlQuery(self.DATABASE)

        sql = "SELECT "\
                "categorie_activite.id_categorie_activite, "\
                "categorie_activite.nom, " \
                "categorie_activite.prix_membre, "\
                "categorie_activite.prix_non_membre, " \
                "categorie_activite.participante_minimum, "\
                "categorie_activite.participante_maximum, " \
                "responsable.prenom, "\
                "responsable.nom, "\
                "lieu.nom, "\
                "type_activite.nom " \
              "FROM "\
                "categorie_activite " \
              "LEFT JOIN responsable "\
                "ON categorie_activite.id_responsable = responsable.id_responsable " \
              "LEFT JOIN lieu ON "\
                "categorie_activite.id_lieu = lieu.id_lieu " \
              "LEFT JOIN type_activite "\
                "ON categorie_activite.id_type_activite = type_activite.id_type_activite "

        # Ajout des options de recherche
        search = self.dock_widget.widget().txt_search.text()
        if search != "":
            if self.dock_widget.widget().cbx_search.currentText() == "Nom de la catégorie":
                sql = sql + "WHERE categorie_activite.nom LIKE '%{}%' ".format(search)
            elif self.dock_widget.widget().cbx_search.currentText() == "Responsable":
                sql = sql + "WHERE responsable.prenom LIKE '%{0}%' " \
                            "OR responsable.nom LIKE '%{0}%' ".format(search)
            else:
                sql = sql + "WHERE lieu.nom LIKE '%{}%' ".format(search)

        # Ajouter les options de tri
        if self.dock_widget.widget().cbx_sort.currentText() == "Nom de la catégorie":
            sql = sql + "ORDER BY categorie_activite.nom "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Responsable":
            sql = sql + "ORDER BY responsable.prenom "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Lieu":
            sql = sql + "ORDER BY lieu.nom "
        elif self.dock_widget.widget().cbx_sort.currentText() == "Prix membre":
            sql = sql + "ORDER BY categorie_activite.prix_membre "
        else:
            sql = sql + "ORDER BY categorie_activite.prix_non_membre "

        # Order du tri
        if self.dock_widget.widget().chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "
        query.exec_(sql)

        # Affichage d'un message d'erreur si la requete echoue
        DatabaseError.sql_error_handler(query.lastError())

        # Show data in table widget
        self.table_widget.setRowCount(0)

        while query.next():
            self.table_widget.insertRow(self.table_widget.rowCount())
            r = self.table_widget.rowCount() - 1

            self.table_widget.setItem(r, 0, QTableWidgetItem(str(query.value(0))))
            self.table_widget.setItem(r, 1, QTableWidgetItem(str(query.value(1))))

            prix = "Membre {0:.2f}".format(query.value(2)) + "$" + "\n" \
                   + "Régulier : {0:.2f}".format(query.value(3)) + "$"
            self.table_widget.setItem(r, 2, QTableWidgetItem(prix))

            participante = str(query.value(4)) + " - " + str(query.value(5))
            self.table_widget.setItem(r, 3, QTableWidgetItem(participante))

            responsable = str(query.value(6)) + " " + str(query.value(7))
            self.table_widget.setItem(r, 4, QTableWidgetItem(responsable))

            self.table_widget.setItem(r, 5, QTableWidgetItem(str(query.value(8))))
            self.table_widget.setItem(r, 6, QTableWidgetItem(str(query.value(9))))

    def afficher_lieu(self):
        """
        Affichage des lieux et des options de tri dans la fenêtre principale
        """
        # Affichage du DockWidget
        self.dock_widget.setWidget(DockWidgetLieu())

        # Table widget parameters
        self.table_widget.setColumnCount(5)
        self.table_widget.setColumnHidden(0, True)
        headers = ["Index", "Nom", "Adresse", "Ville", "Code Postal"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        # Slots
        self.dock_widget.widget().btn_add.clicked.connect(self.nouveau_lieu)
        self.table_widget.clicked.connect(self.modifier_lieu)
        self.dock_widget.widget().txt_search.textEdited.connect(self.update_liste_lieu)
        self.dock_widget.widget().cbx_sort.currentIndexChanged.connect(self.update_liste_lieu)
        self.dock_widget.widget().chk_desc.toggled.connect(self.update_liste_lieu)

        # Update GUI elements
        self.update_liste_lieu()
        self.resize_table()

    def nouveau_lieu(self):
        """
        Ouvre le dialog pour créer un nouveau lieu
        """
        lieu = NouveauLieu(self.DATABASE)
        lieu.accepted.connect(self.update_liste_lieu)
        lieu.exec()

    def modifier_lieu(self, index):
        """
        Ouvre le dialog pour modifier un lieu

        Argument :
            index : Index de la colonne
        """
        id_lieu = self.table_widget.item(index.row(), 0).text()
        modifier_lieu = ModifierLieu(id_lieu, self.DATABASE)
        modifier_lieu.accepted.connect(self.update_liste_lieu)
        modifier_lieu.exec()

    def update_liste_lieu(self):
        """
        Met à jour la liste des lieux lorsque les options de tri sont modifiées
        """
        # Fetch data from database
        query = QSqlQuery(self.DATABASE)
        sql = "SELECT "\
                "id_lieu, "\
                "nom, "\
                "adresse_1, "\
                "ville, "\
                "code_postal "\
              "FROM "\
                "lieu "

        # Ajout des options de recherche
        search = self.dock_widget.widget().txt_search.text()
        if search != "":
            if self.dock_widget.widget().cbx_search.currentText() == "Nom du lieu":
                sql = sql + "WHERE nom LIKE '%{}%' ".format(search)
            else:
                sql = sql + "WHERE ville LIKE '%{}%' ".format(search)

        # Ajouter les options de tri
        if self.dock_widget.widget().cbx_sort.currentText() == "Nom du lieu":
            sql = sql + "ORDER BY nom "
        else:
            sql = sql + "ORDER BY ville "

        # Order du tri
        if self.dock_widget.widget().chk_desc.isChecked():
            sql = sql + "DESC "
        else:
            sql = sql + "ASC "
        query.exec_(sql)

        # Affichage d'un message d'erreur si la requete echoue
        DatabaseError.sql_error_handler(query.lastError())

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


class DockWidgetParticipante(QWidget, Ui_WidgetParticipante):
    """
    Affichage du DockWidget pour les participantes

    Méthodes :
        update_search_placeholder : Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Slots
        self.cbx_search.currentTextChanged.connect(self.update_search_placeholder)

        # Afficher le placeholder pour le texte de recherche
        self.update_search_placeholder(self.cbx_search.currentText())

    def update_search_placeholder(self, text):
        """
        Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change

        Arguments : 
            text : Texte sélectionné dans le ComboBox
        """
        self.txt_search.clear()
        self.txt_search.setPlaceholderText(text)


class DockWidgetActivite(QWidget, Ui_WidgetActivite):
    """
    Affichage du DockWidget pour les activités

    Méthodes :
        update_search_placeholder : Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Affichage de la date par defaut
        self.ded_start.setDate(QDate.currentDate())
        self.ded_end.setDate(QDate(QDate.currentDate().year()+1, QDate.currentDate().month(),
                                              QDate.currentDate().day()))

        # Slots
        self.cbx_search.currentTextChanged.connect(self.update_search_placeholder)

        # Afficher le placeholder pour le texte de recherche
        self.update_search_placeholder(self.cbx_search.currentText())

    def update_search_placeholder(self, text):
        """
        Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change

        Arguments : 
            text : Texte sélectionné dans le ComboBox
        """
        self.txt_search.clear()
        self.txt_search.setPlaceholderText(text)

class DockWidgetLieu(QWidget, Ui_WidgetLieu):
    """
    Affichage du DockWidget pour les lieux

    Méthodes :
        update_search_placeholder : Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Slots
        self.cbx_search.currentTextChanged.connect(self.update_search_placeholder)

        # Afficher le placeholder pour le texte de recherche
        self.update_search_placeholder(self.cbx_search.currentText())

    def update_search_placeholder(self, text):
        """
        Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change

        Arguments : 
            text : Texte sélectionné dans le ComboBox
        """
        self.txt_search.clear()
        self.txt_search.setPlaceholderText(text)


class DockWidgetCategorieActivite(QWidget, Ui_WidgetTypeActivite):
    """
    Affichage du DockWidget pour les catégories d'activité

    Méthodes :
        update_search_placeholder : Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Slots
        self.cbx_search.currentTextChanged.connect(self.update_search_placeholder)

        # Afficher le placeholder pour le texte de recherche
        self.update_search_placeholder(self.cbx_search.currentText())

    def update_search_placeholder(self, text):
        """
        Met à jour le placeholder text de la recherche lorsque l'item du ComboBox change

        Arguments : 
            text : Texte sélectionné dans le ComboBox
        """
        self.txt_search.clear()
        self.txt_search.setPlaceholderText(text)
