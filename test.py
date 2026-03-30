from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QLineEdit,
    QTextEdit,
    QSpinBox,
    QPushButton,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QMessageBox,
    QLabel,
    QTimeEdit,
    QHeaderView
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QTime
from PySide6.QtGui import QPixmap
from pathlib import Path
from datetime import datetime
import sys
import random

import Optimisation_prix_production as data_base


class MainWindow:
    def __init__(self):
        loader = QUiLoader()

        base_dir = Path(__file__).resolve().parent
        ui_path = base_dir / "interface_complet.ui"

        ui_file = QFile(str(ui_path))
        if not ui_file.open(QFile.ReadOnly):
            print("Impossible d'ouvrir le fichier interface_complet.ui")
            sys.exit(1)

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            print("Le chargement du fichier .ui a échoué")
            sys.exit(1)

        # ==========================================================
        # TAB 1 : COMMANDES
        # ==========================================================
        self.labelCurrentDate = self.window.findChild(QLabel, "labelCurrentDate")
        self.InputProductOrder = self.window.findChild(QComboBox, "InputProductOrder")
        self.inputOrderQuantity = self.window.findChild(QSpinBox, "spinBox")
        self.inputStartHour = self.window.findChild(QTimeEdit, "inputStartHour")
        self.BtnOptimize = self.window.findChild(QPushButton, "BtnOptimize")

        self.tableOrders = self.window.findChild(QTableWidget, "tableOrders")
        self.btnAddOrderLine = self.window.findChild(QPushButton, "btnAddOrderLine")
        self.btnRemoveOrderLine = self.window.findChild(QPushButton, "btnRemoveOrderLine")
        self.btnValidateOrder = self.window.findChild(QPushButton, "btnValidateOrder")
        self.labelPriceGraphImage = self.window.findChild(QLabel, "labelPriceGraphImage")

        # ==========================================================
        # TAB 2 : PRODUITS
        # ==========================================================
        self.inputProductName = self.window.findChild(QLineEdit, "inputProductName")
        self.inputDescription = self.window.findChild(QTextEdit, "inputDescription")
        self.inputStepNumber = self.window.findChild(QSpinBox, "inputStepNumber")
        self.inputStepName = self.window.findChild(QLineEdit, "inputStepName")
        self.inputStepMachine = self.window.findChild(QComboBox, "inputStepMachine")
        self.inputStepDuration = self.window.findChild(QSpinBox, "inputStepDuration")
        self.btnAddStep = self.window.findChild(QPushButton, "btnAddStep")
        self.btnCreateMachine = self.window.findChild(QPushButton, "btnCreateMachine")
        self.btnCancel = self.window.findChild(QPushButton, "btnCancel")
        self.btnValidate = self.window.findChild(QPushButton, "btnValidate")
        self.tableSteps = self.window.findChild(QTableWidget, "tableSteps")

        # ==========================================================
        # TAB 3 : BASE DE DONNÉES
        # ==========================================================
        self.inputDatabaseTable = self.window.findChild(QComboBox, "inputDatabaseTable")
        self.btnRefreshDatabase = self.window.findChild(QPushButton, "btnRefreshDatabase")
        self.btnAddDatabaseRow = self.window.findChild(QPushButton, "btnAddDatabaseRow")
        self.btnEditDatabaseRow = self.window.findChild(QPushButton, "btnEditDatabaseRow")
        self.btnDeleteDatabaseRow = self.window.findChild(QPushButton, "btnDeleteDatabaseRow")
        self.tableDatabase = self.window.findChild(QTableWidget, "tableDatabase")

        # ==========================================================
        # VÉRIFICATION DES WIDGETS
        # ==========================================================
        required_widgets = {
            # Tab 1
            "labelCurrentDate": self.labelCurrentDate,
            "InputProductOrder": self.InputProductOrder,
            "spinBox": self.inputOrderQuantity,
            "inputStartHour": self.inputStartHour,
            "BtnOptimize": self.BtnOptimize,
            "tableOrders": self.tableOrders,
            "btnAddOrderLine": self.btnAddOrderLine,
            "btnRemoveOrderLine": self.btnRemoveOrderLine,
            "btnValidateOrder": self.btnValidateOrder,
            "labelPriceGraphImage": self.labelPriceGraphImage,

            # Tab 2
            "inputProductName": self.inputProductName,
            "inputDescription": self.inputDescription,
            "inputStepNumber": self.inputStepNumber,
            "inputStepName": self.inputStepName,
            "inputStepMachine": self.inputStepMachine,
            "inputStepDuration": self.inputStepDuration,
            "btnAddStep": self.btnAddStep,
            "btnCreateMachine": self.btnCreateMachine,
            "btnCancel": self.btnCancel,
            "btnValidate": self.btnValidate,
            "tableSteps": self.tableSteps,

            # Tab 3
            "inputDatabaseTable": self.inputDatabaseTable,
            "btnRefreshDatabase": self.btnRefreshDatabase,
            "btnAddDatabaseRow": self.btnAddDatabaseRow,
            "btnEditDatabaseRow": self.btnEditDatabaseRow,
            "btnDeleteDatabaseRow": self.btnDeleteDatabaseRow,
            "tableDatabase": self.tableDatabase,
        }

        for name, widget in required_widgets.items():
            if widget is None:
                print(f"Widget introuvable dans le .ui : {name}")
                sys.exit(1)

        # ==========================================================
        # CONFIGURATION INITIALE
        # ==========================================================
        self.setup_orders_table()
        self.setup_products_table()
        self.setup_database_table()

        self.display_current_date()
        self.load_price_graph_image("grille_evaluation.png")

        self.inputStartHour.setTime(QTime.currentTime())
        self.inputStepMachine.clear()
        self.InputProductOrder.clear()

        self.load_products_in_order_combo()
        self.load_machines_in_combo()
        self.refresh_database_table()

        # ==========================================================
        # CONNEXIONS
        # ==========================================================
        # Tab 1
        self.btnAddOrderLine.clicked.connect(self.add_order_line)
        self.btnRemoveOrderLine.clicked.connect(self.remove_order_line)
        self.btnValidateOrder.clicked.connect(self.validate_order)
        self.BtnOptimize.clicked.connect(self.optimize_start_hour)

        # Tab 2
        self.btnAddStep.clicked.connect(self.add_step_to_table)
        self.btnCreateMachine.clicked.connect(self.open_machine_creation)
        self.btnCancel.clicked.connect(self.clear_product_form)
        self.btnValidate.clicked.connect(self.add_produit_data_base)

        # Tab 3
        self.btnRefreshDatabase.clicked.connect(self.refresh_database_table)
        self.btnAddDatabaseRow.clicked.connect(self.add_database_row)
        self.btnEditDatabaseRow.clicked.connect(self.edit_database_row)
        self.btnDeleteDatabaseRow.clicked.connect(self.delete_database_row)
        self.inputDatabaseTable.currentIndexChanged.connect(self.refresh_database_table)

    # ==========================================================
    # AFFICHAGE
    # ==========================================================
    def show(self):
        self.window.show()

    # ==========================================================
    # TAB 1 : COMMANDES
    # ==========================================================
    def display_current_date(self):
        self.labelCurrentDate.setText(datetime.now().strftime("%d/%m/%Y"))

    def load_price_graph_image(self, image_name):
        image_path = Path(__file__).resolve().parent / image_name

        if image_path.exists():
            pixmap = QPixmap(str(image_path))
            self.labelPriceGraphImage.setPixmap(
                pixmap.scaled(
                    self.labelPriceGraphImage.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
            )
        else:
            self.labelPriceGraphImage.setText("Image du graphique introuvable")

    def setup_orders_table(self):
        self.tableOrders.setColumnCount(5)
        self.tableOrders.setHorizontalHeaderLabels([
            "Produit",
            "Quantité",
            "Prix",
            "Heure de début",
            "Heure de fin"
        ])
        self.tableOrders.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableOrders.setAlternatingRowColors(True)
        self.tableOrders.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def load_products_in_order_combo(self):
        self.InputProductOrder.clear()
        try:
            produits = data_base.select_Produit("1=1")
            for produit in produits:
                # suppose : [id, nom, description]
                self.InputProductOrder.addItem(str(produit[1]))
        except Exception:
            # si la DB n'est pas encore prête
            self.InputProductOrder.addItems([
                "Produit A",
                "Produit B",
                "Produit C"
            ])

    def optimize_start_hour(self):
        # Placeholder simple
        self.inputStartHour.setTime(QTime(8, 0))
        QMessageBox.information(
            self.window,
            "Optimisation",
            "Heure de début optimisée à 08:00."
        )

    def add_order_line(self):
        product_name = self.InputProductOrder.currentText().strip()
        quantity = self.inputOrderQuantity.value()
        start_time = self.inputStartHour.time().toString("HH:mm")

        if product_name == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez sélectionner un produit.")
            return

        if quantity <= 0:
            QMessageBox.warning(self.window, "Valeur invalide", "La quantité doit être supérieure à 0.")
            return

        # Prix estimé fictif
        estimated_price = round(quantity * 2.5, 2)

        # Heure de fin fictive : +30 min
        start_qtime = self.inputStartHour.time()
        end_qtime = start_qtime.addSecs(30 * 60)
        end_time = end_qtime.toString("HH:mm")

        row = self.tableOrders.rowCount()
        self.tableOrders.insertRow(row)

        self.tableOrders.setItem(row, 0, QTableWidgetItem(product_name))
        self.tableOrders.setItem(row, 1, QTableWidgetItem(str(quantity)))
        self.tableOrders.setItem(row, 2, QTableWidgetItem(f"{estimated_price:.2f} €"))
        self.tableOrders.setItem(row, 3, QTableWidgetItem(start_time))
        self.tableOrders.setItem(row, 4, QTableWidgetItem(end_time))

    def remove_order_line(self):
        current_row = self.tableOrders.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.window, "Aucune ligne sélectionnée", "Veuillez sélectionner une ligne.")
            return
        self.tableOrders.removeRow(current_row)

    def validate_order(self):
        if self.tableOrders.rowCount() == 0:
            QMessageBox.warning(self.window, "Commande vide", "Veuillez ajouter au moins un produit.")
            return

        total_price = 0.0
        for row in range(self.tableOrders.rowCount()):
            price_text = self.tableOrders.item(row, 2).text().replace("€", "").strip().replace(",", ".")
            try:
                total_price += float(price_text)
            except ValueError:
                pass

        QMessageBox.information(
            self.window,
            "Commande validée",
            f"Commande enregistrée avec succès.\nPrix total estimé : {total_price:.2f} €"
        )

    # ==========================================================
    # TAB 2 : PRODUITS
    # ==========================================================
    def setup_products_table(self):
        self.tableSteps.setColumnCount(5)
        self.tableSteps.setHorizontalHeaderLabels([
            "N°",
            "Nom de l'étape",
            "Machine",
            "Durée (s)",
            "Action"
        ])
        self.tableSteps.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableSteps.setAlternatingRowColors(True)
        self.tableSteps.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def load_machines_in_combo(self):
        self.inputStepMachine.clear()
        try:
            machines = data_base.select_Machine("1=1")
            for machine in machines:
                # suppose : [id, nom, ...]
                self.inputStepMachine.addItem(str(machine[1]))
        except Exception:
            # si la DB n'est pas encore prête
            self.inputStepMachine.addItems([
                "Machine 1",
                "Machine 2",
                "Machine 3"
            ])

    def add_step_to_table(self):
        step_number = self.inputStepNumber.value()
        step_name = self.inputStepName.text().strip()
        machine = self.inputStepMachine.currentText().strip()
        duration = self.inputStepDuration.value()

        if step_name == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir un nom d'étape.")
            return

        if machine == "":
            QMessageBox.warning(self.window, "Machine manquante", "Veuillez sélectionner une machine.")
            return

        row = self.tableSteps.rowCount()
        self.tableSteps.insertRow(row)

        self.tableSteps.setItem(row, 0, QTableWidgetItem(str(step_number)))
        self.tableSteps.setItem(row, 1, QTableWidgetItem(step_name))
        self.tableSteps.setItem(row, 2, QTableWidgetItem(machine))
        self.tableSteps.setItem(row, 3, QTableWidgetItem(str(duration)))
        self.tableSteps.setItem(row, 4, QTableWidgetItem("Supprimer"))

        self.inputStepName.clear()
        self.inputStepDuration.setValue(1)

    def add_produit_data_base(self):
        product_name = self.inputProductName.text().strip()
        description = self.inputDescription.toPlainText().strip()

        if product_name == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir un nom de produit.")
            return

        if self.tableSteps.rowCount() == 0:
            QMessageBox.warning(self.window, "Aucune étape", "Veuillez ajouter au moins une étape.")
            return

        try:
            ID_produit = random.randint(1000000000, 9999999999)
            data_base.insert_Produit(ID_produit, product_name, description)

            for row in range(self.tableSteps.rowCount()):
                step_name = self.tableSteps.item(row, 1).text()
                machine_name = self.tableSteps.item(row, 2).text()
                duration = int(self.tableSteps.item(row, 3).text())

                result_machine = data_base.select_Machine(f"Nom_machine='{machine_name}'")
                if not result_machine:
                    raise Exception(f"Machine introuvable : {machine_name}")

                ID_machine = result_machine[0][0]

                data_base.insert_Etape(
                    random.randint(1000000000, 9999999999),
                    step_name,
                    machine_name,
                    duration,
                    ID_produit,
                    ID_machine
                )

            QMessageBox.information(
                self.window,
                "Succès",
                f"Le produit '{product_name}' a bien été enregistré."
            )

            self.clear_product_form()
            self.load_products_in_order_combo()
            self.refresh_database_table()

        except Exception as e:
            QMessageBox.critical(
                self.window,
                "Erreur",
                f"Erreur lors de l'enregistrement du produit :\n{e}"
            )

    def clear_product_form(self):
        self.inputProductName.clear()
        self.inputDescription.clear()
        self.inputStepNumber.setValue(1)
        self.inputStepName.clear()
        self.inputStepDuration.setValue(1)
        self.tableSteps.setRowCount(0)

    def add_machine_to_combo(self, machine_name):
        machine_name = machine_name.strip()
        if machine_name == "":
            return

        existing_machines = [self.inputStepMachine.itemText(i) for i in range(self.inputStepMachine.count())]

        if machine_name not in existing_machines:
            self.inputStepMachine.addItem(machine_name)

    def open_machine_creation(self):
        self.machine_window = MachineWindow(on_machine_added=self.add_machine_to_combo)
        self.machine_window.window.show()

    # ==========================================================
    # TAB 3 : BASE DE DONNÉES
    # ==========================================================
    def setup_database_table(self):
        self.tableDatabase.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableDatabase.setAlternatingRowColors(True)
        self.tableDatabase.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def refresh_database_table(self):
        table_name = self.inputDatabaseTable.currentText()

        self.tableDatabase.clearContents()
        self.tableDatabase.setRowCount(0)

        try:
            if table_name == "Produits":
                self.load_products_in_database_table()
            elif table_name == "Machines":
                self.load_machines_in_database_table()
            elif table_name == "Étapes":
                self.load_steps_in_database_table()
            elif table_name == "Opérateurs":
                self.load_operators_in_database_table()
        except Exception as e:
            QMessageBox.critical(
                self.window,
                "Erreur",
                f"Impossible de charger la table {table_name} :\n{e}"
            )

    def load_products_in_database_table(self):
        self.tableDatabase.setColumnCount(3)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Nom", "Description"])

        rows = data_base.select_Produit("1=1")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:3]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_machines_in_database_table(self):
        self.tableDatabase.setColumnCount(4)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Nom", "Cycle", "Puissance"])

        rows = data_base.select_Machine("1=1")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:4]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_steps_in_database_table(self):
        self.tableDatabase.setColumnCount(6)
        self.tableDatabase.setHorizontalHeaderLabels([
            "ID", "Nom étape", "Machine", "Durée", "ID Produit", "ID Machine"
        ])

        rows = data_base.select_Etape("1=1")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:6]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_operators_in_database_table(self):
        self.tableDatabase.setColumnCount(4)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Prénom", "Nom", "Email"])

        rows = data_base.select_Operateur("1=1")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:4]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def add_database_row(self):
        table_name = self.inputDatabaseTable.currentText()
        QMessageBox.information(
            self.window,
            "Ajouter",
            f"Fonction d'ajout à coder pour la table : {table_name}"
        )

    def edit_database_row(self):
        current_row = self.tableDatabase.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.window, "Aucune ligne sélectionnée", "Veuillez sélectionner une ligne.")
            return

        table_name = self.inputDatabaseTable.currentText()
        QMessageBox.information(
            self.window,
            "Modifier",
            f"Fonction de modification à coder pour la table : {table_name}"
        )

    def delete_database_row(self):
        current_row = self.tableDatabase.currentRow()
        if current_row < 0:
            QMessageBox.warning(self.window, "Aucune ligne sélectionnée", "Veuillez sélectionner une ligne.")
            return

        reply = QMessageBox.question(
            self.window,
            "Confirmation",
            "Voulez-vous supprimer la ligne sélectionnée ?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.No:
            return

        self.tableDatabase.removeRow(current_row)
        QMessageBox.information(self.window, "Suppression", "La ligne a été supprimée du tableau.")

    # ==========================================================
    # UTILITAIRE
    # ==========================================================
    def close(self):
        self.window.close()


class MachineWindow:
    def __init__(self, on_machine_added=None):
        self.on_machine_added = on_machine_added

        loader = QUiLoader()
        ui_path = Path(__file__).resolve().parent / "add_machine.ui"

        ui_file = QFile(str(ui_path))
        if not ui_file.open(QFile.ReadOnly):
            print("Impossible d'ouvrir le fichier add_machine.ui")
            sys.exit(1)

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            print("Le chargement du fichier add_machine.ui a échoué")
            sys.exit(1)

        self.inputMachineName = self.window.findChild(QLineEdit, "inputMachineName")
        self.inputOperatorLastName = self.window.findChild(QLineEdit, "inputOperatorLastName")
        self.inputOperatorFirstName = self.window.findChild(QLineEdit, "inputOperatorFirstName")
        self.inputOperatorEmail = self.window.findChild(QLineEdit, "inputOperatorEmail")
        self.inputMachineNotes = self.window.findChild(QTextEdit, "inputMachineNotes")
        self.inputCycleDuration = self.window.findChild(QSpinBox, "inputCycleDuration")
        self.inputElectricPower = self.window.findChild(QDoubleSpinBox, "inputElectricPower")
        self.btnSaveMachine = self.window.findChild(QPushButton, "btnSaveMachine")
        self.btnCancelMachine = self.window.findChild(QPushButton, "btnCancelMachine")

        required_widgets = {
            "inputMachineName": self.inputMachineName,
            "inputOperatorLastName": self.inputOperatorLastName,
            "inputOperatorFirstName": self.inputOperatorFirstName,
            "inputOperatorEmail": self.inputOperatorEmail,
            "inputCycleDuration": self.inputCycleDuration,
            "inputElectricPower": self.inputElectricPower,
            "btnSaveMachine": self.btnSaveMachine,
            "btnCancelMachine": self.btnCancelMachine,
        }

        for name, widget in required_widgets.items():
            if widget is None:
                print(f"Widget introuvable dans add_machine.ui : {name}")
                sys.exit(1)

        self.btnSaveMachine.clicked.connect(self.save_machine)
        self.btnCancelMachine.clicked.connect(self.window.close)

    def save_machine(self):
        machine_name = self.inputMachineName.text().strip()
        cycle_duration = self.inputCycleDuration.value()
        electric_power = self.inputElectricPower.value()
        operator_last_name = self.inputOperatorLastName.text().strip()
        operator_first_name = self.inputOperatorFirstName.text().strip()
        operator_email = self.inputOperatorEmail.text().strip()

        if machine_name == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir le nom de la machine.")
            return

        if operator_last_name == "" or operator_first_name == "" or operator_email == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez remplir les informations opérateur.")
            return

        if "@" not in operator_email or "." not in operator_email:
            QMessageBox.warning(self.window, "Email invalide", "Veuillez saisir une adresse email valide.")
            return

        try:
            ID_machine = random.randint(1000000000, 9999999999)
            ID_operateur = random.randint(1000000000, 9999999999)

            data_base.insert_Machine(ID_machine, machine_name, cycle_duration, electric_power, ID_operateur)
            data_base.insert_Operateur(ID_operateur, operator_first_name, operator_last_name, operator_email)

            if self.on_machine_added is not None:
                self.on_machine_added(machine_name)

            QMessageBox.information(
                self.window,
                "Succès",
                f"La machine '{machine_name}' a bien été enregistrée."
            )
            self.window.close()

        except Exception as e:
            QMessageBox.critical(
                self.window,
                "Erreur",
                f"Erreur lors de l'enregistrement de la machine :\n{e}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())