# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/central_widget/ui/widget_activite.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WidgetActivite(object):
    def setupUi(self, WidgetActivite):
        WidgetActivite.setObjectName("WidgetActivite")
        WidgetActivite.resize(752, 165)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        WidgetActivite.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(WidgetActivite)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_6 = QtWidgets.QLabel(WidgetActivite)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout.addWidget(self.label_6)
        self.cbx_search = QtWidgets.QComboBox(WidgetActivite)
        self.cbx_search.setObjectName("cbx_search")
        self.cbx_search.addItem("")
        self.cbx_search.addItem("")
        self.horizontalLayout.addWidget(self.cbx_search)
        self.txt_search = QtWidgets.QLineEdit(WidgetActivite)
        self.txt_search.setPlaceholderText("")
        self.txt_search.setObjectName("txt_search")
        self.horizontalLayout.addWidget(self.txt_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btn_add = QtWidgets.QPushButton(WidgetActivite)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout.addWidget(self.btn_add)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_5 = QtWidgets.QLabel(WidgetActivite)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_2.addWidget(self.label_5)
        self.cbx_sort = QtWidgets.QComboBox(WidgetActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbx_sort.sizePolicy().hasHeightForWidth())
        self.cbx_sort.setSizePolicy(sizePolicy)
        self.cbx_sort.setObjectName("cbx_sort")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.cbx_sort.addItem("")
        self.horizontalLayout_2.addWidget(self.cbx_sort)
        self.chk_desc = QtWidgets.QCheckBox(WidgetActivite)
        self.chk_desc.setObjectName("chk_desc")
        self.horizontalLayout_2.addWidget(self.chk_desc)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(WidgetActivite)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.ded_start = QtWidgets.QDateEdit(WidgetActivite)
        self.ded_start.setDisplayFormat("dd-MM-yyyy")
        self.ded_start.setCalendarPopup(True)
        self.ded_start.setObjectName("ded_start")
        self.horizontalLayout_3.addWidget(self.ded_start)
        self.label_4 = QtWidgets.QLabel(WidgetActivite)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.ded_end = QtWidgets.QDateEdit(WidgetActivite)
        self.ded_end.setDisplayFormat("dd-MM-yyyy")
        self.ded_end.setCalendarPopup(True)
        self.ded_end.setObjectName("ded_end")
        self.horizontalLayout_3.addWidget(self.ded_end)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(WidgetActivite)
        QtCore.QMetaObject.connectSlotsByName(WidgetActivite)

    def retranslateUi(self, WidgetActivite):
        _translate = QtCore.QCoreApplication.translate
        WidgetActivite.setWindowTitle(_translate("WidgetActivite", "Form"))
        self.label_6.setText(_translate("WidgetActivite", "Recherche par : "))
        self.cbx_search.setItemText(0, _translate("WidgetActivite", "Nom de l\'activité"))
        self.cbx_search.setItemText(1, _translate("WidgetActivite", "Lieu"))
        self.btn_add.setText(_translate("WidgetActivite", "Nouvelle activité"))
        self.label_5.setText(_translate("WidgetActivite", "Trier par : "))
        self.cbx_sort.setItemText(0, _translate("WidgetActivite", "Nom de l\'activité"))
        self.cbx_sort.setItemText(1, _translate("WidgetActivite", "Lieu"))
        self.cbx_sort.setItemText(2, _translate("WidgetActivite", "Prix régulier"))
        self.cbx_sort.setItemText(3, _translate("WidgetActivite", "Prix membre"))
        self.cbx_sort.setItemText(4, _translate("WidgetActivite", "Date"))
        self.chk_desc.setText(_translate("WidgetActivite", "Ordre décroissant"))
        self.label_3.setText(_translate("WidgetActivite", "Date : "))
        self.label_4.setText(_translate("WidgetActivite", "au"))

