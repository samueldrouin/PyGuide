import pymysql.cursors
from PyQt5.QtWidgets import QMessageBox


def handle_database_error(error):
    """
    Handle database error to show the appropriate error message
    :param error: Error from pymysql
    :return: None
    """
    code, msg = error.args # Get argument from pymysql error

    # Check the error code and show the appropriate warning
    if code == 1092:
        error_message("Erreur d'insertion",msg)


def error_message(title, msg):
    msgbox = QMessageBox
    msgbox.setText(title)
    msgbox.setInformativeText("Contactez l'administrateur de la base de données pour plus d'informations")
    msgbox.setDetailedText(msg)
    msgbox.setStandardButtons(QMessageBox.Close)
    msgbox.setDefaultButton(QMessageBox.Close)
