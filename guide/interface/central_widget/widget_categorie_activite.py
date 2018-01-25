# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/central_widget/ui/widget_categorie_activite.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetTypeActivite(object):
    def setupUi(self, WidgetTypeActivite):
        WidgetTypeActivite.setObjectName("WidgetTypeActivite")
        WidgetTypeActivite.resize(742, 116)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        WidgetTypeActivite.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetTypeActivite)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(WidgetTypeActivite)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.cbx_search = QtWidgets.QComboBox(WidgetTypeActivite)
        self.cbx_search.setObjectName("cbx_search")
        self.cbx_search.addItem("")
        self.cbx_search.addItem("")
        self.cbx_search.addItem("")
        self.horizontalLayout.addWidget(self.cbx_search)
        self.txt_search = QtWidgets.QLineEdit(WidgetTypeActivite)
        self.txt_search.setPlaceholderText("")
        self.txt_search.setObjectName("txt_search")
        self.horizontalLayout.addWidget(self.txt_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_add = QtWidgets.QPushButton(WidgetTypeActivite)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(WidgetTypeActivite)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.cbx_sort = QtWidgets.QComboBox(WidgetTypeActivite)
        self.cbx_sort.setObjectName("cbx_sort")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.horizontalLayout_2.addWidget(self.cbx_sort)
        self.chk_desc = QtWidgets.QCheckBox(WidgetTypeActivite)
        self.chk_desc.setObjectName("chk_desc")
        self.horizontalLayout_2.addWidget(self.chk_desc)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(WidgetTypeActivite)
        QtCore.QMetaObject.connectSlotsByName(WidgetTypeActivite)

    def retranslateUi(self, WidgetTypeActivite):
        _translate = QtCore.QCoreApplication.translate
        WidgetTypeActivite.setWindowTitle(_translate("WidgetTypeActivite", "Form"))
        self.label_2.setText(_translate("WidgetTypeActivite", "Recherche par : "))
        self.cbx_search.setItemText(0, _translate("WidgetTypeActivite", "Nom de la catégorie"))
        self.cbx_search.setItemText(1, _translate("WidgetTypeActivite", "Responsable"))
        self.cbx_search.setItemText(2, _translate("WidgetTypeActivite", "Lieu"))
        self.btn_add.setText(_translate("WidgetTypeActivite", "Nouvelle catégorie"))
        self.label_3.setText(_translate("WidgetTypeActivite", "Trier par : "))
        self.cbx_sort.setItemText(0, _translate("WidgetTypeActivite", "Nom de la catégorie"))
        self.cbx_sort.setItemText(1, _translate("WidgetTypeActivite", "Responsable"))
        self.cbx_sort.setItemText(2, _translate("WidgetTypeActivite", "Lieu"))
        self.cbx_sort.setItemText(3, _translate("WidgetTypeActivite", "Prix membre"))
        self.cbx_sort.setItemText(4, _translate("WidgetTypeActivite", "Prix non membre"))
        self.chk_desc.setText(_translate("WidgetTypeActivite", "Ordre décroissant"))

