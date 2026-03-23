import Optimisation_prix_production as data_base
import price_kwh 
from datetime import datetime, timedelta 
from PySide6.QtWidgets import QApplication
import sys
import gestion_first_page as gestion
import json
import random

if __name__ == "__main__":
#Initialisation de la base de données et insertion des prix
    data_base.createAllTables()
   # data_base.delete_Prix("") #Supprimer les prix déjà stockés dans la base de données pour éviter les doublons

#Récupérer la dernière date de prix stockée dans la base de données
    data = data_base.select_Prix("Debut_date")
    if len(data) > 0:
        last_date = max(row[0] for row in data)
        comp1 = str(last_date)
        print("Dernière date de prix stockée 1:", comp1)
        comp12 = comp1.split(" ")[0]
    else:
        last_date = None
        comp12 = None

#Récupérer la date actuelle et la comparer avec la dernière date de prix stockée
    comp2 = datetime.now()
    if comp2.hour >= 12: #Si l'heure actuelle est supérieure ou égale à 12h, on considère que les prix du jour sont disponibles!!!!
        comp2 = comp2 + timedelta(days=1)
    comp2 = str(comp2)
    comp22 = comp2.split(" ")[0]

    #Comparer la dernière date de prix stockée avec la date actuelle
    print("Dernière date de prix stockée :", comp12)
    print("Date actuelle :", comp22)
    if comp12 != comp22:
        print("probleme") 
        data_prix = price_kwh.info_price()
        for i in range(len(data_prix.keys())):
            data_base.insert_Prix(data_prix.keys()[i], data_prix.get(data_prix.keys()[i]))
        print("aaaaaaaaaaaaaaaaaa") 

#Gestion de l'interface graphique
    app = QApplication(sys.argv)
    # Charger le thème industriel bleu
    with open("style_1.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = gestion.MainWindow()
    window.show()
    app.exec() # Lancement de la boucle d'événements de l'application (affiche la fenêtre et attend les interactions de l'utilisateur)
     
    # Lecture du JSON après fermeture de la fenêtre
    try:
        with open("donnees_formulaire.json", "r", encoding="utf-8") as f:
            resultat = json.load(f)
        data_base.insert_Produit(random.randint(1000000000, 9999999999), resultat["nom_produit"], resultat["description"])
        #data_base.insert_Etape(random.randint(1000000000, 9999999999),resultat["nom_etape"], resultat["numero_etape"], resultat["duree"])

    except FileNotFoundError:
        print("Aucun fichier JSON trouvé. Le bouton Valider n'a peut-être pas été cliqué.")




