"""
Module contenant les QCompleter utilisée dans les dialogs

Tout les QCompleter utilisés doivent être déclarée dans ce module. 

Méthodes:
    ville_completer : Création d'un QCompleter contenant toutes les villes couvertes par le centre de femmes
"""


# PyQt import
from PyQt5.QtWidgets import QCompleter

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
