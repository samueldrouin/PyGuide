"""
Module contenant les validator utilisée dans les dialogs

Tout les validator utilisés doivent être déclarée dans ce module. 

Classes
    Validator : Validator utilisée dans les dialogs
"""

# PyQt import
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp

FILE_NAME_REGEXP = "^[0-9a-zA-Z]{3,45}$"
def file_name_validator():
        """
        Création d'un RegExpValidator pour les noms de fichier

        Return :
            File Name RegExpValidator
        """
        validator = QRegExpValidator(QRegExp(FILE_NAME_REGEXP))
        return validator

class Validator(object):
    """
    Validator utilisée dans les dialogs
    
    Méthodes : 

    """
    ADRESSE_REGEXP = "^[0-9a-zA-ZÀ-ÿ -.]+$"
    NAME_REGEXP = "^[a-zA-ZÀ-ÿ -]+$"
    ZIP_CODE_REGEXP = "^[A-Za-z]{1}[0-9]{1}[A-Za-z]{1}[0-9 ]{1}[0-9]{1}[A-Za-z]{1}[0-9]{1}$"
    PHONE_REGEXP = "^[0-9]{3}[0-9 ]{1}[0-9]{3}[0-9-]{1}[0-9]{4}$"
    POSTE_REGEXP = "^[0-9]{0,6}$"
    NUMERO_MEMBRE_REGEXP = "^[0-9]{0,6}$"
    EMAIL_REGEXP = "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Za-z]{2,4}$"
    FILE_NAME_REGEXP = "^[0-9a-zA-Z]{3,45}$"

    def address_validator(self):
        """
        RegExp validator pour les adresse

        Return : 
            Address RexExpValidator
        """
        validator = QRegExpValidator(QRegExp(self.ADRESSE_REGEXP))
        return validator

    def name_validator(self):
        """
        Création d'un RegExpValidator pour les noms

        Return : 
            Name RegExpValidator
        """
        validator = QRegExpValidator(QRegExp(self.NAME_REGEXP))
        return validator

    def zip_code_validator(self):
        """
        Création d'un RegExpValidator pour les codes postaux canadiens. 

        Seul les code postaux sous le format 'A0A 0A0' sont acceptables. 

        Return :
            Zip Code RegExpValidator
        """
        validator = QRegExpValidator(QRegExp(self.ZIP_CODE_REGEXP))
        return validator

    def phone_validator(self):
        """
        Création d'un RegExpValidator pour les numéro de téléphone. 

        Seul les numéro de téléphone sous le format '000 000-0000' sont acceptables. 

        Return :
            Phone number RegExpValidator
        """
        validator = QRegExpValidator(QRegExp(self.PHONE_REGEXP))
        return validator

    def poste_validator(self):
        """
        Création d'un RegExpValidator pour les postes téléphoniques

        Seul les postes contenant 6 chiffres ou moins sont acceptés. Cette limite est arbitraire et peut être modifiée au besoins. 

        Return : 
            Poste RegExpValidator
        """
        validator = QRegExpValidator(QRegExp(self.POSTE_REGEXP))
        return validator

    def numero_membre_validator(self):
        """
        Création d'un RegExpValidator pour le numéro de membre

        Seul les numéro de membre contenant 6 chiffres ou moins sont acceptés. Cette limite est arbitraire et peut-être modifiée au besoins. 
        
        Return :
            Member number RegExpValidator
        """
        validator = QRegExpValidator(QRegExp(self.NUMERO_MEMBRE_REGEXP))
        return validator

    def email_validator(self):
        """
        Création d'un RegExpValidator pour les adresse courriel

        Le validator oblige qu'une adresse soit structurée 'aaa@aaa.aa' tel que le nombre de a est illimité 
        sauf pour le domaine qui est limité à 4. Cependant, il n'empêche pas l'ajout d'une adresse qui ne contient 
        par de '@' ou de domaine. 

        Return :
            Email RegExpValidator
        """
        validator = QRegExpValidator(QRegExp(self.EMAIL_REGEXP))
        return validator
