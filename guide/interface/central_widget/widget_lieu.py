# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/central_widget/ui/widget_lieu.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetLieu(object):
    def setupUi(self, WidgetLieu):
        WidgetLieu.setObjectName("WidgetLieu")
        WidgetLieu.resize(766, 138)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        WidgetLieu.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetLieu)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(WidgetLieu)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cbx_search = QtWidgets.QComboBox(WidgetLieu)
        self.cbx_search.setObjectName("cbx_search")
        self.cbx_search.addItem("")
        self.cbx_search.addItem("")
        self.horizontalLayout.addWidget(self.cbx_search)
        self.txt_search = QtWidgets.QLineEdit(WidgetLieu)
        self.txt_search.setPlaceholderText("")
        self.txt_search.setObjectName("txt_search")
        self.horizontalLayout.addWidget(self.txt_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_add = QtWidgets.QPushButton(WidgetLieu)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(WidgetLieu)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.cbx_sort = QtWidgets.QComboBox(WidgetLieu)
        self.cbx_sort.setObjectName("cbx_sort")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.horizontalLayout_2.addWidget(self.cbx_sort)
        self.chk_desc = QtWidgets.QCheckBox(WidgetLieu)
        self.chk_desc.setObjectName("chk_desc")
        self.horizontalLayout_2.addWidget(self.chk_desc)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(WidgetLieu)
        QtCore.QMetaObject.connectSlotsByName(WidgetLieu)

    def retranslateUi(self, WidgetLieu):
        _translate = QtCore.QCoreApplication.translate
        WidgetLieu.setWindowTitle(_translate("WidgetLieu", "Form"))
        self.label_2.setText(_translate("WidgetLieu", "Recherche par : "))
        self.cbx_search.setItemText(0, _translate("WidgetLieu", "Nom du lieu"))
        self.cbx_search.setItemText(1, _translate("WidgetLieu", "Ville"))
        self.btn_add.setText(_translate("WidgetLieu", "Nouveau lieu"))
        self.label_3.setText(_translate("WidgetLieu", "Trier par : "))
        self.cbx_sort.setItemText(0, _translate("WidgetLieu", "Nom du lieu"))
        self.cbx_sort.setItemText(1, _translate("WidgetLieu", "Ville"))
        self.chk_desc.setText(_translate("WidgetLieu", "Ordre décroissant"))

