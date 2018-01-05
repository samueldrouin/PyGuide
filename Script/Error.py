# PyQt import
from PyQt5.QtWidgets import QMessageBox

class DatabaseError(object):
    """Message d'erreur pour la base de donnee"""

class DataError(object):
    """Message d'erreur pour les donnees"""
    # Définition des textes
    NUMERO_TELEPHONE_INVALIDE = "Numéro de téléphone invalide"
    NUMERO_TELEPHONE_INEXISTANT_INFORMATION = "Il n'existe aucun compte à ce numéro de téléphone. Vérifiez que le " \
                                              "numéro est entré correctement."
    NUMERO_TELEPHONE_INVALIDE_INFORMATION = "Veuillez entrer un numéro de téléphone valide."

    AUCUN_COMPTE = "Aucun compte"
    AUCUN_ARTICLE = "Aucune activité sélectionnée"
    AUCUN_ARTICLE_INFORMATION = "Veuillez sélectionner une activité à ajouter."

    @classmethod
    def numero_telephone_inexistant(self):
        """Indiquer à l'utilisateur qu'il n'existe pas de compte avec ce numero"""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.AUCUN_COMPTE)
        msgbox.setText(self.AUCUN_COMPTE)
        msgbox.setInformativeText(self.NUMERO_TELEPHONE_INEXISTANT_INFORMATION)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @classmethod
    def numero_telephone_invalide(self):
        """Indique à l'utilisateur que le numero de telephone est invalide"""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.NUMERO_TELEPHONE_INVALIDE)
        msgbox.setText(self.NUMERO_TELEPHONE_INVALIDE)
        msgbox.setInformativeText(self.NUMERO_TELEPHONE_INVALIDE_INFORMATION)
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()

    @classmethod
    def aucun_article_selectionne(self):
        """Indique à l'utilisateur qu'aucun article n'est sélectionné"""
        msgbox = QMessageBox()
        msgbox.setWindowTitle(self.AUCUN_ARTICLE)
        msgbox.setText(self.AUCUN_ARTICLE)
        msgbox.setInformativeText(self.AUCUN_ARTICLE_INFORMATION)
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.Ok)
        msgbox.setDefaultButton(QMessageBox.Ok)
        msgbox.exec()
