# Python import
from PyQt5.QtWidgets import QDialog, QFileDialog
from PyQt5.QtCore import QSettings
from PyQt5 import uic
import os
from pathlib import Path

class Settings(QDialog):
    def __init__(self):
        super(Settings, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'settings.ui')
        uic.loadUi(ui, self)

        # Slots
        self.btn_cancel.clicked.connect(self.close)
        self.btn_fichier.clicked.connect(self.get_database_path)
        self.btn_appliquer.clicked.connect(self.save_settings)

        # Charge les réglages existants
        self.load_current_settings()

    def load_current_settings(self):
        """
        Charge les réglages
        """
        settings = QSettings("Samuel Drouin", "GUIDE-CFR")
        database = settings.value("Database")
        self.txt_base_donnee.setText(database)

    def get_database_path(self):
        """
        Chemin vers la base de donnees
        """
        fileName = QFileDialog.getOpenFileName(self, "Ouvrir la base de données", str(Path.home()),
                                               "Base de donnée SQLite (*.GUIDE)")
        self.txt_base_donnee.setText(fileName[0])

    def save_settings(self):
        """
        Enregistre les reglages
        """
        settings = QSettings("Samuel Drouin", "GUIDE-CFR")
        settings.setValue("Database", self.txt_base_donnee.text())
        self.close()