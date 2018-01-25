# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/ui/type_activite.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TypeActivite(object):
    def setupUi(self, TypeActivite):
        TypeActivite.setObjectName("TypeActivite")
        TypeActivite.resize(400, 117)
        TypeActivite.setMinimumSize(QtCore.QSize(400, 117))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        TypeActivite.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(TypeActivite)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_titre = QtWidgets.QLabel(TypeActivite)
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
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(TypeActivite)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.txt_nom = QtWidgets.QLineEdit(TypeActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txt_nom.sizePolicy().hasHeightForWidth())
        self.txt_nom.setSizePolicy(sizePolicy)
        self.txt_nom.setObjectName("txt_nom")
        self.horizontalLayout.addWidget(self.txt_nom)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btn_cancel = QtWidgets.QPushButton(TypeActivite)
        self.btn_cancel.setAutoDefault(False)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_2.addWidget(self.btn_cancel)
        self.btn_add = QtWidgets.QPushButton(TypeActivite)
        self.btn_add.setDefault(True)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_2.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(TypeActivite)
        QtCore.QMetaObject.connectSlotsByName(TypeActivite)

    def retranslateUi(self, TypeActivite):
        _translate = QtCore.QCoreApplication.translate
        TypeActivite.setWindowTitle(_translate("TypeActivite", "Type d\'activité"))
        self.lbl_titre.setText(_translate("TypeActivite", "Type d\'activité"))
        self.label_2.setText(_translate("TypeActivite", "Nom : "))
        self.txt_nom.setPlaceholderText(_translate("TypeActivite", "Nom du type d\'activité"))
        self.btn_cancel.setText(_translate("TypeActivite", "Annuler"))
        self.btn_add.setText(_translate("TypeActivite", "Ajouter"))

