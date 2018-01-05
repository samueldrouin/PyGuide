"""Création et modification des participantes"""

# Python import
import os

# PyQt import
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlQuery
from PyQt5 import uic

# Project import
from inscription_membre import NouvelleInscription, RenouvelerInscription
from form import Form


class Participante(Form):
    """Dialog permettant la création et la modification des participantes"""
    def __init__(self):
        super(Participante, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'participante.ui')
        uic.loadUi(ui, self)

        # Instance variable definition
        self.participante_id = None
        self.database = None

        # Validator
        self.txt_prenom.setValidator(self.name_validator())
        self.txt_nom.setValidator(self.name_validator())
        self.txt_adresse1.setValidator(self.address_validator())
        self.txt_adresse2.setValidator(self.address_validator())
        self.txt_ville.setValidator(self.name_validator())
        self.txt_code_postal.setValidator(self.zip_code_validator())
        self.txt_telephone1.setValidator(self.phone_validator())
        self.txt_poste1.setValidator(self.poste_validator())
        self.txt_telephone2.setValidator(self.phone_validator())
        self.txt_poste2.setValidator(self.poste_validator())
        self.txt_numero_membre.setValidator(self.numero_membre_validator())
        self.txt_email.setValidator(self.email_validator())

        # Completer
        self.txt_ville.setCompleter(self.ville_completer())

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
        self.txt_code_postal.cursorPositionChanged.connect(self.zip_code_parsing)
        self.txt_telephone1.cursorPositionChanged.connect(self.phone_number_parsing)
        self.txt_telephone2.cursorPositionChanged.connect(self.phone_number_parsing)
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
                msgbox = QMessageBox()
                msgbox.setWindowTitle("Information manquante")
                msgbox.setText("Information manquante")
                msgbox.setInformativeText("Le premier numéro de téléphone doit être valide")
                msgbox.setIcon(QMessageBox.Warning)
                msgbox.setStandardButtons(QMessageBox.Ok)
                msgbox.setDefaultButton(QMessageBox.Ok)
                msgbox.exec()
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Information manquante")
            msgbox.setText("Information manquante")
            if self.txt_prenom.text() == "" and len(self.txt_telephone1.text()) != 12:
                informative_text = "Le prénom et le premier numéro de téléphone doivent être valide"
            else:
                informative_text = "Le prénom doit être valide"
            msgbox.setInformativeText(informative_text)
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.exec()
        return False

    def prepare_data(self):
        """
        Prepare des donnees du formulaire pour l'envoie a la base de donnees
        """
        fields = {}

        appelation = self.check_string(self.cbx_appelation.currentText())
        fields['Appelation'] = appelation

        prenom = self.check_string(self.txt_prenom.text())
        fields['Prenom'] = prenom

        nom = self.check_string(self.txt_nom.text())
        fields['Nom'] = nom

        address1 = self.check_string(self.txt_adresse1.text())
        fields['Address1'] = address1

        address2 = self.check_string(self.txt_adresse2.text())
        fields['Address2'] = address2

        ville = self.check_string(self.txt_ville.text())
        fields['Ville'] = ville

        province = self.check_string(self.cbx_province.currentText())
        fields['Province'] = province

        code_postal = self.check_string(self.txt_code_postal.text())
        fields['Code Postal'] = code_postal

        courriel = self.check_string(self.txt_email.text())
        fields['Courriel'] = courriel

        phone_number1 = self.check_phone_number(self.txt_telephone1.text())
        fields['Phone Number 1'] = phone_number1

        poste1 = self.check_int(self.txt_poste1.text())
        fields['Poste 1'] = poste1

        phone_number2 = self.check_phone_number(self.txt_telephone2.text())
        fields['Phone Number 2'] = phone_number2

        poste2 = self.check_int(self.txt_poste2.text())
        fields['Poste 2'] = poste2

        if self.sbx_annee_naissance.value() == 0:
            annee_naissance = QDate(1,1,1).toJulianDay()
        else:
            annee_naissance = QDate(self.sbx_annee_naissance.value(), 1, 1).toJulianDay()
        fields['Annee Naissance'] = annee_naissance

        personne_nourries = self.sbx_personnes_nourries.value()
        fields['Personne nourries']  = personne_nourries

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
            inscription_membre = RenouvelerInscription(nom, phone, self.participante_id, self.database)
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
            inscription_membre = NouvelleInscription(nom, phone, self.participante_id, self.database)
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

    def zip_code_parsing(self, old, new):
        """
        Parsing zip code
        :param old: Old cursor position
        :param new: New cursor position
        """
        if new == 4 and old == 3:
            zip_code = self.txt_code_postal.text()
            if zip_code[3] != " ":
                zip_code = zip_code[:3] + " " + zip_code[3:]
                self.txt_code_postal.setText(zip_code)

    def phone_number_parsing(self, old, new):
        """
        Parsing phone number
        :param old: Old cursor position
        :param new: New cursor position
        """
        phone_number = self.sender().text()
        if new == 4 and old == 3:
            if phone_number[3] != " ":
                phone_number = phone_number[:3] + " " + phone_number[3:]
                self.sender().setText(phone_number)
        if new == 8 and old == 7:
            if phone_number[7] != "-":
                phone_number = phone_number[:7] + "-" + phone_number[7:]
                self.sender().setText(phone_number)

    def show_member_informations(self):
        """
        Afficher les informations sur le membre
        """
        query = QSqlQuery(self.database)
        query.prepare("SELECT actif, numero_membre, membre_honoraire, date_renouvellement "
                      "FROM membre WHERE id_participante = :id_participante")
        query.bindValue(':id_participante', int(self.participante_id))
        query.exec_()

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
            date = QDate.fromJulianDay(int(query.value(3)))
            self.ded_renouvellement.setDate(date)

            # Ne pas afficher la date de renouvellement pour un membre honoraire
            if self.chk_honoraire.isChecked():
                self.ded_renouvellement.setHidden(True)
                self.lbl_renouvellement.setHidden(True)


class NouvelleParticipante(Participante):
    """Dialog permettant la création de nouvelle participante"""
    def __init__(self, database):
        super(NouvelleParticipante, self).__init__()

        # Instance variable definition
        self.database = database

        # Titre de la fenetre
        self.setWindowTitle("Nouvelle participante")
        self.lbl_title.setText("Nouvelle participante")

    def process_data(self, prepared_data):
        # Insert data
        query = QSqlQuery(self.database)
        query.prepare("INSERT INTO participante (appellation, prenom, nom, adresse_1, adresse_2, ville, province, code_postal," \
              "courriel, telephone_1, poste_telephone_1, telephone_2, poste_telephone_2, date_naissance, " \
              "personne_nourrie, consentement_photo) " \
              "VALUES (:appelation, :prenom, :nom, :adresse1, :adresse2, :ville, :province, :codepostal, "
                      ":courriel, :phone1, :poste1, :phone2, :poste2, :anneenaissance, :personnenourries, "
                      ":consentementphoto)")
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

        if self.sender() == self.btn_add:
            self.accept()
        else:
            # Fetch inserted participante_id
            query = QSqlQuery()
            query.exec_("SELECT last_insert_rowid()")
            query.first()
            self.participante_id = query.value(0)


class ModifierParticipante(Participante):
    """Dialog permettant la modification de participante"""
    def __init__(self, participante_id, database):
        super(ModifierParticipante, self).__init__()

        # Instance variable definition
        self.database = database
        self.participante_id = participante_id

        # Titre de la fenetre
        self.setWindowTitle("Modifier une participante")
        self.lbl_title.setText("Modifier une participante")

        # Interface graphique
        self.btn_add.setText("Modifier")

        # Afficher les informations de la participante
        self.show_participante_informations()

        # Affiche les informations du membre s'il y en a
        self.show_member_informations()

    def show_participante_informations(self):
        """
        Affiche les informations de la participante
        """

        # Get informations from database
        query = QSqlQuery(self.database)
        query.prepare   ("SELECT appellation, prenom, nom, adresse_1, adresse_2, ville, province, code_postal," \
              "courriel, telephone_1, poste_telephone_1, telephone_2, poste_telephone_2, date_naissance, " \
              "personne_nourrie, consentement_photo FROM participante WHERE id_participante = :idparticipante")
        query.bindValue(':idparticipante', int(self.participante_id))
        query.exec_()

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
        self.sbx_annee_naissance.setValue(QDate.fromJulianDay(int(query.value(13))).year())
        self.sbx_personnes_nourries.setValue(int(query.value(14)))

        if int(query.value(15)):
            self.cbx_photo.setChecked(True)
        else:
            self.cbx_photo.setChecked(False)

        self.show_member_informations()

    def process_data(self, prepared_data):
        query = QSqlQuery(self.database)
        query.prepare("UPDATE participante "
                      "SET appellation = :appelation, prenom = :prenom, nom = :nom, adresse_1 = :adresse1, "
                      "adresse_2 = :adresse2, ville = :ville, province = :province, code_postal = :codepostal, "
                      "courriel = :courriel, telephone_1 = :phone1, poste_telephone_1 = :poste1, "
                      "telephone_2 = :phone2, poste_telephone_2 = :poste2, "
                      "date_naissance = :anneenaissance, personne_nourrie = :personnenourries, "
                      "consentement_photo = :consentementphoto "
                      "WHERE id_participante = :id_participante")
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
        query.bindValue(':id_participante', int(self.participante_id))
        query.exec_()

        if self.sender() == self.btn_add:
            self.accept()
