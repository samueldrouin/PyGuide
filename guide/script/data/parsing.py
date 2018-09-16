# This file is part of PyGuide.
#
# PyGuide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyGuide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyGuide.  If not, see <http://www.gnu.org/licenses/>.

"""
Module permettant le parsing de certain textes nécessitant un affichage spécifique

Méthodes : 
    phone_number_parsing : Parsing des numéro de téléphone
    zip_code_parsing : Parsing des code postaux canadiens
"""


def phone_number_parsing(old, new, value):
    """
    Parsing des numéro de téléphone

    Argument :
        old : Ancienne position du curseur
        new : Nouvelle position du curseur
        str : Texte

    Return
        Parsed phone number
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


def zip_code_parsing(old, new, value):
    """
    Parsing des code postaux canadiens
    
    Arguments :
        old : Ancienne position du curseur
        new : Nouvelle position du curseur

    Return : 
        Parsed zip code
    """
    # Ajouter l'espace au code postal
    if new == 4 and old == 3:
        if value[3] != " ":
            value = value[:3] + " " + value[3:]

    # Retourner le code postal en majuscules
    return value.upper()
