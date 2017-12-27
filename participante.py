# Python import
from PyQt5.QtWidgets import QCompleter, QMessageBox
from PyQt5.QtCore import Qt, QDate
from PyQt5 import uic
import os

# Project import
from inscription_membre import InscriptionMembre
from form import Form


class Participante(Form):
    def __init__(self):
        super(Participante, self).__init__()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'participante.ui')
        uic.loadUi(ui, self)

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

        # Completer
        self.txt_ville.setCompleter(self.ville_completer())

        # Default date values
        # Annee de naissance
        current_date = QDate.currentDate()
        self.ded_date_naissance.setDate(current_date)

        # Slots
        self.btn_cancel.clicked.connect(self.close)
        self.txt_code_postal.cursorPositionChanged.connect(self.zip_code_parsing)
        self.txt_telephone1.cursorPositionChanged.connect(self.phone_number_parsing)
        self.txt_telephone2.cursorPositionChanged.connect(self.phone_number_parsing)
        self.chk_membre.clicked.connect(self.nouveau_membre)
        self.chk_honoraire.clicked.connect(self.set_honoraire)
        self.btn_add.clicked.connect(self.check_fields)

    def check_fields(self):
        """
        Check if every required fields are filled
        """
        if self.txt_prenom.text() is not None:
            if self.txt_telephone1 is not None:
                self.prepare_data()
        else:
            msgbox = QMessageBox()
            msgbox.setWindowTitle("Information manquante")
            if self.txt_prenom.text() is None and self.txt_telephone1 is None:
                msgbox.setInformativeText("Le prénom et le premier numéro de téléphone doivent être valide")
            elif self.txt_prenom.text() is not None and self.txt_telephone1 is None:
                msgbox.setInformativeText("Le premier numéro de téléphone doit être valide")
            elif self.txt_prenom.text() is None and self.txt_telephone1 is not None:
                msgbox.setInformativeText("Le prénom doit être valide")
            msgbox.setIcon(QMessageBox.Warning)
            msgbox.setStandardButtons(QMessageBox.Ok)
            msgbox.setDefaultButton(QMessageBox.Ok)
            msgbox.exec()

    def prepare_data(self):
        """
        Prepare des donnees du formulaire pour l'envoie a la base de donnees
        """
        fields = []
        fields.append(self.cbx_appelation.currentText())
        fields.append(self.txt_prenom.text())

        nom = self.txt_nom.text()
        if nom is "":
            nom = None
        fields.append(nom)

        address1 = self.txt_adresse1.text()
        if address1 is "":
            address1 = None
        fields.append(address1)

        address2 = self.txt_adresse2.text()
        if address2 is "":
            address2 = None
        fields.append(address2)

        ville = self.txt_ville.text()
        if ville is "":
            ville = None
        fields.append(ville)
        fields.append(self.cbx_province.currentText())

        code_postal = self.txt_code_postal.text()
        if code_postal is "":
            code_postal = None
        fields.append(code_postal)

        phone_number1 = self.txt_telephone1.text()
        if phone_number1 is not "":
            phone_number1 = phone_number1.replace(" ", "")
            phone_number1 = phone_number1.replace("-", "")
            phone_number1 = int(phone_number1)
        else:
            phone_number1 = None
        fields.append(phone_number1)

        poste1 = self.txt_poste1.text()
        if poste1 is not "":
            poste1 = int(poste1)
        else:
            poste1 = None
        fields.append(poste1)

        phone_number2 = self.txt_telephone2.text()
        if phone_number2 is not "":
            phone_number2 = phone_number2.replace(" ", "")
            phone_number2 = phone_number2.replace("-", "")
            phone_number2 = int(phone_number2)
        else:
            phone_number2 = None
        fields.append(phone_number2)

        poste2 = self.txt_poste2.text()
        if poste2 is not "":
            poste2 = int(poste2)
        else:
            poste2 = None
        fields.append(poste2)

        annee_naissance = self.ded_date_naissance.date().toJulianDay()
        fields.append(annee_naissance)

        fields.append(self.sbx_personnes_nourries.value())

        fields.append(self.cbx_photo.isChecked())

        self.process_data(fields)

    def process_data(self, prepared_data):
        pass

    def set_honoraire(self):
        """
        Confirme que le status du membre doit etre change pour honoraire
        """
        msgbox = QMessageBox()
        msgbox.setWindowTitle("Inscription d'un membre honoraire")
        msgbox.setText("Inscription d'un membre honoraire")
        msgbox.setInformativeText("Êtes-vous certain de vouloir inscrire ce membre comme honoraire")
        msgbox.setIcon(QMessageBox.Information)
        msgbox.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        msgbox.setDefaultButton(QMessageBox.Yes)
        ret = msgbox.exec()

        if ret == QMessageBox.No:
            self.chk_honoraire.setChecked(False)

    def nouveau_membre(self):
        """
        Ouvre la fenetre pour inscrire un nouveau membre
        """
        inscription_membre = InscriptionMembre()
        inscription_membre.inscrit.connect(self.membre_inscrit)
        inscription_membre.cancelled.connect(self.inscription_annulee)
        inscription_membre.exec()

    def membre_inscrit(self):
        """
        Indique que le membre est inscrit
        """
        self.chk_membre.setChecked(True)
        self.chk_membre.setEnabled(False)

        # Activation du membre
        self.chk_actif.setChecked(True)

        # Indiquer la date de renouvellement par defaut
        if QDate.currentDate().month() > 9:
            annee_renouvellement = QDate.currentDate().year()+1
        else:
            annee_renouvellement = QDate.currentDate().year()

        date_renouvellement = QDate(annee_renouvellement,9,1)
        self.ded_renouvellement.setDate(date_renouvellement)

        # Afficher les informations du membre
        self.chk_actif.setHidden(False)
        self.lbl_numero_membre.setHidden(False)
        self.txt_numero_membre.setHidden(False)
        self.chk_honoraire.setHidden(False)
        self.lbl_renouvellement.setHidden(False)
        self.ded_renouvellement.setHidden(False)


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


class NouvelleParticipante(Participante):
    def __init__(self, database):
        super(NouvelleParticipante, self).__init__()

        # Instance variable definition
        self.database = database

        # Titre de la fenetre
        self.setWindowTitle("Nouvelle participante")
        self.lbl_title.setText("Nouvelle participante")

        # Cacher les informations du membre
        self.chk_actif.setHidden(True)
        self.lbl_numero_membre.setHidden(True)
        self.txt_numero_membre.setHidden(True)
        self.chk_honoraire.setHidden(True)
        self.lbl_renouvellement.setHidden(True)
        self.ded_renouvellement.setHidden(True)

    def process_data(self, prepared_data):
        c = self.connection.cursor()

