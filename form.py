"""Classe de base des dialogs"""

# PyQt import
from PyQt5.QtWidgets import QDialog, QCompleter, QMessageBox
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator


class Form(QDialog):
    """Classe de base des dialogs"""
    # Constante definition
    STATUS_INSCRIPTION_ANNULEE = 0
    STATUS_INSCRIPTION = 1
    STATUS_FACTURE = 2
    STATUS_REMBOURSE = 3

    @staticmethod
    def address_validator():
        """
        RegExp validator for address
        :return: Address RexExpValidator
        """
        validator = QRegExpValidator(QRegExp("^[0-9a-zA-ZÀ-ÿ -.]+$"))
        return validator

    @staticmethod
    def name_validator():
        """
        RegExp validator for name
        :return: Name RegExpValidator
        """
        validator = QRegExpValidator(QRegExp("^[a-zA-ZÀ-ÿ -]+$"))
        return validator

    @staticmethod
    def zip_code_validator():
        """
        RegExp validator for canadian zip code
        :return: Zip Code RegExpValidator
        """
        validator = QRegExpValidator(QRegExp("^[A-Za-z]{1}[0-9]{1}[A-Za-z]{1}[0-9 ]{1}[0-9]{1}[A-Za-z]{1}[0-9]{1}$"))
        return validator

    @staticmethod
    def phone_validator():
        """
        RegExp validator for phone number
        :return: Phone number RegExpValidator
        """
        validator = QRegExpValidator(QRegExp("^[0-9]{3}[0-9 ]{1}[0-9]{3}[0-9-]{1}[0-9]{4}$"))
        return validator

    @staticmethod
    def poste_validator():
        """
        RegExp validator for poste
        :return: Poste RegExpValidator
        """
        validator = QRegExpValidator(QRegExp("^[0-9]{0,5}$"))
        return validator

    @staticmethod
    def numero_membre_validator():
        """
        RegExp validator for member number
        :return: Member number RegExpValidator
        """
        validator = QRegExpValidator(QRegExp("^[0-9]{0,10}$"))
        return validator

    @staticmethod
    def email_validator():
        """
        RegExp validator for email
        :return: Email RegExpValidator
        """
        validator = QRegExpValidator(QRegExp("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,4}$"))
        return validator

    @staticmethod
    def ville_completer():
        """
        Haut-Richelieu cities completer
        :return: Completer
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

    @staticmethod
    def check_string(value):
        """
        Check if the string s is empty for SQLite
        :param s: String
        :return: String or None
        """
        if not value:
            value = None
        return value

    @staticmethod
    def check_int(value):
        """
        Convert s to an int for SQLite
        :param s: String
        :return: Int or None
        """
        if value == "":
            value = None
        else:
            int(value)
        return value

    @staticmethod
    def check_phone_number(value):
        """
        Convert s to phone number for SQLite
        :param s: String
        :return: Phone number Int or None
        """
        if value != "":
            value = value.replace(" ", "")
            value = value.replace("-", "")
            value = int(value)
        else:
            value = None
        return value

    @staticmethod
    def xstr(value):
        """
        Return and empty string instead of None
        :param s: String or None
        :return: String or empty string
        """
        if not value:
            value = ''
        return value

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
