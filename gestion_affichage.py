from PySide6.QtWidgets import (
    QFormLayout,
    QAbstractItemView,
    QComboBox,
    QDoubleSpinBox,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QTimeEdit
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt, QTime
import sys
import Optimisation_prix_production as data_base
from PySide6.QtGui import QPixmap
from pathlib import Path
from datetime import datetime

class MainWindow:
    def __init__(self):
        loader = QUiLoader()
        ui_file = QFile("interface_complet.ui")

        if not ui_file.open(QFile.ReadOnly):
            print("Impossible d'ouvrir le fichier .ui")
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
        self.step_liste = []
        self.inputProductName = self.window.findChild(QLineEdit, "inputProductName")
        self.inputDescription = self.window.findChild(QTextEdit, "inputDescription")
        self.inputStepNumber = self.window.findChild(QSpinBox, "inputStepNumber")
        self.inputStepName = self.window.findChild(QLineEdit, "inputStepName")
        self.inputStepMachine = self.window.findChild(QComboBox, "inputStepMachine")
        self.inputStepDuration = self.window.findChild(QSpinBox, "inputStepDuration")
        self.btnAddStep = self.window.findChild(QPushButton, "btnAddStep")
        self.btnCreateMachine = self.window.findChild(QPushButton, "btnCreateMachine")
        self.btnValidate = self.window.findChild(QPushButton, "btnValidate")
        self.btnCancel = self.window.findChild(QPushButton, "btnCancel")
        # === Tableau des étapes ===
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
        self.load_price_graph_image("graphique_prix_2026-03-31_18-34-44.png")

        self.inputStartHour.setTime(QTime.currentTime())
        self.inputStepMachine.clear()
        self.InputProductOrder.clear()

        self.load_products_in_order_combo()
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
    # TAB 1 : COMMANDES
    # ==========================================================
    def display_current_date(self):
        self.labelCurrentDate.setText(datetime.now().strftime("%d/%m/%Y"))

    def load_price_graph_image(self, image_name):
        pixmap = QPixmap(image_name)
        if not pixmap.isNull():
            self.labelPriceGraphImage.setPixmap(pixmap)
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
            self.InputProductOrder.addItems(["Créé un produit dans l'onglet Produits"])

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

    def clear_product_form(self):
        self.inputProductName.clear()
        self.inputDescription.clear()
        self.inputStepNumber.setValue(1)
        self.inputStepName.clear()
        self.inputStepDuration.setValue(1)
        self.tableSteps.setRowCount(0)

    # AJOUT D’UNE ÉTAPE DANS LE TABLEAU
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
        self.step_liste.append((step_name, step_number, duration, machine))

    def add_produit_data_base(self):
        Name_produit = self.inputProductName.text().strip()
        data_base.insert_Produit(Name_produit, self.inputDescription.toPlainText().strip())
        ID_produit = data_base.select_Produit(f"Nom_produit='{Name_produit}'")[0][0]
        for step in self.step_liste:
            ID_machine = data_base.select_Machine(f"Nom_machine='{step[3]}'")[0][0] # Récupérer l'ID de la machine "Four" pour l'exemple
            data_base.insert_Etape(step[0], step[1], step[2], ID_produit, ID_machine)
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
        self.tableDatabase.setColumnCount(3)#nombre de collonnes à afficher
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Nom", "Description"])

        rows = data_base.select_Produit("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:3]):#afficher les 3 premières colonnes (ID, Nom, Description)
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_machines_in_database_table(self):
        self.tableDatabase.setColumnCount(5)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Nom","Durée" ,"Puissance", "ID opérateur"])

        rows = data_base.select_Machine("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:5]): 
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_steps_in_database_table(self):
        self.tableDatabase.setColumnCount(6)
        self.tableDatabase.setHorizontalHeaderLabels([
            "ID", "Nom Étape", "N° Éxecution", "Durée", "ID Produit", "ID Machine"
        ])

        rows = data_base.select_Etape("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:6]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_operators_in_database_table(self):
        self.tableDatabase.setColumnCount(4)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Prénom", "Nom", "Email"])

        rows = data_base.select_Operateur("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:4]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def add_database_row(self):
        self.tabWidget = self.window.findChild(QTabWidget, "tabWidget")# Récupérer le QTabWidget
        for i in range(self.tabWidget.count()):# Parcourir les onglets pour trouver celui qui correspond à "Produits"
            if self.tabWidget.tabText(i) == "Produits":
                self.tabWidget.setCurrentIndex(i)# Afficher l'onglet "Produits"
                break

    def edit_database_row(self):
        current_row = self.tableDatabase.currentRow()
        if current_row < 0:
            QMessageBox.warning(
                self.window,
                "Aucune ligne sélectionnée",
                "Veuillez sélectionner une ligne.") 
            return
        table_name = self.inputDatabaseTable.currentText()
        row_data = []
        for col in range(self.tableDatabase.columnCount()):
            item = self.tableDatabase.item(current_row, col)
            row_data.append(item.text() if item else "")

        self.edit_window = EditRowWindow(
            table_name=table_name,
            row_data=row_data,
            on_save_callback=self.refresh_database_table,
            parent=self.window)
        
        self.edit_window.show()

    def delete_database_row(self):
        table_name = self.inputDatabaseTable.currentText()
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
        elif reply == QMessageBox.Yes:
            if table_name == "Produits":
                data_base.delete_Produit(f"ID_produit={self.tableDatabase.item(current_row, 0).text()}")
            elif table_name == "Machines":
                data_base.delete_Machine(f"ID_machine={self.tableDatabase.item(current_row, 0).text()}")
            elif table_name == "Étapes":
                data_base.delete_Etape(f"ID_etape={self.tableDatabase.item(current_row, 0).text()}")
            elif table_name == "Opérateurs":
                data_base.delete_Operateur(f"ID_operateur={self.tableDatabase.item(current_row, 0).text()}")

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
        try:
            data_base.insert_Operateur(data["operator_last_name"], data["operator_first_name"], data["operator_email"])
            print(data_base.select_Operateur(f"Nom_operateur='{data['operator_last_name']}' AND Prenom_operateur='{data['operator_first_name']}' AND Email='{data['operator_email']}'"))
            ID_operateur = data_base.select_Operateur(f"Nom_operateur='{data['operator_last_name']}' AND Prenom_operateur='{data['operator_first_name']}' AND Email='{data['operator_email']}'")[0][0]
            data_base.insert_Machine(data["name"],cycle_duration,electric_power,ID_operateur)
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


class EditRowWindow:
    def __init__(self, table_name, row_data, on_save_callback=None, parent=None):
        self.table_name = table_name
        self.row_data = row_data
        self.on_save_callback = on_save_callback
        self.parent = parent
        self.inputs = {}

        loader = QUiLoader()
        ui_file = QFile("edit_row_window.ui")

        if not ui_file.open(QFile.ReadOnly):
            print("Impossible d'ouvrir le fichier .ui")
            sys.exit(1)

        self.window = loader.load(ui_file)
        ui_file.close()

        if self.window is None:
            print("Le chargement du fichier .ui a échoué")
            sys.exit(1)

        self.labelTitle = self.window.findChild(QLabel, "labelTitle")
        self.labelSubtitle = self.window.findChild(QLabel, "labelSubtitle")
        self.btnSave = self.window.findChild(QPushButton, "btnSave")
        self.btnCancel = self.window.findChild(QPushButton, "btnCancel")
        self.formFieldsLayout = self.window.findChild(QFormLayout, "formFieldsLayout")

        required = {
            "labelTitle": self.labelTitle,
            "labelSubtitle": self.labelSubtitle,
            "btnSave": self.btnSave,
            "btnCancel": self.btnCancel,
            "formFieldsLayout": self.formFieldsLayout,
        }
        for name, widget in required.items():
            if widget is None:
                raise RuntimeError(f"Widget introuvable dans edit_row_window.ui : {name}")

        self.labelTitle.setText(f"Modifier : {self.table_name}")
        self.labelSubtitle.setText(
            "Modifiez les champs de la ligne sélectionnée puis cliquez sur Enregistrer."
        )

        self.build_form()

        self.btnSave.clicked.connect(self.save_changes)
        self.btnCancel.clicked.connect(self.window.close)

    def show(self):
        self.window.show()

    def get_labels_for_table(self):
        if self.table_name == "Produits":
            return ["ID", "Nom", "Description"]
        if self.table_name == "Machines":
            return ["ID", "Nom", "Durée", "Puissance", "ID opérateur"]
        if self.table_name == "Étapes":
            return ["ID", "Nom étape", "Numéro exécution", "Durée", "ID produit", "ID machine"]
        if self.table_name == "Opérateurs":
            return ["ID", "Nom", "Prénom", "Email"]
        return [f"Champ {i + 1}" for i in range(len(self.row_data))]

    def build_form(self):
        labels = self.get_labels_for_table()

        for i, label_text in enumerate(labels):
            line_edit = QLineEdit()
            line_edit.setText(str(self.row_data[i]) if i < len(self.row_data) else "")

            if i == 0:
                line_edit.setReadOnly(True)

            self.inputs[label_text] = line_edit
            self.formFieldsLayout.addRow(f"{label_text} :", line_edit)

    def save_changes(self):
        try:
            if self.table_name == "Produits":
                self._save_produit()
            elif self.table_name == "Machines":
                self._save_machine()
            elif self.table_name == "Étapes":
                self._save_etape()
            elif self.table_name == "Opérateurs":
                self._save_operateur()
            else:
                QMessageBox.warning(self.window, "Table non gérée", f"La table '{self.table_name}' n'est pas encore gérée.")
                return

            QMessageBox.information(self.window, "Succès", "Modification enregistrée avec succès.")

            if self.on_save_callback is not None:
                self.on_save_callback()

            self.window.close()

        except Exception as e:
            QMessageBox.critical(self.window, "Erreur", f"Impossible d'enregistrer les modifications :\n{e}")

    def _save_produit(self):
        id_produit = int(self.inputs["ID"].text())
        nom = self.inputs["Nom"].text().strip()
        description = self.inputs["Description"].text().strip()

        if nom == "":
            raise ValueError("Le nom du produit ne peut pas être vide.")

        data_base.update_Produit(id_produit, nom, description, f"ID_produit={id_produit}")

    def _save_machine(self):
        id_machine = int(self.inputs["ID"].text())
        nom = self.inputs["Nom"].text().strip()
        duree = int(self.inputs["Durée"].text())
        puissance = float(self.inputs["Puissance"].text().replace(",", "."))
        id_operateur = int(self.inputs["ID opérateur"].text())

        if nom == "":
            raise ValueError("Le nom de la machine ne peut pas être vide.")

        data_base.update_Machine(id_machine, nom, duree, puissance, id_operateur, f"ID_machine={id_machine}")

    def _save_etape(self):
        id_etape = int(self.inputs["ID"].text())
        nom_etape = self.inputs["Nom étape"].text().strip()
        numero_execution = int(self.inputs["Numéro exécution"].text())
        duree = int(self.inputs["Durée"].text())
        id_produit = int(self.inputs["ID produit"].text())
        id_machine = int(self.inputs["ID machine"].text())

        if nom_etape == "":
            raise ValueError("Le nom de l'étape ne peut pas être vide.")

        data_base.update_Etape(
            id_etape,
            nom_etape,
            numero_execution,
            duree,
            id_produit,
            id_machine,
            f"ID_etape={id_etape}",
        )

    def _save_operateur(self):
        id_operateur = int(self.inputs["ID"].text())
        nom = self.inputs["Nom"].text().strip()
        prenom = self.inputs["Prénom"].text().strip()
        email = self.inputs["Email"].text().strip()

        if nom == "" or prenom == "" or email == "":
            raise ValueError("Tous les champs opérateur sont obligatoires.")

        if "@" not in email or "." not in email:
            raise ValueError("Veuillez saisir une adresse email valide.")

        data_base.update_Operateur(id_operateur, nom, prenom, email, f"ID_operateur={id_operateur}")
