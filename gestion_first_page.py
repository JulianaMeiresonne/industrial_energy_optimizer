from PySide6.QtWidgets import QLineEdit, QTextEdit, QSpinBox, QPushButton # Import des classes nécessaires depuis PySide6 (interface graphique)
from PySide6.QtUiTools import QUiLoader # Permet de charger un fichier .ui (créé avec Qt Designer)
from PySide6.QtCore import QFile # Permet de manipuler des fichiers (ici pour ouvrir le .ui)
import sys # Module système (utile pour gérer l'application, arguments, exit…)
import json


class MainWindow:
    def __init__(self):
        loader = QUiLoader() # Création d'un chargeur pour lire le fichier .ui
        ui_file = QFile("first_page_1.ui") # Ouverture du fichier .ui (interface graphique)

        if not ui_file.open(QFile.ReadOnly):
            print("Impossible d'ouvrir le fichier .ui")
            sys.exit(1) # Si le fichier ne s'ouvre pas, afficher un message d'erreur et quitter l'application

        self.window = loader.load(ui_file) # Chargement du contenu du fichier .ui dans self.window
        ui_file.close()

        if self.window is None:
            print("Le chargement du fichier .ui a échoué")
            sys.exit(1) # Si le chargement échoue, afficher un message d'erreur et quitter l'application

        # === Récupération des widgets ===
        self.lineEdit = self.window.findChild(QLineEdit, "lineEdit")
        self.textEdit = self.window.findChild(QTextEdit, "textEdit")
        self.lineEdit_2 = self.window.findChild(QLineEdit, "lineEdit_2")
        self.spinBox = self.window.findChild(QSpinBox, "spinBox")
        self.spinBox_2 = self.window.findChild(QSpinBox, "spinBox_2")
        self.valider = self.window.findChild(QPushButton, "pushButton_2")

        if self.valider is None:
            print("Bouton pushButton_2 introuvable")
            sys.exit(1)

        self.valider.clicked.connect(self.on_valider_clicked)

    def on_valider_clicked(self):
        print("Valider cliqué !")

        # Dictionnaire Python
        donnees = {
            "nom_produit": self.lineEdit.text(),
            "description": self.textEdit.toPlainText(),
            "nom_etape": self.lineEdit_2.text(),
            "numero_etape": self.spinBox.value(),
            "duree": self.spinBox_2.value()
        }

        # Écriture dans un fichier JSON
        with open("donnees_formulaire.json", "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=4)

        print("Données enregistrées dans donnees_formulaire.json")

    def show(self):
        self.window.show()
