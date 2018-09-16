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

"""Sélection d'un élément"""
# Python import
import os
from pathlib import Path

# PyQt import
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView, QDialog

# Interface import
from interface.ui_selection import Ui_Selection


class Selection(QDialog, Ui_Selection):
    """Dialog pour la sélection d'un élément"""
    def __init__(self):
        super(Selection, self).__init__()
        self.setupUi(self)

        # Slots
        self.table_widget.itemClicked.connect(self.accept)

        # Paramètre du tableau
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def get_value(self):
        """
        Obtenir la valeur de l'index selectionne
        :return: Nombre de l'index
        """
        return self.table_widget.item(self.table_widget.currentRow(), 0).text()

    def afficher_liste(self, lst):
        """
        Afficher la liste d'items dans le TableWidget
        :param lst: Liste de dictionnaire (la liste ne doit pas être vide)
        """

        # Paramètres du table widget
        self.table_widget.setRowCount(len(lst))

        row = 0
        for dictionary in lst:
            column = 0
            for item in dictionary:
                self.table_widget.setItem(row, column, QTableWidgetItem(str(dictionary[item])))
                column = column + 1
            row = row + 1


class SelectionParticipante(Selection):
    """Dialog pour la sélection d'une participante"""
    def __init__(self, lst):
        super(SelectionParticipante, self).__init__()

        # Paramètres de la table
        self.table_widget.setColumnCount(2)
        headers = ["INDEX", "Nom"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setColumnHidden(0, True)

        # Afficher la liste
        self.afficher_liste(lst)


class SelectionStatistique(Selection):
    """Dialog pour la sélection d'une statistique"""
    def __init__(self, lst):
        super(SelectionStatistique, self).__init__()

        # Paramètres de la table
        self.table_widget.setColumnCount(2)
        headers = ["FICHIER", "Nom"]
        self.table_widget.setHorizontalHeaderLabels(headers)
        self.table_widget.setColumnHidden(0, True)

        # Afficher la liste
        self.afficher_liste(lst)
