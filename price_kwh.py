from entsoe import EntsoePandasClient
import pandas as pd
from datetime import datetime, timedelta

def info_price():
    token = '18eedb45-a6bc-42a4-9836-7193f3b3c2d9'
    client = EntsoePandasClient(api_key =token)

    aujourd_hui = datetime.now()
    annee_aujourd_hui = aujourd_hui.year
    mois_aujourd_hui = aujourd_hui.month
    jour_aujourd_hui = aujourd_hui.day
    date_formatee_aujourd_hui = f"{annee_aujourd_hui:04d}{mois_aujourd_hui:02d}{jour_aujourd_hui:02d}" 
    demain = datetime.now() + timedelta(days=1)
    annee_demain = demain.year
    mois_demain = demain.month
    jour_demain = demain.day
    date_formatee_demain = f"{annee_demain:04d}{mois_demain:02d}{jour_demain:02d}"

    
    country_code ='BE'
    start_date = pd.Timestamp(date_formatee_aujourd_hui, tz='Europe/Brussels') #premier argument = date YYYYMMDD (inclue)
    end_date = pd.Timestamp(date_formatee_demain, tz='Europe/Brussels') #deuxieme argument = the time zone (exclue)

    #Requette recuperer prix sur Entsoe
    data_prix =client.query_day_ahead_prices(country_code, start=start_date, end=end_date)#EUR/KWh

    return data_prix