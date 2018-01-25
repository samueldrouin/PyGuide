"""Classe de base des dialogs"""

# PyQt import
from PyQt5.QtWidgets import QDialog, QCompleter, QMessageBox
from PyQt5.QtCore import Qt


class Form(QDialog):
    """Classe de base des dialogs"""
    @staticmethod
    def message_box_missing_information(text):
        """
        MessageBox lorsqu'une information est manquante dans un formulaire
        :param text: Informative text
        :return:
        """
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Information manquante")
        msgbox.setText("Information manquante")
        msgbox.setInformativeText(text)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @staticmethod
    def phone_number_parsing(old, new, value):
        """
        Parsing phone number
        :param old: Old cursor position
        :param new: New cursor position
        :param str: Current text string
        :return: Parsed phone number
        """
        # Ajouter le premier espace
        if new == 4 and old == 3:
            if value[3] != " ":
                phone_number = value[:3] + " " + value[3:]
                return phone_number
        # Ajouter le dash
        if new == 8 and old == 7:
            if value[7] != "-":
                phone_number = value[:7] + "-" + value[7:]
                return phone_number
        # Aucune modification ne doit être effectuée
        return value

    @staticmethod
    def zip_code_parsing(old, new, value):
        """
        Parsing zip code
        :param old: Old cursor position
        :param new: New cursor position
        :return: Code postal formatte
        """
        # Ajouter l'espace au code postal
        if new == 4 and old == 3:
            if value[3] != " ":
                value = value[:3] + " " + value[3:]

        # Retourner le code postal en majuscules
        return value.upper()
