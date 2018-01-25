"""Création et modification des participantes"""

# Python import
import os

# PyQt import
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic

# Project import
from facturation.inscription_membre import NouvelleInscription, RenouvelerInscription
from form import Form
from script.database import Error
from script.interface import Validator
from script.interface import Completer
from facturation import facturation
from script.database import DataProcessing
from script.data import DataError

# Interface import
from interface.participante import Ui_Participante


class Participante(Form, Ui_Participante):
    """Dialog permettant la création et la modification des participantes"""
    def __init__(self, database):
        super(Participante, self).__init__()
        # Affichage de l'interface graphique
        self.setupUi(self)

        # Instance variable definition
        self.ID_PARTICIPANTE = None
        self.DATABASE = database

        # Validator
        self.txt_prenom.setValidator(Validator.name_validator())
        self.txt_nom.setValidator(Validator.name_validator())
        self.txt_adresse1.setValidator(Validator.address_validator())
        self.txt_adresse2.setValidator(Validator.address_validator())
        self.txt_ville.setValidator(Validator.name_validator())
        self.txt_code_postal.setValidator(Validator.zip_code_validator())
        self.txt_telephone1.setValidator(Validator.phone_validator())
        self.txt_poste1.setValidator(Validator.poste_validator())
        self.txt_telephone2.setValidator(Validator.phone_validator())
        self.txt_poste2.setValidator(Validator.poste_validator())
        self.txt_numero_membre.setValidator(Validator.numero_membre_validator())
        self.txt_email.setValidator(Validator.email_validator())

        # Completer
        self.txt_ville.setCompleter(Completer.ville_completer())

        # Cacher les informations du membre par default
        self.chk_actif.setHidden(True)
        self.lbl_numero_membre.setHidden(True)
        self.txt_numero_membre.setHidden(True)
        self.chk_honoraire.setHidden(True)
        self.lbl_renouvellement.setHidden(True)
        self.ded_renouvellement.setHidden(True)
        self.btn_renew.setHidden(True)

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.txt_code_postal.cursorPositionChanged.connect(self.afficher_code_postal)
        self.txt_telephone1.cursorPositionChanged.connect(self.set_parsed_phone_number)
        self.txt_telephone2.cursorPositionChanged.connect(self.set_parsed_phone_number)
        self.chk_membre.clicked.connect(self.nouveau_membre)
        self.btn_add.clicked.connect(self.check_fields)
        self.cbx_appelation.currentTextChanged.connect(self.appellation_changed)
        self.btn_renew.clicked.connect(self.renouveler_status_membre)

    def appellation_changed(self, text):
        """
        Change le nom selon l'appellation choisie
        """
        if text == "Mme." or text == "M." or text == "Autre" or text == "Employée":
            self.txt_nom.show()
            self.lbl_annee_naissance.show()
            self.sbx_annee_naissance.show()
            self.lbl_personne_nourries.show()
            self.sbx_personnes_nourries.show()
            self.lbl_consentement.show()
            self.cbx_photo.show()
            self.txt_prenom.setPlaceholderText("Prénom")
        else:
            self.txt_nom.hide()
            self.lbl_annee_naissance.hide()
            self.sbx_annee_naissance.hide()
            self.lbl_personne_nourries.hide()
            self.sbx_personnes_nourries.hide()
            self.lbl_consentement.hide()
            self.cbx_photo.hide()
            self.txt_prenom.setPlaceholderText(text)

    def check_fields(self):
        """
        Verifier si tout les champs requis sont completes
        :return: True si les donnees sont valides
        """
        if self.txt_prenom.text() != "":
            if len(self.txt_telephone1.text()) == 12:
                self.prepare_data()
                return True
            else:
                DataError.message_box_missing_information("Le premier numéro de téléphone doit être valide")
        else:
            if self.txt_prenom.text() == "" and len(self.txt_telephone1.text()) != 12:
                informative_text = "Le prénom et le premier numéro de téléphone doivent être valide"
            else:
                informative_text = "Le prénom doit être valide"
            DataError.message_box_missing_information(informative_text)
        return False

    def prepare_data(self):
        """
        Prepare des donnees du formulaire pour l'envoie a la base de donnees
        """
        fields = {}

        appelation = DataProcessing.check_string(self.cbx_appelation.currentText())
        fields['Appelation'] = appelation

        prenom = DataProcessing.check_string(self.txt_prenom.text())
        fields['Prenom'] = prenom

        nom = DataProcessing.check_string(self.txt_nom.text())
        fields['Nom'] = nom

        address1 = DataProcessing.check_string(self.txt_adresse1.text())
        fields['Address1'] = address1

        address2 = DataProcessing.check_string(self.txt_adresse2.text())
        fields['Address2'] = address2

        ville = DataProcessing.check_string(self.txt_ville.text())
        fields['Ville'] = ville

        province = DataProcessing.check_string(self.cbx_province.currentText())
        fields['Province'] = province

        code_postal = DataProcessing.check_string(self.txt_code_postal.text())
        fields['Code Postal'] = code_postal

        courriel = DataProcessing.check_string(self.txt_email.text())
        fields['Courriel'] = courriel

        phone_number1 = DataProcessing.check_phone_number(self.txt_telephone1.text())
        fields['Phone Number 1'] = phone_number1

        poste1 = DataProcessing.check_int(self.txt_poste1.text())
        fields['Poste 1'] = poste1

        phone_number2 = DataProcessing.check_phone_number(self.txt_telephone2.text())
        fields['Phone Number 2'] = phone_number2

        poste2 = DataProcessing.check_int(self.txt_poste2.text())
        fields['Poste 2'] = poste2

        annee_naissance = DataProcessing.check_int(self.sbx_annee_naissance.value())
        fields['Annee Naissance'] = annee_naissance

        personne_nourries = self.sbx_personnes_nourries.value()
        fields['Personne nourries'] = personne_nourries

        consentement_photo = self.cbx_photo.isChecked()
        fields['Consentement photo'] = consentement_photo

        self.process_data(fields)

    def process_data(self, prepared_data):
        """
        Requete SQLite
        Implante dans les subclass
        :param prepared_data: Donnees pour la requete SQLite
        """
        pass

    def renouveler_status_membre(self):
        """
        Ouvrir la fenetre pour renouveler le status de membre
        """
        if self.check_fields():
            # Préparation des parametres
            nom = self.txt_prenom.text() + " " + self.txt_nom.text()
            phone = self.txt_telephone1.text()

            # Ouverture de la fenetre d'inscription
            inscription_membre = RenouvelerInscription(nom, phone, self.ID_PARTICIPANTE,
                                                       self.DATABASE)
            inscription_membre.accepted.connect(self.show_member_informations)
            inscription_membre.exec()

    def nouveau_membre(self):
        """
        Ouvre la fenetre pour inscrire un nouveau membre
        """
        # Inscription du participant
        if self.check_fields():
            # Préparation des parametres
            nom = self.txt_prenom.text() + " " + self.txt_nom.text()
            phone = self.txt_telephone1.text()

            # Ouverture de la fenetre d'inscription
            inscription_membre = NouvelleInscription(nom, phone, self.ID_PARTICIPANTE,
                                                     self.DATABASE)
            inscription_membre.accepted.connect(self.show_member_informations)
            inscription_membre.rejected.connect(self.inscription_annulee)
            inscription_membre.exec()
        else:
            self.inscription_annulee()

    def inscription_annulee(self):
        """
        Active le status de membre
        """
        self.chk_membre.setChecked(False)

    def afficher_code_postal(self, old, new):
        """
        Affiche le code postal formatté
        :param old: Old cursor position
        :param new: New cursor position
        """
        code_postal = self.zip_code_parsing(old, new, self.sender().text())
        self.sender().setText(code_postal)

    def set_parsed_phone_number(self, old, new):
        """
        Parsing phone number
        :param old: Old cursor position
        :param new: New cursor position
        """
        phone_number = self.phone_number_parsing(old, new, self.sender().text())
        self.sender().setText(phone_number)

    def show_member_informations(self):
        """
        Afficher les informations sur le membre
        """
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                        "actif, "
                        "numero_membre, "
                        "membre_honoraire, "
                        "date_renouvellement "
                      "FROM "
                        "membre "
                      "WHERE "
                        "id_participante = :id_participante")
        query.bindValue(':id_participante', int(self.ID_PARTICIPANTE))
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        if query.first() and int(query.value(0)):
            # Afficher les champs du formulaire
            self.chk_actif.setHidden(False)
            self.txt_numero_membre.setHidden(False)
            self.lbl_numero_membre.setHidden(False)
            self.chk_honoraire.setHidden(False)
            self.ded_renouvellement.setHidden(False)
            self.lbl_renouvellement.setHidden(False)
            self.btn_renew.setHidden(False)

            # Ajouter les informations dans les champs
            self.chk_membre.setChecked(True)
            self.chk_membre.setEnabled(False)
            self.chk_actif.setChecked(True)
            self.txt_numero_membre.setText(str(query.value(1)))
            self.chk_honoraire.setChecked(int(query.value(2)))
            date = QDate.fromString(query.value(3), 'yyyy-MM-dd')
            self.ded_renouvellement.setDate(date)

            # Ne pas afficher la date de renouvellement pour un membre honoraire
            if self.chk_honoraire.isChecked():
                self.ded_renouvellement.setHidden(True)
                self.lbl_renouvellement.setHidden(True)


class NouvelleParticipante(Participante):
    """Dialog permettant la création de nouvelle participante"""
    def __init__(self, database):
        super(NouvelleParticipante, self).__init__(database)

        # Titre de la fenetre
        self.setWindowTitle("Nouvelle participante")
        self.lbl_title.setText("Nouvelle participante")

        # Cacher les transactions pour une nouvelle participante
        self.lbl_transaction.setHidden(True)
        self.tbl_transaction.setHidden(True)
        self.lbl_inscription.setHidden(True)
        self.tbl_inscription.setHidden(True)
        self.line.setHidden(True)

    def process_data(self, prepared_data):
        # Insert data
        query = QSqlQuery(self.DATABASE)
        query.prepare("INSERT INTO participante "
                        "(appellation, "
                        "prenom, "
                        "nom, "
                        "adresse_1, "
                        "adresse_2, "
                        "ville, "
                        "province, "
                        "code_postal, "
                        "courriel, "
                        "telephone_1, "
                        "poste_telephone_1, "
                        "telephone_2, "
                        "poste_telephone_2, "
                        "date_naissance, "
                        "personne_nourrie, "
                        "consentement_photo) "
                      "VALUES "
                        "(:appelation, "
                        ":prenom, "
                        ":nom, "
                        ":adresse1, "
                        ":adresse2, "
                        ":ville, "
                        ":province, "
                        ":codepostal, "
                        ":courriel, "
                        ":phone1, "
                        ":poste1, "
                        ":phone2, "
                        ":poste2, "
                      ":anneenaissance, :personnenourries, :consentementphoto)")
        query.bindValue(':appelation', prepared_data['Appelation'])
        query.bindValue(':prenom', prepared_data['Prenom'])
        query.bindValue(':nom', prepared_data['Nom'])
        query.bindValue(':adresse1', prepared_data['Address1'])
        query.bindValue(':adresse2', prepared_data['Address2'])
        query.bindValue(':ville', prepared_data['Ville'])
        query.bindValue(':province', prepared_data['Province'])
        query.bindValue(':codepostal', prepared_data['Code Postal'])
        query.bindValue(':courriel', prepared_data['Courriel'])
        query.bindValue(':phone1', prepared_data['Phone Number 1'])
        query.bindValue(':poste1', prepared_data['Poste 1'])
        query.bindValue(':phone2', prepared_data['Phone Number 2'])
        query.bindValue(':poste2', prepared_data['Poste 2'])
        query.bindValue(':anneenaissance', prepared_data['Annee Naissance'])
        query.bindValue(':personnenourries', prepared_data['Personne nourries'])
        query.bindValue(':consentementphoto', prepared_data['Consentement photo'])
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            # Continuer le traitement seulement si la requete reussie
            if self.sender() == self.btn_add:
                self.accept()
            else:
                # Fetch inserted participante_id
                query = QSqlQuery()
                query.exec_("SELECT last_insert_rowid()")
                Error.DatabaseError.sql_error_handler(query.lastError())
                query.first()
                self.ID_PARTICIPANTE = query.value(0)


class ModifierParticipante(Participante):
    """Dialog permettant la modification de participante"""
    def __init__(self, participante_id, database):
        super(ModifierParticipante, self).__init__(database)

        # Instance variable definition
        self.ID_PARTICIPANTE = participante_id

        # Titre de la fenetre
        self.setWindowTitle("Modifier une participante")
        self.lbl_title.setText("Modifier une participante")

        # Interface graphique
        self.btn_add.setText("Modifier")

        # Afficher les informations de la participante
        self.show_participante_informations()
        self.afficher_transaction()
        self.afficher_inscription()

        # Affiche les informations du membre s'il y en a
        self.show_member_informations()

    def afficher_transaction(self):
        """Afficher les transaction pour la participante"""
        # Obtenir la liste des transactions 
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                        "facture.date, "
                        "article.description, "
                        "article.prix "
                      "FROM facture "
                      "INNER JOIN article ON article.id_facture = facture.id_facture "
                      "WHERE facture.id_participante = :id_participante")
        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            return # Ne pas continuer avec des informations incompletes

        while(query.next()):
            # Préparation du tableau
            self.tbl_transaction.insertRow(self.tbl_transaction.rowCount())
            r = self.tbl_transaction.rowCount() - 1

            self.tbl_transaction.setItem(r, 0, QTableWidgetItem(str(query.value(1))))

            prix = "{0:.2f}$".format(query.value(2))
            self.tbl_transaction.setItem(r, 1, QTableWidgetItem(prix))

            date = QDateTime().fromString(query.value(0), 'yyyy-MM-dd hh:mm:ss').date().toString('dd MMM yyyy')
            self.tbl_transaction.setItem(r, 2, QTableWidgetItem(date))

    def afficher_inscription(self):
        """Afficher les inscription pour la participante"""
        # Obtenir la liste des transactions 
        query = QSqlQuery()
        query.prepare("SELECT "
                        "categorie_activite.nom, "
                        "activite.date, "
                        "activite.heure_debut, "
                        "activite.heure_fin "
                      "FROM inscription "
                      "LEFT JOIN activite "
                        "ON inscription.id_activite = activite.id_activite "
                      "LEFT JOIN categorie_activite "
                        "ON activite.id_categorie_activite = categorie_activite.id_categorie_activite "
                      "WHERE "
                        "(inscription.id_participante = :id_participante) "
                        "AND (activite.date >= :current_date) "
                        "AND (inscription.status = :status) "
                        "AND (activite.status = 1)"
                      "ORDER BY categorie_activite.nom ASC, activite.date ASC")
        query.bindValue(':id_participante', self.ID_PARTICIPANTE)
        query.bindValue(':current_date', QDate.currentDate().toString('yyyy-MM-dd'))
        query.bindValue(':status', facturation.STATUS_INSCRIPTION)
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if Error.DatabaseError.sql_error_handler(query.lastError()):
            return # Ne pas continuer avec des informations incompletes

        while(query.next()):
            # Préparation du tableau
            self.tbl_inscription.insertRow(self.tbl_inscription.rowCount())
            r = self.tbl_inscription.rowCount() - 1

            self.tbl_inscription.setItem(r, 0, QTableWidgetItem(str(query.value(0))))

            date = QDate().fromString(query.value(1), 'yyyy-MM-dd').toString('dd MMM yyyy')
            self.tbl_inscription.setItem(r, 1, QTableWidgetItem(date))

            heure_debut = QTime.fromString(query.value(2), 'HH:mm').toString('hh:mm')
            heure_fin = QTime.fromString(query.value(3), 'HH:mm').toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.tbl_inscription.setItem(r, 2, QTableWidgetItem(heure))

    def show_participante_informations(self):
        """
        Affiche les informations de la participante
        """

        # Get informations from database
        query = QSqlQuery(self.DATABASE)
        query.prepare("SELECT "
                        "appellation, "
                        "prenom, "
                        "nom, "
                        "adresse_1, "
                        "adresse_2, "
                        "ville, "
                        "province, "
                        "code_postal, "
                        "courriel, "
                        "telephone_1, "
                        "poste_telephone_1, "
                        "telephone_2, "
                        "poste_telephone_2, "
                        "date_naissance, "
                        "personne_nourrie, "
                        "consentement_photo "
                      "FROM "
                        "participante "
                      "WHERE "
                        "id_participante = :idparticipante")
        query.bindValue(':idparticipante', int(self.ID_PARTICIPANTE))
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        Error.DatabaseError.sql_error_handler(query.lastError())

        query.first()

        # Add informations to form
        self.cbx_appelation.setCurrentText(query.value(0))
        self.txt_prenom.setText(query.value(1))
        self.txt_nom.setText(query.value(2))
        self.txt_adresse1.setText(query.value(3))
        self.txt_adresse2.setText(query.value(4))
        self.txt_ville.setText(query.value(5))
        self.cbx_province.setCurrentText(query.value(6))
        self.txt_code_postal.setText(query.value(7))
        self.txt_email.setText(query.value(8))

        # Set phone number format
        telephone1_str = str(query.value(9))
        telephone1 = telephone1_str[:3] + " " + telephone1_str[3:6] + "-" + telephone1_str[6:]

        self.txt_telephone1.setText(telephone1)
        self.txt_poste1.setText(str(query.value(10)))

        # Set phone number 2 format if the phone number exist only
        if query.value(11):
            telephone2_str = str(query.value(11))
            telephone2 = telephone2_str[:3] + " " + telephone2_str[3:6] + "-" + telephone2_str[6:]
            self.txt_telephone2.setText(telephone2)

        self.txt_poste2.setText(str(query.value(12)))
        self.sbx_annee_naissance.setValue(int(query.value(13)))
        self.sbx_personnes_nourries.setValue(int(query.value(14)))

        if int(query.value(15)):
            self.cbx_photo.setChecked(True)
        else:
            self.cbx_photo.setChecked(False)

        self.show_member_informations()

    def process_data(self, prepared_data):
        query = QSqlQuery(self.DATABASE)
        query.prepare("UPDATE participante "
                      "SET "
                        "appellation = :appelation, "
                        "prenom = :prenom, "
                        "nom = :nom, "
                        "adresse_1 = :adresse1, "
                        "adresse_2 = :adresse2, "
                        "ville = :ville, "
                        "province = :province, "
                        "code_postal = :codepostal, "
                        "courriel = :courriel, "
                        "telephone_1 = :phone1, "
                        "poste_telephone_1 = :poste1, "
                        "telephone_2 = :phone2, "
                        "poste_telephone_2 = :poste2, "
                        "date_naissance = :anneenaissance, "
                        "personne_nourrie = :personnenourries, "
                        "consentement_photo = :consentementphoto "
                      "WHERE "
                        "id_participante = :id_participante")
        query.bindValue(':appelation', prepared_data['Appelation'])
        query.bindValue(':prenom', prepared_data['Prenom'])
        query.bindValue(':nom', prepared_data['Nom'])
        query.bindValue(':adresse1', prepared_data['Address1'])
        query.bindValue(':adresse2', prepared_data['Address2'])
        query.bindValue(':ville', prepared_data['Ville'])
        query.bindValue(':province', prepared_data['Province'])
        query.bindValue(':codepostal', prepared_data['Code Postal'])
        query.bindValue(':courriel', prepared_data['Courriel'])
        query.bindValue(':phone1', prepared_data['Phone Number 1'])
        query.bindValue(':poste1', prepared_data['Poste 1'])
        query.bindValue(':phone2', prepared_data['Phone Number 2'])
        query.bindValue(':poste2', prepared_data['Poste 2'])
        query.bindValue(':anneenaissance', prepared_data['Annee Naissance'])
        query.bindValue(':personnenourries', prepared_data['Personne nourries'])
        query.bindValue(':consentementphoto', prepared_data['Consentement photo'])
        query.bindValue(':id_participante', int(self.ID_PARTICIPANTE))
        query.exec_()

        # Affichage d'un message d'erreur si la requete echoue
        if not Error.DatabaseError.sql_error_handler(query.lastError()):
            # Fermeture du dialog seulement si la requete reussie
            # et le signal vient du bouton add
            if self.sender() == self.btn_add:
                self.accept()
