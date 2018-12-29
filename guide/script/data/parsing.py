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
    if new == 3 and old == 2:
        value = value + " "
    # Ajouter le dash
    if new == 7 and old == 6:
        value = value + "-"
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
    if new == 3 and old == 2:
        value = value + " "
    return value.upper()
