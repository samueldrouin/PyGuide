"""
Module contenant les messages d'erreur concernant les traitement des fichiers par le programme

Méthodes : 
    db_creation : Affiche un message d'erreur qui indique à l'utilisateur qu'il n'existe pas de compte avec ce numero
"""

# PyQt import
from PyQt5.QtWidgets import QMessageBox

# Définition des messages d'erreur
ERR_CREATION = "Erreur dans la création d'un fichier"

DB_CREATION = "Erreur dans la création de la base de données"
DB_CREATION_INFORMATION = "Erreur {} lors de la création de la base de données."


def db_creation(errno, errstr):
    """
    Affiche un message d'erreur si la base de données ne peut pas être créée

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERR_CREATION)
    msgbox.setText(DB_CREATION)
    msgbox.setInformativeText(DB_CREATION_INFORMATION.format(errno))
    msgbox.setDetailedText(errstr)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()
