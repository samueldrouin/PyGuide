"""Statistiques"""
# Python import
import os

# PyQt import
from PyQt5 import uic
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import QSignalMapper

# Project import
from form import Form

class Statistiques(Form):
    """Dialog des statistiques"""
    LISTE_COLONNE_ACTIVITE = ["", "Date", "Heure début", "Heure fin", "Date limite d'inscription", "Status"]
    LISTE_COLONNE_ARTICLE = ["", "Prix", "Description"]
    LISTE_COLONNE_CATEGORIE_ACTIVITE = ["", "Nom", "Prix membre", "Prix régulier", "Nombre de participantes minimum",
                                        "Nombre de participantes maximum"]
    LISTE_COLONNE_FACTURE = ["", "Date", "Numéro de reçu", "Total"]
    LISTE_COLONNE_GROUPE = ["", "Femme 0-4 ans", "Homme 0-4 ans", "Femme 5-11 ans", "Homme 5-12 ans", 
                            "Femme 12-17 ans", "Homme 12-17 ans", "Femme 18-34 ans", "Homme 18-34 ans", 
                            "Femme 35-64 ans", "Homme 35-64 ans", "Femme 65+ ans", "Homme 65+ ans"]
    LISTE_COLONNE_INSCRIPTION = ["", "Status", "Présent", "Date"]
    LISTE_COLONNE_LIEU = ["", "Nom", "Adresse", "Vi lle", "Province", "Code postal"]
    LISTE_COLONNE_MEMBRE = ["", "Actif", "Numéro de membre", "Honoraire", "Date de renouvellement"]
    LISTE_COLONNE_PARTICIPANTE = ["", "Appelation", "Prénom", "Nom", "Adresse", "Ville", 
                                  "Province", "Code postal", "Courriel", "Téléphone 1", "Téléphone 2", 
                                  "Année de naissance", "Consentement photo"]
    LISTE_COLONNE_RESPONSABLE = ["", "Prénom", "Nom"]
    LISTE_COLONNE_TYPE_ACTIVITE = ["", "Nom"]
    LISTE_CONTRAINTE_MEME_TABLE = ["et"]
    LISTE_CONTRAINTE_AUTRE_TABLE = ["", "et", "et exclusif", "ou"]

    def __init__(self, database):
        super(Statistiques, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'statistique.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.DATABASE = database
        self.liste_table = ["", "Activité", "Article", "Catégorie d'activité", "Facture", "Groupe", 
                   "Inscription", "Lieu", "Membre", "Participante", "Responsable", "Type d'activité"]

        # Afficher la premier ligne
        self.ajouter_ligne_champ()

        # Slots
        self.btn_annuler.clicked.connect(self.reject)

    def ajouter_ligne_champ(self):
        """Ajouter une ligne au tableau"""
        self.tbl_champs.insertRow(self.tbl_champs.rowCount())
        r = self.tbl_champs.rowCount() - 1

        # ComboBox Table
        table_mapper = QSignalMapper(self)
        cbx_table = QComboBox()
        cbx_table.addItems(self.liste_table)
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
        contrainte_mapper = QSignalMapper(self)
        cbx_contrainte = QComboBox()
        cbx_contrainte.addItem("")
        contrainte_mapper.setMapping(cbx_contrainte, r)
        cbx_contrainte.activated.connect(contrainte_mapper.map)
        self.tbl_champs.setCellWidget(r, 2, cbx_contrainte)
        contrainte_mapper.setMapping(self.tbl_champs, r)
        contrainte_mapper.mapped[int].connect(self.colonne_selectionnee)

    def colonne_selectionnee(self, row):
        """Ajouter une colonne si la derniere colonne est selectionnee"""
        r = self.tbl_champs.rowCount() - 1
        if row == r:
            if self.tbl_champs.cellWidget(r, 1).currentText() != "":
                if self.tbl_champs.cellWidget(r, 2).currentText() != "":
                    self.ajouter_ligne_champ()
    
    def creer_liste_table(self, row):
        """Créer la liste des tables à afficher"""
        # Modifier la liste dans champs utilisable
        text = self.tbl_champs.cellWidget(row, 0).currentText()
        if text == "Article" or text == "Facture":
            self.liste_table.remove("Activité")
            self.liste_table.remove("Catégorie d'activité")
            self.liste_table.remove("Groupe")
            self.liste_table.remove("Inscription")
            self.liste_table.remove("Lieu")
            self.liste_table.remove("Type d'activité")
            self.liste_table.remove("Responsable")
        else:
            self.liste_table.remove("Article")
            self.liste_table.remove("Facture")
        sorted(self.liste_table)

        # Modifier la liste dans champs pour les widget existant
        self.modifier_liste_existante(row)

    def modifier_liste_existante(self, row):
        """Modifier la liste dans les ComboBox existant"""
        current_text = self.tbl_champs.cellWidget(row, 0).currentText()
        self.tbl_champs.cellWidget(row, 0).clear()
        self.tbl_champs.cellWidget(row, 0).addItems(self.liste_table)
        self.tbl_champs.cellWidget(row, 0).setCurrentText(current_text)

    def table_selectionnee(self, row):
        """
        Afficher les informations relative à la table sélectionnée
        dans les combobox colonne et contraintes
        """
        # Créer la liste des tables disponibles
        if row == 0:
            self.creer_liste_table(row)

        # Effacer le contenu existant
        self.tbl_champs.cellWidget(row, 1).clear()
        self.tbl_champs.cellWidget(row, 2).clear()

        # Déterminer le nom de la table
        table = self.tbl_champs.cellWidget(row, 0).currentText()

        # Afficher les champs pour la colonne et le constrainte
        if table == "Activité":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_ACTIVITE)
            self.afficher_contraintes(row)
        elif table == "Article":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_ARTICLE)
            self.afficher_contraintes(row)
        elif table == "Catégorie d'activité":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_CATEGORIE_ACTIVITE)
            self.afficher_contraintes(row)
        elif table == "Facture":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_FACTURE)
            self.afficher_contraintes(row)
        elif table == "Groupe":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_GROUPE)
            self.afficher_contraintes(row)
        elif table == "Inscription":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_INSCRIPTION)
            self.afficher_contraintes(row)
        elif table == "Lieu":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_LIEU)
            self.afficher_contraintes(row)
        elif table == "Membre":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_MEMBRE)
            self.afficher_contraintes(row)
        elif table == "Participante":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_PARTICIPANTE)
            self.afficher_contraintes(row)
        elif table == "Responsable":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_RESPONSABLE)
            self.afficher_contraintes(row)
        elif table == "Type d'activité":
            self.tbl_champs.cellWidget(row, 1).addItems(self.LISTE_COLONNE_TYPE_ACTIVITE)
            self.afficher_contraintes(row)

    def afficher_contraintes(self, row):
        """Afficher les contraintes dans le combobox"""
        if self.verifier_nombre_table():
            self.tbl_champs.cellWidget(row, 2).addItems(self.LISTE_CONTRAINTE_MEME_TABLE)
        else:
            self.tbl_champs.cellWidget(row, 2).addItems(self.LISTE_CONTRAINTE_AUTRE_TABLE)
        
    def verifier_nombre_table(self):
        """Vérifie le nombre de table présentes dans le tableau"""
        lastText = self.tbl_champs.cellWidget(0, 0).currentText()
        for r in range(self.tbl_champs.rowCount()-1):
            for c in range(self.tbl_champs.columnCount()-1):
                currentText = self.tbl_champs.cellWidget(r, c).currentText()
                if lastText != currentText:
                    return False
        return True

    def afficher_option_tri(self):
        """Afficher les options de tri"""
        liste_table = []
        # Ajouter les éléments à la liste
        for r in range(self.tbl_champs.rowCount()-1):
            for c in range(self.tbl_champs.columnCount()-1):
                text = self.tbl_champs.cellWidget(r, c).currentText()
                if text == "Activité":
                    liste_table = set(liste_table).add("Activité")
                    liste_table = set(liste_table).add("Catégorie d'activité")
                    liste_table = set(liste_table).add("Type d'activité")
                elif text == "Article":
                    liste_table = set(liste_table).add("Article")
                    liste_table = set(liste_table).add("Facture")
                elif text == "Catégorie d'activité":
                    liste_table = set(liste_table).add("Catégorie d'activité")
                    liste_table = set(liste_table).add("Responsable")
                    liste_table = set(liste_table).add("Type d'activité")
                    liste_table = set(liste_table).add("Lieu")
                elif text == "Facture":
                    liste_table = set(liste_table).add("Facture")
                    liste_table = set(liste_table).add("Participante")
                    liste_table = set(liste_table).add("Membre")
                elif text == "Groupe":
                    liste_table = set(liste_table).add("Groupe")
                    liste_table = set(liste_table).add("Activité")
                    liste_table = set(liste_table).add("Catégorie d'activité")
                    liste_table = set(liste_table).add("Type d'activité")
                elif text == "Inscription":
                    liste_table = set(liste_table).add("Inscription")
                    liste_table = set(liste_table).add("Activité")
                    liste_table = set(liste_table).add("Catégorie d'activité")
                    liste_table = set(liste_table).add("Type d'activité")
                    liste_table = set(liste_table).add("Participante")
                    liste_table = set(liste_table).add("Membre")
                elif text == "Lieu":
                    liste_table = set(liste_table).add("Lieu")
                elif text == "Membre":
                    liste_table = set(liste_table).add("Participante")
                    liste_table = set(liste_table).add("Membre")
                elif text == "Participante":
                    liste_table = set(liste_table).add("Participante")
                elif text == "Responsable":
                    liste_table = set(liste_table).add("Responsable")
                elif text == "Type d'activité":
                    liste_table = set(liste_table).add("Type d'activité")
        sorted(liste_table)
