from PySide6.QtWidgets import (
    QDoubleSpinBox,
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
        self.btnCreateMachine.clicked.connect(self.open_machine_creation)
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

        '''self.tableSteps.setEditTriggers(
            QAbstractItemView.DoubleClicked
            | QAbstractItemView.SelectedClicked
            | QAbstractItemView.EditKeyPressed
            | QAbstractItemView.AnyKeyPressed
        )'''

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
        ID_produit = random.randint(1000000000, 9999999999)
        ID_machine = data_base.select_Machine("Nom_machine='{machine}'")[0][0] # Récupérer l'ID de la machine "Four" pour l'exemple
        data_base.insert_Produit(ID_produit, self.inputProductName.text().strip(), self.inputDescription.toPlainText().strip())
        data_base.insert_Etape(random.randint(1000000000, 9999999999), self.inputStepName.text().strip(), self.inputStepMachine.currentText().strip(), self.inputStepDuration.value(), ID_produit,ID_machine)
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

    def open_machine_creation(self):
        self.machine_window = MachineWindow(on_machine_added=self.add_machine_to_combo)
        self.machine_window.window.show()

class MachineWindow:
    def __init__(self, on_machine_added=None):
        self.on_machine_added = on_machine_added

        loader = QUiLoader()
        ui_file = QFile("add_machine.ui")   # <-- on charge bien add_machine.ui

        if not ui_file.open(QFile.ReadOnly):
            print("Impossible d'ouvrir le fichier add_machine.ui")
            sys.exit(1)

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            print("Le chargement du fichier add_machine.ui a échoué")
            sys.exit(1)

        # Champs texte
        self.inputMachineName = self.window.findChild(QLineEdit, "inputMachineName")
        self.inputOperatorLastName = self.window.findChild(QLineEdit, "inputOperatorLastName")
        self.inputOperatorFirstName = self.window.findChild(QLineEdit, "inputOperatorFirstName")
        self.inputOperatorEmail = self.window.findChild(QLineEdit, "inputOperatorEmail")
        self.inputMachineNotes = self.window.findChild(QTextEdit, "inputMachineNotes")

        # Champs numériques
        self.inputCycleDuration = self.window.findChild(QSpinBox, "inputCycleDuration")
        self.inputElectricPower = self.window.findChild(QDoubleSpinBox, "inputElectricPower")

        # Boutons
        self.btnSaveMachine = self.window.findChild(QPushButton, "btnSaveMachine")
        self.btnCancelMachine = self.window.findChild(QPushButton, "btnCancelMachine")

        # === Vérification de sécurité ===
        required_widgets = {
            "inputMachineName": self.inputMachineName,
            "inputCycleDuration": self.inputCycleDuration,
            "inputElectricPower": self.inputElectricPower,
            "inputOperatorLastName": self.inputOperatorLastName,
            "inputOperatorFirstName": self.inputOperatorFirstName,
            "inputOperatorEmail": self.inputOperatorEmail,
            "btnSaveMachine": self.btnSaveMachine,
            "btnCancelMachine": self.btnCancelMachine,
        }

        for name, widget in required_widgets.items():
            if widget is None:
                print(f"Widget introuvable dans add_machine.ui : {name}")
                sys.exit(1)

        # === Connexions ===
        self.btnSaveMachine.clicked.connect(self.save_machine)
        self.btnCancelMachine.clicked.connect(self.close_window)

    def close_window(self):
        self.window.close()

    def get_machine_data(self):
        return {
            "name": self.inputMachineName.text().strip(),
            "cycle_duration": int(self.inputCycleDuration.text().strip()),
            "electric_power": float(self.inputElectricPower.text().strip()),
            "operator_last_name": self.inputOperatorLastName.text().strip(),
            "operator_first_name": self.inputOperatorFirstName.text().strip(),
            "operator_email": self.inputOperatorEmail.text().strip(),
            "notes": self.inputMachineNotes.toPlainText().strip() if self.inputMachineNotes else ""
        }

    def validate_fields(self, data):
        if data["name"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir le nom de la machine.")
            return False # QMessageBox.warning fait les page d'alerte 

        if data["cycle_duration"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir la durée du cycle.")
            return False

        if data["electric_power"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir la puissance électrique.")
            return False

        if data["operator_last_name"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir le nom de l'opérateur.")
            return False

        if data["operator_first_name"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir le prénom de l'opérateur.")
            return False

        if data["operator_email"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir l'email de l'opérateur.")
            return False

        # Vérification numérique simple
        try:
            int(data["cycle_duration"])
        except ValueError:
            print( data["cycle_duration"])
            print( data["cycle_duration"].type())
            QMessageBox.warning(self.window, "Valeur invalide", "La durée du cycle doit être un nombre.")
            return False

        '''try:
            float(data["electric_power"])
        except ValueError:
            QMessageBox.warning(self.window, "Valeur invalide", "La puissance électrique doit être un nombre.")
            return False'''

        # Vérification email simple
        if "@" not in data["operator_email"] or "." not in data["operator_email"]:
            QMessageBox.warning(self.window, "Email invalide", "Veuillez saisir une adresse email valide.")
            return False

        return True

    def save_machine(self):
        data = self.get_machine_data()

        if not self.validate_fields(data):
            return

        # Conversion
        cycle_duration = int(data["cycle_duration"])
        electric_power = float(data["electric_power"])
        ID_operateur = random.randint(1000000000, 9999999999)
        try:
            data_base.insert_Machine(random.randint(1000000000, 9999999999),data["name"],cycle_duration,electric_power,ID_operateur)
            data_base.insert_Operateur(ID_operateur,data["operator_first_name"],data["operator_last_name"],data["operator_email"])
            print("Machine enregistrée :")
            print(f"Nom : {data['name']}")
            print(f"Durée cycle : {cycle_duration}")
            print(f"Puissance : {electric_power}")
            print(f"Opérateur : {data['operator_first_name']} {data['operator_last_name']}")
            print(f"Email : {data['operator_email']}")
            print(f"Notes : {data['notes']}")

            # Callback vers MainWindow pour ajouter la machine dans le combo
            if self.on_machine_added is not None:
                self.on_machine_added(data["name"])

            QMessageBox.information(
                self.window,
                "Succès",
                f"La machine '{data['name']}' a bien été enregistrée."
            )

            self.window.close()
        except Exception as e:
            QMessageBox.critical(
                self.window,
                "Erreur",
                f"Erreur lors de l'enregistrement de la machine :\n{e}")

