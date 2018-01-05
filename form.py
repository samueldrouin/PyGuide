"""Classe de base des dialogs"""

# PyQt import
from PyQt5.QtWidgets import QDialog, QCompleter, QMessageBox
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator


class Form(QDialog):
    """Classe de base des dialogs"""

    @staticmethod
    def address_validator():
        """
        RegExp validator for address
        :return: Address RexExpValidator
        """
        v = QRegExpValidator(QRegExp("^[0-9a-zA-ZÀ-ÿ -.]+$"))
        return v

    @staticmethod
    def name_validator():
        """
        RegExp validator for name
        :return: Name RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[a-zA-ZÀ-ÿ -]+$"))
        return v

    @staticmethod
    def zip_code_validator():
        """
        RegExp validator for canadian zip code
        :return: Zip Code RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[A-Za-z]{1}[0-9]{1}[A-Za-z]{1}[0-9 ]{1}[0-9]{1}[A-Za-z]{1}[0-9]{1}$"))
        return v

    @staticmethod
    def phone_validator():
        """
        RegExp validator for phone number
        :return: Phone number RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[0-9]{3}[0-9 ]{1}[0-9]{3}[0-9-]{1}[0-9]{4}$"))
        return v

    @staticmethod
    def poste_validator():
        """
        RegExp validator for poste
        :return: Poste RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[0-9]{0,5}$"))
        return v

    @staticmethod
    def numero_membre_validator():
        """
        RegExp validator for member number
        :return: Member number RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[0-9]{0,10}$"))
        return v

    @staticmethod
    def email_validator():
        """
        RegExp validator for email
        :return: Email RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,4}$"))
        return v

    @staticmethod
    def ville_completer():
        """
        Haut-Richelieu cities completer
        :return: Completer
        """
        liste_ville = ["Saint-Jean-sur-Richelieu", "Saint-Blaise-sur-Richelieu", "Saint-Paul-de-l'Île-aux-Noix",
                       "Saint-Valentin", "Lacolle", "Noyan", "Saint-Sébastien", "Henryville", "Saint-Alexandre",
                       "Sainte-Anne-de-Sabrevois", "Sainte-Brigide-d'Iberville", "Mont-Saint-Grégoire",
                       "Venise-en-Québec", "Saint-Georges-de-Clarenceville"]
        c = QCompleter(liste_ville)
        c.setCaseSensitivity(Qt.CaseInsensitive)
        return c

    @staticmethod
    def check_string(str):
        """
        Check if the string s is empty for SQLite
        :param s: String
        :return: String or None
        """
        if not str:
            str = None
        return str

    @staticmethod
    def check_int(str):
        """
        Convert s to an int for SQLite
        :param s: String
        :return: Int or None
        """
        if str == "":
            str = None
        else:
            int(str)
        return str

    @staticmethod
    def check_phone_number(str):
        """
        Convert s to phone number for SQLite
        :param s: String
        :return: Phone number Int or None
        """
        if str != "":
            str = str.replace(" ", "")
            str = str.replace("-", "")
            str = int(str)
        else:
            str = None
        return str

    @staticmethod
    def xstr(str):
        """
        Return and empty string instead of None
        :param s: String or None
        :return: String or empty string
        """
        if not str:
            str = ''
        return str

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
