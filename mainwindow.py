# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui = os.path.join(os.path.dirname(__file__),'UI','mainwindow.ui')
        uic.loadUi(ui, self)

        # Actions
        self.act_consult_participantes.triggered.connect(self.open_consult_participantes)
        self.act_consult_activites.triggered.connect(self.open_consult_activite)
        self.act_consult_lieux.triggered.connect(self.open_consult_lieux)
        self.act_consult_type_activite.triggered.connect(self.open_consult_type_activite)

    def open_consult_participantes(self):
        """
        Affiche le widget des options de tri pour les participantes
        Affiche la liste des participantes correspondant aux options de tri
        :return: Aucun
        """
        central_widget = CentralWidgetParticipantes()
        self.setCentralWidget(central_widget)

    def open_consult_activite(self):
        """
        Affiche le widget des options de tri pour les activités
        Affiche la liste des activités correspondant aux options de tri
        :return: Aucun
        """
        central_widget = CentralWidgetActivite()
        self.setCentralWidget(central_widget)

    def open_consult_type_activite(self):
        """
        Affiche le widget des options de tri pour les types d'activites
        Affiche la liste des types d'activites correspondant aux options de tri
        :return: Aucun
        """
        central_widget = CentralWidgetTypeActivite()
        self.setCentralWidget(central_widget)

    def open_consult_lieux(self):
        """
        Affiche le widget des options de tri pour les lieux
        Affiche la liste des lieux correspondant aux options de tri
        :return:
        """
        central_widget = CentralWidgetLieux()
        self.setCentralWidget(central_widget)


class CentralWidget(QWidget):
    def __init__(self):
        super(CentralWidget, self).__init__()
        self.layout = QVBoxLayout(self)


class CentralWidgetParticipantes(CentralWidget):
    def __init__(self):
        super(CentralWidgetParticipantes, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'widget_participantes.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)


class CentralWidgetActivite(CentralWidget):
    def __init__(self):
        super(CentralWidgetActivite, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'widget_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)


class CentralWidgetLieux(CentralWidget):
    def __init__(self):
        super(CentralWidgetLieux, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'widget_lieux.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)


class CentralWidgetTypeActivite(CentralWidget):
    def __init__(self):
        super(CentralWidgetTypeActivite, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'widget_type_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
