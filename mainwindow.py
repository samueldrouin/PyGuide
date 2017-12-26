# Python import
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTableWidget
import os

# Projet import
from participante import Participante
from lieu import Lieu
from activite import Activite
from categorie_activite import CategorieActivite

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        ui = os.path.join(os.path.dirname(__file__),'GUI','mainwindow.ui')
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
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_participantes.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_participante)

    def nouvelle_participante(self):
        """
        Ouvrir le dialog pour creer une nouvelle participante
        :return:
        """
        participante = Participante(self)
        participante.setWindowTitle("Nouvelle participante")
        participante.exec()


class CentralWidgetActivite(CentralWidget):
    def __init__(self):
        super(CentralWidgetActivite, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_activite)

    def nouvelle_activite(self):
        """
        Ouvrir le dialog pour creer une nouvelle activite
        :return:
        """
        activite = Activite(self)
        activite.setWindowTitle("Nouvelle activité")
        activite.exec()


class CentralWidgetLieux(CentralWidget):
    def __init__(self):
        super(CentralWidgetLieux, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_lieux.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouveau_lieu)

    def nouveau_lieu(self):
        """
        Ouvrir le dialog pour créer un nouveau lieu
        :return:
        """
        lieu = Lieu(self)
        lieu.setWindowTitle("Nouveau lieu")
        lieu.exec()


class CentralWidgetCategorieActivite(CentralWidget):
    def __init__(self):
        super(CentralWidgetCategorieActivite, self).__init__()
        self.top_widget = QWidget()
        ui = os.path.join(os.path.dirname(__file__), 'GUI', 'CentralWidget', 'widget_categorie_activite.ui')
        uic.loadUi(ui, self.top_widget)
        self.layout.addWidget(self.top_widget)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        # Slots
        self.top_widget.btn_add.clicked.connect(self.nouvelle_categorie_activite)

    def nouvelle_categorie_activite(self):
        """
        Ouvrir le dialog pour créer une nouvelle categorie d'activite
        :return:
        """
        categorie_activite = CategorieActivite(self)
        categorie_activite.setWindowTitle("Nouvelle catégorie d'activité")
        categorie_activite.exec()
