from PySide6.QtWidgets import (
    QApplication,
    QLineEdit,
    QTextEdit,
    QSpinBox,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QMessageBox
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import sys
import Optimisation_prix_production as data_base
import random


class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("first_page.ui")

        if not ui_file.open(QFile.ReadOnly):
            print("Impossible d'ouvrir le fichier .ui")
            sys.exit(1)

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            print("Le chargement du fichier .ui a échoué")
            sys.exit(1)

        # === Widgets généraux ===
        self.inputProductName = self.window.findChild(QLineEdit, "inputProductName")
        self.inputDescription = self.window.findChild(QTextEdit, "inputDescription")

        # === Widgets d'ajout d'étape ===
        self.inputStepNumber = self.window.findChild(QSpinBox, "inputStepNumber")
        self.inputStepName = self.window.findChild(QLineEdit, "inputStepName")
        self.inputStepMachine = self.window.findChild(QComboBox, "inputStepMachine")
        self.inputStepDuration = self.window.findChild(QSpinBox, "inputStepDuration")
        self.btnAddStep = self.window.findChild(QPushButton, "btnAddStep")
        self.btnCreateMachine = self.window.findChild(QPushButton, "btnCreateMachine")
        self.btnValidate = self.window.findChild(QPushButton, "btnValidate")
        # === Tableau des étapes ===
        self.tableSteps = self.window.findChild(QTableWidget, "tableSteps")

        # Vérifications de sécurité
        required_widgets = {
            "inputProductName": self.inputProductName,
            "inputDescription": self.inputDescription,
            "inputStepNumber": self.inputStepNumber,
            "inputStepName": self.inputStepName,
            "inputStepMachine": self.inputStepMachine,
            "inputStepDuration": self.inputStepDuration,
            "btnAddStep": self.btnAddStep,
            "btnCreateMachine": self.btnCreateMachine,
            "tableSteps": self.tableSteps,
        }

        for name, widget in required_widgets.items():
            if widget is None:
                print(f"Widget introuvable dans le .ui : {name}")
                sys.exit(1)

        # Configuration du tableau
        self.setup_table()

        # Le menu machine est vide au départ
        self.inputStepMachine.clear()

        # Connexions des boutons
        self.btnAddStep.clicked.connect(self.add_step_to_table)
        #self.btnCreateMachine.clicked.connect(self.open_create_machine_page)
        self.btnValidate.clicked.connect(self.add_produit_data_base)

    # ---------------------------------------------------------
    # CONFIGURATION DU TABLEAU
    # ---------------------------------------------------------
    def setup_table(self):
        self.tableSteps.setColumnCount(5)
        self.tableSteps.setHorizontalHeaderLabels([
            "N°",
            "Nom de l'étape",
            "Machine",
            "Durée (s)",
            "Action"
        ])

        self.tableSteps.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
            | QAbstractItemView.AnyKeyPressed
        )

        self.tableSteps.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableSteps.setAlternatingRowColors(True)

    # ---------------------------------------------------------
    # AJOUT D’UNE ÉTAPE DANS LE TABLEAU
    # ---------------------------------------------------------
    def add_step_to_table(self):
        step_number = self.inputStepNumber.value()
        step_name = self.inputStepName.text().strip()
        machine = self.inputStepMachine.currentText().strip()
        duration = self.inputStepDuration.value()

        # Vérification du nom
        if step_name == "":
            QMessageBox.warning(
                self.window,
                "Champ manquant",
                "Veuillez saisir un nom d'étape."
            )
            return

        # Vérification machine
        if machine == "":
            QMessageBox.warning(
                self.window,
                "Machine manquante",
                "Veuillez sélectionner une machine ou en créer une nouvelle."
            )
            return

        # Ajouter une ligne
        row = self.tableSteps.rowCount()
        self.tableSteps.insertRow(row)

        # Créer les cellules
        item_number = QTableWidgetItem(str(step_number))
        item_name = QTableWidgetItem(step_name)
        item_machine = QTableWidgetItem(machine)
        item_duration = QTableWidgetItem(str(duration))
        item_action = QTableWidgetItem("Supprimer")

        # Insérer les cellules
        self.tableSteps.setItem(row, 0, item_number)
        self.tableSteps.setItem(row, 1, item_name)
        self.tableSteps.setItem(row, 2, item_machine)
        self.tableSteps.setItem(row, 3, item_duration)
        self.tableSteps.setItem(row, 4, item_action)

        # Réinitialiser certains champs
        self.inputStepName.clear()
        self.inputStepDuration.setValue(1)

        print(f"Étape ajoutée : {step_number} - {step_name} - {machine} - {duration}s")

    # ---------------------------------------------------------
    # FUTURE PAGE DE CRÉATION DE MACHINE
    # ---------------------------------------------------------
    def add_produit_data_base(self):
        data_base.insert_Produit(random.randint(1000000000, 9999999999), self.inputProductName.text().strip(), self.inputDescription.toPlainText().strip())

    # ---------------------------------------------------------
    # EXEMPLE : AJOUT MANUEL D'UNE MACHINE
    # ---------------------------------------------------------
    def add_machine_to_combo(self, machine_name):
        machine_name = machine_name.strip()
        if machine_name == "":
            return

        # Éviter les doublons
        existing_machines = [
            self.inputStepMachine.itemText(i)
            for i in range(self.inputStepMachine.count())
        ]

        if machine_name not in existing_machines:
            self.inputStepMachine.addItem(machine_name)
