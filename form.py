# Python import
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5 import uic
import os


class Form(QDialog):
    def __init__(self):
        super(Form, self).__init__()

    @staticmethod
    def address_validator():
        """
        RegExp validator for address
        :return: Address RexExpValidator
        """
        v = QRegExpValidator(QRegExp("^[0-9a-zA-ZÀ-ÿ -.]{0,45}$"))
        return v

    @staticmethod
    def name_validator():
        """
        RegExp validator for name
        :return: Name RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[a-zA-ZÀ-ÿ -]{0,45}$"))
        return v

    @staticmethod
    def zip_code_validator():
        """
        RegExp validator for canadian zip code
        :return: Zip Code RegExpValidator
        """
        v = QRegExpValidator(QRegExp("^[A-Z]{1}[0-9]{1}[A-Z]{1}[0-9 ]{1}[0-9]{1}[A-Z]{1}[0-9]{1}$"))
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