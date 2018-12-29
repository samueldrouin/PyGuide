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
This module contains three classes that handle participant creation and modification :
    Participant: Base participant class that handle GUI function common to both subclasses
    NewParticipant: Class that manage functions specific to the dialog to create new participants
    UpdateParticipant: Class that manage functions specific to the dialog to update existing participants

While this module handle the participant management functions, it does not manage the member status since it's an
element of the billing module.
"""


# PyQt import
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QHBoxLayout, QCheckBox, QLineEdit, QDateEdit, QPushButton, \
    QSpacerItem, QSizePolicy, QLabel, QAbstractSpinBox
from PyQt5.QtCore import QDate, QTime, QDateTime
from PyQt5.QtSql import QSqlQuery

# Project import
from guide.facturation.inscription_membre import NouvelleInscription, RenouvelerInscription
from guide.facturation import facturation
from guide.script.database import database_error
from guide.script.database import data_processing
from guide.script.interface import validator
from guide.script.interface import completer
from guide.script.data import data_error
from guide.script.data import parsing
from guide.script.database import sqlite_query

# Interface import
from guide.interface.ui_participante import Ui_Participante


class _Participant(QDialog, Ui_Participante):
    """
    Base participant class that handle GUI function common to both NewParticipant and UpdateParticipant subclasses

    This class should contain all the interface functions, signals/slots connections and database processing common
    to both subclasses. This class can also contain context specific function that verify the called subclass to process
    data accordingly.

    This class should never be called directly.
    """

    def __init__(self, database):
        super(_Participant, self).__init__()
        # Affichage de l'interface graphique
        self.setupUi(self)

        # Instance variable definition
        self.ID_PARTICIPANTE = None
        self.DATABASE = database

        # Validator
        self.txt_prenom.setValidator(validator.name_validator())
        self.txt_nom.setValidator(validator.name_validator())
        self.txt_adresse1.setValidator(validator.address_validator())
        self.txt_adresse2.setValidator(validator.address_validator())
        self.txt_ville.setValidator(validator.name_validator())
        self.txt_code_postal.setValidator(validator.zip_code_validator())
        self.txt_telephone1.setValidator(validator.phone_validator())
        self.txt_poste1.setValidator(validator.poste_validator())
        self.txt_telephone2.setValidator(validator.phone_validator())
        self.txt_poste2.setValidator(validator.poste_validator())
        self.txt_email.setValidator(validator.email_validator())

        # Completer
        self.txt_ville.setCompleter(completer.ville_completer())

        # Slots
        self.btn_cancel.clicked.connect(self.reject)
        self.txt_code_postal.cursorPositionChanged.connect(self.set_parsed_zip_code)
        self.txt_telephone1.cursorPositionChanged.connect(self.set_parsed_phone_number)
        self.txt_telephone2.cursorPositionChanged.connect(self.set_parsed_phone_number)
        self.btn_inscription.clicked.connect(self.add_membership)
        self.btn_add.clicked.connect(self.process_data)
        self.cbx_appelation.currentTextChanged.connect(self.appellation_changed)
        self.resize(self.minimumSize())

    def appellation_changed(self, text):
        """
        Change l'apparence du dialog selon le type d'appelation sélectionnée
        """
        if text == "Mme." or text == "M." or text == "Autre" or text == "Employée":
            # Afficher le placeholder pour le prénom
            self.txt_prenom.setPlaceholderText("Prénom")

            # Ajouter les widget au grid layout et les afficher
            self.txt_nom.show() # Ne pas ajouter, appartient à un autre layout 

            self.lay_informations.addWidget(self.lbl_annee_naissance, 10, 0)
            self.lbl_annee_naissance.show()

            self.lay_informations.addWidget(self.sbx_annee_naissance, 10, 1)
            self.sbx_annee_naissance.show()

            self.lay_informations.addWidget(self.lbl_personne_nourries, 11, 0)
            self.lbl_personne_nourries.show()

            self.lay_informations.addWidget(self.sbx_personnes_nourries, 11, 1)
            self.sbx_personnes_nourries.show()

            self.lay_informations.addWidget(self.lbl_consentement, 12, 0)
            self.lbl_consentement.show()

            self.lay_informations.addWidget(self.cbx_photo, 12, 1)
            self.cbx_photo.show()
        else:
            # Afficher le placeholder pour le nom
            self.txt_prenom.setPlaceholderText(text)

            # Retirer les widgets du grid layout et les cacher
            self.txt_nom.hide() # Ne pas retirer, appartient à un autre layout 

            self.lay_informations.removeWidget(self.lbl_annee_naissance)
            self.lbl_annee_naissance.hide()

            self.lay_informations.removeWidget(self.sbx_annee_naissance)
            self.sbx_annee_naissance.hide()

            self.lay_informations.removeWidget(self.lbl_personne_nourries)
            self.lbl_personne_nourries.hide()

            self.lay_informations.removeWidget(self.sbx_personnes_nourries)
            self.sbx_personnes_nourries.hide()

            self.lay_informations.removeWidget(self.lbl_consentement)
            self.lbl_consentement.hide()

            self.lay_informations.removeWidget(self.cbx_photo)
            self.cbx_photo.hide()

        # Ajuster la taille du dialog
        self.resize(self.minimumSize())

    def check_fields(self):
        """
        Verify that all the required fields are complete and valid

        Returns :
            True if all the required fields are valid and complete
        """
        if self.txt_prenom.text() != "":
            if len(self.txt_telephone1.text()) == 12:
                return True
            else:
                data_error.message_box_missing_information("Le premier numéro de téléphone doit être valide.")
        else:
            if self.txt_prenom.text() == "" and len(self.txt_telephone1.text()) != 12:
                informative_text = "Le prénom et le premier numéro de téléphone doivent être valide."
            else:
                informative_text = "Le prénom doit être valide."
            data_error.message_box_missing_information(informative_text)
        return False

    def prepare_data(self):
        """
        Prepare the dialog form data to the format required for the database

        Return:
            Diactionary of the form data
        """
        return {
            'appellation': data_processing.check_string(self.cbx_appelation.currentText()),
            'prenom': data_processing.check_string(self.txt_prenom.text()),
            'nom': data_processing.check_string(self.txt_nom.text()),
            'adresse_1': data_processing.check_string(self.txt_adresse1.text()),
            'adresse_2': data_processing.check_string(self.txt_adresse2.text()),
            'ville': data_processing.check_string(self.txt_ville.text()),
            'province': data_processing.check_string(self.cbx_province.currentText()),
            'code_postal': data_processing.check_string(self.txt_code_postal.text()),
            'courriel': data_processing.check_string(self.txt_email.text()),
            'telephone_1': data_processing.check_phone_number(self.txt_telephone1.text()),
            'poste_telephone_1': data_processing.check_int(self.txt_poste1.text()),
            'telephone_2': data_processing.check_phone_number(self.txt_telephone2.text()),
            'poste_telephone_2': data_processing.check_int(self.txt_poste2.text()),
            'date_naissance': data_processing.check_int(self.sbx_annee_naissance.value()),
            'personne_nourrie': self.sbx_personnes_nourries.value(),
            'consentement_photo': self.cbx_photo.isChecked()
        }

    def process_data(self):
        """
        Process the prepared form data in the database. This function support both creation and update depending on
        the class name.
        """
        if self.check_fields():
            prepared_data = self.prepare_data()

            if prepared_data is not None:
                if self.__class__.__name__ == 'NewParticipant':
                    successfull_insert = sqlite_query.execute(
                        ":/member/participant/member/participant/create_participant_insert.sql",
                        prepared_data, self.DATABASE)

                    successfull_update = sqlite_query.execute(
                        ":/member/participant/member/participant/create_participant_update.sql",
                        prepared_data, self.DATABASE)
                    successfull = successfull_insert and successfull_update
                elif self.__class__.__name__ == 'UpdateParticipant':
                    successfull = sqlite_query.execute(":/member/participant/member/participant/update_participant.sql",
                                                       prepared_data, self.DATABASE)
                if successfull:
                    if self.sender() == self.btn_add:
                        self.accept()

    def renew_membership(self):
        """
        Open the dialog to renew the participant membership.
        """
        if self.check_fields():
            nom = self.txt_prenom.text() + " " + self.txt_nom.text()
            phone = self.txt_telephone1.text()

            inscription_membre = RenouvelerInscription(nom, phone, self.ID_PARTICIPANTE,
                                                       self.DATABASE)
            inscription_membre.accepted.connect(self.show_member_informations)
            inscription_membre.exec()

    def add_membership(self):
        """
        Open the dialog to start the participant membership.
        """
        if self.check_fields():
            nom = self.txt_prenom.text() + " " + self.txt_nom.text()
            phone = self.txt_telephone1.text()

            inscription_membre = NouvelleInscription(nom, phone, self.ID_PARTICIPANTE,
                                                     self.DATABASE)
            inscription_membre.accepted.connect(self.show_member_informations)
            inscription_membre.rejected.connect(self.member_inscription_canceled)
            inscription_membre.exec()
        else:
            self.member_inscription_canceled()

    def member_inscription_canceled(self):
        """
        Re-establish the non member state if the inscription is canceled
        """
        self.chk_membre.setChecked(False)

    def set_parsed_zip_code(self, old, new):
        """
        Parse the zip code and set the lineedit text to the parsed string.

        Arguments :
            old: Cursor old position
            new: Cursor new position
        """
        self.sender().setText(parsing.zip_code_parsing(old, new, self.sender().text()))

    def set_parsed_phone_number(self, old, new):
        """
        Parse the phone number and set the linedit text to the parsed string.

        Arguments :
            old: Cursor old position
            new: Cursor new position
        """
        self.sender().setText(parsing.phone_number_parsing(old, new, self.sender().text()))

    def show_member_informations(self):
        """
        Afficher les informations sur le membre
        """
        # Obtenir les informations de la base de données
        successfull, query = sqlite_query.execute(":/member/participant/member/participant/member_informations.sql",
                                                  {'id_participante': int(self.ID_PARTICIPANTE)}, self.DATABASE)

        if successfull and query.first() and int(query.value('actif')):
            self.add_member_ui_elements(bool(query.value('membre_honoraire')))
            self.chk_honoraire.setChecked(bool(query.value('membre_honoraire')))
            self.txt_numero_membre.setText(str(query.value('numero_membre')))

            if not bool(query.value('membre_honoraire')):
                date = QDate.fromString(query.value('date_renouvellement'), 'yyyy-MM-dd')
                self.ded_renouvellement.setDate(date)

    def add_member_ui_elements(self, honorary=False):
        """
        Add member ui elements to the dialog.

        Arguments :
            honorary: Honorary member
        """

        # Remove the new member button
        self.lay_status.removeItem(self.lay_membre)
        self.btn_inscription.hide()

        # Show the member status fields
        self.chk_membre.setChecked(True)
        self.chk_membre.setEnabled(False)

        self.chk_actif = QCheckBox("Actif")
        self.chk_actif.setEnabled(False)
        self.chk_actif.setChecked(True)

        self.chk_honoraire = QCheckBox("Honoraire")
        self.chk_honoraire.setEnabled(False)

        self.layout_membre = QHBoxLayout()
        self.layout_membre.addWidget(self.chk_actif)
        self.layout_membre.addWidget(self.chk_honoraire)
        self.layout_membre.addItem(QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout_membre.addStretch()
        self.lay_status.addLayout(self.layout_membre, 0, 1)

        # Show the member number fields
        self.layout_numero = QHBoxLayout()
        self.txt_numero_membre = QLineEdit()
        self.txt_numero_membre.setMinimumWidth(100)
        self.txt_numero_membre.setReadOnly(True)

        self.lbl_numero_membre = QLabel("Numéro de membre :")
        self.lbl_numero_membre.setMinimumWidth(150)
        self.lbl_numero_membre.setMaximumWidth(150)

        self.spacer_membre = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout_numero.addWidget(self.txt_numero_membre)
        self.layout_numero.addItem(self.spacer_membre)
        self.layout_numero.addStretch()

        self.lay_status.addWidget(self.lbl_numero_membre, 1, 0)
        self.lay_status.addLayout(self.layout_numero, 1, 1)

        # Show the renewal data fields
        if not honorary:
            self.ded_renouvellement = QDateEdit()
            self.ded_renouvellement.setReadOnly(True)
            self.ded_renouvellement.setButtonSymbols(QAbstractSpinBox.NoButtons)
            self.ded_renouvellement.setDisplayFormat("dd-MM-yyyy")
            self.ded_renouvellement.setCalendarPopup(False)

            self.btn_renouvellement = QPushButton("Renouvellement")
            self.btn_renouvellement.clicked.connect(self.renew_membership)

            self.lbl_renouvellement = QLabel("Date de renouvellement :")
            self.lbl_renouvellement.setMinimumWidth(150)
            self.lbl_renouvellement.setMaximumWidth(150)

            self.layout_renouvellement = QHBoxLayout()
            self.layout_renouvellement.addWidget(self.ded_renouvellement)
            self.layout_renouvellement.addItem(QSpacerItem(100, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
            self.layout_renouvellement.addWidget(self.btn_renouvellement)
            self.layout_renouvellement.addStretch()

            self.lay_status.addWidget(self.lbl_renouvellement, 2, 0)
            self.lay_status.addLayout(self.layout_renouvellement, 2, 1)

        self.resize(self.minimumSize())

    def show_transaction(self):
        """
        Show transactions made by the participant.
        """
        successfull, query = sqlite_query.execute(":/member/participant/member/participant/participant_transactions.sql",
                                                  {'id_participante': self.ID_PARTICIPANTE}, self.DATABASE)

        if successfull:
            while query.next():
                self.tbl_transaction.insertRow(self.tbl_transaction.rowCount())
                r = self.tbl_transaction.rowCount() - 1

                self.tbl_transaction.setItem(r, 0, QTableWidgetItem(str(query.value(1))))

                prix = "{0:.2f}$".format(query.value(2))
                self.tbl_transaction.setItem(r, 1, QTableWidgetItem(prix))

                date = QDateTime().fromString(query.value(0), 'yyyy-MM-dd hh:mm:ss').date().toString('dd MMM yyyy')
                self.tbl_transaction.setItem(r, 2, QTableWidgetItem(date))

    def show_participante_informations(self):
        """
        Affiche les informations de la participante
        """
        successfull, query = sqlite_query.execute(":/member/participant/member/participant/participant_informations.sql",
                                                  {'id_participante': int(self.ID_PARTICIPANTE)}, self.DATABASE)

        query.first()

        # Add informations to form
        self.cbx_appelation.setCurrentText(query.value('appellation'))
        self.txt_prenom.setText(query.value('prenom'))
        self.txt_nom.setText(query.value('nom'))
        self.txt_adresse1.setText(query.value('adresse_1'))
        self.txt_adresse2.setText(query.value('adresse_2'))
        self.txt_ville.setText(query.value('ville'))
        self.cbx_province.setCurrentText(query.value('province'))
        self.txt_code_postal.setText(query.value('code_postal'))
        self.txt_email.setText(query.value('courriel'))

        # Set phone number format
        telephone1_str = str(query.value('telephone_1'))
        telephone1 = telephone1_str[:3] + " " + telephone1_str[3:6] + "-" + telephone1_str[6:]

        self.txt_telephone1.setText(telephone1)
        self.txt_poste1.setText(str(query.value('poste_telephone_1')))

        # Set phone number 2 format if the phone number exist only
        if query.value('telephone_2'):
            telephone2_str = str(query.value('telephone_2'))
            telephone2 = telephone2_str[:3] + " " + telephone2_str[3:6] + "-" + telephone2_str[6:]
            self.txt_telephone2.setText(telephone2)

        self.txt_poste2.setText(str(query.value('poste_telephone_2')))
        self.sbx_annee_naissance.setValue(int(query.value('date_naissance')))
        self.sbx_personnes_nourries.setValue(int(query.value('personne_nourrie')))

        if int(query.value('consentement_photo')):
            self.cbx_photo.setChecked(True)
        else:
            self.cbx_photo.setChecked(False)

        self.show_member_informations()

    def show_inscription(self):
        """
        Show the participant inscriptions.
        """
        prepared_data = {
            'id_participante': int(self.ID_PARTICIPANTE),
            'current_date': QDate.currentDate().toString('yyyy-MM-dd'),
            'status': facturation.STATUS_INSCRIPTION
        }
        successfull, query = sqlite_query.execute(":/member/participant/member/participant/participant_inscription.sql",
                                                  prepared_data, self.DATABASE)

        while query.next():
            self.tbl_inscription.insertRow(self.tbl_inscription.rowCount())
            r = self.tbl_inscription.rowCount() - 1

            self.tbl_inscription.setItem(r, 0, QTableWidgetItem(str(query.value('categorie_activite.nom'))))

            date = QDate().fromString(query.value('activite.date'), 'yyyy-MM-dd').toString('dd MMM yyyy')
            self.tbl_inscription.setItem(r, 1, QTableWidgetItem(date))

            heure_debut = QTime.fromString(query.value('activite.heure_debut'), 'HH:mm').toString('hh:mm')
            heure_fin = QTime.fromString(query.value('activite.heure_fin'), 'HH:mm').toString('hh:mm')
            heure = heure_debut + " à " + heure_fin
            self.tbl_inscription.setItem(r, 2, QTableWidgetItem(heure))


class NewParticipant(_Participant):
    """Dialog permettant la création de nouvelle participante"""
    def __init__(self, database):
        super(NewParticipant, self).__init__(database)

        # Titre de la fenetre
        self.setWindowTitle("Nouvelle participante")
        self.lbl_title.setText("Nouvelle participante")

        # Cacher les transactions pour une nouvelle participante
        self.lbl_transaction.setHidden(True)
        self.tbl_transaction.setHidden(True)
        self.lbl_inscription.setHidden(True)
        self.tbl_inscription.setHidden(True)
        self.line.setHidden(True)
        self.resize(self.minimumSize())

    def add_membership(self):
        """
        Open the dialog to start the participant membership.

        This function is reimplanted to add the additionnal step to get the participant number after it's creation
        in order to
        """
        if self.check_fields():
            self.process_data()
            successfull, query = sqlite_query.execute(":/global/global/last_insert_rowid.sql", None, self.DATABASE)
            query.first()

            nom = self.txt_prenom.text() + " " + self.txt_nom.text()
            phone = self.txt_telephone1.text()

            self.ID_PARTICIPANTE = query.value(0)

            inscription_membre = NouvelleInscription(nom, phone, self.ID_PARTICIPANTE, self.DATABASE)
            inscription_membre.accepted.connect(self.show_member_informations)
            inscription_membre.rejected.connect(self.member_inscription_canceled)
            inscription_membre.exec()
        else:
            self.member_inscription_canceled()


class UpdateParticipant(_Participant):
    """Dialog permettant la modification de participante"""
    def __init__(self, participante_id, database):
        super(UpdateParticipant, self).__init__(database)

        # Instance variable definition
        self.ID_PARTICIPANTE = participante_id

        # Titre de la fenetre
        self.setWindowTitle("Modifier une participante")
        self.lbl_title.setText("Modifier une participante")

        # Interface graphique
        self.btn_add.setText("Modifier")

        # Afficher les informations de la participante
        self.show_participante_informations()
        self.show_transaction()
        self.show_inscription()
