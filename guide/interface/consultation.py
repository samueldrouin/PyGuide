# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/ui/consultation.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Consultation(object):
    def setupUi(self, Consultation):
        Consultation.setObjectName("Consultation")
        Consultation.resize(700, 500)
        Consultation.setMinimumSize(QtCore.QSize(700, 500))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        Consultation.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(Consultation)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_title = QtWidgets.QLabel(Consultation)
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
        self.verticalLayout.addWidget(self.lbl_title)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(Consultation)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.txt_search = QtWidgets.QLineEdit(Consultation)
        self.txt_search.setObjectName("txt_search")
        self.horizontalLayout.addWidget(self.txt_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_add = QtWidgets.QPushButton(Consultation)
        self.btn_add.setAutoDefault(False)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tbl_resultat = QtWidgets.QTableWidget(Consultation)
        self.tbl_resultat.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tbl_resultat.setAlternatingRowColors(True)
        self.tbl_resultat.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tbl_resultat.setObjectName("tbl_resultat")
        self.tbl_resultat.setColumnCount(2)
        self.tbl_resultat.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_resultat.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tbl_resultat.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tbl_resultat)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btn_close = QtWidgets.QPushButton(Consultation)
        self.btn_close.setDefault(True)
        self.btn_close.setObjectName("btn_close")
        self.horizontalLayout_3.addWidget(self.btn_close)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Consultation)
        QtCore.QMetaObject.connectSlotsByName(Consultation)

    def retranslateUi(self, Consultation):
        _translate = QtCore.QCoreApplication.translate
        Consultation.setWindowTitle(_translate("Consultation", "Consultation"))
        self.lbl_title.setText(_translate("Consultation", "Consultation"))
        self.label_2.setText(_translate("Consultation", "Recherche : "))
        self.txt_search.setPlaceholderText(_translate("Consultation", "Nom"))
        self.btn_add.setText(_translate("Consultation", "Ajouter"))
        item = self.tbl_resultat.horizontalHeaderItem(0)
        item.setText(_translate("Consultation", "Index"))
        item = self.tbl_resultat.horizontalHeaderItem(1)
        item.setText(_translate("Consultation", "Nom"))
        self.btn_close.setText(_translate("Consultation", "Fermer"))

