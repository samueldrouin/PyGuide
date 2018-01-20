"""Statistiques"""
# Python import
import os

# PyQt import
from PyQt5 import uic
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QSignalMapper
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Project import
from form import Form
from Script import Error

class Statistiques(Form):
    """Dialog des statistiques"""
    # Liste des colonnes
    LISTE_COLONNE_ACTIVITE = ["", "Date", "Heure début", "Heure fin", "Date limite d'inscription", "Status"]
    LISTE_COLONNE_ARTICLE = ["", "Prix", "Description"]
    LISTE_COLONNE_CATEGORIE_ACTIVITE = ["", "Nom", "Prix membre", "Prix régulier", "Nombre de participantes minimum",
                                        "Nombre de participantes maximum"]
    LISTE_COLONNE_FACTURE = ["", "Date", "Numéro de reçu", "Total"]
    LISTE_COLONNE_GROUPE = ["", "Femme 0-4 ans", "Homme 0-4 ans", "Femme 5-11 ans", "Homme 5-12 ans", 
                            "Femme 12-17 ans", "Homme 12-17 ans", "Femme 18-34 ans", "Homme 18-34 ans", 
                            "Femme 35-64 ans", "Homme 35-64 ans", "Femme 65+ ans", "Homme 65+ ans"]
    LISTE_COLONNE_INSCRIPTION = ["", "Status", "Présent", "Date"]
    LISTE_COLONNE_LIEU = ["", "Nom", "Adresse", "Ville", "Province", "Code postal"]
    LISTE_COLONNE_MEMBRE = ["", "Actif", "Numéro de membre", "Honoraire", "Date de renouvellement"]
    LISTE_COLONNE_PARTICIPANTE = ["", "Appelation", "Prénom", "Nom", "Adresse", "Ville", 
                                  "Province", "Code postal", "Courriel", "Téléphone 1", "Téléphone 2", 
                                  "Année de naissance", "Consentement photo"]
    LISTE_COLONNE_RESPONSABLE = ["", "Prénom", "Nom"]
    LISTE_COLONNE_TYPE_ACTIVITE = ["", "Nom"]
    LISTE_CONTRAINTE_MEME_TABLE = ["et"]
    LISTE_CONTRAINTE_AUTRE_TABLE = ["et", "et exclusif", "ou"]

    # Dictionnaire des tables pertinentes de la base de donnée
    #   Key : Nom de la table
    #   Value : Nom pour l'affichage
    DICT_TABLE = {
                  'activite' : {'nom' : 'Activité', 'reference' : ['activite', 'categorie_activite']},
                  'article' : {'nom' : 'Article', 'reference' : ['article', 'facture', 'activite']},
                  'categorie_activite' : {'nom' : 'Catégorie d\'activité', 'reference' : ['categorie_activite', 'responsable', 'type_activite', 'lieu']},
                  'facture' : {'nom' : 'Facture', 'reference' : ['facture', 'participante']},
                  'groupe' : {'nom' : 'Groupe', 'reference' : ['groupe', 'activite']},
                  'inscription': {'nom' : 'Inscription', 'reference' : ['inscription', 'participante', 'activite']},
                  'lieu' : {'nom' : 'Lieu', 'reference' : ['lieu']},
                  'membre' :  {'nom' : 'Membre', 'reference' : ['membre', 'participante']},
                  'participante' : {'nom' : 'Participante', 'reference' : ['participante']},
                  'responsable' : {'nom' : 'Responsable', 'reference' : ['responsable']},
                  'type_activite' : {'nom' : 'Type d\'activité', 'reference' : ['type_activite']}
                  }

    """
    Valeur des types de donnée

    Les types de donnée peuvent être soit des types standard "String", "Integer"... ou encore un type derivé de 
    ceux-ci. Il sert à indiquer comment la donnée doit être traitée pour l'affichage ainsi que dans quel type de 
    statistique il est possible de l'afficher. 
    """
    TYPE_STRING = 0
    TYPE_INTEGER = 1
    TYPE_DATE = 2
    TYPE_TIME = 3
    TYPE_BOOLEAN = 4
    TYPE_DATETIME = 5
    # Type pour l'affichage correct des prix
    TYPE_PRIX = 6
    # Type utilisé pour les status d'inscription seulement
    # Nécessaire pour passer entiers de la base de donnée à une valeur compréhensible par l'utilisateur
    TYPE_STATUS_INSCRIPTION = 7

    """
    Information sur la tables de la base de donnée

    Ces listes servent à faire la correspondance entre les noms affichée et le nom réel dans la base de donnée. 
    Lors de la création des ComboBox, le texte est la Value et les data est la Key

    Les colonnes qui contiennent dans foreign key ne doivent pas être ajoutées à ces dictionnaires. 

    Liste des colonnes pour chaque table de la base de donnée
        Key : Nom de la table
        Value : Nom pour l'affichage
    """
    # Colonne de la table activité
    DICT_ACTIVITE = {
                     'date' : {'nom' : 'Date', 'type' : TYPE_DATE},
                     'heure_debut' : {'nom' : 'Heure de début', 'type' : TYPE_TIME},
                     'heure_fin' : {'nom' : 'Heure de fin', 'type' : TYPE_TIME},
                     'date_limite_inscription' : {'nom' : 'Date limite d\'inscription', 'type' : TYPE_DATE},
                     'status' : {'nom' : 'Activité annulée', 'type' : TYPE_BOOLEAN}
                    }

    # Colonne de la table article
    DICT_ARTICLE = {
                    'prix': {'nom' : 'Prix', 'type' : TYPE_PRIX},
                    'description' : {'nom' : 'Description', 'type' : TYPE_STRING}
                   }

    # Colonne de la table categorie d'activité
    DICT_CATEGORIE_ACTIVITE = {
                               'nom' : {'nom' : 'Nom', 'type' : TYPE_STRING},
                               'prix_membre' : {'nom' : 'Prix membre', 'type' : TYPE_PRIX},
                               'prix_non_membre' : {'nom' : 'Prix régulier', 'type' : TYPE_PRIX},
                               'participante_minimum' : {'nom' : 'Nombre de participante minimum', 'type' : TYPE_INTEGER},
                               'participante_maximum' : {'nom' : 'Nombre de participante maximum', 'type' : TYPE_INTEGER}
                              }

    # Colonne de la table facture
    DICT_FACTURE = {
                    'date' : {'nom' : 'Date', 'type' : TYPE_DATE},
                    'numero_recu' : {'nom' : 'Numéro du reçu', 'type' : TYPE_INTEGER},
                    'total' : {'nom' : 'Total', 'type' : TYPE_PRIX}
                   }

    # Colonne de la table groupe
    DICT_GROUPE = {
                   'f_0_4' : {'nom' : 'Femme 0-4 ans', 'type' : TYPE_INTEGER},
                   'f_5_11' : {'nom' : 'Femme 5-11 ans', 'type' : TYPE_INTEGER},
                   'f_12_17' : {'nom' : 'Femme 12-17 ans', 'type' : TYPE_INTEGER},
                   'f_18_34' : {'nom' : 'Femme 18-34 ans', 'type' : TYPE_INTEGER},
                   'f_35_64' : {'nom' : 'Femme 35-64 ans', 'type' : TYPE_INTEGER},
                   'f_65' : {'nom' : 'Femme 65+ ans', 'type' : TYPE_INTEGER},
                   'h_0_4' : {'nom' : 'Homme 0-4 ans', 'type' : TYPE_INTEGER},
                   'h_5_11' : {'nom' : 'Homme 5-11 ans', 'type' : TYPE_INTEGER},
                   'h_12_17' : {'nom' : 'Homme 12-17 ans', 'type' : TYPE_INTEGER},
                   'h_18_34' : {'nom' : 'Homme 18-34 ans', 'type' : TYPE_INTEGER},
                   'h_35_64' : {'nom' : 'Homme 35-64 ans', 'type' : TYPE_INTEGER},
                   'h_65' : {'nom' : 'Homme 65+ ans', 'type' : TYPE_INTEGER}
                  }

    # Colonne de la table des inscriptions
    DICT_INSCRIPTION = {
                        'status' : {'nom' : 'Status', 'type' : TYPE_STATUS_INSCRIPTION},
                        'present' : {'nom' : 'Présent', 'type' : TYPE_BOOLEAN},
                        'time' : {'nom' : 'Date', 'type' : TYPE_DATE}
                       }

    # Colonne de la table des lieux
    DICT_LIEU = {
                  'nom' : {'nom' : 'Nom', 'type' : TYPE_STRING},
                  'adresse_1' : {'nom' : 'Adresse ligne 1', 'type' : TYPE_STRING},
                  'adresse_2' : {'nom' : 'Adresse ligne 2', 'type' : TYPE_STRING},
                  'ville' : {'nom' : 'Ville', 'type' : TYPE_STRING},
                  'province' : {'nom' : 'Province', 'type' : TYPE_STRING},
                  'code_postal' : {'nom' : 'Code postal', 'type' : TYPE_STRING}
                 }

    # Colonne de la table des membres
    DICT_MEMBRE = {
                   'actif' : {'nom' : 'Actif', 'type' : TYPE_BOOLEAN},
                   'numero_membre' : {'nom' : 'Numéro de membre', 'type' : TYPE_STRING},
                   'membre_honoraire' : {'nom' : 'Membre honoraire', 'type' : TYPE_BOOLEAN},
                   'date_renouvellement' : {'nom' : 'Date de renouvellement', 'type' : TYPE_DATE}
                  }

    # Colonne de la table des participantes
    DICT_PARTICIPANTE = {
                         'appellation' : {'nom' : 'Appellation', 'type' : TYPE_STRING},
                         'prenom' : {'nom' : 'Prénom', 'type' : TYPE_STRING},
                         'nom' : {'nom' : 'Nom', 'type' : TYPE_STRING},
                         'adresse_1' : {'nom' : 'Adresse ligne 1', 'type' : TYPE_STRING},
                         'adresse_2' : {'nom' : 'Adresse ligne 2', 'type' : TYPE_STRING},
                         'ville' : {'nom' : 'Ville', 'type' : TYPE_STRING},
                         'province' : {'nom' : 'Province', 'type' : TYPE_STRING},
                         'code_postal' : {'nom' : 'Code postal', 'type' : TYPE_STRING},
                         'courriel' : {'nom' : 'Adresse courriel', 'type' : TYPE_STRING},
                         'telephone_1' : {'nom' : 'Téléphone 1', 'type' : TYPE_INTEGER},
                         'telephone_2' : {'nom' : 'Téléphone 2', 'type' : TYPE_INTEGER},
                         'poste_telephone_1' : {'nom' : 'Poste de téléphone 1', 'type' : TYPE_INTEGER},
                         'poste_telephone_2' : {'nom' : 'Poste de téléphone 2', 'type' : TYPE_INTEGER},
                         'date_naissance' : {'nom' : 'Année de naissance', 'type' : TYPE_INTEGER},
                         'personne_nourrie' : {'nom' : 'Nombre de personne nourries', 'type' : TYPE_INTEGER},
                         'consentement_photo' : {'nom' : 'Consentement photo', 'type' : TYPE_BOOLEAN}
                        }

    # Colonne de la table des responsables
    DICT_RESPONSABLE = {
                        'prenom' : {'nom' : 'Prénom', 'type' : TYPE_STRING},
                        'nom' : {'nom' : 'Nom', 'type' : TYPE_STRING}
                       }

    # Colonne de la table du type d'activité
    DICT_TYPE_ACTIVITE = {
                          'nom' : {'nom' : 'Nom', 'type' : TYPE_STRING}
                         }

    def __init__(self, database):
        super(Statistiques, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'statistique.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.DATABASE = database
        self.DICT_TABLE = None
        self.DICT_COLONNES = None
        self.liste_tri = [""] # Liste vide pour les tables du tri

        # Créer la liste des tables
        self.generer_liste_tables()
        self.generer_liste_colonnes()

        # Afficher la premier ligne
        self.ajouter_ligne_champ()

        # Slots
        self.btn_annuler.clicked.connect(self.reject)

    """
    Gestion de la table des champs
    """

    def ajouter_ligne_champ(self):
        """Ajouter une ligne au tableau des champs"""

        # Ajouter une ligne à la table
        self.tbl_champs.insertRow(self.tbl_champs.rowCount())
        r = self.tbl_champs.rowCount() - 1

        # ComboBox Table
        table_mapper = QSignalMapper(self)
        cbx_table = QComboBox()
        cbx_table.addItems(self.generer_liste_table_champs(r))
        table_mapper.setMapping(cbx_table, r)
        cbx_table.activated.connect(table_mapper.map)
        self.tbl_champs.setCellWidget(r, 0, cbx_table)
        table_mapper.setMapping(self.tbl_champs, r)
        table_mapper.mapped[int].connect(self.table_selectionnee)

        # Combobox colonne vide
        colonne_mapper = QSignalMapper(self)
        cbx_colonne = QComboBox()
        cbx_colonne.addItem("")
        colonne_mapper.setMapping(cbx_colonne, r)
        cbx_colonne.activated.connect(colonne_mapper.map)
        self.tbl_champs.setCellWidget(r, 1, cbx_colonne)
        colonne_mapper.setMapping(self.tbl_champs, r)
        colonne_mapper.mapped[int].connect(self.colonne_selectionnee)

        # ComboBox contrainte vide
        cbx_contrainte = QComboBox()
        cbx_contrainte.addItem("")
        self.tbl_champs.setCellWidget(r, 2, cbx_contrainte)

    def colonne_selectionnee(self, row):
        """Afficher la ligne suivante"""
        if self.tbl_champs.cellWidget(row, 1).currentText() != "":
            self.ajouter_ligne_champ()

    def table_selectionnee(self, row):
        """
        Afficher les informations relative à la table sélectionnée
        dans les combobox colonne et contraintes
        """
        # Effacer le contenu existant
        self.tbl_champs.cellWidget(row, 1).clear()
        self.tbl_champs.cellWidget(row, 2).clear()

        # Déterminer le nom de la table
        table = self.tbl_champs.cellWidget(row, 0).currentText()

        # Afficher les champs pour la colonne et le constrainte
        if table == "Activité":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_ACTIVITE)
        elif table == "Article":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_ARTICLE)
        elif table == "Catégorie d'activité":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_CATEGORIE_ACTIVITE)
        elif table == "Facture":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_FACTURE)
        elif table == "Groupe":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_GROUPE)
        elif table == "Inscription":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_INSCRIPTION)
        elif table == "Lieu":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_LIEU)
        elif table == "Membre":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_MEMBRE)
        elif table == "Participante":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_PARTICIPANTE)
        elif table == "Responsable":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_RESPONSABLE)
        elif table == "Type d'activité":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_TYPE_ACTIVITE)

        # Pour toute les rangees sauf la premiere
        if row != 0:
            self.afficher_contraintes(row) # Afficher les contraintes de la ligne precedente
            self.make_read_only(row) # Disable le combobox de la ligne precedante

    def make_read_only(self, row):
        """Disable le combobox de la ligne precedente"""
        r = row-1
        self.tbl_champs.cellWidget(r, 0).setEnabled(False)

    def afficher_contraintes(self, row):
        """
        Afficher les contraintes dans le combobox de la ligne précédente
        :param row: Ligne actuelle
        """
        # Ligne de la colonne précédente
        r = row - 1

        # Tableau des lignes actuelle et suivante
        last_table = self.tbl_champs.cellWidget(r, 0).currentText()
        current_table = self.tbl_champs.cellWidget(row, 0).currentText()
        
        if last_table == current_table:
            self.tbl_champs.cellWidget(r, 2).addItems(self.LISTE_CONTRAINTE_MEME_TABLE)
        else:
            self.tbl_champs.cellWidget(r, 2).addItems(self.LISTE_CONTRAINTE_AUTRE_TABLE)

    def ajouter_ligne_tri(self):
        """Ajouter une ligne au tableau du tri"""
        self.tbl_tri.insertRow(self.tbl_tri.rowCount())
        r = self.tbl_tri.rowCount() - 1

        # ComboBox Table
        cbx_table = QComboBox()
        cbx_table.addItems(self.liste_tri)
        self.tbl_tri.setCellWidget(r, 0, cbx_table)

        # Combobox colonne vide
        cbx_colonne = QComboBox()
        cbx_colonne.addItem("")
        self.tbl_tri.setCellWidget(r, 1, cbx_colonne)

        # ComboBox contrainte vide
        cbx_operateur = QComboBox()
        cbx_operateur.addItem("")
        self.tbl_tri.setCellWidget(r, 2, cbx_operateur)

        # ComboBox contrainte vide
        cbx_contrainte = QComboBox()
        cbx_contrainte.addItem("")
        self.tbl_tri.setCellWidget(r, 3, cbx_contrainte)

        if r < 0:
            self.modifier_liste_tri_existante()

    def modifier_liste_tri_existante(self):
        """Modifier la liste dans les ComboBox existant"""
        for r in range(self.tbl_tri.rowCount()-1):
            current_text = self.tbl_tri.cellWidget(row, 0).currentText()
            self.tbl_tri.cellWidget(row, 0).clear()
            self.tbl_tri.cellWidget(row, 0).addItems(self.liste_table)
            self.tbl_tri.cellWidget(row, 0).setCurrentText(current_text)

    def creer_option_tri(self):
        """Afficher les options de tri"""
        # Ajouter les éléments à la liste
        for r in range(self.tbl_champs.rowCount()-1):
            text = self.tbl_champs.cellWidget(r, 0).currentText()
            if text == "Activité":
                self.liste_tri.append("Activité")
                self.liste_tri.append("Catégorie d'activité")
                self.liste_tri.append("Type d'activité")
            elif text == "Article":
                self.liste_tri.append("Article")
                self.liste_tri.append("Facture")
            elif text == "Catégorie d'activité":
                self.liste_tri.append("Catégorie d'activité")
                self.liste_tri.append("Responsable")
                self.liste_tri.append("Type d'activité")
                self.liste_tri.append("Lieu")
            elif text == "Facture":
                self.liste_tri.append("Facture")
                self.liste_tri.append("Participante")
                self.liste_tri.append("Membre")
            elif text == "Groupe":
                self.liste_tri.append("Groupe")
                self.liste_tri.append("Activité")
                self.liste_tri.append("Catégorie d'activité")
                self.liste_tri.append("Type d'activité")
            elif text == "Inscription":
                self.liste_tri.append("Inscription")
                self.liste_tri.append("Activité")
                self.liste_tri.append("Catégorie d'activité")
                self.liste_tri.append("Type d'activité")
                self.liste_tri.append("Participante")
                self.liste_tri.append("Membre")
            elif text == "Lieu":
                self.liste_tri.append("Lieu")
            elif text == "Membre":
                self.liste_tri.append("Participante")
                self.liste_tri.append("Membre")
            elif text == "Participante":
                self.liste_tri.append("Participante")
            elif text == "Responsable":
                self.liste_tri.append("Responsable")
            elif text == "Type d'activité":
                self.liste_tri.append("Type d'activité")
            continue

        # Effacer les duplicatat
        set(self.liste_tri)

        # Trier la liste
        sorted(self.liste_tri)

    def generer_liste_table_champs(self, row):
        """
        Générer la liste des tables disponible pour les champs
        :param row: Range du tableau qui vient d'être ajoutée
        :return: Liste des tables
        """
        liste_table_champs = [""]
        # Ajouter les éléments à la liste

        # Ajouter tout les éléments pour la première rangée
        if row == 0:
            for key, value in self.DICT_TABLE.items():
                liste_table_champs.append(value)
        # Ajouter le contenu pour les rangee suivantes
        # Basée sur le tableau de la rangée précédente
        else:
            text = self.tbl_champs.cellWidget(row-1, 0).currentText()
            if text == self.DICT_TABLE['activite']:
                liste_table_champs.append(self.DICT_TABLE['activite'])
                liste_table_champs.append(self.DICT_TABLE['categorie_activite'])
            elif text == self.DICT_TABLE['article']:
                liste_table_champs.append(self.DICT_TABLE['article'])
                liste_table_champs.append(self.DICT_TABLE['facture'])
            elif text == self.DICT_TABLE['categorie_activite']:
                liste_table_champs.append(self.DICT_TABLE['categorie_activite'])
                liste_table_champs.append(self.DICT_TABLE['responsable'])
                liste_table_champs.append(self.DICT_TABLE['type_activite'])
                liste_table_champs.append(self.DICT_TABLE['lieu'])
            elif text == self.DICT_TABLE['facture']:
                liste_table_champs.append(self.DICT_TABLE['facture'])
                liste_table_champs.append(self.DICT_TABLE['participante'])
            elif text == self.DICT_TABLE['groupe']:
                liste_table_champs.append(self.DICT_TABLE['groupe'])
                liste_table_champs.append(self.DICT_TABLE['activite'])
            elif text == self.DICT_TABLE['inscription']:
                liste_table_champs.append(self.DICT_TABLE['inscription'])
                liste_table_champs.append(self.DICT_TABLE['activite'])
                liste_table_champs.append(self.DICT_TABLE['participante'])
            elif text == self.DICT_TABLE['lieu']:
                liste_table_champs.append(self.DICT_TABLE['lieu'])
            elif text == self.DICT_TABLE['membre']:
                liste_table_champs.append(self.DICT_TABLE['participante'])
                liste_table_champs.append(self.DICT_TABLE['membre'])
            elif text == self.DICT_TABLE['participante']:
                liste_table_champs.append(self.DICT_TABLE['participante'])
            elif text == self.DICT_TABLE['responsable']:
                liste_table_champs.append(self.DICT_TABLE['responsable'])
            elif text == self.DICT_TABLE['type_activite']:
                liste_table_champs.append(self.DICT_TABLE['type_activite'])

        # Effacer les duplicatat
        set(liste_table_champs)

        # Trier la liste
        sorted(liste_table_champs)

        return liste_table_champs

    def generer_liste_colonnes(self):
        """Générer la liste des colonnes pour toutes les tables dans la liste des tables"""
        # Pour toute les entree du dictionnaire des tables
        for key in self.DICT_TABLE.items():
            
            pass

    def generer_liste_tables(self):
        """
        Générer la liste des tables à partir de la base de donnéees
        - Recherche de la liste des tables de la base de données
        - Modification des noms pour les noms complets
        """
        # Obtenir la liste des tables de la base de donnees
        liste_table = self.DATABASE.tables()
        
        # Afficher un message s'il y a une erreur
        Error.DatabaseError.sql_error_handler(self.DATABASE.lastError())

        # Retirer les entrees qui servent au fonctionnement interne de la base de donnees
        liste_table.remove("sqlite_sequence")

        # Transformer la liste en dictionnaire
        liste_table.sort()
        self.DICT_TABLE = dict(zip(liste_table, liste_table))
