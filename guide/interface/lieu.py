# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/ui/lieu.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Lieu(object):
    def setupUi(self, Lieu):
        Lieu.setObjectName("Lieu")
        Lieu.resize(440, 285)
        Lieu.setMinimumSize(QtCore.QSize(440, 285))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        Lieu.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Lieu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_titre = QtWidgets.QLabel(Lieu)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_titre.sizePolicy().hasHeightForWidth())
        self.lbl_titre.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_titre.setFont(font)
        self.lbl_titre.setObjectName("lbl_titre")
        self.verticalLayout.addWidget(self.lbl_titre)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(Lieu)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.txt_nom = QtWidgets.QLineEdit(Lieu)
        self.txt_nom.setObjectName("txt_nom")
        self.horizontalLayout.addWidget(self.txt_nom)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.label_3 = QtWidgets.QLabel(Lieu)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.txt_adresse1 = QtWidgets.QLineEdit(Lieu)
        self.txt_adresse1.setObjectName("txt_adresse1")
        self.horizontalLayout_2.addWidget(self.txt_adresse1)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_4 = QtWidgets.QLabel(Lieu)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.txt_ville = QtWidgets.QLineEdit(Lieu)
        self.txt_ville.setObjectName("txt_ville")
        self.gridLayout.addWidget(self.txt_ville, 0, 0, 1, 1)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.gridLayout)
        self.label_5 = QtWidgets.QLabel(Lieu)
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.txt_adresse2 = QtWidgets.QLineEdit(Lieu)
        self.txt_adresse2.setObjectName("txt_adresse2")
        self.horizontalLayout_3.addWidget(self.txt_adresse2)
        self.formLayout.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.label_6 = QtWidgets.QLabel(Lieu)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.cbx_province = QtWidgets.QComboBox(Lieu)
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
        self.horizontalLayout_4.addWidget(self.cbx_province)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_7 = QtWidgets.QLabel(Lieu)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.txt_code_postal = QtWidgets.QLineEdit(Lieu)
        self.txt_code_postal.setObjectName("txt_code_postal")
        self.horizontalLayout_5.addWidget(self.txt_code_postal)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.formLayout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_5)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.btn_cancel = QtWidgets.QPushButton(Lieu)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_6.addWidget(self.btn_cancel)
        self.btn_add = QtWidgets.QPushButton(Lieu)
        self.btn_add.setAutoDefault(True)
        self.btn_add.setDefault(True)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_6.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)

        self.retranslateUi(Lieu)
        QtCore.QMetaObject.connectSlotsByName(Lieu)
        Lieu.setTabOrder(self.txt_nom, self.txt_adresse1)
        Lieu.setTabOrder(self.txt_adresse1, self.txt_adresse2)
        Lieu.setTabOrder(self.txt_adresse2, self.txt_ville)
        Lieu.setTabOrder(self.txt_ville, self.cbx_province)
        Lieu.setTabOrder(self.cbx_province, self.txt_code_postal)
        Lieu.setTabOrder(self.txt_code_postal, self.btn_add)
        Lieu.setTabOrder(self.btn_add, self.btn_cancel)

    def retranslateUi(self, Lieu):
        _translate = QtCore.QCoreApplication.translate
        Lieu.setWindowTitle(_translate("Lieu", "Form"))
        self.lbl_titre.setText(_translate("Lieu", "Lieu"))
        self.label_2.setText(_translate("Lieu", "Nom du lieu : "))
        self.txt_nom.setPlaceholderText(_translate("Lieu", "Nom du lieu"))
        self.label_3.setText(_translate("Lieu", "Rue :"))
        self.txt_adresse1.setPlaceholderText(_translate("Lieu", "Adresse"))
        self.label_4.setText(_translate("Lieu", "Ville :"))
        self.txt_ville.setPlaceholderText(_translate("Lieu", "Ville"))
        self.txt_adresse2.setPlaceholderText(_translate("Lieu", "Adresse 2 (facultatif)"))
        self.label_6.setText(_translate("Lieu", "Province : "))
        self.cbx_province.setItemText(0, _translate("Lieu", "Québec"))
        self.cbx_province.setItemText(1, _translate("Lieu", "Alberta"))
        self.cbx_province.setItemText(2, _translate("Lieu", "Colombie-Britannique"))
        self.cbx_province.setItemText(3, _translate("Lieu", "Île-du-Prince-Édouard"))
        self.cbx_province.setItemText(4, _translate("Lieu", "Manitoba"))
        self.cbx_province.setItemText(5, _translate("Lieu", "Nouveau-Brunswick"))
        self.cbx_province.setItemText(6, _translate("Lieu", "Nouvelle-Écosse"))
        self.cbx_province.setItemText(7, _translate("Lieu", "Nunavut"))
        self.cbx_province.setItemText(8, _translate("Lieu", "Ontario"))
        self.cbx_province.setItemText(9, _translate("Lieu", "Saskatchewan"))
        self.cbx_province.setItemText(10, _translate("Lieu", "Terre-Neuve-et-Labrador"))
        self.cbx_province.setItemText(11, _translate("Lieu", "Territoires du Nord-Ouest"))
        self.cbx_province.setItemText(12, _translate("Lieu", "Yukon"))
        self.label_7.setText(_translate("Lieu", "Code postal : "))
        self.txt_code_postal.setPlaceholderText(_translate("Lieu", "Code postal"))
        self.btn_cancel.setText(_translate("Lieu", "Annuler"))
        self.btn_add.setText(_translate("Lieu", "Ajouter"))

