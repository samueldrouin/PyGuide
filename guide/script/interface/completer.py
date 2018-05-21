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

"""
Module contenant les QCompleter utilisée dans les dialogs

Tout les QCompleter utilisés doivent être déclarée dans ce module. 

Méthodes:
    ville_completer : Création d'un QCompleter contenant toutes les villes couvertes par le centre de femmes
"""


# PyQt import
from PyQt5.QtWidgets import QCompleter
from PyQt5.QtCore import Qt

def ville_completer():
        """
        Création d'un QCompleter contenant toutes les villes couvertes par le centre de femmes

        Return :
            QCompleter contenant les villes couverte par le centre de femmes
        """
        liste_ville = ["Saint-Jean-sur-Richelieu",
                       "Saint-Blaise-sur-Richelieu",
                       "Saint-Paul-de-l'Île-aux-Noix",
                       "Saint-Valentin", "Lacolle",
                       "Noyan",
                       "Saint-Sébastien",
                       "Henryville",
                       "Saint-Alexandre",
                       "Sainte-Anne-de-Sabrevois",
                       "Sainte-Brigide-d'Iberville",
                       "Mont-Saint-Grégoire",
                       "Venise-en-Québec",
                       "Saint-Georges-de-Clarenceville"]
        completer = QCompleter(liste_ville)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        return completer
