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


# PyQt import
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlError


# Liste des code d'erreur SQLite
SQLITE_ERROR = 1 # Generic error
SQLITE_INTERNAL = 2 # Internal logic error in SQLite
SQLITE_PERM = 3 # Access permission denied
SQLITE_ABORT = 4 # Callback routine requested an abort
SQLITE_BUSY = 5 # The database file is locked
SQLITE_LOCKED = 6 # A table in the database is locked
SQLITE_NOMEM = 7 # A malloc() failed
SQLITE_READONLY = 8 # Attempt to write a readonly database
SQLITE_INTERRUPT = 9 # Operation terminated by sqlite3_interrupt()
SQLITE_IOERR = 10 # Some kind of disk I/O error occurred
SQLITE_CORRUPT = 11 # The database disk image is malformed
SQLITE_NOTFOUND = 12 # Unknown opcode in sqlite3_file_control()
SQLITE_FULL = 13 # Insertion failed because database is full
SQLITE_CANTOPEN = 14 # Unable to open the database file
SQLITE_PROTOCOL = 15 # Database lock protocol error
SQLITE_EMPTY = 16 # Internal use only
SQLITE_SCHEMA = 17 # The database schema changed 
SQLITE_TOOBIG = 18 # String or BLOB exceeds size limit
SQLITE_CONSTRAINT = 19 # Abort due to constraint violation
SQLITE_MISMATCH = 20 # Data type mismatch
SQLITE_MISUSE = 21 # Library used incorrectly
SQLITE_NOLFS = 22 # Uses OS features not supported on host
SQLITE_AUTH = 23 # Authorization denied 
SQLITE_FORMAT = 24 # Not used
SQLITE_RANGE = 25 # 2nd parameter to sqlite3_bind out of range
SQLITE_NOTADB = 26 # File opened that is not a database file
SQLITE_NOTICE = 27 # Notifications from sqlite3_log()
SQLITE_WARNING = 28 # Warnings from sqlite3_log()
SQLITE_ROW = 100 # sqlite3_step() has another row ready
SQLITE_DONE = 101 # sqlite3_step() has finished executing


# Définition du nom des fenêtres
BOX_TITLE = "Erreur de base de donnée"

# Définition des messages d'erreur pour les erreurs SQLite
ERREUR_GENERIQUE = "Erreur générique SQLite"
ERREUR_GENERIQUE_INFORMATION = "La transaction n'a pas pu être effectuée à cause d'une erreur générique. " \
                                "Veuillez réessayer."
    
ERREUR_PERM = "Accès interdit"
ERREUR_PERM_INFORMATION = "L'accès à la base de données est interdit. Assurez-vous d'avoir les permissions " \
                            "nécessaires pour y accéder."

ERREUR_DB_LOCKED = "Base de donnée verrouillée"
ERREUR_DB_LOCKED_INFORMATION = "Impossible d'accéder à la base de données."

ERREUR_TABLE_LOCKED = "Tableau de la base de données vérouillé"
ERREUR_TABLE_LOCKED_INFORMATION = "Impossible d'accéder à un tableau de la base de données."

ERREUR_DISQUE = "Erreur disque"
ERREUR_DISQUE_INFORMATION = "Erreur disque lors de la communication avec la base de données."

ERREUR_MEMOIRE = "Erreur mémoire"
ERREUR_MEMOIRE_INFORMATION = "Erreur lors de l'allocation de la mémoire."

ERREUR_CORRUPTION = "Base de données corrompue"
ERREUR_CORRUPTION_INFORMATION = "La base de données est corrompue et doit être réparée avant de pouvoir être utilisée à nouveau."

ERREUR_ACCES = "Base de données inaccessible"
ERREUR_OUVERTURE = "Impossible d'ouvrir la base de données"
ERREUR_ACCES_INFORMATION = "Vérifiez dans les réglages que le chemin vers la base de données est valide."

ERREUR_DONNEE = "Donnée invalide entrée"
ERREUR_TOOBIG_INFORMATION = "Le texte entré est trop long pour pouvoir être ajouté."
ERREUR_CONSTRAINT_INFORMATION = "Une contraine n'est pas respectée."
ERREUR_MISMATCH_INFORMATION = "Le format de donnée ne correspond pas à ce qui est attendu"

ERREUR_FICHIER = "Fichier invalide"
ERREUR_FICHIER_INFORMATION = "Le fichier sélectionné n'est pas une base de données valide. " \
                                "Veuillez modifier le fichier dans les réglages. "

ERREUR_UNHANDELED = "Erreur non gérée"
ERREUR_UNHANDELED_INFORMATION = "Cette erreur n'est pas gérée. Référez-vous au message d'erreur SQLite."

ERREUR_STATEMENT = "Erreur dans la requête"
ERREUR_STATEMENT_INFORMATION = "La requête n'a pas pu être effectuée."

ERREUR_TRANSACTION = "Erreur dans la transaction"
ERREUR_TRANSACTION_INFORMATION = "La transaction n'a pas pu être effectuée."

ERREUR_CONNECTION = "Erreur lors de la connection"
ERREUR_CONNECTION_INFORMATION = "La connection avec la base de données n'a pas pu être établie."

# Définition pour les messages d'erreurs gérés pour le programme
# Les définitions suivants incluent tous les messages qui ne sont pas gérés par
# la fonction sql_error_handler

AUCUNE_DATABASE = "Aucune base de donnée au chemin indiqué"
AUCUNE_DATABASE_INFORMATION = "La base de donnée n'existe plus au chemin indiqué dans les réglages. "\
                              "Veuillez sélectionner le nouvel emplacement de la base de données ou "\
                              "en créer une nouvelle."

ANCIENNE_VERSION = "Impossible d'ouvrir la base de données"
ANCIENNE_VERSION_INFORMATION = "La base de données est une ancienne version et ne peut être ouverte avec cette version du programme. " \
                               "Vous devez créer une nouvelle base de données pour continuer d'utiliser ce programme."


def sql_error_handler(err):
    """
    Gestion des erreurs SQLite
    :param err: QSqlError
    :return: True si erreur
    """
    # Paramètre commun à toute les MessageBox
    msgbox = QMessageBox()
    msgbox.setWindowTitle(BOX_TITLE)
    msgbox.setIcon(QMessageBox.Warning)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)

    if err.type() == QSqlError.StatementError:
        msgbox.setText(ERREUR_STATEMENT)
        msgbox.setInformativeText(ERREUR_STATEMENT_INFORMATION)
        msgbox.setDetailedText(err.text())
        msgbox.exec()
        return True

    elif err.type() == QSqlError.TransactionError:
        msgbox.setText(ERREUR_TRANSACTION)
        msgbox.setInformativeText(ERREUR_TRANSACTION_INFORMATION)
        msgbox.setDetailedText(err.text())
        msgbox.exec()
        return True

    elif err.type() == QSqlError.ConnectionError:
        msgbox.setText(ERREUR_CONNECTION)
        msgbox.setInformativeText(ERREUR_CONNECTION_INFORMATION)
        msgbox.setDetailedText(err.text())
        msgbox.exec()
        return True
    elif err.type() == QSqlError.UnknownError:
        # Informations sur l'erreur
        if err.nativeErrorCode() != "":
            code = int(err.nativeErrorCode())
            text = err.text()
            msgbox.setDetailedText(text)

            # Afficher le MessageBox
            msgbox = QMessageBox()
            msgbox.setWindowTitle(BOX_TITLE)
            if code == SQLITE_ERROR:
                msgbox.setText(ERREUR_GENERIQUE)
                msgbox.setInformativeText(ERREUR_GENERIQUE_INFORMATION)
            elif code == SQLITE_PERM:
                msgbox.setText(ERREUR_PERM)
                msgbox.setInformativeText(ERREUR_PERM_INFORMATION)
            elif code == SQLITE_BUSY:
                msgbox.setText(ERREUR_DB_LOCKED)
                msgbox.setInformativeText(ERREUR_DB_LOCKED_INFORMATION)
            elif code == SQLITE_LOCKED:
                msgbox.setText(ERREUR_TABLE_LOCKED)
                msgbox.setInformativeText(ERREUR_TABLE_LOCKED_INFORMATION)
            elif code == SQLITE_NOMEM:
                msgbox.setText(ERREUR_MEMOIRE)
                msgbox.setInformativeText(ERREUR_MEMOIRE_INFORMATION)
            elif code == SQLITE_READONLY:
                msgbox.setText(ERREUR_PERM)
                msgbox.setInformativeText(ERREUR_PERM_INFORMATION)
            elif code == SQLITE_IOERR:
                msgbox.setText(ERREUR_DISQUE)
                msgbox.setInformativeText(ERREUR_DISQUE_INFORMATION)
            elif code == SQLITE_CORRUPT:
                msgbox.setText(ERREUR_CORRUPTION)
                msgbox.setInformativeText(ERREUR_CORRUPTION_INFORMATION)
            elif code == SQLITE_NOTFOUND:
                msgbox.setText(ERREUR_ACCES)
                msgbox.setInformativeText(ERREUR_ACCES_INFORMATION)
            elif code == SQLITE_CANTOPEN:
                msgbox.setText(ERREUR_OUVERTURE)
                msgbox.setInformativeText(ERREUR_ACCES_INFORMATION)
            elif code == SQLITE_TOOBIG:
                msgbox.setText(ERREUR_DONNEE)
                msgbox.setInformativeText(ERREUR_TOOBIG_INFORMATION)
            elif code == SQLITE_CONSTRAINT:
                msgbox.setText(ERREUR_DONNEE)
                msgbox.setInformativeText(ERREUR_CONSTRAINT_INFORMATION)
            elif code == SQLITE_MISMATCH:
                msgbox.setText(ERREUR_DONNEE)
                msgbox.setInformativeText(ERREUR_MISMATCH_INFORMATION)
            elif code == SQLITE_NOTADB:
                msgbox.setText(ERREUR_FICHIER)
                msgbox.setInformativeText(ERREUR_FICHIER_INFORMATION)
            else:
                msgbox.setText(ERREUR_UNHANDELED)
                msgbox.setInformativeText(ERREUR_UNHANDELED_INFORMATION)
        msgbox.exec()

        return True
    return False


def aucune_database():
    """
    Affiche un message d'erreur qui indique à l'utilisateur qu'aucune base de donnée n'est sélectionnée

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(BOX_TITLE)
    msgbox.setText(AUCUNE_DATABASE)
    msgbox.setInformativeText(AUCUNE_DATABASE_INFORMATION)
    msgbox.setIcon(QMessageBox.Critical)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()


def ancienne_version():
    """
    Affiche un message d'erreur qui indique à l'utilisateur que la base de données enregistrée est une ancienne
    version qui ne peut être ouverte avec cette version du programme

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(BOX_TITLE)
    msgbox.setText(ANCIENNE_VERSION)
    msgbox.setInformativeText(ANCIENNE_VERSION_INFORMATION)
    msgbox.setIcon(QMessageBox.Critical)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()
