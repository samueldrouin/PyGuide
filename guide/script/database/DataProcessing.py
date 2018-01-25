"""
Module permettant le traitement des données reçue ou envoyée à la base de donnée. 

Ce module est responsable seulement des étapes de traitement simple. Par exemple, il est responsable de vérifier si un string est vide
ou encore si une valeur doit être considérée comme nulle. Le traitement complexe des données ne soit pas être effectué par cette classe. 
Si une fonction doit traiter plus qu'une donnée, elle ne doit pas être placée ici. 

Méthodes : 
    check_string : Vérifie si un string le contenu d'un string
    check_int : Convertit un string en entier 
    check_phone_number : convertit un numéro de téléphone en nombre entier
"""

def check_string(str):
    """
    Vérifie si un string le contenu d'un string. 
    
    Arguments :
        value : string à vérifier

    Return : 
        String ou None (si le string est vide)
    """
    if not str:
        return None
    return str

def check_int(value):
    """
    Convertit un string en entier. 
    
    Arguments :
        value : string à vérifier

    Return : 
        Int ou None (si le string est vide)
    """
    if str == "":
        return None
    else:
        return int(str)

def check_phone_number(str):
    """
    Convertit un numéro de téléphone en nombre entier
    
    Arguments : 
        Value : string à convertir

    Return :
        Entier ou None (si le numéro de téléphone est vide)
    """
    if value:
        value = value.replace(" ", "")
        value = value.replace("-", "")
        return int(value)
    else:
        return None
