# PyQt import
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtSql import QSqlError

class DatabaseError(object):
    """Message d'erreur pour la base de donnee"""

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

    # Définition des messages d'erreur
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

    @classmethod
    def sql_error_handler(self, err):
        """
        Gestion des erreurs SQLite
        :param err: QSqlError
        :return: True si erreur
        """
        # Paramètre commun à toute les MessageBox
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.BOX_TITLE)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)

        if err.type() == QSqlError.StatementError:
            msgbox.setText(self.ERREUR_STATEMENT)
            msgbox.setInformativeText(self.ERREUR_STATEMENT_INFORMATION)
            msgbox.setDetailedText(err.text())
            msgbox.exec()
            return True

        elif err.type() == QSqlError.TransactionError:
            msgbox.setText(self.ERREUR_TRANSACTION)
            msgbox.setInformativeText(self.ERREUR_TRANSACTION_INFORMATION)
            msgbox.setDetailedText(err.text())
            msgbox.exec()
            return True

        elif err.type() == QSqlError.ConnectionError:
            msgbox.setText(self.ERREUR_CONNECTION)
            msgbox.setInformativeText(self.ERREUR_CONNECTION_INFORMATION)
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
                msgbox.setWindowTitle(self.BOX_TITLE)
                if code == self.SQLITE_ERROR:
                    msgbox.setText(self.ERREUR_GENERIQUE)
                    msgbox.setInformativeText(self.ERREUR_GENERIQUE_INFORMATION)
                elif code == self.SQLITE_PERM:
                    msgbox.setText(self.ERREUR_PERM)
                    msgbox.setInformativeText(self.ERREUR_PERM_INFORMATION)
                elif code == self.SQLITE_BUSY:
                    msgbox.setText(self.ERREUR_DB_LOCKED)
                    msgbox.setInformativeText(self.ERREUR_DB_LOCKED_INFORMATION)
                elif code == self.SQLITE_LOCKED:
                    msgbox.setText(self.ERREUR_TABLE_LOCKED)
                    msgbox.setInformativeText(self.ERREUR_TABLE_LOCKED_INFORMATION)
                elif code == self.SQLITE_NOMEM:
                    msgbox.setText(self.ERREUR_MEMOIRE)
                    msgbox.setInformativeText(self.ERREUR_MEMOIRE_INFORMATION)
                elif code == self.SQLITE_READONLY:
                    msgbox.setText(self.ERREUR_PERM)
                    msgbox.setInformativeText(self.ERREUR_PERM_INFORMATION)
                elif code == self.SQLITE_IOERR:
                    msgbox.setText(self.ERREUR_DISQUE)
                    msgbox.setInformativeText(self.ERREUR_DISQUE_INFORMATION)
                elif code == self.SQLITE_CORRUPT:
                    msgbox.setText(self.ERREUR_CORRUPTION)
                    msgbox.setInformativeText(self.ERREUR_CORRUPTION_INFORMATION)
                elif code == self.SQLITE_NOTFOUND:
                    msgbox.setText(self.ERREUR_ACCES)
                    msgbox.setInformativeText(self.ERREUR_ACCES_INFORMATION)
                elif code == self.SQLITE_CANTOPEN:
                    msgbox.setText(self.ERREUR_OUVERTURE)
                    msgbox.setInformativeText(self.ERREUR_ACCES_INFORMATION)
                elif code == self.SQLITE_TOOBIG:
                    msgbox.setText(self.ERREUR_DONNEE)
                    msgbox.setInformativeText(self.ERREUR_TOOBIG_INFORMATION)
                elif code == self.SQLITE_CONSTRAINT:
                    msgbox.setText(self.ERREUR_DONNEE)
                    msgbox.setInformativeText(self.ERREUR_CONSTRAINT_INFORMATION)
                elif code == self.SQLITE_MISMATCH:
                    msgbox.setText(self.ERREUR_DONNEE)
                    msgbox.setInformativeText(self.ERREUR_MISMATCH_INFORMATION)
                elif code == self.SQLITE_NOTADB:
                    msgbox.setText(self.ERREUR_FICHIER)
                    msgbox.setInformativeText(self.ERREUR_FICHIER_INFORMATION)
                else:
                    msgbox.setText(self.ERREUR_UNHANDELED)
                    msgbox.setInformativeText(self.ERREUR_UNHANDELED_INFORMATION)
            msgbox.exec()

            return True
        return False


class DataError(object):
    """Message d'erreur pour les donnees"""
    # Définition des messages d'erreur
    ERREUR_DONNEE = "Donnée invalide"

    NUMERO_TELEPHONE_INVALIDE = "Numéro de téléphone invalide"
    NUMERO_TELEPHONE_INEXISTANT_INFORMATION = "Il n'existe aucun compte à ce numéro de téléphone. Vérifiez que le " \
                                              "numéro est entré correctement."
    NUMERO_TELEPHONE_INVALIDE_INFORMATION = "Veuillez entrer un numéro de téléphone valide."

    AUCUN_COMPTE = "Aucun compte"
    AUCUN_ARTICLE = "Aucune activité sélectionnée"
    AUCUN_ARTICLE_INFORMATION = "Veuillez sélectionner une activité à ajouter."

    ACTIVITE_COMPLETE = "Activité complète"
    ACTIVITE_COMPLETE_INFORMATION = "La participante sera mise sur la liste d'attente."

    TROP_CHAMPS = "Trop de champs"
    TROP_CHAMPS_INFORMATION = "Il doit y avoir quatre champs ou moins pour pouvoir générer un PDF."

    AUCUN_NOM = "Aucun nom"
    AUCUN_NOM_STATISTIQUE = "La statistique doit avoir un nom pour pouvoir être enregistrée"

    REQUETE_VIDE = "Requête vide"
    REQUETE_VIDE_INFORMATION = "Impossible d'effectuer une requête vide. Ajoutez des champs à la requête puis réessayez."

    @classmethod
    def numero_telephone_inexistant(self):
        """Indiquer à l'utilisateur qu'il n'existe pas de compte avec ce numero"""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.ERREUR_DONNEE)
        msgbox.setText(self.AUCUN_COMPTE)
        msgbox.setInformativeText(self.NUMERO_TELEPHONE_INEXISTANT_INFORMATION)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @classmethod
    def numero_telephone_invalide(self):
        """Indique à l'utilisateur que le numero de telephone est invalide"""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.ERREUR_DONNEE)
        msgbox.setText(self.NUMERO_TELEPHONE_INVALIDE)
        msgbox.setInformativeText(self.NUMERO_TELEPHONE_INVALIDE_INFORMATION)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @classmethod
    def aucun_article_selectionne(self):
        """Indique à l'utilisateur qu'aucun article n'est sélectionné"""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.ERREUR_DONNEE)
        msgbox.setText(self.AUCUN_ARTICLE)
        msgbox.setInformativeText(self.AUCUN_ARTICLE_INFORMATION)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @classmethod
    def activite_complete(self):
        """
        Indique a l'utilisateur que l'activité sélectionnée est complète
        :return: Sélection de l'utilisateur
        """
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.ERREUR_DONNEE)
        msgbox.setText(self.ACTIVITE_COMPLETE)
        msgbox.setInformativeText(self.ACTIVITE_COMPLETE_INFORMATION)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgbox.setDefaultButton(QMessageBox.Yes)
        return msgbox.exec()

    @classmethod
    def trop_champs(self):
        """
        Indique a l'utilisateur qu'il y a trop de champs pour qu'ils puissent être affichés
        """
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.ERREUR_DONNEE)
        msgbox.setText(self.TROP_CHAMPS)
        msgbox.setInformativeText(self.TROP_CHAMPS_INFORMATION)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @classmethod
    def aucun_nom_statistique(self):
        """
        Indique a l'utilisateur qu'une statistique doit avoir un nom pour pouvoir être enregistrée
        """
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.ERREUR_DONNEE)
        msgbox.setText(self.AUCUN_NOM)
        msgbox.setInformativeText(self.AUCUN_NOM_STATISTIQUE)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @classmethod
    def requete_vide(self):
        """
        Indique a l'utilisateur que la requete est vide
        """
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.ERREUR_DONNEE)
        msgbox.setText(self.REQUETE_VIDE)
        msgbox.setInformativeText(self.REQUETE_VIDE_INFORMATION)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()
