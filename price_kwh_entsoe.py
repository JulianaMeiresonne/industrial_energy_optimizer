from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#Initialisation du client 
token = '18eedb45-a6bc-42a4-9836-7193f3b3c2d9'
client = EntsoePandasClient(api_key =token)

# Récupère la date actuelle
aujourd_hui = datetime.now()
annee_aujourd_hui = aujourd_hui.year
mois_aujourd_hui = aujourd_hui.month
jour_aujourd_hui = aujourd_hui.day
date_formatee_aujourd_hui = f"{annee_aujourd_hui:04d}{mois_aujourd_hui:02d}{jour_aujourd_hui:02d}"
# Récupère la date de demain 
demain = datetime.now() + timedelta(days=1)
annee_demain = demain.year
mois_demain = demain.month
jour_demain = demain.day
date_formatee_demain = f"{annee_demain:04d}{mois_demain:02d}{jour_demain:02d}"

#Definir les paramètre pour la query
country_code ='BE'
start_date = pd.Timestamp(date_formatee_aujourd_hui, tz='Europe/Brussels') #premier argument = date YYYYMMDD (inclue)
end_date = pd.Timestamp(date_formatee_demain, tz='Europe/Brussels') #deuxieme argument = the time zone (exclue)

#Requette recuperer prix sur Entsoe
data1 =client.query_day_ahead_prices(country_code, start=start_date, end=end_date)#EUR/KWh
print(data1)
    

''' 
comparateur1 = str(data1.keys()[-1])
comparateur12 = comparateur1.split(" ")[0]
comparateur2 = aujourd_hui
print(comparateur1)
print(aujourd_hui)
#print(data1.get(data1.keys()[0]))
if aujourd_hui == data1.keys()[-1]:
    print("aaaaaaaaaaaaaaaaaa")


plt.close('all')
data1.plot()
plt.legend(loc='best')
plt.title('Belgian price consumption')
plt.show()
'''

