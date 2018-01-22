"""
Module permettant de créer des statistiques. 

Le module n'est pas responsable de l'affichage ni du traitement vers la base de donnée. Il sert seulement à créer
des fichiers XML contenant les requetes à effectuer pour obtenir les statistiques. 

L'objectif est de fournir à l'utilisateur une interface simple et conviviale pour effectuer des requêtes SQLite
sans que l'utilisateur n'ai à écrire de code. 

Classes
    Statistiques : Dialog par lequel l'utilisateur peut créer des ficher de statistiques.
"""

# Python import
import os

# PyQt import
from PyQt5 import uic
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem
from PyQt5.QtCore import QSignalMapper, Qt
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtGui import QPalette

# Project import
from form import Form
from Script import Error
from Script.DataVerification import DataVerification

class Statistiques(Form):
    """
    Dialog par lequel l'utilisateur peut créer des ficher de statistiques.

    Le dialog est composé de deux tables : 
    1) La table des champs qui présente à l'utilisateur tout les champs de la base de donnée qu'ils peut intégrer
    aux statistiques. 
    2) La table de tri qui présente à l'utilisateur toute les options de tri qu'ils peut utiliser sur la base de donnée. 
    Cette table ne gère par le formattage des paramètres. L'utilisateur doit se référer au manuel d'utilisateur
    pour s'assurer de formatter convenablement les données. 

    Méthodes
        ajouter_ligne_champs : Ajoute une ligne à la table des champs
        creer_combo_box : Ajoute un ComboBox dans le tablea avec un mapping vers le numéro de ligne 
        remplire_combobox : Ajoute la liste d'un dictionnaire à un combobox
        colonne_champs_selectionnee : Affiche la ligne suivante dans la table des champs
        table_champs_selectionnee : Afficher les informations relative à la table sélectionnée
                                    dans les combobox colonne et contraintes
        set_style : Ajout du style aux lignes du tableau
        make_read_only : Disable le combobox de la ligne precedente
        generer_liste_table_champ : Générer le dictionnaire des tables à afficher dans les ComboBox du tableau des champs
        afficher_contraintes : Afficher les contraintes dans le combobox de la ligne précédente
        afficher_liste_table_ordre : Affiche la liste des tables dans le ComboBox de tri
        afficher_liste_colonne_ordre : Affiche la liste des colonnes dans le ComboBox de tri
        dictionnaire_colonne : Passer la valeur du dictionnaire des colonnes qui correspond à la table fournir
    """
    # Liste des contraintes
    CONTRAINTE_MEME_TABLE = ["et"]
    CONTRAINTE_AUTRE_TABLE = ["INNER JOIN", "LEFT JOIN", "CROSS JOIN"]
    OPERATEUR = ["=", ">", "<", "<=", ">="]

    # Dictionnaire des tables pertinentes de la base de donnée
    #   Key : Nom de la table
    #   Value : Nom pour l'affichage
    DICT_TABLE = {
                  'activite' : {'nom': 'Activité'},
                  'article' : {'nom': 'Article'},
                  'categorie_activite' : {'nom': 'Catégorie d\'activité'},
                  'facture' : {'nom': 'Facture'},
                  'groupe' : {'nom': 'Groupe'},
                  'inscription': {'nom': 'Inscription'},
                  'lieu' : {'nom': 'Lieu'},
                  'membre' : {'nom': 'Membre'},
                  'participante' : {'nom': 'Participante'},
                  'responsable' : {'nom': 'Responsable'},
                  'type_activite' : {'nom': 'Type d\'activité'}
                  }

    DICT_REFERENCE_TABLE = {
                            'activite' : 
                                {'to' : ['categorie_activite'],
                                 'from' : ['article', 'groupe', 'inscription']},
                            'article' : 
                                {'to' : ['facture', 'activite'], 
                                 'from' : []}, 
                            'categorie_activite' : 
                                {'to' : ['responsable', 'type_activite', 'lieu'],
                                 'from' : ['activite']},
                            'facture' : 
                                {'to' : ['participante'],
                                 'from' : ['article']},
                            'groupe' : 
                                {'to' : ['activite'],
                                 'from' : []},
                            'inscription' : 
                                {'to' : ['participante', 'activite'],
                                 'from' : []},
                            'lieu' : 
                                {'to' : [],
                                 'from' : ['categorie_activite']},
                            'membre' : 
                                {'to' : ['participante'],
                                 'from' : []},
                            'participante' : 
                                {'to' : [],
                                 'from' : ['facture', 'inscription', 'membre']},
                            'responsable' : 
                                {'to' : [],
                                 'from' : ['categorie_activite']},
                            'type_activite' : 
                                {'to' : [],
                                 'from' : ['categorie_activite']},
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
        self.liste_tri = [""] # Liste vide pour les tables du tri

        # Afficher la premier ligne
        self.ajouter_ligne_champ()

        # Slots
        self.btn_annuler.clicked.connect(self.reject)
        self.cbx_table.activated.connect(self.afficher_liste_colonne_ordre)

    """
    Méthodes communes aux deux types de table
    """

    def dictionnaire_colonne(self, table):
        """
        Passer la valeur du dictionnaire des colonnes qui correspond à la table fournir

        Arguments : 
            table : Identifiant d'une table

        Return : 
            Dictionnaire des colonnes pour cette table
        """
        # Afficher les champs pour la colonne et le constrainte
        if table == "activite":
            return self.DICT_ACTIVITE
        elif table == "article":
            return self.DICT_ARTICLE
        elif table == "categorie_activite":
            return self.DICT_CATEGORIE_ACTIVITE
        elif table == "facture":
            return self.DICT_FACTURE
        elif table == "groupe":
            return self.DICT_GROUPE
        elif table == "inscription":
            return self.DICT_INSCRIPTION
        elif table == "lieu":
            return self.DICT_LIEU
        elif table == "membre":
            return self.DICT_MEMBRE
        elif table == "participante":
            return self.DICT_PARTICIPANTE
        elif table == "responsable":
            return self.DICT_RESPONSABLE
        elif table == "type_activite":
            return self.DICT_TYPE_ACTIVITE

    def liste_table_champs(self):
        """
        Construire la liste des tables affichées dans le tableau des champs

        Toute les tables ne sont retournées qu'une seule fois. 

        Return : 
            Dictionnaire des tables sous le format {'database_label' : {'nom' : 'Nom de la table'}
        """
        dict_champs = {}
        # Gérérer la liste des tables
        for r in range(self.tbl_champs.rowCount()-1):
            table_label = self.tbl_champs.cellWidget(r, 0).currentData()
            if table_label:
                dict_champs[table_label] = {'nom' : self.DICT_TABLE[table_label]['nom']}

        return dict_champs

    def creer_combo_box(self, table, row, column, method):
        """
        Ajoute un ComboBox avec un mapping du signal "activated" pour transmettre la ligne
        du tableau plutôt que l'index du ComboBox au tableau des champs. 

        Arguments:
            table : Table auquel le ComboBox doit être ajouté
            row : Ligne du tableau à laquelle le ComboBox doit être ajouté
            column : Colonne du tableau à laquelle le ComboBox doit être ajouté
            method : Fonction qui sera connectée au mapping
        """
        # Créer un nouveau ComboBox
        cbx = QComboBox()

        # Ajouter un mapper pour transmettre la ligne du tableau plutôt que l'index du ComboBox
        # lorsque la valeur est modifiée
        mapper = QSignalMapper(self)
        mapper.setMapping(cbx, row)
        cbx.activated.connect(mapper.map)
        table.setCellWidget(row, column, cbx)
        mapper.setMapping(table, row)
        mapper.mapped[int].connect(method)

    def remplire_combobox(self, cbx, dict, ajouter_vide = True):
        """
        Ajoute la liste du dictionnaire à un combobox

        Le dictionnaire doit minimalement être sous la forme
            dict = {'database_label' : {'nom' : 'Nom de la table'}
        pour que cette fonction puisse être utilisée

        Arguments :
            cbx : ComboBox auquel les items doivent être ajoutés
            dict : Dictionnaire contenant le nom ainsi que le label dans la base de donnée
                   pour les items à ajouter
            ajouter_vide : Ajouter un champ vide au début du ComboBox
        """
        # Ajouter une ligne vide
        if ajouter_vide:
            cbx.addItem("")

        # Ajouter une éléments du dictionnaire
        for key, value in sorted(dict.items()):
            cbx.addItem(value['nom'], key)

    def set_row_style(self, table, row):
        """
        Ajout du style aux lignes du tableau

        Arguments :
            table : Tableau contenant la ligne
            row : Ligne dont le style sera modifieé
        """
        if row % 2:
            style = "QComboBox {\
                        border: 0px solid gray;\
                        background-color: #e9e7e3;\
                        font-size: 12px\
                     } \
                     QScrollBar:horizontal { \
                        border: 2px solid grey; \
                        background: #32CC99; \
                        height: 15px; \
                        margin: 0px 20px 0 20px; \
                     }\
                     QComboBox::drop-down {\
                        border: 0px; \
                     }\
                     QComboBox::down-arrow {\
                        image: url(Resources/DropDownArrow.png);\
                        width: 10px;\
                        height: 10px;\
                     }"
        else:
            style = "QComboBox {\
                        border: 0px solid gray;\
                        background-color: #ffffff;\
                        font-size: 12px\
                     } \
                     QScrollBar:horizontal { \
                        border: 2px solid grey; \
                        background: #32CC99; \
                        height: 15px; \
                        margin: 0px 20px 0 20px; \
                     }\
                     QComboBox::drop-down {\
                        border: 0px; \
                     }\
                     QComboBox::down-arrow {\
                        image: url(Resources/DropDownArrow.png);\
                        width: 10px;\
                        height: 10px;\
                     }"
        for c in range(table.columnCount()):
            if isinstance(table.cellWidget(row, c), QComboBox):
                table.cellWidget(row, c).setStyleSheet(style)

    """
    Gestion de la table des champs
    """

    def ajouter_ligne_champ(self):
        """
        Ajouter une ligne au tableau des champs
        
        Cette fonction ne peut pas être utilisée pour des deux tables puisque toute les fonction à appeler sont différentes
        """

        # Ajouter une ligne à la table
        self.tbl_champs.insertRow(self.tbl_champs.rowCount())
        r = self.tbl_champs.rowCount() - 1

        # ComboBox Table
        self.creer_combo_box(self.tbl_champs, r, 0, self.table_champs_selectionnee)
        self.remplire_combobox(self.tbl_champs.cellWidget(r, 0), self.generer_liste_table_champ(r))

        # Combobox colonne vide
        cbx_colonne = QComboBox()
        self.tbl_champs.setCellWidget(r, 1, cbx_colonne)

        # ComboBox contrainte vide
        cbx_contrainte = QComboBox()
        self.tbl_champs.setCellWidget(r, 2, cbx_contrainte)

        # Ajouter le style à la ligne
        self.set_row_style(self.tbl_champs, r)

    def generer_liste_table_champ(self, row):
        """
        Générer le dictionnaire des tables à afficher dans les ComboBox du tableau des champs.

        Seule les tables qui ont un foreign key sur la table de la ligne précédente sont affichée pour éviter
        de créer des requêtes qui sont impossibles. 

        Arguments : 
            row : Ligne sur laquelle le ComboBox est ajouté
        Return : 
            Dictionnaire des tables
        """
        # Afficher toute les tables pour la première colonne
        if row == 0:
            return self.DICT_TABLE
        # Afficher seulement les tables ayant une foreign key pour les colonnes suivantes
        else:
            # Obtenir la table de la rangee precendante
            last_table = self.tbl_champs.cellWidget(row-1, 0).currentData()

            # Créer la liste des tables ayant une référence vers ou de cette table
            reference_dict =  self.DICT_REFERENCE_TABLE[last_table]
            reference_to = reference_dict['to']
            reference_from = reference_dict['from']
            reference_list = reference_to + reference_from
            
            # Construire le dictionnaire à retourner
            dict = {}
            for reference in reference_list:
                dict[reference] = {'nom' : self.DICT_TABLE[reference]['nom']}

            return dict

    def table_champs_selectionnee(self, row):
        """
        Afficher les informations relative à la table sélectionnée
        dans les combobox colonne et contraintes

        Arguments : 
            row : Ligne du table qui a été activée
        """
        if not DataVerification.is_empty(self.tbl_champs.cellWidget(row, 0).currentText()):
            # Effacer le contenu existant
            self.tbl_champs.cellWidget(row, 1).clear()
            self.tbl_champs.cellWidget(row, 2).clear()

            # Déterminer le nom de la 

            table = self.tbl_champs.cellWidget(row, 0).currentData()

            # Afficher les champs pour la colonne et le constrainte
            dict_colonne = self.dictionnaire_colonne(table)
            self.remplire_combobox(self.tbl_champs.cellWidget(row, 1), dict_colonne)

            # Pour toute les rangees sauf la premiere
            if row != 0:
                self.afficher_contraintes(row) # Afficher les contraintes de la ligne precedente

            # Disable le combobox de la ligne
            self.make_read_only(row)

            # Ajout d'une nouvelle ligne
            self.ajouter_ligne_champ()

            # Ajouter les tables au ComboBox de tri
            self.afficher_liste_table_ordre()

            # Activer la table de tri
            self.activer_table_tri()

    def make_read_only(self, row):
        """
        Disable le combobox de la ligne precedente
        
        Cette méthode évite la création de combinaison impossible de table dans la requete. 

        Arguments : 
            row : Ligne du table pour laquelle une table vient être sélectionnée
        """
        if not DataVerification.is_empty(self.tbl_champs.cellWidget(row, 0).currentText()):
            self.tbl_champs.cellWidget(row, 0).setEnabled(False)

    def afficher_contraintes(self, row):
        """
        Afficher les contraintes dans le combobox de la ligne précédente
        Arguments :
            row : Ligne actuelle
        """
        # Ligne de la colonne précédente
        r = row - 1

        # Tableau des lignes actuelle et suivante
        last_table = self.tbl_champs.cellWidget(r, 0).currentText()
        current_table = self.tbl_champs.cellWidget(row, 0).currentText()
        
        if last_table == current_table:
            self.tbl_champs.cellWidget(r, 2).addItems(self.CONTRAINTE_MEME_TABLE)
        else:
            self.tbl_champs.cellWidget(r, 2).addItems(self.CONTRAINTE_AUTRE_TABLE)

    def activer_table_tri(self):
        """
        Ajoute le contenu à la table de tri

        Cette fonction est activée à chaque fois qu'un élément est ajouté à la table des champs. 
        Elle efface d'abord tout le contenu existante de la table de tri pour éviter la création d'erreur. 
        Cette fonctionnalité doit être gardée tant que la fonction n'est pas améliorée
        """
        self.tbl_tri.setRowCount(0)
        self.ajouter_ligne_tri()

    def ajouter_ligne_tri(self):
        """Ajouter une ligne au tableau du tri"""
        self.tbl_tri.insertRow(self.tbl_tri.rowCount())
        r = self.tbl_tri.rowCount() - 1

        # ComboBox Table
        self.creer_combo_box(self.tbl_tri, r, 0, self.table_tri_selectionnee)
        self.remplire_combobox(self.tbl_tri.cellWidget(r, 0), self.liste_table_champs())

        # Combobox colonne vide
        cbx_colonne = QComboBox()
        self.tbl_tri.setCellWidget(r, 1, cbx_colonne)

        # ComboBox opérateur
        cbx_operateur = QComboBox()
        self.tbl_tri.setCellWidget(r, 2, cbx_operateur)

        # Item vide
        self.tbl_tri.setItem(r, 3, QTableWidgetItem(""))

        # Ajouter le style à la ligne
        self.set_row_style(self.tbl_tri, r)

    def table_tri_selectionnee(self, row):
        """
        Afficher les informations relative à la table sélectionnée
        dans les combobox colonne et contraintes

        Arguments : 
            row : Ligne du table qui a été activée
        """
        if not DataVerification.is_empty(self.tbl_tri.cellWidget(row, 0).currentText()):
            # Effacer le contenu existant
            self.tbl_tri.cellWidget(row, 1).clear()
            self.tbl_tri.cellWidget(row, 2).clear()
            self.tbl_tri.item(row, 3).setText("")

            # Déterminer le nom de la table
            table = self.tbl_tri.cellWidget(row, 0).currentData()

            # Afficher les champs pour la colonne
            dict_colonne = self.dictionnaire_colonne(table)
            self.remplire_combobox(self.tbl_tri.cellWidget(row, 1), dict_colonne, ajouter_vide = False)

            # Afficher les champs pour l'opérateur
            self.tbl_tri.cellWidget(row, 2).addItems(self.OPERATEUR)

            # Pour toute les rangees sauf la premiere
            if row != 0:
                self.afficher_contraintes(row) # Afficher les contraintes de la ligne precedente

            # Ajout d'une nouvelle ligne
            self.ajouter_ligne_tri()

    def afficher_liste_table_ordre(self):
        """
        Affiche la liste des tables dans le ComboBox de tri

        La liste est mise à jours lorsqu'une table est ajoutée dans la table des champs
        """
        # Vider la liste existante
        self.cbx_table.clear()

        # Obtenir la liste des tables dans le tableau des champs
        dict_table = self.liste_table_champs()

        # Afficher les tables dans le ComboBox
        for key, value in sorted(dict_table.items()):
            self.cbx_table.addItem(value['nom'], key)

        # Afficher la liste des colonnes
        self.afficher_liste_colonne_ordre()

    def afficher_liste_colonne_ordre(self):
        """
        Affiche la liste des colonnes dans le ComboBox de tri

        La liste est mise à jours lorsque le ComboBox de tri contenant la table est modifié
        """
        # Vider la liste existante
        self.cbx_colonne.clear()

        # Obtenir la table sélectionnée
        current_data = self.cbx_table.currentData()
        dict_colonne = self.dictionnaire_colonne(current_data)

        # Afficher les colonnes dans le ComboBox
        for key, value in sorted(dict_colonne.items()):
            self.cbx_colonne.addItem(value['nom'], key)
