# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/ui/participante.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Participante(object):
    def setupUi(self, Participante):
        Participante.setObjectName("Participante")
        Participante.resize(925, 681)
        Participante.setMinimumSize(QtCore.QSize(925, 681))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        Participante.setFont(font)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(Participante)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.lbl_title = QtWidgets.QLabel(Participante)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_title.sizePolicy().hasHeightForWidth())
        self.lbl_title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_title.setFont(font)
        self.lbl_title.setObjectName("lbl_title")
        self.verticalLayout_8.addWidget(self.lbl_title)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_17 = QtWidgets.QLabel(Participante)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.verticalLayout_2.addWidget(self.label_17)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbx_appelation = QtWidgets.QComboBox(Participante)
        self.cbx_appelation.setObjectName("cbx_appelation")
        self.cbx_appelation.addItem("")
        self.cbx_appelation.addItem("")
        self.cbx_appelation.addItem("")
        self.cbx_appelation.addItem("")
        self.cbx_appelation.addItem("")
        self.cbx_appelation.addItem("")
        self.cbx_appelation.addItem("")
        self.horizontalLayout_4.addWidget(self.cbx_appelation)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label = QtWidgets.QLabel(Participante)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txt_prenom = QtWidgets.QLineEdit(Participante)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_prenom.sizePolicy().hasHeightForWidth())
        self.txt_prenom.setSizePolicy(sizePolicy)
        self.txt_prenom.setObjectName("txt_prenom")
        self.horizontalLayout.addWidget(self.txt_prenom)
        self.txt_nom = QtWidgets.QLineEdit(Participante)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_nom.sizePolicy().hasHeightForWidth())
        self.txt_nom.setSizePolicy(sizePolicy)
        self.txt_nom.setObjectName("txt_nom")
        self.horizontalLayout.addWidget(self.txt_nom)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_3 = QtWidgets.QLabel(Participante)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.txt_adresse1 = QtWidgets.QLineEdit(Participante)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_adresse1.sizePolicy().hasHeightForWidth())
        self.txt_adresse1.setSizePolicy(sizePolicy)
        self.txt_adresse1.setObjectName("txt_adresse1")
        self.horizontalLayout_5.addWidget(self.txt_adresse1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.label_13 = QtWidgets.QLabel(Participante)
        self.label_13.setText("")
        self.label_13.setObjectName("label_13")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.txt_adresse2 = QtWidgets.QLineEdit(Participante)
        self.txt_adresse2.setObjectName("txt_adresse2")
        self.horizontalLayout_6.addWidget(self.txt_adresse2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_6)
        self.label_4 = QtWidgets.QLabel(Participante)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.txt_ville = QtWidgets.QLineEdit(Participante)
        self.txt_ville.setObjectName("txt_ville")
        self.horizontalLayout_7.addWidget(self.txt_ville)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_7)
        self.label_5 = QtWidgets.QLabel(Participante)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.cbx_province = QtWidgets.QComboBox(Participante)
        self.cbx_province.setObjectName("cbx_province")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.cbx_province.addItem("")
        self.horizontalLayout_8.addWidget(self.cbx_province)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.formLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_8)
        self.label_6 = QtWidgets.QLabel(Participante)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.txt_code_postal = QtWidgets.QLineEdit(Participante)
        self.txt_code_postal.setObjectName("txt_code_postal")
        self.horizontalLayout_9.addWidget(self.txt_code_postal)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem5)
        self.formLayout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_9)
        self.label_7 = QtWidgets.QLabel(Participante)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txt_telephone1 = QtWidgets.QLineEdit(Participante)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_telephone1.sizePolicy().hasHeightForWidth())
        self.txt_telephone1.setSizePolicy(sizePolicy)
        self.txt_telephone1.setObjectName("txt_telephone1")
        self.horizontalLayout_2.addWidget(self.txt_telephone1)
        self.txt_poste1 = QtWidgets.QLineEdit(Participante)
        self.txt_poste1.setObjectName("txt_poste1")
        self.horizontalLayout_2.addWidget(self.txt_poste1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.formLayout.setLayout(8, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_8 = QtWidgets.QLabel(Participante)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txt_telephone2 = QtWidgets.QLineEdit(Participante)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_telephone2.sizePolicy().hasHeightForWidth())
        self.txt_telephone2.setSizePolicy(sizePolicy)
        self.txt_telephone2.setObjectName("txt_telephone2")
        self.horizontalLayout_3.addWidget(self.txt_telephone2)
        self.txt_poste2 = QtWidgets.QLineEdit(Participante)
        self.txt_poste2.setObjectName("txt_poste2")
        self.horizontalLayout_3.addWidget(self.txt_poste2)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.formLayout.setLayout(9, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.lbl_annee_naissance = QtWidgets.QLabel(Participante)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_annee_naissance.setFont(font)
        self.lbl_annee_naissance.setObjectName("lbl_annee_naissance")
        self.formLayout.setWidget(10, QtWidgets.QFormLayout.LabelRole, self.lbl_annee_naissance)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.sbx_annee_naissance = QtWidgets.QSpinBox(Participante)
        self.sbx_annee_naissance.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sbx_annee_naissance.setMaximum(3000)
        self.sbx_annee_naissance.setObjectName("sbx_annee_naissance")
        self.horizontalLayout_10.addWidget(self.sbx_annee_naissance)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.formLayout.setLayout(10, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_10)
        self.lbl_personne_nourries = QtWidgets.QLabel(Participante)
        self.lbl_personne_nourries.setObjectName("lbl_personne_nourries")
        self.formLayout.setWidget(11, QtWidgets.QFormLayout.LabelRole, self.lbl_personne_nourries)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.sbx_personnes_nourries = QtWidgets.QSpinBox(Participante)
        self.sbx_personnes_nourries.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sbx_personnes_nourries.setProperty("value", 0)
        self.sbx_personnes_nourries.setObjectName("sbx_personnes_nourries")
        self.horizontalLayout_11.addWidget(self.sbx_personnes_nourries)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem9)
        self.formLayout.setLayout(11, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_11)
        self.lbl_consentement = QtWidgets.QLabel(Participante)
        self.lbl_consentement.setObjectName("lbl_consentement")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.lbl_consentement)
        self.label_2 = QtWidgets.QLabel(Participante)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cbx_photo = QtWidgets.QCheckBox(Participante)
        self.cbx_photo.setObjectName("cbx_photo")
        self.formLayout.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.cbx_photo)
        self.label_12 = QtWidgets.QLabel(Participante)
        self.label_12.setObjectName("label_12")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.txt_email = QtWidgets.QLineEdit(Participante)
        self.txt_email.setObjectName("txt_email")
        self.horizontalLayout_14.addWidget(self.txt_email)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem10)
        self.formLayout.setLayout(7, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_14)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_membre = QtWidgets.QLabel(Participante)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_membre.setFont(font)
        self.lbl_membre.setObjectName("lbl_membre")
        self.verticalLayout.addWidget(self.lbl_membre)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.chk_membre = QtWidgets.QCheckBox(Participante)
        self.chk_membre.setEnabled(True)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.chk_membre.setPalette(palette)
        self.chk_membre.setCheckable(True)
        self.chk_membre.setChecked(False)
        self.chk_membre.setObjectName("chk_membre")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.chk_membre)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.chk_actif = QtWidgets.QCheckBox(Participante)
        self.chk_actif.setEnabled(False)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.chk_actif.setPalette(palette)
        self.chk_actif.setCheckable(True)
        self.chk_actif.setObjectName("chk_actif")
        self.horizontalLayout_12.addWidget(self.chk_actif)
        self.chk_honoraire = QtWidgets.QCheckBox(Participante)
        self.chk_honoraire.setEnabled(False)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.chk_honoraire.setPalette(palette)
        self.chk_honoraire.setCheckable(True)
        self.chk_honoraire.setTristate(False)
        self.chk_honoraire.setObjectName("chk_honoraire")
        self.horizontalLayout_12.addWidget(self.chk_honoraire)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem11)
        self.formLayout_2.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_12)
        self.lbl_numero_membre = QtWidgets.QLabel(Participante)
        self.lbl_numero_membre.setObjectName("lbl_numero_membre")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lbl_numero_membre)
        self.lbl_renouvellement = QtWidgets.QLabel(Participante)
        self.lbl_renouvellement.setObjectName("lbl_renouvellement")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.lbl_renouvellement)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.ded_renouvellement = QtWidgets.QDateEdit(Participante)
        self.ded_renouvellement.setReadOnly(True)
        self.ded_renouvellement.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.ded_renouvellement.setDisplayFormat("dd-MM-yyyy")
        self.ded_renouvellement.setCalendarPopup(False)
        self.ded_renouvellement.setObjectName("ded_renouvellement")
        self.horizontalLayout_15.addWidget(self.ded_renouvellement)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem12)
        self.btn_renew = QtWidgets.QPushButton(Participante)
        self.btn_renew.setAutoDefault(False)
        self.btn_renew.setObjectName("btn_renew")
        self.horizontalLayout_15.addWidget(self.btn_renew)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_15)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.txt_numero_membre = QtWidgets.QLineEdit(Participante)
        self.txt_numero_membre.setMinimumSize(QtCore.QSize(0, 0))
        self.txt_numero_membre.setReadOnly(True)
        self.txt_numero_membre.setObjectName("txt_numero_membre")
        self.horizontalLayout_16.addWidget(self.txt_numero_membre)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem13)
        self.formLayout_2.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_16)
        self.verticalLayout.addLayout(self.formLayout_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.horizontalLayout_17.addLayout(self.verticalLayout_3)
        self.line = QtWidgets.QFrame(Participante)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout_17.addWidget(self.line)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lbl_transaction = QtWidgets.QLabel(Participante)
        self.lbl_transaction.setObjectName("lbl_transaction")
        self.verticalLayout_4.addWidget(self.lbl_transaction)
        self.tbl_transaction = QtWidgets.QTableWidget(Participante)
        self.tbl_transaction.setObjectName("tbl_transaction")
        self.tbl_transaction.setColumnCount(3)
        self.tbl_transaction.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_transaction.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_transaction.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_transaction.setHorizontalHeaderItem(2, item)
        self.verticalLayout_4.addWidget(self.tbl_transaction)
        self.verticalLayout_7.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lbl_inscription = QtWidgets.QLabel(Participante)
        self.lbl_inscription.setObjectName("lbl_inscription")
        self.verticalLayout_6.addWidget(self.lbl_inscription)
        self.tbl_inscription = QtWidgets.QTableWidget(Participante)
        self.tbl_inscription.setObjectName("tbl_inscription")
        self.tbl_inscription.setColumnCount(3)
        self.tbl_inscription.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_inscription.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_inscription.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_inscription.setHorizontalHeaderItem(2, item)
        self.verticalLayout_6.addWidget(self.tbl_inscription)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.horizontalLayout_17.addLayout(self.verticalLayout_7)
        self.verticalLayout_8.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem14)
        self.btn_cancel = QtWidgets.QPushButton(Participante)
        self.btn_cancel.setAutoDefault(False)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_13.addWidget(self.btn_cancel)
        self.btn_add = QtWidgets.QPushButton(Participante)
        self.btn_add.setDefault(True)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_13.addWidget(self.btn_add)
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        spacerItem15 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem15)

        self.retranslateUi(Participante)
        QtCore.QMetaObject.connectSlotsByName(Participante)
        Participante.setTabOrder(self.cbx_appelation, self.txt_prenom)
        Participante.setTabOrder(self.txt_prenom, self.txt_nom)
        Participante.setTabOrder(self.txt_nom, self.txt_adresse1)
        Participante.setTabOrder(self.txt_adresse1, self.txt_adresse2)
        Participante.setTabOrder(self.txt_adresse2, self.txt_ville)
        Participante.setTabOrder(self.txt_ville, self.cbx_province)
        Participante.setTabOrder(self.cbx_province, self.txt_code_postal)
        Participante.setTabOrder(self.txt_code_postal, self.txt_email)
        Participante.setTabOrder(self.txt_email, self.txt_telephone1)
        Participante.setTabOrder(self.txt_telephone1, self.txt_poste1)
        Participante.setTabOrder(self.txt_poste1, self.txt_telephone2)
        Participante.setTabOrder(self.txt_telephone2, self.txt_poste2)
        Participante.setTabOrder(self.txt_poste2, self.sbx_annee_naissance)
        Participante.setTabOrder(self.sbx_annee_naissance, self.sbx_personnes_nourries)
        Participante.setTabOrder(self.sbx_personnes_nourries, self.cbx_photo)
        Participante.setTabOrder(self.cbx_photo, self.btn_add)
        Participante.setTabOrder(self.btn_add, self.btn_cancel)
        Participante.setTabOrder(self.btn_cancel, self.chk_honoraire)
        Participante.setTabOrder(self.chk_honoraire, self.ded_renouvellement)
        Participante.setTabOrder(self.ded_renouvellement, self.chk_actif)
        Participante.setTabOrder(self.chk_actif, self.chk_membre)

    def retranslateUi(self, Participante):
        _translate = QtCore.QCoreApplication.translate
        Participante.setWindowTitle(_translate("Participante", "Participante"))
        self.lbl_title.setText(_translate("Participante", "Participante"))
        self.label_17.setText(_translate("Participante", "Informations sur la participante"))
        self.cbx_appelation.setItemText(0, _translate("Participante", "Mme."))
        self.cbx_appelation.setItemText(1, _translate("Participante", "M."))
        self.cbx_appelation.setItemText(2, _translate("Participante", "Organisme"))
        self.cbx_appelation.setItemText(3, _translate("Participante", "École"))
        self.cbx_appelation.setItemText(4, _translate("Participante", "Municipalité"))
        self.cbx_appelation.setItemText(5, _translate("Participante", "Employée"))
        self.cbx_appelation.setItemText(6, _translate("Participante", "Autre"))
        self.label.setText(_translate("Participante", "Nom : "))
        self.txt_prenom.setPlaceholderText(_translate("Participante", "Prénom"))
        self.txt_nom.setPlaceholderText(_translate("Participante", "Nom"))
        self.label_3.setText(_translate("Participante", "Adresse :"))
        self.txt_adresse1.setPlaceholderText(_translate("Participante", "Adresse"))
        self.txt_adresse2.setPlaceholderText(_translate("Participante", "Adresse 2 (facultatif)"))
        self.label_4.setText(_translate("Participante", "Ville : "))
        self.txt_ville.setPlaceholderText(_translate("Participante", "Ville"))
        self.label_5.setText(_translate("Participante", "Province : "))
        self.cbx_province.setItemText(0, _translate("Participante", "Québec"))
        self.cbx_province.setItemText(1, _translate("Participante", "Alberta"))
        self.cbx_province.setItemText(2, _translate("Participante", "Colombie-Britannique"))
        self.cbx_province.setItemText(3, _translate("Participante", "Île-du-Prince-Édouard"))
        self.cbx_province.setItemText(4, _translate("Participante", "Manitoba"))
        self.cbx_province.setItemText(5, _translate("Participante", "Nouveau-Brunswick"))
        self.cbx_province.setItemText(6, _translate("Participante", "Nouvelle-Écosse"))
        self.cbx_province.setItemText(7, _translate("Participante", "Nunavut"))
        self.cbx_province.setItemText(8, _translate("Participante", "Ontario"))
        self.cbx_province.setItemText(9, _translate("Participante", "Saskatchewan"))
        self.cbx_province.setItemText(10, _translate("Participante", "Terre-Neuve-et-Labrador"))
        self.cbx_province.setItemText(11, _translate("Participante", "Territoires du Nord-Ouest"))
        self.cbx_province.setItemText(12, _translate("Participante", "Yukon"))
        self.label_6.setText(_translate("Participante", "Code postal : "))
        self.txt_code_postal.setPlaceholderText(_translate("Participante", "Code postal"))
        self.label_7.setText(_translate("Participante", "Téléphone 1 : "))
        self.txt_telephone1.setPlaceholderText(_translate("Participante", "Téléphone 1"))
        self.txt_poste1.setPlaceholderText(_translate("Participante", "Poste"))
        self.label_8.setText(_translate("Participante", "Téléphone 2 : "))
        self.txt_telephone2.setPlaceholderText(_translate("Participante", "Téléphone 2 (facultatif)"))
        self.txt_poste2.setPlaceholderText(_translate("Participante", "Poste"))
        self.lbl_annee_naissance.setText(_translate("Participante", "Année de naissance : "))
        self.lbl_personne_nourries.setText(_translate("Participante", "Personnes nourries : "))
        self.lbl_consentement.setText(_translate("Participante", "Consentement photo : "))
        self.label_2.setText(_translate("Participante", "Appelation : "))
        self.cbx_photo.setText(_translate("Participante", "La participante consent à être prise en photo"))
        self.label_12.setText(_translate("Participante", "Courriel : "))
        self.txt_email.setPlaceholderText(_translate("Participante", "Courriel"))
        self.lbl_membre.setText(_translate("Participante", "Status de membre"))
        self.chk_membre.setText(_translate("Participante", "Membre"))
        self.chk_actif.setText(_translate("Participante", "Actif"))
        self.chk_honoraire.setStatusTip(_translate("Participante", "Activer le status de membre honoraire pour ce membre."))
        self.chk_honoraire.setText(_translate("Participante", "Honoraire"))
        self.lbl_numero_membre.setText(_translate("Participante", "Numéro de membre"))
        self.lbl_renouvellement.setText(_translate("Participante", "Date de renouvellement"))
        self.btn_renew.setText(_translate("Participante", "Renouveler"))
        self.txt_numero_membre.setPlaceholderText(_translate("Participante", "Numéro de membre"))
        self.lbl_transaction.setText(_translate("Participante", "Transactions"))
        item = self.tbl_transaction.horizontalHeaderItem(0)
        item.setText(_translate("Participante", "Description"))
        item = self.tbl_transaction.horizontalHeaderItem(1)
        item.setText(_translate("Participante", "Prix"))
        item = self.tbl_transaction.horizontalHeaderItem(2)
        item.setText(_translate("Participante", "Date"))
        self.lbl_inscription.setText(_translate("Participante", "Inscription"))
        item = self.tbl_inscription.horizontalHeaderItem(0)
        item.setText(_translate("Participante", "Nom"))
        item = self.tbl_inscription.horizontalHeaderItem(1)
        item.setText(_translate("Participante", "Date"))
        item = self.tbl_inscription.horizontalHeaderItem(2)
        item.setText(_translate("Participante", "Heure"))
        self.btn_cancel.setText(_translate("Participante", "Annuler"))
        self.btn_add.setText(_translate("Participante", "Ajouter"))
