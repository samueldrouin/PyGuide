#This file is part of PyGuide.
#
#PyGuide is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#PyGuide is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with PyGuide.  If not, see <http://www.gnu.org/licenses/>.

# Python import
import os
from pathlib import Path
import errno

# PyQt import
from PyQt5.QtWidgets import QWizard, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QDialog
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Project import
from interface.ui_preparation_wizard import Ui_PreparationWizard
from script.interface import validator
from script.data import file_error
from script.database import database_error

# Définition des ID des pages
PAGE_DESCRIPTION = 0
PAGE_SELECTION = 1
PAGE_INFORMATIONS = 2
PAGE_CONTACT = 3
PAGE_MODULE = 4
PAGE_FIN = 5

# Définition des chemins par défaut
PATH_STATS = str(os.path.join(Path.home(), 'Documents', 'GUIDE', 'Statistics'))
PATH_DB = str(os.path.join(Path.home(), 'Documents', 'GUIDE', 'Database'))

# Définition des requêtes pour créer les tables
QUERY_GUIDE = "\
CREATE TABLE guide ( \
    module  INTEGER NOT NULL \
                    UNIQUE, \
    version INTEGER NOT NULL \
)"
VERSION_GUIDE = 2
MODULE_GUIDE = 0
GUIDE = {'query' : QUERY_GUIDE, 'version' : VERSION_GUIDE, 'module' : MODULE_GUIDE}

QUERY_ACTIVITE = " \
CREATE TABLE activite ( \
    id_activite             INTEGER, \
    id_categorie_activite   INTEGER NOT NULL, \
    date                    INTEGER NOT NULL, \
    heure_debut             INTEGER NOT NULL, \
    heure_fin               INTEGER NOT NULL, \
    date_limite_inscription INTEGER NOT NULL, \
    status                  INTEGER NOT NULL \
                                    DEFAULT (1), \
    PRIMARY KEY ( \
        id_activite \
    ) \
)"
VERSION_ACTIVITE = 1
MODULE_ACTIVITE = 1
ACTIVITE = {'query' : QUERY_ACTIVITE, 'version' : VERSION_ACTIVITE, 'module' : MODULE_ACTIVITE}

QUERY_ARTICLE = " \
CREATE TABLE article ( \
    id_article  INTEGER, \
    id_facture  INTEGER, \
    id_activite INTEGER REFERENCES activite (id_activite) ON DELETE RESTRICT \
                                                          ON UPDATE CASCADE \
                        NOT NULL, \
    prix        REAL, \
    description TEXT, \
    PRIMARY KEY ( \
        id_article \
    ), \
    FOREIGN KEY ( \
        id_facture \
    ) \
    REFERENCES facture (id_facture)  \
)"
VERSION_ARTICLE = 1
MODULE_ARTICLE = 2
ARTICLE = {'query' : QUERY_ARTICLE, 'version' : VERSION_ARTICLE, 'module' : MODULE_ARTICLE}

QUERY_CATEGORIE_ACTIVITE = "\
CREATE TABLE categorie_activite ( \
    id_categorie_activite INTEGER PRIMARY KEY, \
    nom                   TEXT    NOT NULL \
                                  UNIQUE, \
    prix_membre           REAL    DEFAULT (0) \
                                  NOT NULL, \
    prix_non_membre       REAL    DEFAULT (0) \
                                  NOT NULL, \
    participante_minimum  INTEGER DEFAULT (0) \
                                  NOT NULL, \
    participante_maximum  INTEGER NOT NULL \
                                  DEFAULT (0), \
    id_responsable        INTEGER NOT NULL \
                                  REFERENCES responsable (id_responsable) ON DELETE RESTRICT \
                                                                          ON UPDATE CASCADE, \
    id_type_activite      INTEGER REFERENCES type_activite (id_type_activite) ON DELETE RESTRICT \
                                                                              ON UPDATE CASCADE \
                                  NOT NULL, \
    id_lieu               INTEGER REFERENCES lieu (id_lieu) ON DELETE RESTRICT \
                                                            ON UPDATE CASCADE \
                                  NOT NULL \
)"
VERSION_CATEGORIE_ACTIVITE = 1
MODULE_CATEGORIE_ACTIVITE = 3
CATEGORIE_ACTIVITE = {'query' : QUERY_CATEGORIE_ACTIVITE, 'version' : VERSION_CATEGORIE_ACTIVITE, 'module' : MODULE_CATEGORIE_ACTIVITE}

QUERY_FACTURE = "\
CREATE TABLE facture ( \
    id_facture      INTEGER  PRIMARY KEY AUTOINCREMENT, \
    date            DATETIME DEFAULT (datetime('now', 'localtime') ), \
    numero_recu     TEXT, \
    id_participante INTEGER  NOT NULL, \
    total           REAL, \
    FOREIGN KEY ( \
        id_participante \
    ) \
    REFERENCES participante (id_participante) ON DELETE RESTRICT \
                                              ON UPDATE CASCADE \
)"
VERSION_FACTURE = 1
MODULE_FACTURE = 4
FACTURE = {'query' : QUERY_FACTURE, 'version' : VERSION_FACTURE, 'module' : MODULE_FACTURE}

QUERY_GROUPE = "\
CREATE TABLE groupe ( \
    id_groupe   INTEGER PRIMARY KEY, \
    id_activite INTEGER REFERENCES activite (id_activite) ON DELETE RESTRICT \
                                                          ON UPDATE CASCADE \
                        NOT NULL \
                        UNIQUE, \
    f_0_4       INTEGER DEFAULT (0), \
    f_5_11      INTEGER DEFAULT (0), \
    f_12_17     INTEGER DEFAULT (0), \
    f_18_34     INTEGER DEFAULT (0), \
    f_35_64     INTEGER DEFAULT (0), \
    f_65        INTEGER DEFAULT (0), \
    h_0_4       INTEGER DEFAULT (0), \
    h_5_11      INTEGER DEFAULT (0), \
    h_12_17     INTEGER DEFAULT (0), \
    h_18_34     INTEGER DEFAULT (0), \
    h_35_64     INTEGER DEFAULT (0), \
    h_65        INTEGER DEFAULT (0) \
)"
VERSION_GROUPE = 1
MODULE_GROUPE = 5
GROUPE = {'query' : QUERY_GROUPE, 'version' : VERSION_GROUPE, 'module' : MODULE_GROUPE}

QUERY_INSCRIPTION = "\
CREATE TABLE inscription ( \
    id_inscription  INTEGER  PRIMARY KEY AUTOINCREMENT, \
    id_participante INTEGER  NOT NULL, \
    id_activite     INTEGER  NOT NULL, \
    status          INTEGER  NOT NULL, \
    present         INTEGER, \
    time            DATETIME DEFAULT (datetime('now', 'localtime') ), \
    FOREIGN KEY ( \
        id_participante \
    ) \
    REFERENCES participante (id_participante) ON DELETE RESTRICT \
                                              ON UPDATE CASCADE, \
    FOREIGN KEY ( \
        id_activite \
    ) \
    REFERENCES activite (id_activite) ON DELETE RESTRICT \
                                      ON UPDATE CASCADE \
)"
VERSION_INSCRIPTION = 1
MODULE_INSCRIPTION = 6
INSCRIPTION = {'query' : QUERY_INSCRIPTION, 'version' : VERSION_INSCRIPTION, 'module' : MODULE_INSCRIPTION}

QUERY_LIEU = "\
CREATE TABLE lieu ( \
    id_lieu     INTEGER PRIMARY KEY, \
    nom         TEXT    NOT NULL, \
    adresse_1   TEXT    NOT NULL, \
    adresse_2   TEXT, \
    ville       TEXT, \
    province    TEXT, \
    code_postal TEXT, \
    UNIQUE ( \
        nom, \
        adresse_1 \
    ) \
    ON CONFLICT ABORT \
)"
VERSION_LIEU = 1
MODULE_LIEU = 7
LIEU = {'query' : QUERY_LIEU, 'version' : VERSION_LIEU, 'module' : MODULE_LIEU}

QUERY_MEMBRE = "\
CREATE TABLE membre ( \
    id_membre           INTEGER PRIMARY KEY, \
    actif               BOOLEAN, \
    id_participante     INTEGER REFERENCES participante (id_participante) ON DELETE RESTRICT \
                                                                          ON UPDATE RESTRICT, \
    numero_membre       INTEGER, \
    membre_honoraire    BOOLEAN, \
    date_renouvellement DATE \
)"
VERSION_MEMBRE = 1
MODULE_MEMBRE = 8
MEMBRE = {'query' : QUERY_MEMBRE, 'version' : VERSION_MEMBRE, 'module' : MODULE_MEMBRE}

QUERY_PARTICIPANTE = "\
CREATE TABLE participante ( \
    id_participante    INTEGER PRIMARY KEY, \
    appellation        TEXT, \
    prenom             TEXT    NOT NULL, \
    nom                TEXT, \
    adresse_1          TEXT, \
    adresse_2          TEXT, \
    ville              TEXT, \
    province           TEXT, \
    code_postal        TEXT, \
    courriel           TEXT, \
    telephone_1        INTEGER NOT NULL, \
    telephone_2        INTEGER, \
    poste_telephone_1  INTEGER, \
    poste_telephone_2  INTEGER, \
    date_naissance     INTEGER, \
    personne_nourrie   INTEGER, \
    consentement_photo BOOLEAN, \
    UNIQUE ( \
        prenom, \
        nom, \
        telephone_1 \
    ) \
    ON CONFLICT ABORT \
)"
VERSION_PARTICIPANTE = 1
MODULE_PARTICIPANTE = 9
PARTICIPANTE = {'query' : QUERY_PARTICIPANTE, 'version' : VERSION_PARTICIPANTE, 'module' : MODULE_PARTICIPANTE}

QUERY_RESPONSABLE = "\
CREATE TABLE responsable ( \
    id_responsable INTEGER PRIMARY KEY, \
    prenom         TEXT    NOT NULL, \
    nom            TEXT, \
    UNIQUE ( \
        prenom, \
        nom \
    ) \
    ON CONFLICT ABORT \
)"
VERSION_RESPONSABLE = 1
MODULE_RESPONSABLE = 10
RESPONSABLE = {'query' : QUERY_RESPONSABLE, 'version' : VERSION_RESPONSABLE, 'module' : MODULE_RESPONSABLE}

QUERY_TYPE_ACTIVITE = "\
CREATE TABLE type_activite ( \
    id_type_activite INTEGER PRIMARY KEY, \
    nom              TEXT    NOT NULL \
                             UNIQUE \
)" 
VERSION_TYPE_ACTIVITE = 1
MODULE_TYPE_ACTIVITE = 11
TYPE_ACTIVITE = {'query' : QUERY_TYPE_ACTIVITE, 'version' : VERSION_TYPE_ACTIVITE, 'module' : MODULE_TYPE_ACTIVITE}

QUERY_INFORMATIONS = "\
CREATE TABLE informations ( \
    nom         TEXT    NOT NULL, \
    departement TEXT, \
    adresse1    TEXT    NOT NULL, \
    adresse2    TEXT, \
    ville       TEXT    NOT NULL, \
    code_postal TEXT, \
    province    TEXT, \
    pays        TEXT, \
    telephone   INTEGER, \
    poste       INTEGER, \
    sf          INTEGER, \
    sf_poste    INTEGER, \
    fax         INTEGER, \
    fax_poste   INTEGER, \
    courriel    TEXT \
)"
VERSION_INFORMATIONS = 1
MODULE_INFORMATIONS = 12
INFORMATIONS = {'query' : QUERY_INFORMATIONS, 'version' : VERSION_INFORMATIONS, 'module' : MODULE_INFORMATIONS}

class PreparationWizard(QWizard, Ui_PreparationWizard):
    def __init__(self):
        super(PreparationWizard, self).__init__()

        # Interface graphique
        self.setupUi(self)

        # Afficher la bannière
        # Déterminer la dimension de l'image
        wb = self.img_banniere.width()
        hb = self.img_banniere.height()

        # Charger l'image
        scene = QGraphicsScene()
        pixmap = QGraphicsPixmapItem(QPixmap(":/global/Banniere.png").scaled(wb, hb, Qt.KeepAspectRatio))
        scene.addItem(pixmap)
        self.img_banniere.setScene(scene)
        self.img_banniere.show()  

        # Afficher les copyrights
        # Déterminer la dimension de l'image
        wc = self.img_copyrights.width()
        hc = self.img_copyrights.height()

        # Charger l'image
        scene = QGraphicsScene()
        pixmap = QGraphicsPixmapItem(QPixmap(":/global/Copyrights.png").scaled(wc, hc, Qt.KeepAspectRatio))
        scene.addItem(pixmap)
        self.img_copyrights.setScene(scene)
        self.img_copyrights.show()

        # Enregistrer les champs qui doivent être remplis pour que l'assistant puisse continuer
        self.pgs_selection.registerField("emplacementDB", self.txt_emplacement_db)
        self.pgs_selection.registerField("emplacementStats", self.txt_emplacement_stats)
        self.pgs_informations.registerField("nom*", self.txt_nom)
        self.pgs_informations.registerField("departement", self.txt_departement)
        self.pgs_informations.registerField("adresse1*", self.txt_adresse_1)
        self.pgs_informations.registerField("adresse2", self.txt_adresse_2)
        self.pgs_informations.registerField("ville*", self.txt_ville)
        self.pgs_informations.registerField("code_postal", self.txt_code_postal)
        self.pgs_informations.registerField("province", self.txt_province)
        self.pgs_informations.registerField("pays", self.txt_pays)
        self.pgs_contact.registerField("telephone", self.txt_telephone)
        self.pgs_contact.registerField("poste", self.txt_poste)
        self.pgs_contact.registerField("sf", self.txt_sf)
        self.pgs_contact.registerField("poste_sf", self.txt_poste_sf)
        self.pgs_contact.registerField("fax", self.txt_fax)
        self.pgs_contact.registerField("poste_fax", self.txt_poste_fax)
        self.pgs_contact.registerField("courriel", self.txt_courriel)
        self.pgs_module.registerField("activite", self.chk_activite)
        self.pgs_module.registerField("categorie_activite", self.chk_categorie_activite)
        self.pgs_module.registerField("lieu", self.chk_lieu)
        self.pgs_module.registerField("responsable", self.chk_responsable)
        self.pgs_module.registerField("type_activite", self.chk_type_activite)
        self.pgs_module.registerField("article", self.chk_article)
        self.pgs_module.registerField("facturation", self.chk_facturation)
        self.pgs_module.registerField("inscription", self.chk_inscription)
        self.pgs_module.registerField("groupe", self.chk_groupe)
        self.pgs_module.registerField("membre", self.chk_membre)
        self.pgs_module.registerField("participante", self.chk_partitipante)

        # Validator
        self.txt_nom.setValidator(validator.name_validator())
        self.txt_adresse_1.setValidator(validator.address_validator())
        self.txt_adresse_2.setValidator(validator.address_validator())
        self.txt_ville.setValidator(validator.name_validator())
        self.txt_code_postal.setValidator(validator.zip_code_validator())
        self.txt_province.setValidator(validator.name_validator())
        self.txt_pays.setValidator(validator.name_validator())
        self.txt_telephone.setValidator(validator.phone_validator())
        self.txt_poste.setValidator(validator.poste_validator())
        self.txt_sf.setValidator(validator.phone_validator())
        self.txt_poste_sf.setValidator(validator.poste_validator())
        self.txt_fax.setValidator(validator.phone_validator())
        self.txt_poste_fax.setValidator(validator.poste_validator())
        self.txt_courriel.setValidator(validator.email_validator())

        # Afficher les emplacements par défaut
        self.afficher_emplacement()

        # Slots
        self.rbt_nouvelle_db.toggled.connect(self.afficher_emplacement)
        self.rbt_db_existante.toggled.connect(self.afficher_emplacement)
        self.btn_emplacement_db.clicked.connect(self.get_database_path)
        self.btn_emplacement_stats.clicked.connect(self.get_stats_folder)
        self.chk_activite.toggled.connect(self.selection_module)
        self.chk_categorie_activite.toggled.connect(self.selection_module)
        self.chk_lieu.toggled.connect(self.selection_module)
        self.chk_responsable.toggled.connect(self.selection_module)
        self.chk_type_activite.toggled.connect(self.selection_module)
        self.chk_article.toggled.connect(self.selection_module)
        self.chk_facturation.toggled.connect(self.selection_module)
        self.chk_inscription.toggled.connect(self.selection_module)
        self.chk_groupe.toggled.connect(self.selection_module)
        self.chk_membre.toggled.connect(self.selection_module)
        self.chk_partitipante.toggled.connect(self.selection_module)
        self.chk_tout.toggled.connect(self.selection_module)

    def selection_module(self, checked):
        """
        Afficher les dépendances des modules
        """
        btn = self.sender()

        # Décocher le bouton tout si n'importe quel élément est décoché
        if not checked:
            self.chk_tout.setChecked(False)

        # Traiter les dépendances des modules
        if btn == self.chk_tout:
            if checked:
                self.chk_activite.setChecked(True)
                self.chk_categorie_activite.setChecked(True)
                self.chk_lieu.setChecked(True)
                self.chk_responsable.setChecked(True)
                self.chk_type_activite.setChecked(True)
                self.chk_article.setChecked(True)
                self.chk_facturation.setChecked(True)
                self.chk_inscription.setChecked(True)
                self.chk_groupe.setChecked(True)
                self.chk_membre.setChecked(True)
                self.chk_partitipante.setChecked(True)
        elif btn == self.chk_activite:
            if checked:
                self.chk_categorie_activite.setChecked(True)
                self.chk_lieu.setChecked(True)
                self.chk_responsable.setChecked(True)
                self.chk_type_activite.setChecked(True)
            else:
                self.chk_article.setChecked(False)
                self.chk_inscription.setChecked(False)
                self.chk_groupe.setChecked(False)
        elif btn == self.chk_categorie_activite:
            if not checked:
                self.chk_activite.setChecked(False)
        elif btn == self.chk_lieu:
            if not checked:
                self.chk_categorie_activite.setChecked(False)
        elif btn == self.chk_responsable:
            if not checked:
                self.chk_categorie_activite.setChecked(False)
        elif btn == self.chk_type_activite:
            if not checked:
                self.chk_categorie_activite.setChecked(False)
        elif btn == self.chk_article:
            if checked:
                self.chk_activite.setChecked(True)
        elif btn == self.chk_facturation:
            if checked:
                self.chk_partitipante.setChecked(True)
        elif btn == self.chk_inscription:
            if checked:
                self.chk_partitipante.setChecked(True)
                self.chk_activite.setChecked(True)
        elif btn == self.chk_groupe:
            if checked:
                self.chk_activite.setChecked(True)
        elif btn == self.chk_membre:
            if checked:
                self.chk_partitipante.setChecked(True)
        elif btn == self.chk_partitipante:
            if not checked:
                self.chk_membre.setChecked(False)
                self.chk_inscription.setChecked(False)
                self.chk_facturation.setChecked(False)

    def afficher_emplacement(self):
        """
        Modifie les champs selon si une nouvelle base de données est créée ou une existante est sélectionnée
        """
        # Afficher les emplacements par défaut
        self.txt_emplacement_db.setText(PATH_DB)
        self.txt_emplacement_stats.setText(PATH_STATS)

        # Afficher le label de l'emplacement de la base de donnée
        if self.rbt_db_existante.isChecked():
            self.lbl_emplacement_db.setText("Emplacement de la base de données : ")
        else:
            self.lbl_emplacement_db.setText("Dossier de la base de données : ")

    def get_database_path(self):
        """
        Obtenir le chemin vers une base de données existante ou le dossier ou elle doit être enregistrée
        """
        # Obtenir le chemin vers un fichier existant
        if self.rbt_db_existante.isChecked():
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.ExistingFile)
            dialog.setWindowTitle("Ouvrir la base de donnée")
            dialog.setDirectory(str(Path.home()))
            dialog.setNameFilter("Fichier GUIDE (*.guide)")
            if dialog.exec():
                self.txt_emplacement_db.setText(os.path.abspath(dialog.selectedFiles()[0]))

        # Obtenir le dossier ou la nouvelle base de données sera créée
        else:
            dialog = QFileDialog(self)
            dialog.setFileMode(QFileDialog.Directory)
            dialog.setWindowTitle("Dossier pour enregistrer la base de données")
            dialog.setDirectory(str(os.path.join(Path.home(), 'Documents')))
            if dialog.exec():
                self.txt_emplacement_db.setText(os.path.abspath(dialog.selectedFiles()[0]))

    def get_stats_folder(self):
        """
        Chemin vers le dossier statistiques
        """

        # Obtenir le dossier ou les statistiques de l'utilisateur selon enregistrées
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setWindowTitle("Dossier pour enregistrer les fichers statistique")
        dialog.setDirectory(str(os.path.join(Path.home(), 'Documents')))
        if dialog.exec():
            self.txt_emplacement_stats.setText(os.path.abspath(dialog.selectedFiles()[0]))

    def nextId(self):
        """
        Modifier l'ordre d'affichage des pages de l'assistant selon les sélections de l'utilisateur
        """
        current_id = self.currentId()
        if current_id == PAGE_DESCRIPTION:
            return PAGE_SELECTION
        elif current_id == PAGE_SELECTION:
            if self.rbt_db_existante.isChecked():
                return PAGE_FIN
            else:
                return PAGE_INFORMATIONS
        elif current_id == PAGE_INFORMATIONS:
            return PAGE_CONTACT
        elif current_id == PAGE_CONTACT:
            return PAGE_MODULE
        elif current_id == PAGE_MODULE:
            return PAGE_FIN
        else:
            return -1

    def accept(self):
        """
        Effectuer les opérations de fermeture du dialog :
            - Créer une nouvelle base de données
            - Connecter une base de données existante au programme
        """
        # Obtenir les informations sur les emplacements
        db_dir = self.pgs_selection.field("emplacementDB")
        stats_dir = self.pgs_selection.field("emplacementStats")

        if self.rbt_nouvelle_db.isChecked():
            # Obtenir les informations des champs de l'assistant
            nom = self.pgs_informations.field("nom")
            departement = self.pgs_informations.field("departement")
            adresse1 = self.pgs_informations.field("adresse1")
            adresse2 = self.pgs_informations.field("adresse2")
            ville = self.pgs_informations.field("ville")
            code_postal = self.pgs_informations.field("code_postal")
            province = self.pgs_informations.field("province")
            pays = self.pgs_informations.field("pays")

            telephone = self.pgs_contact.field("telephone")
            poste = self.pgs_contact.field("poste")
            sf = self.pgs_contact.field("sf")
            poste_sf = self.pgs_contact.field("poste_sf")
            fax = self.pgs_contact.field("fax")
            poste_fax = self.pgs_contact.field("poste_fax")
            courriel = self.pgs_contact.field("courriel")

            activite = self.pgs_module.field("activite")
            categorie_activite = self.pgs_module.field("categorie_activite")
            lieu = self.pgs_module.field("lieu")
            responsable = self.pgs_module.field("responsable")
            type_activite = self.pgs_module.field("type_activite")
            article = self.pgs_module.field("article")
            facturation = self.pgs_module.field("facturation")
            inscription = self.pgs_module.field("inscription")
            groupe = self.pgs_module.field("groupe")
            membre = self.pgs_module.field("membre")
            participante = self.pgs_module.field("participante")

            # Créer le chemin vers la base de données
            try:
                os.makedirs(db_dir)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    file_error.db_creation(error.errno, error.strerror)

            # Créer le chemin vers le dossier pour les statistiques
            try:
                os.makedirs(stats_dir)
            except OSError as error:
                if error.errno != errno.EEXIST:
                    file_error.db_creation(error.errno, error.strerror)

            # Créer la base de données
            filename = nom + '.guide'
            db_dir = str(os.path.join(db_dir, filename))
            db = QSqlDatabase.addDatabase('QSQLITE')
            db.setDatabaseName(db_dir)

            # Afficher une erreur si la base de données ne peut pas être créer
            if not db.open():
                database_error.sql_error_handler(db.lastError())
                return # Empêche de continuer la création de la base de données

            # Créer les tableaux de la base de données
            # Commencer une transaction
            db.transaction()

            # Affichage d'un message d'erreur si la requete echoue
            if database_error.sql_error_handler(db.lastError()):
                return # Empêche de continuer la création de la base de données

            # Créer les tables
            # Créer la table guide
            QSqlQuery().exec_(GUIDE['query'])

            # Affichage d'un message d'erreur si la requete echoue
            if database_error.sql_error_handler(QSqlQuery().lastError()):
                db.rollback() # Annuler la transaction
                return # Empêche de continuer la création de la base de données

            # Ajouter le numéro de version
            query = QSqlQuery()
            query.prepare("INSERT INTO guide (module, version) \
                          VALUES (:module, :version)")
            query.bindValue(':module', GUIDE['module'])
            query.bindValue(':version', GUIDE['version'])
            query.exec_()
            # Affichage d'un message d'erreur si la requete echoue
            if database_error.sql_error_handler(query.lastError()):
                db.rollback() # Annuler la transaction
                return # Empêche de continuer la création de la base de données

            # Déterminer les autres tables à ajouter
            liste_table = []
            liste_table.append(INFORMATIONS)

            if activite:
                liste_table.append(ACTIVITE)
            if categorie_activite:
                liste_table.append(CATEGORIE_ACTIVITE)
            if lieu:
                liste_table.append(LIEU)
            if responsable:
                liste_table.append(RESPONSABLE)
            if type_activite:
                liste_table.append(TYPE_ACTIVITE)
            if article:
                liste_table.append(ARTICLE)
            if facturation:
                liste_table.append(FACTURE)
            if inscription:
                liste_table.append(INSCRIPTION)
            if groupe:
                liste_table.append(GROUPE)
            if membre:
                liste_table.append(MEMBRE)
            if participante:
                liste_table.append(PARTICIPANTE)

            # Ajouter les autres tables à la base de données
            for table in liste_table:
                QSqlQuery().exec_(table['query'])

                # Affichage d'un message d'erreur si la requete echoue
                if database_error.sql_error_handler(query.lastError()):
                    db.rollback() # Annuler la transaction
                    return # Empêche de continuer la création de la base de données

                # Ajouter le numéro de version
                query = QSqlQuery()
                query.prepare("INSERT INTO guide (module, version) \
                              VALUES (:module, :version)")
                query.bindValue(':module', table['module'])
                query.bindValue(':version', table['version'])
                query.exec_()
                # Affichage d'un message d'erreur si la requete echoue
                if database_error.sql_error_handler(query.lastError()):
                    db.rollback() # Annuler la transaction
                    return # Empêche de continuer la création de la base de données

            # Terminer la transaction
            db.commit()

            # Affichage d'un message d'erreur si la requete echoue
            if database_error.sql_error_handler(db.lastError()):
                db.rollback() # Annuler la transaction
                return # Empêche la fermeture du dialog

        settings = QSettings("SDR Soft", "PyGUIDE")
        settings.setValue("Database", db_dir)
        settings.setValue("Statistique", stats_dir)

        QDialog.accept(self)
