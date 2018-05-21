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

"""Modification des réglages du programme"""
# Python import
import os
from pathlib import Path

# PyQt import
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QSettings, QSize
from PyQt5.QtGui import QIcon

# Interface import
from interface.setting import Ui_Setting

# Resource import 
import resources

class Setting(QDialog, Ui_Setting):
    """Dialog permettant de modifier les réglages du programme"""
    def __init__(self):
        super(Setting, self).__init__()
        self.setupUi(self)

        # Afficher les images des boutons
        self.btn_fichier.setIcon(QIcon(":/global/Folder.png"))
        self.btn_statistique.setIcon(QIcon(":/global/Folder.png"))

        # Slots
        self.btn_cancel.clicked.connect(self.close)
        self.btn_fichier.clicked.connect(self.get_database_path)
        self.btn_statistique.clicked.connect(self.get_statistique_folder)
        self.btn_appliquer.clicked.connect(self.save_settings)

        # Charge les réglages existants
        self.load_current_settings()

    def load_current_settings(self):
        """
        Charge les réglages
        """
        settings = QSettings("SDR Soft", "PyGUIDE")
        database = settings.value("Database")
        statistique = settings.value("Statistique")
        self.txt_base_donnee.setText(database)
        self.txt_statistique.setText(statistique)

    def get_database_path(self):
        """
        Chemin vers la base de donnees
        """
        file_name = QFileDialog.getOpenFileName(self, "Ouvrir la base de données", str(Path.home()),
                                                "Base de donnée SQLite (*.guide)")
        self.txt_base_donnee.setText(os.path.abspath(file_name[0]))

    def get_statistique_folder(self):
        """
        Chemin vers le dossier statistiques
        """
        dialog = QFileDialog.getExistingDirectory(self, "Dossier pour enregistrer les fichers statistique", 
                                                  str(os.path.join(Path.home(), 'Documents')))

        self.txt_statistique.setText(os.path.abspath(folder))

    def save_settings(self):
        """
        Enregistre les reglages
        """
        settings = QSettings("SDR Soft", "PyGUIDE")
        settings.setValue("Database", self.txt_base_donnee.text())
        settings.setValue("Statistique", self.txt_statistique.text())
        self.close()
