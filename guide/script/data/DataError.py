"""
Module contenant les messages d'erreur concernant les données entrées par l'utilisateur

Les messages d'erreur de la base de donnée sont gérés par la classe DatabaseError

Méthodes : 
    numero_telephone_inexistant : Affiche un message d'erreur qui indique à l'utilisateur qu'il n'existe pas de compte avec ce numero
    numero_telephone_invalide : Affiche un message d'erreur qui indique à l'utilisateur que le numero de telephone est invalide
    aucun_article_selectionne : Affiche un message d'erreur qui indique à l'utilisateur qu'aucun article n'est sélectionné
    activite_complete : Affiche un message d'erreur qui indique a l'utilisateur que l'activité sélectionnée est complète
    trop_champs : Affiche un message d'erreur qui indique a l'utilisateur qu'il y a trop de champs pour qu'ils puissent être affichés
    aucun_nom_statistique : Affiche un message d'erreur qui indique a l'utilisateur qu'une statistique doit avoir un nom pour pouvoir être enregistrée
    message_box_missing_information : Affiche un message d'erreur qui indique à l'utilisateur qu'une information est manquante dans un formulaire
    facturation_impossible : Affiche un message d'erreur qui indique à l'utilisateur d'une activité ne peut pas être facturée à deux reprises
    activite_contingentee : Affiche un message d'erreur qui indique à l'utilisateur que l'activité est contingentee
    remboursement_impossible : Affiche un message d'erreur qui indique à l'utilisateur que le remboursement de l'activité est impossible
"""

# PyQt import
from PyQt5.QtWidgets import QMessageBox

# Définition des messages d'erreur
ERREUR_DONNEE = "Donnée invalide"
INFORMATION_MANQUANTE = "Information manquante"

NUMERO_TELEPHONE_INVALIDE = "Numéro de téléphone invalide"
NUMERO_TELEPHONE_INEXISTANT_INFORMATION = "Il n'existe aucun compte à ce numéro de téléphone. Vérifiez que le " \
                                            "numéro est entré correctement."
NUMERO_TELEPHONE_INVALIDE_INFORMATION = "Veuillez entrer un numéro de téléphone valide."

AUCUN_COMPTE = "Aucun compte"
AUCUN_ARTICLE = "Aucune activité sélectionnée"
AUCUN_ARTICLE_INFORMATION = "Veuillez sélectionner une activité à ajouter."

ACTIVITE_COMPLETE = "Activité complète"
ACTIVITE_COMPLETE_INFORMATION = "La participante sera mise sur la liste d'attente."

TROP_CHAMPS = "Trop de champs"
TROP_CHAMPS_INFORMATION = "Il doit y avoir quatre champs ou moins pour pouvoir générer un PDF."

AUCUN_NOM = "Aucun nom"
AUCUN_NOM_STATISTIQUE = "La statistique doit avoir un nom pour pouvoir être enregistrée"

REQUETE_VIDE = "Requête vide"
REQUETE_VIDE_INFORMATION = "Impossible d'effectuer une requête vide. Ajoutez des champs à la requête puis réessayez."

FACTURATION_IMPOSSIBLE = "Facturation impossible"
FACTURATION_IMPOSSIBLE_INFORMATION = "Impossible de facturer une activité qui à déjà été facturée"

ACTIVITE_CONTINGENTEE = "Activité contingentée"
ACTIVITE_CONTINGENTEE_INFORMATION = "En continuant l'annulation, vous allez retirer à la participante sa priorité sur la liste. Voulez-vous continuer ? "

REMBOURSEMENT_IMPOSSIBLE = "Remboursement impossible"
REMBOURSEMENT_IMPOSSIBLE_INFORMATION = "Impossible de rembourser une activité qui n'a jamais été facturée"

def numero_telephone_inexistant():
    """
    Affiche un message d'erreur qui indique à l'utilisateur qu'il n'existe pas de compte avec ce numero

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERREUR_DONNEE)
    msgbox.setText(AUCUN_COMPTE)
    msgbox.setInformativeText(NUMERO_TELEPHONE_INEXISTANT_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def numero_telephone_invalide():
    """
    Affiche un message d'erreur qui indique à l'utilisateur que le numero de telephone est invalide
    
    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERREUR_DONNEE)
    msgbox.setText(NUMERO_TELEPHONE_INVALIDE)
    msgbox.setInformativeText(NUMERO_TELEPHONE_INVALIDE_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def aucun_article_selectionne():
    """
    Affiche un message d'erreur qui indique à l'utilisateur qu'aucun article n'est sélectionné

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERREUR_DONNEE)
    msgbox.setText(AUCUN_ARTICLE)
    msgbox.setInformativeText(AUCUN_ARTICLE_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def activite_complete():
    """
    Affiche un message d'erreur qui indique a l'utilisateur que l'activité sélectionnée est complète

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERREUR_DONNEE)
    msgbox.setText(ACTIVITE_COMPLETE)
    msgbox.setInformativeText(ACTIVITE_COMPLETE_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    msgbox.setDefaultButton(QMessageBox.Yes)
    return msgbox.exec()

def trop_champs():
    """
    Affiche un message d'erreur qui indique a l'utilisateur qu'il y a trop de champs pour qu'ils puissent être affichés

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERREUR_DONNEE)
    msgbox.setText(TROP_CHAMPS)
    msgbox.setInformativeText(TROP_CHAMPS_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def aucun_nom_statistique():
    """
    Affiche un message d'erreur qui indique a l'utilisateur qu'une statistique doit avoir un nom pour pouvoir être enregistrée

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERREUR_DONNEE)
    msgbox.setText(AUCUN_NOM)
    msgbox.setInformativeText(AUCUN_NOM_STATISTIQUE)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def requete_vide():
    """
    Affiche un message d'erreur qui indique a l'utilisateur que la requete est vide

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ERREUR_DONNEE)
    msgbox.setText(REQUETE_VIDE)
    msgbox.setInformativeText(REQUETE_VIDE_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def message_box_missing_information(text):
    """
    Affiche un message d'erreur qui indique à l'utilisateur qu'une information est manquante dans un formulaire

    Argument : 
        text : Texte informatif

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(INFORMATION_MANQUANTE)
    msgbox.setText(INFORMATION_MANQUANTE)
    msgbox.setInformativeText(text)
    msgbox.setIcon(QMessageBox.Warning)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def facturation_impossible():
    """
    Affiche un message d'erreur qui indique à l'utilisateur d'une activité ne peut pas être facturée à deux reprises

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(FACTURATION_IMPOSSIBLE)
    msgbox.setText(FACTURATION_IMPOSSIBLE)
    msgbox.setInformativeText(FACTURATION_IMPOSSIBLE_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()

def activite_contingentee():
    """
    Affiche un message d'erreur qui indique à l'utilisateur que l'activité est contingentee

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(ACTIVITE_CONTINGENTEE)
    msgbox.setText(ACTIVITE_CONTINGENTEE)
    msgbox.setInformativeText(ACTIVITE_CONTINGENTEE_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
    msgbox.setDefaultButton(QMessageBox.Yes)
    return msgbox.exec()

def remboursement_impossible():
    """
    Affiche un message d'erreur qui indique à l'utilisateur que le remboursement de l'activité est impossible

    Return :
        Sélection de l'utilisateur
    """
    msgbox = QMessageBox()
    msgbox.setWindowTitle(REMBOURSEMENT_IMPOSSIBLE)
    msgbox.setText(REMBOURSEMENT_IMPOSSIBLE)
    msgbox.setInformativeText(REMBOURSEMENT_IMPOSSIBLE_INFORMATION)
    msgbox.setIcon(QMessageBox.Information)
    msgbox.setStandardButtons(QMessageBox.Ok)
    msgbox.setDefaultButton(QMessageBox.Ok)
    return msgbox.exec()
