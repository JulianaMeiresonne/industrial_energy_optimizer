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
    QTimeEdit,
)
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTime
from PySide6.QtGui import QPixmap
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import sys
import Optimisation_prix_production as data_base


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
        self.liste_produit_id_order = []
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

        # Création des tables si besoin
        try:
            data_base.createAllTables()
        except Exception as e:
            print(f"Attention : impossible d'initialiser les tables : {e}")

        # ==========================================================
        # CONFIGURATION INITIALE
        # ==========================================================
        self.setup_orders_table()
        self.setup_products_table()
        self.setup_database_table()

        self.display_current_date()
        self.load_price_graph_image("graphique_prix_2026-04-02_13-04-30.png")

        self.inputStartHour.setTime(QTime.currentTime())
        self.inputStepMachine.clear()
        self.InputProductOrder.clear()

        self.load_products_in_order_combo()
        self.load_machines_in_step_combo()
        self.refresh_database_table()

        # ==========================================================
        # CONNEXIONS
        # ==========================================================
        self.btnAddOrderLine.clicked.connect(self.add_order_line)
        self.btnRemoveOrderLine.clicked.connect(self.remove_order_line)
        self.btnValidateOrder.clicked.connect(self.validate_order)
        self.BtnOptimize.clicked.connect(self.optimize_start_hour)

        self.btnAddStep.clicked.connect(self.add_step_to_table)
        self.btnCreateMachine.clicked.connect(self.open_machine_creation)
        self.btnCancel.clicked.connect(self.clear_product_form)
        self.btnValidate.clicked.connect(self.add_produit_data_base)

        self.btnRefreshDatabase.clicked.connect(self.refresh_database_table)
        self.btnAddDatabaseRow.clicked.connect(self.add_database_row)
        self.btnEditDatabaseRow.clicked.connect(self.edit_database_row)
        self.btnDeleteDatabaseRow.clicked.connect(self.delete_database_row)
        self.inputDatabaseTable.currentIndexChanged.connect(self.refresh_database_table)

    # ==========================================================
    # HELPERS GÉNÉRAUX
    # ==========================================================

    def escape_sql(self, value):
        return str(value).replace("'", "''")

    def get_table_item_text(self, table, row, col, default=""):
        item = table.item(row, col)
        return item.text().strip() if item else default

    # ==========================================================
    # HELPERS BDD
    # ==========================================================

    def get_steps_for_product(self, product_id):
        rows = data_base.select_Etape(f"ID_produit={product_id}")
        rows.sort(key=lambda x: int(x[2]))
        return rows

    def get_machine_by_id(self, machine_id):
        rows = data_base.select_Machine(f"ID_machine={machine_id}")
        return rows[0] if rows else None

    def get_operator_by_id(self, operator_id):
        rows = data_base.select_Operateur(f"ID_operateur={operator_id}")
        return rows[0] if rows else None

    def get_product_by_id(self, product_id):
        rows = data_base.select_Produit(f"ID_produit={product_id}")
        return rows[0] if rows else None

    def get_product_by_name(self, product_name):
        product_name = self.escape_sql(product_name)
        rows = data_base.select_Produit(f"Nom_produit='{product_name}'")
        return rows[0] if rows else None

    def get_machine_by_name(self, machine_name):
        machine_name = self.escape_sql(machine_name)
        rows = data_base.select_Machine(f"Nom_machine='{machine_name}'")
        return rows[0] if rows else None

    def get_product_name_by_id(self, product_id):
        product = self.get_product_by_id(product_id)
        return product[1] if product and len(product) > 1 else f"Produit #{product_id}"

    def get_machine_name_by_id(self, machine_id):
        machine = self.get_machine_by_id(machine_id)
        return machine[1] if machine and len(machine) > 1 else f"Machine #{machine_id}"

    def get_operator_name_by_id(self, operator_id):
        operator = self.get_operator_by_id(operator_id)
        if operator and len(operator) >= 3:
            return f"{operator[2]} {operator[1]}"
        return f"Opérateur #{operator_id}"

    # ==========================================================
    # CALCULS : PRIX, HEURE DE FIN, ALERTES, E-MAILS
    # ==========================================================

    def save_order_to_database(self):
        if self.tableOrders.rowCount() == 0:
            return None

        data_base.insert_Commande()
        rows = data_base.select_Commande("TRUE")

        if not rows:
            raise Exception("Aucune commande trouvée après insertion.")

        id_commande = max(row[0] for row in rows)

        for row in range(self.tableOrders.rowCount()):
            product_name = self.get_table_item_text(self.tableOrders, row, 0)
            quantity_text = self.get_table_item_text(self.tableOrders, row, 1)
            price_text = self.get_table_item_text(self.tableOrders, row, 2)
            start_text = self.get_table_item_text(self.tableOrders, row, 3)

            if not product_name or not quantity_text or not start_text:
                continue

            try:
                quantity = int(quantity_text)
            except ValueError:
                continue

            try:
                prix_produit = float(price_text.replace("€", "").replace(",", ".").strip())
            except ValueError:
                prix_produit = 0.0

            product = self.get_product_by_name(product_name)
            if not product:
                continue

            id_produit = product[0]

            date_depart = datetime.combine(
                datetime.now().date(),
                datetime.strptime(start_text, "%H:%M").time()
            ).strftime("%Y-%m-%d %H:%M:%S")

            data_base.insert_LienProduitCommande(
                id_produit,
                id_commande,
                date_depart,
                prix_produit,
                quantity
            )

        return id_commande

    def get_today_price_for_time(self, start_hour):
        rows = data_base.select_Prix("TRUE")
        if not rows:
            return 0.0

        aujourd_hui = datetime.now().date()
        heure_cible, minute_cible = map(int, start_hour.split(":"))

        exact_match = None
        same_hour_match = None
        nearest_before = None

        for row in rows:
            try:
                db_dt_raw = row[0]
                db_price_raw = row[1]

                db_dt = datetime.fromisoformat(str(db_dt_raw).replace(" ", "T"))
                db_price = float(str(db_price_raw).replace(",", "."))

                if db_dt.date() != aujourd_hui:
                    continue

                if db_dt.hour == heure_cible and db_dt.minute == minute_cible:
                    exact_match = db_price
                    break

                if db_dt.hour == heure_cible and same_hour_match is None:
                    same_hour_match = db_price

                if (db_dt.hour < heure_cible) or (db_dt.hour == heure_cible and db_dt.minute <= minute_cible):
                    if nearest_before is None or db_dt > nearest_before[0]:
                        nearest_before = (db_dt, db_price)

            except Exception as e:
                print(f"Erreur lecture prix {row} : {e}")
                continue

        if exact_match is not None:
            return exact_match
        if same_hour_match is not None:
            return same_hour_match
        if nearest_before is not None:
            return nearest_before[1]

        return 0.0

    def compute_product_cost_and_end(self, product_id, start_dt, quantity):
        steps = self.get_steps_for_product(product_id)
        product_name = self.get_product_name_by_id(product_id)

        if not steps:
            return 0.0, start_dt, [f"Aucune étape trouvée pour le produit '{product_name}'."], [], []

        price_kwh = self.get_today_price_for_time(start_dt.strftime("%H:%M"))

        total_duration_minutes = 0.0
        total_energy_kwh = 0.0
        timing_alerts = []
        price_alerts = []
        email_lines = []

        current_dt = start_dt

        for _ in range(quantity):
            for step in steps:
                _, step_name, _, step_duration, _, machine_id = step

                machine = self.get_machine_by_id(machine_id)
                if not machine:
                    timing_alerts.append(
                        f"Machine introuvable pour l'étape '{step_name}' du produit '{product_name}'."
                    )
                    continue

                _, machine_name, machine_duration, machine_power_kw, operator_id = machine

                machine_duration = float(str(machine_duration).replace(",", "."))
                step_duration = float(str(step_duration).replace(",", "."))
                machine_power_kw = float(str(machine_power_kw).replace(",", "."))

                if machine_duration != 1 and step_duration == 1:
                    real_duration_minutes = machine_duration
                elif step_duration != 1 and machine_duration == 1:
                    real_duration_minutes = step_duration
                elif machine_duration != 1 and step_duration != 1:
                    real_duration_minutes = step_duration * machine_duration
                else:
                    real_duration_minutes = 1.0

                total_duration_minutes += real_duration_minutes

                duration_hours = real_duration_minutes / 60.0
                step_energy_kwh = machine_power_kw * duration_hours
                total_energy_kwh += step_energy_kwh

                step_start = current_dt
                step_end = step_start + timedelta(minutes=real_duration_minutes)

                operator = self.get_operator_by_id(operator_id)
                if operator:
                    _, nom_operateur, prenom_operateur, email_operateur = operator
                    email_lines.append({
                        "email": email_operateur,
                        "operator_name": f"{prenom_operateur} {nom_operateur}",
                        "product_name": product_name,
                        "machine_name": machine_name,
                        "step_name": step_name,
                        "start": step_start.strftime("%H:%M"),
                        "end": step_end.strftime("%H:%M")
                    })

                current_dt = step_end

        end_dt = start_dt + timedelta(minutes=total_duration_minutes)
        total_cost = total_energy_kwh * price_kwh

        if end_dt.date() != start_dt.date():
            timing_alerts.append(
                f"Le produit '{product_name}' finit après minuit : {end_dt.strftime('%d/%m/%Y %H:%M')}"
            )

        if price_kwh < 0:
            price_alerts.append(
                f"Prix négatif détecté aujourd'hui à {start_dt.strftime('%H:%M')} : {price_kwh:.4f} €/kWh"
            )

        return total_cost, end_dt, timing_alerts, price_alerts, email_lines

    def check_price_alerts(self, seuil_prix):
        alerts = []
        rows = data_base.select_Prix("TRUE")

        if not rows:
            return alerts

        aujourd_hui = datetime.now().date()

        for row in rows:
            try:
                db_dt = datetime.fromisoformat(str(row[0]).replace(" ", "T"))
                db_price = float(str(row[1]).replace(",", "."))

                if db_dt.date() == aujourd_hui and db_price < seuil_prix:
                    alerts.append(f"{db_dt.strftime('%H:%M')} : {db_price:.4f} €/kWh")

            except Exception:
                continue

        return alerts

    def send_order_emails(self, email_lines):
        """
        Écrit les e-mails des opérateurs dans un fichier texte
        au lieu de les envoyer par SMTP.
        """
        if not email_lines:
            QMessageBox.warning(
                self.window,
                "Planning",
                "Aucun planning disponible pour générer les e-mails."
            )
            return

        heure_str = datetime.now().strftime("%H:%M le %d/%m/%Y")
        fichier_mail = f"Email_Planification_{datetime.now().strftime('%Y%m%d-%Hh%M')}.txt"

        emails_ecrits = 0
        emails_erreurs = 0

        grouped_by_email = {}

        for line in email_lines:
            recipient = line.get("email", "").strip()
            if recipient:
                grouped_by_email.setdefault(recipient, []).append(line)

        if not grouped_by_email:
            QMessageBox.warning(
                self.window,
                "Planning",
                "Aucune adresse e-mail valide trouvée pour les opérateurs."
            )
            return

        try:
            with open(fichier_mail, "w", encoding="utf-8") as f:
                for email_operateur, lines in grouped_by_email.items():
                    operator_name = lines[0].get("operator_name", "Opérateur")

                    f.write(f"À        : {email_operateur}\n")
                    f.write("Sujet    : Planning validé de production\n")
                    f.write("-" * 100 + "\n")
                    f.write(f"Bonjour {operator_name},\n\n")
                    f.write("Voici votre planning de production.\n")
                    f.write(f"Heure de génération : {heure_str}.\n\n")

                    for line in lines:
                        f.write(f"Produit      : {line.get('product_name', 'Produit inconnu')}\n")
                        f.write(f"Machine      : {line.get('machine_name', 'Machine inconnue')}\n")
                        f.write(f"Tâche        : {line.get('step_name', 'Étape inconnue')}\n")
                        f.write(f"Heure début  : {line.get('start', '--:--')}\n")
                        f.write(f"Heure fin    : {line.get('end', '--:--')}\n")
                        f.write("\n")

                    f.write("Merci de préparer votre poste et de suivre ce planning.\n\n")
                    f.write("Cordialement,\n")
                    f.write("Application de gestion de production\n")
                    f.write("-" * 100 + "\n\n")

                    emails_ecrits += 1
                    print(f"E-mail écrit pour {operator_name} ({email_operateur})")

            QMessageBox.information(
                self.window,
                "Fichier généré",
                f"{emails_ecrits} e-mail(s) écrit(s) dans le fichier :\n{fichier_mail}"
            )

        except Exception as e:
            emails_erreurs += 1
            QMessageBox.critical(
                self.window,
                "Erreur",
                f"Erreur lors de l'écriture du fichier mail :\n{e}"
            )

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
        self.liste_produit_id_order = []

        try:
            produits = data_base.select_Produit("1=1")
            for produit in produits:
                self.InputProductOrder.addItem(str(produit[1]))
                self.liste_produit_id_order.append(produit[0])

            if not produits:
                self.InputProductOrder.addItem("Créez un produit dans l'onglet Produits")

        except Exception as e:
            print(f"Erreur chargement produits : {e}")
            self.InputProductOrder.addItem("Créez un produit dans l'onglet Produits")

    def load_machines_in_step_combo(self):
        self.inputStepMachine.clear()
        try:
            machines = data_base.select_Machine("1=1")
            for machine in machines:
                self.inputStepMachine.addItem(str(machine[1]))
        except Exception as e:
            print(f"Erreur chargement machines : {e}")

    def optimize_start_hour(self):
        self.inputStartHour.setTime(QTime(8, 0))
        QMessageBox.information(
            self.window,
            "Optimisation",
            "Heure de début optimisée à 08:00."
        )

    def add_order_line(self):
        product_name = self.InputProductOrder.currentText().strip()
        quantity = self.inputOrderQuantity.value()
        start_time = self.inputStartHour.time()

        if product_name == "" or product_name == "Créez un produit dans l'onglet Produits":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez sélectionner un produit.")
            return

        if quantity <= 0:
            QMessageBox.warning(self.window, "Valeur invalide", "La quantité doit être supérieure à 0.")
            return

        product = self.get_product_by_name(product_name)
        if not product:
            QMessageBox.warning(self.window, "Produit introuvable", f"Le produit '{product_name}' est introuvable.")
            return

        product_id = product[0]

        start_dt = datetime.combine(
            datetime.now().date(),
            datetime.strptime(start_time.toString("HH:mm"), "%H:%M").time()
        )

        estimated_price, end_dt, timing_messages, price_messages, _ = self.compute_product_cost_and_end(
            product_id, start_dt, quantity
        )

        row = self.tableOrders.rowCount()
        self.tableOrders.insertRow(row)

        self.tableOrders.setItem(row, 0, QTableWidgetItem(product_name))
        self.tableOrders.setItem(row, 1, QTableWidgetItem(str(quantity)))
        self.tableOrders.setItem(row, 2, QTableWidgetItem(f"{estimated_price:.2f} €"))
        self.tableOrders.setItem(row, 3, QTableWidgetItem(start_dt.strftime("%H:%M")))
        self.tableOrders.setItem(row, 4, QTableWidgetItem(end_dt.strftime("%H:%M")))

        if timing_messages:
            QMessageBox.warning(self.window, "Alerte de timing", "\n".join(timing_messages))

        if price_messages:
            QMessageBox.warning(self.window, "Alerte de prix", "\n".join(price_messages))

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
        all_timing_alerts = []
        all_price_alerts = []
        all_email_lines = []

        for row in range(self.tableOrders.rowCount()):
            product_name = self.get_table_item_text(self.tableOrders, row, 0)
            quantity_text = self.get_table_item_text(self.tableOrders, row, 1)
            start_text = self.get_table_item_text(self.tableOrders, row, 3)

            if not product_name or not quantity_text or not start_text:
                continue

            try:
                quantity = int(quantity_text)
            except ValueError:
                all_timing_alerts.append(f"Quantité invalide pour '{product_name}'")
                continue

            product = self.get_product_by_name(product_name)
            if not product:
                all_timing_alerts.append(f"Produit introuvable : '{product_name}'")
                continue

            product_id = product[0]

            start_dt = datetime.combine(
                datetime.now().date(),
                datetime.strptime(start_text, "%H:%M").time()
            )

            product_cost, end_dt, timing_alerts, price_alerts, email_lines = self.compute_product_cost_and_end(
                product_id, start_dt, quantity
            )

            total_price += product_cost
            all_timing_alerts.extend(timing_alerts)
            all_price_alerts.extend(price_alerts)
            all_email_lines.extend(email_lines)

            self.tableOrders.setItem(row, 2, QTableWidgetItem(f"{product_cost:.2f} €"))
            self.tableOrders.setItem(row, 4, QTableWidgetItem(end_dt.strftime("%H:%M")))

        seuil_prix = 0.0
        global_price_alerts = self.check_price_alerts(seuil_prix)

        if global_price_alerts:
            all_price_alerts.append(f"Prix inférieurs à {seuil_prix:.2f} €/kWh aujourd'hui :")
            all_price_alerts.extend(global_price_alerts)

        try:
            self.send_order_emails(all_email_lines)
        except Exception as e:
            all_price_alerts.append(f"Erreur d'envoi e-mail : {e}")

        try:
            id_commande = self.save_order_to_database()
        except Exception as e:
            QMessageBox.critical(
                self.window,
                "Erreur base de données",
                f"Impossible d'enregistrer la commande :\n{e}"
            )
            return

        message = (
            f"Commande enregistrée avec succès.\n"
            f"N° commande : {id_commande}\n"
            f"Prix total estimé : {total_price:.2f} €"
        )

        if all_timing_alerts:
            message += "\n\nAlertes de timing :\n" + "\n".join(all_timing_alerts)

        if all_price_alerts:
            message += "\n\nAlertes de prix :\n" + "\n".join(all_price_alerts)

        QMessageBox.information(self.window, "Commande validée", message)

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
        self.step_liste = []

    def add_step_to_table(self):
        step_number = self.inputStepNumber.value()
        step_name = self.inputStepName.text().strip()
        machine = self.inputStepMachine.currentText().strip()
        duration = self.inputStepDuration.value()

        if step_name == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir un nom d'étape.")
            return

        if machine == "":
            QMessageBox.warning(
                self.window,
                "Machine manquante",
                "Veuillez sélectionner une machine ou en créer une nouvelle."
            )
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

        self.step_liste.append((step_name, step_number, duration, machine))

    def add_produit_data_base(self):
        name_produit = self.inputProductName.text().strip()

        if name_produit == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir un nom de produit.")
            return

        if not self.step_liste:
            QMessageBox.warning(self.window, "Aucune étape", "Veuillez ajouter au moins une étape.")
            return

        try:
            data_base.insert_Produit(name_produit, self.inputDescription.toPlainText().strip())
        except Exception as e:
            QMessageBox.critical(self.window, "Erreur", f"Impossible d'insérer le produit :\n{e}")
            return

        result_produit = self.get_product_by_name(name_produit)

        if not result_produit:
            QMessageBox.critical(self.window, "Erreur", "Impossible de retrouver le produit après insertion.")
            return

        id_produit = result_produit[0]

        for step in self.step_liste:
            machine = self.get_machine_by_name(step[3])
            if not machine:
                QMessageBox.critical(self.window, "Erreur", f"Machine introuvable : {step[3]}")
                return

            id_machine = machine[0]
            try:
                data_base.insert_Etape(step[0], step[1], step[2], id_produit, id_machine)
            except Exception as e:
                QMessageBox.critical(self.window, "Erreur", f"Impossible d'insérer l'étape '{step[0]}' :\n{e}")
                return

        QMessageBox.information(self.window, "Succès", f"Le produit '{name_produit}' a bien été enregistré.")
        self.clear_product_form()
        self.load_products_in_order_combo()
        self.refresh_database_table()

    def add_machine_to_combo(self, machine_name):
        machine_name = machine_name.strip()
        if machine_name == "":
            return

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
        self.tableDatabase.setColumnCount(3)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Nom", "Description"])

        rows = data_base.select_Produit("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:3]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_machines_in_database_table(self):
        self.tableDatabase.setColumnCount(5)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Nom", "Durée", "Puissance", "ID opérateur"])

        rows = data_base.select_Machine("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:5]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_steps_in_database_table(self):
        self.tableDatabase.setColumnCount(6)
        self.tableDatabase.setHorizontalHeaderLabels([
            "ID", "Nom Étape", "N° Exécution", "Durée", "ID produit", "ID machine"
        ])

        rows = data_base.select_Etape("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:6]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def load_operators_in_database_table(self):
        self.tableDatabase.setColumnCount(4)
        self.tableDatabase.setHorizontalHeaderLabels(["ID", "Nom", "Prénom", "Email"])

        rows = data_base.select_Operateur("TRUE")
        for row_data in rows:
            row = self.tableDatabase.rowCount()
            self.tableDatabase.insertRow(row)

            for col, value in enumerate(row_data[:4]):
                self.tableDatabase.setItem(row, col, QTableWidgetItem(str(value)))

    def add_database_row(self):
        self.tabWidget = self.window.findChild(QTabWidget, "tabWidget")
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == "Produits":
                self.tabWidget.setCurrentIndex(i)
                break

    def edit_database_row(self):
        current_row = self.tableDatabase.currentRow()
        if current_row < 0:
            QMessageBox.warning(
                self.window,
                "Aucune ligne sélectionnée",
                "Veuillez sélectionner une ligne."
            )
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
            parent=self.window
        )

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

        try:
            if table_name == "Produits":
                data_base.delete_Produit(f"ID_produit={self.tableDatabase.item(current_row, 0).text()}")
            elif table_name == "Machines":
                data_base.delete_Machine(f"ID_machine={self.tableDatabase.item(current_row, 0).text()}")
            elif table_name == "Étapes":
                data_base.delete_Etape(f"ID_etape={self.tableDatabase.item(current_row, 0).text()}")
            elif table_name == "Opérateurs":
                data_base.delete_Operateur(f"ID_operateur={self.tableDatabase.item(current_row, 0).text()}")
        except Exception as e:
            QMessageBox.critical(self.window, "Erreur", f"Suppression impossible :\n{e}")
            return

        self.tableDatabase.removeRow(current_row)
        QMessageBox.information(self.window, "Suppression", "La ligne a été supprimée du tableau.")

    def close(self):
        self.window.close()


class MachineWindow:
    def __init__(self, on_machine_added=None):
        self.on_machine_added = on_machine_added

        loader = QUiLoader()
        ui_file = QFile("add_machine.ui")

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

        self.btnSaveMachine.clicked.connect(self.save_machine)
        self.btnCancelMachine.clicked.connect(self.close_window)

    def close_window(self):
        self.window.close()

    def get_machine_data(self):
        return {
            "name": self.inputMachineName.text().strip(),
            "cycle_duration": self.inputCycleDuration.value(),
            "electric_power": self.inputElectricPower.value(),
            "operator_last_name": self.inputOperatorLastName.text().strip(),
            "operator_first_name": self.inputOperatorFirstName.text().strip(),
            "operator_email": self.inputOperatorEmail.text().strip(),
            "notes": self.inputMachineNotes.toPlainText().strip() if self.inputMachineNotes else "",
        }

    def validate_fields(self, data):
        if data["name"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir le nom de la machine.")
            return False

        if data["cycle_duration"] <= 0:
            QMessageBox.warning(self.window, "Valeur invalide", "Veuillez saisir une durée de cycle supérieure à 0.")
            return False

        if data["electric_power"] <= 0:
            QMessageBox.warning(self.window, "Valeur invalide", "Veuillez saisir une puissance électrique supérieure à 0.")
            return False

        if data["operator_last_name"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir le nom de l'opérateur.")
            return False

        if data["operator_first_name"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir le prénom de l'opérateur.")
            return False

        if data["operator_email"] == "":
            QMessageBox.warning(self.window, "Champ manquant", "Veuillez saisir l'e-mail de l'opérateur.")
            return False

        if "@" not in data["operator_email"] or "." not in data["operator_email"]:
            QMessageBox.warning(self.window, "E-mail invalide", "Veuillez saisir une adresse e-mail valide.")
            return False

        return True

    def save_machine(self):
        data = self.get_machine_data()

        if not self.validate_fields(data):
            return

        cycle_duration = int(data["cycle_duration"])
        electric_power = float(data["electric_power"])

        try:
            data_base.insert_Operateur(
                data["operator_last_name"],
                data["operator_first_name"],
                data["operator_email"]
            )

            nom = str(data["operator_last_name"]).replace("'", "''")
            prenom = str(data["operator_first_name"]).replace("'", "''")
            email = str(data["operator_email"]).replace("'", "''")

            result_operateur = data_base.select_Operateur(
                f"Nom_operateur='{nom}' "
                f"AND Prenom_operateur='{prenom}' "
                f"AND Email='{email}'"
            )

            if not result_operateur:
                raise Exception("Opérateur introuvable après insertion.")

            id_operateur = result_operateur[0][0]

            data_base.insert_Machine(data["name"], cycle_duration, electric_power, id_operateur)

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
                f"Erreur lors de l'enregistrement de la machine :\n{e}"
            )


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

        if nom == "":
            raise ValueError("Le nom de la machine ne peut pas être vide.")

        try:
            duree = int(self.inputs["Durée"].text().strip())
        except ValueError:
            raise ValueError("La durée doit être un entier.")

        try:
            puissance = float(self.inputs["Puissance"].text().replace(",", ".").strip())
        except ValueError:
            raise ValueError("La puissance doit être un nombre valide.")

        try:
            id_operateur = int(self.inputs["ID opérateur"].text().strip())
        except ValueError:
            raise ValueError("Le champ 'ID opérateur' doit contenir un identifiant numérique.")

        data_base.update_Machine(id_machine, nom, duree, puissance, id_operateur, f"ID_machine={id_machine}")

    def _save_etape(self):
        id_etape = int(self.inputs["ID"].text())
        nom_etape = self.inputs["Nom étape"].text().strip()

        if nom_etape == "":
            raise ValueError("Le nom de l'étape ne peut pas être vide.")

        try:
            numero_execution = int(self.inputs["Numéro exécution"].text().strip())
        except ValueError:
            raise ValueError("Le numéro d'exécution doit être un entier.")

        try:
            duree = int(self.inputs["Durée"].text().strip())
        except ValueError:
            raise ValueError("La durée doit être un entier.")

        try:
            id_produit = int(self.inputs["ID produit"].text().strip())
        except ValueError:
            raise ValueError("Le champ 'ID produit' doit contenir un identifiant numérique.")

        try:
            id_machine = int(self.inputs["ID machine"].text().strip())
        except ValueError:
            raise ValueError("Le champ 'ID machine' doit contenir un identifiant numérique.")

        data_base.update_Etape(
            id_etape,
            nom_etape,
            numero_execution,
            duree,
            id_produit,
            id_machine,
            f"ID_etape={id_etape}"
        )

    def _save_operateur(self):
        id_operateur = int(self.inputs["ID"].text())
        nom = self.inputs["Nom"].text().strip()
        prenom = self.inputs["Prénom"].text().strip()
        email = self.inputs["Email"].text().strip()

        if nom == "" or prenom == "" or email == "":
            raise ValueError("Tous les champs opérateur sont obligatoires.")

        if "@" not in email or "." not in email:
            raise ValueError("Veuillez saisir une adresse e-mail valide.")

        data_base.update_Operateur(id_operateur, nom, prenom, email, f"ID_operateur={id_operateur}")