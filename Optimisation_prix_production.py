# Module généré par GenDB.py
#===========================
import sqlite3
from PySide6.QtSql import QSqlDatabase, QSqlTableModel

def createAllTables():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# Produit
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Produit
			(
				ID_produit INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_produit TEXT UNIQUE NOT NULL,
				Description_produit TEXT
			)
			''')

	# Prix
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Prix
			(
				Debut_date DATETIME NOT NULL,
				Prix_kwh REAL NOT NULL,
				PRIMARY KEY (Debut_date)
			)
			''')

	# Commande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Commande
			(
				ID_commande INTEGER PRIMARY KEY AUTOINCREMENT
			)
			''')

	# Operateur
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Operateur
			(
				ID_operateur INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_operateur TEXT NOT NULL,
				Prenom_operateur TEXT NOT NULL,
				Email TEXT NOT NULL
			)
			''')

	# Machine
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Machine
			(
				ID_machine INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_machine TEXT NOT NULL,
				Duree INTEGER,
				Puissance_elec REAL NOT NULL,
				ID_operateur INTEGER,
				FOREIGN KEY (ID_operateur) REFERENCES Operateur(ID_operateur)
			)
			''')

	# LienProduitCommande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS LienProduitCommande
			(
				ID_produit INTEGER NOT NULL,
				ID_commande INTEGER NOT NULL,
				Date_depart DATETIME NOT NULL,
				Prix_produit REAL,
				Quantite INTEGER NOT NULL,
				PRIMARY KEY (ID_produit, ID_commande),
				FOREIGN KEY (ID_produit) REFERENCES Produit(ID_produit),
				FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande)
			)
			''')

	# Etape
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Etape
			(
				ID_etape INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_etape TEXT NOT NULL,
				Numero_excution INTEGER NOT NULL,
				Duree INTEGER NOT NULL,
				ID_produit INTEGER,
				ID_machine INTEGER,
				FOREIGN KEY (ID_produit) REFERENCES Produit(ID_produit),
				FOREIGN KEY (ID_machine) REFERENCES Machine(ID_machine)
			)
			''')
	conn.commit()
	conn.close()

def createTables_Produit():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# Produit
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Produit
			(
				ID_produit INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_produit TEXT UNIQUE NOT NULL,
				Description_produit TEXT
			)
			''')
	conn.commit()
	conn.close()

def createTables_Prix():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# Prix
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Prix
			(
				Debut_date DATETIME NOT NULL,
				Prix_kwh REAL NOT NULL,
				PRIMARY KEY (Debut_date)
			)
			''')
	conn.commit()
	conn.close()

def createTables_Commande():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# Commande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Commande
			(
				ID_commande INTEGER PRIMARY KEY AUTOINCREMENT
			)
			''')
	conn.commit()
	conn.close()

def createTables_Operateur():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# Operateur
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Operateur
			(
				ID_operateur INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_operateur TEXT NOT NULL,
				Prenom_operateur TEXT NOT NULL,
				Email TEXT NOT NULL
			)
			''')
	conn.commit()
	conn.close()

def createTables_Machine():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# Machine
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Machine
			(
				ID_machine INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_machine TEXT NOT NULL,
				Duree INTEGER,
				Puissance_elec REAL NOT NULL,
				ID_operateur INTEGER,
				FOREIGN KEY (ID_operateur) REFERENCES Operateur(ID_operateur)
			)
			''')
	conn.commit()
	conn.close()

def createTables_LienProduitCommande():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# LienProduitCommande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS LienProduitCommande
			(
				ID_produit INTEGER NOT NULL,
				ID_commande INTEGER NOT NULL,
				Date_depart DATETIME NOT NULL,
				Prix_produit REAL,
				Quantite INTEGER NOT NULL,
				PRIMARY KEY (ID_produit, ID_commande),
				FOREIGN KEY (ID_produit) REFERENCES Produit(ID_produit),
				FOREIGN KEY (ID_commande) REFERENCES Commande(ID_commande)
			)
			''')
	conn.commit()
	conn.close()

def createTables_Etape():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	# Etape
	cur.execute('''
			CREATE TABLE IF NOT EXISTS Etape
			(
				ID_etape INTEGER PRIMARY KEY AUTOINCREMENT,
				Nom_etape TEXT NOT NULL,
				Numero_excution INTEGER NOT NULL,
				Duree INTEGER NOT NULL,
				ID_produit INTEGER,
				ID_machine INTEGER,
				FOREIGN KEY (ID_produit) REFERENCES Produit(ID_produit),
				FOREIGN KEY (ID_machine) REFERENCES Machine(ID_machine)
			)
			''')
	conn.commit()
	conn.close()

# INSERT INTO Produit
def insert_Produit(Nom_produit,Description_produit):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Produit (Nom_produit,Description_produit) "
	sqlQuery+=f"VALUES ('{Nom_produit}','{Description_produit}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Prix
def insert_Prix(Debut_date,Prix_kwh):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Prix (Debut_date,Prix_kwh) "
	sqlQuery+=f"VALUES ('{Debut_date}',{Prix_kwh})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Commande
def insert_Commande():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Commande () "
	sqlQuery+=f"VALUES ()"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Operateur
def insert_Operateur(Nom_operateur,Prenom_operateur,Email):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Operateur (Nom_operateur,Prenom_operateur,Email) "
	sqlQuery+=f"VALUES ('{Nom_operateur}','{Prenom_operateur}','{Email}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Machine
def insert_Machine(Nom_machine,Duree,Puissance_elec,ID_operateur):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Machine (Nom_machine,Duree,Puissance_elec,ID_operateur) "
	sqlQuery+=f"VALUES ('{Nom_machine}',{Duree},{Puissance_elec},{ID_operateur})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO LienProduitCommande
def insert_LienProduitCommande(ID_produit,ID_commande,Date_depart,Prix_produit,Quantite):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO LienProduitCommande (ID_produit,ID_commande,Date_depart,Prix_produit,Quantite) "
	sqlQuery+=f"VALUES ({ID_produit},{ID_commande},'{Date_depart}',{Prix_produit},{Quantite})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO Etape
def insert_Etape(Nom_etape,Numero_excution,Duree,ID_produit,ID_machine):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO Etape (Nom_etape,Numero_excution,Duree,ID_produit,ID_machine) "
	sqlQuery+=f"VALUES ('{Nom_etape}',{Numero_excution},{Duree},{ID_produit},{ID_machine})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# SELECT fields FROM Produit WHERE condition
def select_Produit(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="SELECT ID_produit,Nom_produit,Description_produit FROM Produit"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Prix WHERE condition
def select_Prix(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="SELECT Debut_date,Prix_kwh FROM Prix"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Commande WHERE condition
def select_Commande(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="SELECT ID_commande FROM Commande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Operateur WHERE condition
def select_Operateur(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="SELECT ID_operateur,Nom_operateur,Prenom_operateur,Email FROM Operateur"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Machine WHERE condition
def select_Machine(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="SELECT ID_machine,Nom_machine,Duree,Puissance_elec,ID_operateur FROM Machine"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM LienProduitCommande WHERE condition
def select_LienProduitCommande(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="SELECT ID_produit,ID_commande,Date_depart,Prix_produit,Quantite FROM LienProduitCommande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM Etape WHERE condition
def select_Etape(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="SELECT ID_etape,Nom_etape,Numero_excution,Duree,ID_produit,ID_machine FROM Etape"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# UPDATE Produit SET fields=value WHERE condition
def update_Produit(ID_produit,Nom_produit,Description_produit,WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Produit SET ID_produit = {ID_produit},Nom_produit='{Nom_produit}',Description_produit='{Description_produit}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Prix SET fields=value WHERE condition
def update_Prix(Debut_date,Prix_kwh,WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Prix SET Debut_date='{Debut_date}',Prix_kwh = {Prix_kwh}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Commande SET fields=value WHERE condition
def update_Commande(ID_commande,WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Commande SET ID_commande = {ID_commande}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Operateur SET fields=value WHERE condition
def update_Operateur(ID_operateur,Nom_operateur,Prenom_operateur,Email,WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Operateur SET ID_operateur = {ID_operateur},Nom_operateur='{Nom_operateur}',Prenom_operateur='{Prenom_operateur}',Email='{Email}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Machine SET fields=value WHERE condition
def update_Machine(ID_machine,Nom_machine,Duree,Puissance_elec,ID_operateur,WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Machine SET ID_machine = {ID_machine},Nom_machine='{Nom_machine}',Duree = {Duree},Puissance_elec = {Puissance_elec},ID_operateur = {ID_operateur}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE LienProduitCommande SET fields=value WHERE condition
def update_LienProduitCommande(ID_produit,ID_commande,Date_depart,Prix_produit,Quantite,WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE LienProduitCommande SET ID_produit = {ID_produit},ID_commande = {ID_commande},Date_depart='{Date_depart}',Prix_produit = {Prix_produit},Quantite = {Quantite}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE Etape SET fields=value WHERE condition
def update_Etape(ID_etape,Nom_etape,Numero_excution,Duree,ID_produit,ID_machine,WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE Etape SET ID_etape = {ID_etape},Nom_etape='{Nom_etape}',Numero_excution = {Numero_excution},Duree = {Duree},ID_produit = {ID_produit},ID_machine = {ID_machine}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Produit WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_Produit(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Produit"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Prix WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_Prix(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Prix"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Commande WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_Commande(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Commande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Operateur WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_Operateur(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Operateur"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Machine WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_Machine(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Machine"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM LienProduitCommande WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_LienProduitCommande(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM LienProduitCommande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM Etape WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_Etape(WHERE):
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM Etape"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Produit
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_Produit():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Produit"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Prix
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_Prix():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Prix"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Commande
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_Commande():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Commande"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Operateur
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_Operateur():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Operateur"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Machine
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_Machine():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Machine"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE LienProduitCommande
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_LienProduitCommande():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE LienProduitCommande"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE Etape
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_Etape():
	conn = sqlite3.connect("Optimisation_prix_production.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE Etape"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

