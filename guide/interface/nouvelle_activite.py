# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/Volumes/[C] Windows 10/Users/samueldrouin/source/repos/GUIDE-CFR/guide/interface/ui/nouvelle_activite.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NouvelleActivite(object):
    def setupUi(self, NouvelleActivite):
        NouvelleActivite.setObjectName("NouvelleActivite")
        NouvelleActivite.resize(480, 454)
        NouvelleActivite.setMinimumSize(QtCore.QSize(480, 454))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        NouvelleActivite.setFont(font)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(NouvelleActivite)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lbl_titre = QtWidgets.QLabel(NouvelleActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_titre.sizePolicy().hasHeightForWidth())
        self.lbl_titre.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_titre.setFont(font)
        self.lbl_titre.setObjectName("lbl_titre")
        self.verticalLayout_4.addWidget(self.lbl_titre)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_8 = QtWidgets.QLabel(NouvelleActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(140, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout.addWidget(self.label_8)
        self.cbx_category_activite = QtWidgets.QComboBox(NouvelleActivite)
        self.cbx_category_activite.setObjectName("cbx_category_activite")
        self.horizontalLayout.addWidget(self.cbx_category_activite)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(NouvelleActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(140, 0))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.rbt_unique = QtWidgets.QRadioButton(NouvelleActivite)
        self.rbt_unique.setChecked(True)
        self.rbt_unique.setObjectName("rbt_unique")
        self.verticalLayout.addWidget(self.rbt_unique)
        self.rbt_hebdomadaire = QtWidgets.QRadioButton(NouvelleActivite)
        self.rbt_hebdomadaire.setObjectName("rbt_hebdomadaire")
        self.verticalLayout.addWidget(self.rbt_hebdomadaire)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.widget_unique = QtWidgets.QWidget(NouvelleActivite)
        self.widget_unique.setObjectName("widget_unique")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget_unique)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.hlay_unique = QtWidgets.QHBoxLayout()
        self.hlay_unique.setObjectName("hlay_unique")
        self.lbl_unique = QtWidgets.QLabel(self.widget_unique)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_unique.sizePolicy().hasHeightForWidth())
        self.lbl_unique.setSizePolicy(sizePolicy)
        self.lbl_unique.setMinimumSize(QtCore.QSize(140, 0))
        self.lbl_unique.setObjectName("lbl_unique")
        self.hlay_unique.addWidget(self.lbl_unique)
        self.ded_unique = QtWidgets.QDateEdit(self.widget_unique)
        self.ded_unique.setDisplayFormat("dd-MM-yyyy")
        self.ded_unique.setCalendarPopup(True)
        self.ded_unique.setObjectName("ded_unique")
        self.hlay_unique.addWidget(self.ded_unique)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hlay_unique.addItem(spacerItem1)
        self.verticalLayout_3.addLayout(self.hlay_unique)
        self.verticalLayout_4.addWidget(self.widget_unique)
        self.widget_recurrente = QtWidgets.QWidget(NouvelleActivite)
        self.widget_recurrente.setObjectName("widget_recurrente")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget_recurrente)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lbl_debut = QtWidgets.QLabel(self.widget_recurrente)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_debut.sizePolicy().hasHeightForWidth())
        self.lbl_debut.setSizePolicy(sizePolicy)
        self.lbl_debut.setMinimumSize(QtCore.QSize(140, 0))
        self.lbl_debut.setObjectName("lbl_debut")
        self.horizontalLayout_4.addWidget(self.lbl_debut)
        self.ded_debut = QtWidgets.QDateEdit(self.widget_recurrente)
        self.ded_debut.setDisplayFormat("dd-MM-yyyy")
        self.ded_debut.setCalendarPopup(True)
        self.ded_debut.setObjectName("ded_debut")
        self.horizontalLayout_4.addWidget(self.ded_debut)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lbl_fin = QtWidgets.QLabel(self.widget_recurrente)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_fin.sizePolicy().hasHeightForWidth())
        self.lbl_fin.setSizePolicy(sizePolicy)
        self.lbl_fin.setMinimumSize(QtCore.QSize(140, 0))
        self.lbl_fin.setObjectName("lbl_fin")
        self.horizontalLayout_5.addWidget(self.lbl_fin)
        self.ded_fin = QtWidgets.QDateEdit(self.widget_recurrente)
        self.ded_fin.setDisplayFormat("dd-MM-yyyy")
        self.ded_fin.setCalendarPopup(True)
        self.ded_fin.setObjectName("ded_fin")
        self.horizontalLayout_5.addWidget(self.ded_fin)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lbl_exclusion = QtWidgets.QLabel(self.widget_recurrente)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_exclusion.sizePolicy().hasHeightForWidth())
        self.lbl_exclusion.setSizePolicy(sizePolicy)
        self.lbl_exclusion.setMinimumSize(QtCore.QSize(140, 0))
        self.lbl_exclusion.setObjectName("lbl_exclusion")
        self.horizontalLayout_6.addWidget(self.lbl_exclusion)
        self.ded_exclusion = QtWidgets.QDateEdit(self.widget_recurrente)
        self.ded_exclusion.setDisplayFormat("dd-MM-yyyy")
        self.ded_exclusion.setCalendarPopup(True)
        self.ded_exclusion.setObjectName("ded_exclusion")
        self.horizontalLayout_6.addWidget(self.ded_exclusion)
        self.btn_ajouter_exclusion = QtWidgets.QPushButton(self.widget_recurrente)
        self.btn_ajouter_exclusion.setObjectName("btn_ajouter_exclusion")
        self.horizontalLayout_6.addWidget(self.btn_ajouter_exclusion)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_3 = QtWidgets.QLabel(self.widget_recurrente)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(140, 0))
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_7.addWidget(self.label_3)
        self.txt_exclusion = QtWidgets.QLineEdit(self.widget_recurrente)
        self.txt_exclusion.setReadOnly(True)
        self.txt_exclusion.setObjectName("txt_exclusion")
        self.horizontalLayout_7.addWidget(self.txt_exclusion)
        self.btn_vider = QtWidgets.QPushButton(self.widget_recurrente)
        self.btn_vider.setObjectName("btn_vider")
        self.horizontalLayout_7.addWidget(self.btn_vider)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addWidget(self.widget_recurrente)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(NouvelleActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(140, 0))
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.sbx_fin_inscription = QtWidgets.QSpinBox(NouvelleActivite)
        self.sbx_fin_inscription.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.sbx_fin_inscription.setObjectName("sbx_fin_inscription")
        self.horizontalLayout_3.addWidget(self.sbx_fin_inscription)
        self.label_4 = QtWidgets.QLabel(NouvelleActivite)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem5)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_6 = QtWidgets.QLabel(NouvelleActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(140, 0))
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_8.addWidget(self.label_6)
        self.tim_debut = QtWidgets.QTimeEdit(NouvelleActivite)
        self.tim_debut.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.tim_debut.setDisplayFormat("hh:mm")
        self.tim_debut.setCalendarPopup(False)
        self.tim_debut.setObjectName("tim_debut")
        self.horizontalLayout_8.addWidget(self.tim_debut)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_7 = QtWidgets.QLabel(NouvelleActivite)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(140, 0))
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_9.addWidget(self.label_7)
        self.tim_fin = QtWidgets.QTimeEdit(NouvelleActivite)
        self.tim_fin.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.tim_fin.setDisplayFormat("hh:mm")
        self.tim_fin.setObjectName("tim_fin")
        self.horizontalLayout_9.addWidget(self.tim_fin)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem7)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem8)
        self.btn_cancel = QtWidgets.QPushButton(NouvelleActivite)
        self.btn_cancel.setObjectName("btn_cancel")
        self.horizontalLayout_10.addWidget(self.btn_cancel)
        self.btn_add = QtWidgets.QPushButton(NouvelleActivite)
        self.btn_add.setAutoDefault(True)
        self.btn_add.setDefault(True)
        self.btn_add.setObjectName("btn_add")
        self.horizontalLayout_10.addWidget(self.btn_add)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem9)

        self.retranslateUi(NouvelleActivite)
        QtCore.QMetaObject.connectSlotsByName(NouvelleActivite)

    def retranslateUi(self, NouvelleActivite):
        _translate = QtCore.QCoreApplication.translate
        NouvelleActivite.setWindowTitle(_translate("NouvelleActivite", "Nouvelle activité"))
        self.lbl_titre.setText(_translate("NouvelleActivite", "Nouvelle activité"))
        self.label_8.setText(_translate("NouvelleActivite", "Catégorie d\'activité : "))
        self.label_2.setText(_translate("NouvelleActivite", "Type d\'activité : "))
        self.rbt_unique.setText(_translate("NouvelleActivite", "Unique"))
        self.rbt_hebdomadaire.setText(_translate("NouvelleActivite", "Hebdomadaire"))
        self.lbl_unique.setText(_translate("NouvelleActivite", "Date :"))
        self.lbl_debut.setText(_translate("NouvelleActivite", "Début : "))
        self.lbl_fin.setText(_translate("NouvelleActivite", "Fin : "))
        self.lbl_exclusion.setStatusTip(_translate("NouvelleActivite", "Retirer les dates où l\'activité n\'a pas lieu"))
        self.lbl_exclusion.setText(_translate("NouvelleActivite", "Exclusion : "))
        self.btn_ajouter_exclusion.setText(_translate("NouvelleActivite", "Ajouter"))
        self.txt_exclusion.setPlaceholderText(_translate("NouvelleActivite", "Liste des exclusions"))
        self.btn_vider.setText(_translate("NouvelleActivite", "Vider"))
        self.label.setText(_translate("NouvelleActivite", "Fin des inscriptions : "))
        self.label_4.setText(_translate("NouvelleActivite", "jour(s) avant l\'activité"))
        self.label_6.setText(_translate("NouvelleActivite", "Heure de début : "))
        self.label_7.setText(_translate("NouvelleActivite", "Heure de fin : "))
        self.btn_cancel.setText(_translate("NouvelleActivite", "Annuler"))
        self.btn_add.setText(_translate("NouvelleActivite", "Ajouter"))

