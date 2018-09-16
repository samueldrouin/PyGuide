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
