"""
Module permettant le traitement des données reçue ou envoyée à la base de donnée. 

Ce module est responsable seulement des étapes de traitement simple. Par exemple, il est responsable de vérifier si un string est vide
ou encore si une valeur doit être considérée comme nulle. Le traitement complexe des données ne soit pas être effectué par cette classe. 
Si une fonction doit traiter plus qu'une donnée, elle ne doit pas être placée ici. 

Classes
    DataVerification : Traitement de données reçue ou envoyée à la base de donnée
"""

class DataVerification(object):
    """
    Traitement de données reçue ou envoyée à la base de donnée

    Méthodes : 
        is_empty : Vérifie si un string est vide
    """

    @staticmethod
    def is_empty(string):
        """
        Vérifie si un string est vide. 

        Cette fonction ne vérifie pas si le string est nul, mais seulement s'il est vide ('')
        
        Arguments : 
            string : Valeur du string à vérifier
        Return : 
            True si le string est vide
            False si le string ne l'est pas
        """
        if string == "":
            return True
        else:
            return False
