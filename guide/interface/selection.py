# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/ui/selection.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Selection(object):
    def setupUi(self, Selection):
        Selection.setObjectName("Selection")
        Selection.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Selection)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_titre = QtWidgets.QLabel(Selection)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.lbl_titre.setFont(font)
        self.lbl_titre.setObjectName("lbl_titre")
        self.verticalLayout.addWidget(self.lbl_titre)
        self.table_widget = QtWidgets.QTableWidget(Selection)
        self.table_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_widget.setAlternatingRowColors(True)
        self.table_widget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_widget.setObjectName("table_widget")
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
        self.verticalLayout.addWidget(self.table_widget)

        self.retranslateUi(Selection)
        QtCore.QMetaObject.connectSlotsByName(Selection)

    def retranslateUi(self, Selection):
        _translate = QtCore.QCoreApplication.translate
        Selection.setWindowTitle(_translate("Selection", "Dialog"))
        self.lbl_titre.setText(_translate("Selection", "Titre"))

