from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp


"""
Update RegExp below
DO NOT change caracter limit unless database VARCHAR limit is updated
"""
name = "^[0-9a-zA-ZÀ-ÿ -]{0,45}$"
address = "^[0-9a-zA-ZÀ-ÿ -.]{0,45}$"
city = "^[a-zA-ZÀ-ÿ -]{0,45}$"

"""
This code pattern SHOULD NOT be changed
To create a new validator use the existing pattern
RegExp should be updated in global functions rather than in validator
"""


def address_validator():
    """
    RegExp validator for address

    Implemented in :
    Place address

    :return: Address RexExpValidator
    """
    v = QRegExpValidator(QRegExp(address))
    return v


def name_validator():
    """
    RegExp validator for address
    Allow numbers in name

    Implemented in :
    Place name

    :return: Name RexExpValidator
    """
    v = QRegExpValidator(QRegExp(name))
    return v


def city_validator():
    """
    RegExp validator for city

    Implemented in :
    Place city

    :return: City RegExpValidator
    """
    v = QRegExpValidator(QRegExp(city))
    return v