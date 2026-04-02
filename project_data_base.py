import Optimisation_prix_production as data_base
import price_kwh 
from datetime import datetime, timedelta 
from PySide6.QtCore import QLocale
from PySide6.QtWidgets import QApplication
import sys
import gestion_affichage as gestion
import matplotlib.pyplot as plt
filename = filename = f"graphique_prix_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"

if __name__ == "__main__":
    data_base.createAllTables()

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
    comp2 = str(comp2)
    comp22 = comp2.split(" ")[0]
    if  datetime.now().hour >= 12 and comp12 != comp22: #Si l'heure actuelle est supérieure ou égale à 12h, on considère que les prix du jour sont disponibles!!!!
        comp2 = comp2 + timedelta(days=1)

    #Comparer la dernière date de prix stockée avec la date actuelle
    print("Dernière date de prix stockée :", comp12)
    print("Date actuelle :", comp22)
    if comp12 != comp22:
        print("nouveaux prix disponibles") 
        data_prix = price_kwh.info_price()
        data_prix.plot()
        plt.title('Belgian price consumption')
        plt.xlabel('Date')
        plt.ylabel('Price (EUR/kWh)')
        plt.savefig(filename, dpi=300, bbox_inches='tight')# Enregistrer le graphique avec une résolution de 300 dpi et des marges ajustées
        plt.close()# Fermer la figure pour libérer de la mémoire
        for i in range(len(data_prix.keys())):
            data_base.insert_Prix(data_prix.keys()[i], data_prix.get(data_prix.keys()[i]))
        print("prix mis à jour dans la base de données") 

#Gestion de l'interface graphique
# Force le point au lieu de la virgule
    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedStates))
    app = QApplication(sys.argv)
    # Charger le thème industriel bleu
    with open("style_0.qss", "r") as f:
        app.setStyleSheet(f.read())
    window = gestion.MainWindow()
    #machines = data_base.select_Machine("Nom_machine='Four'")
    #machines = data_base.select_Machine("ID_machine=1959042371")
    machines = data_base.select_Machine("TRUE") # Récupérer toutes les machines de la base de données
    for a in machines:
        if a[1] != None:
            window.add_machine_to_combo(a[1])  # Assuming the machine name is the first column
        else:
            print("Aucune machine trouvée dans la base de données.")
    window.window.show()
    app.exec() 





