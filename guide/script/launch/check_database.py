# This file is part of PyGuide.
#
# PyGuide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyGuide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyGuide.  If not, see <http://www.gnu.org/licenses/>.

"""
Module responsable de la vérification de l'état de la base de données. 

Ce module n'est responsable que de la vérification. Les modifications et des réparations 
sont effectuées par d'autre modules. 

Methode : 
    check_database_created : Vérifie qu'une base de donnée est enregistrée dans les réglages
    check_database_exist : Vérifie si la base de donnée enregistrée existe
    check_database_open : Vérifie si la base de données peut ouvrir
    check_table_module : Vérifier si la base de données contient la table de modules installés
    preparation_wizard : Ouvre l'assistant de préparation du programme GUIDE
"""


# Python import
import os.path

# PyQt import
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QSettings
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

# Project import
from guide.script.launch.preparation_wizard import PreparationWizard
from guide.script.database import database_error


def check_database_created():
    """
    Vérifie qu'une base de donnée est enregistrée dans les réglages. 

    Si aucune base de données n'existe, demande à l'utilisateur d'en créer une nouvelle. 
    """

    settings = QSettings("SDR Soft", "PyGUIDE")
    database = settings.value("Database")

    # Ouvrir un wizard pour créer une première base de donnée
    # si une base de donnée n'a pas déjà été créée dans les réglages
    if not database:
        preparation_wizard()

    # Continuer la vérification de la base de donnée
    return check_database_exist(database)
            

def check_database_exist(database):
    """
    Vérifie si la base de donnée enregistrée existe
    """

    # Ouvrir un wizard pour créer une première base de donnée
    # si le fichier de base de donnée n'existe plus
    if not os.path.isfile(database):
        # Indique à l'utilisateur que la base de donnée n'existe plus
        ret = database_error.aucune_database()

        # Ouvre l'assistance de préparation GUIDE pour modifier le chemin de la base de donnée
        if ret == QMessageBox.Ok:
            preparation_wizard()

    # Continuer la vérification de la base de donnée
    return check_database_open(database)


def check_database_open(database):
    """
    Vérifie si la base de données peut ouvrir
    """

    # Préparation de la connection à la base de donnée
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(database)

    # Vérifier si la base de données ouvre
    if db.open():
        # Continuer la vérification de la base de donnée
        return check_table_module(db)
    else:
        # Avertit l'utilisateur d'une erreur de connection et ferme le programme
        database_error.sql_error_handler(db.lastError())
        

def check_table_module(db):
    """
    Vérifier si la base de données contient la table de modules installés
    """

    # Obtenir les informations de la base de donnees
    query = QSqlQuery(db)
    query.prepare("SELECT count(*) "
                  "FROM sqlite_master "
                  "WHERE type='table' AND name='guide' ")
    query.exec_()

    # Affichage d'un message d'erreur si la requete echoue
    database_error.sql_error_handler(query.lastError())

    # Obtenir les informations
    query.first()
    count = query.value(0)

    # Vérifier si la table des modules installés existe
    if count:
        # Retourner la base de données
        return db
    else:
        # Indique à l'utilisateur qu'il s'agit d'une ancienne version de la base de donnée
        ret = database_error.ancienne_version()

        # Ouvre l'assistance de préparation GUIDE pour créer une nouvelle base de données
        if ret == QMessageBox.Ok:
            preparation_wizard()


def preparation_wizard():
    """
    Ouvre l'assistant de préparation du programme GUIDE
    """
    preparation_wizard = PreparationWizard()
    preparation_wizard.accepted.connect(check_database_created)
    preparation_wizard.exec()
    check_database_created()
