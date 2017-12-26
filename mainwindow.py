# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui = os.path.join(os.path.dirname(__file__),'UI','mainwindow.ui')
        uic.loadUi(ui, self)
        self.set_participantes_central_widget()

        # Actions
        self.act_consult_participantes.triggered.connect(self.set_participantes_central_widget)
        self.act_consult_activites.triggered.connect(self.set_activite_central_widget)
        self.act_consult_lieux.triggered.connect(self.set_lieux_central_widget)
        self.act_consult_type_activite.triggered.connect(self.set_categorie_activite_central_widget)

    def set_participantes_central_widget(self):
        """
        Affichage de la liste des participantes et des options de tri
        :return: Aucun
        """
        central_widget = CentralWidgetParticipantes()
        self.setCentralWidget(central_widget)

    def set_activite_central_widget(self):
        """
        Affichage de la liste des activites et des options de tri
        :return: Aucun
        """
        central_widget = CentralWidgetActivite()
        self.setCentralWidget(central_widget)

    def set_categorie_activite_central_widget(self):
        """
        Affichage de la liste des type d'activite et des options de tri
        :return: Aucun
        """
        central_widget = CentralWidgetCategorieActivite()
        self.setCentralWidget(central_widget)

    def set_lieux_central_widget(self):
        """
        Affichage des lieux et des options de tri
        :return:
        """
        central_widget = CentralWidgetLieux()
        self.setCentralWidget(central_widget)


"""
Classe principale pour les CentralWidget
Contient les fonction communes à tout les CentralWidget
"""
class CentralWidget(QWidget):
    def __init__(self):
        super(CentralWidget, self).__init__()
        self.layout = QVBoxLayout(self)


"""
CentralWidget spécifiques :
- Options de tri spécifique
- Tableau avec les informations à afficher
"""
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


class CentralWidgetCategorieActivite(CentralWidget):
    def __init__(self):
        super(CentralWidgetCategorieActivite, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'UI', 'widget_categorie_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)
