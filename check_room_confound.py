import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
co2 = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')

ROOM_ID = {11:1,12:1,13:1,14:1,15:1,16:1, 20:2,21:2,22:2,23:2,24:2,25:2, 55:3,
           17:4,18:4,19:4, 29:5,30:5,31:5, 26:6,27:6, 32:7,33:7,34:7,
           35:8,36:8,37:8, 38:9, 41:10,42:10,43:10,44:10,45:10,46:10,
           50:11,51:11, 90:12}
ROOM_LABEL = {1:'Chambre',2:'Séjour/Salon',3:'Studio',4:'Cuisine',5:'SdB',
              6:'Buanderie',7:'WC',8:'Bureau',9:'Chaufferie',10:'Cave',11:'Garage',12:'Ext'}

print('=== Piece du capteur CO2 par logement ===')
room = co2.groupby('CODELIEU')['IDN_PIECE'].first().map(ROOM_ID).map(ROOM_LABEL)
print(room.value_counts(dropna=False).to_string())

# ===== day-types (reproduit) =====
co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour
pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']
prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()

lab = KMeans(n_clusters=4, n_init=30, random_state=42).fit_predict(prof.values)
dt = pd.DataFrame({'daytype': lab}, index=prof.index).reset_index()
dt['room'] = dt['CODELIEU'].map(room)

print('\n=== Day-type x piece du capteur (% en ligne) ===')
ct = pd.crosstab(dt['daytype'], dt['room'], normalize='index') * 100
print(ct.round(0).to_string())
print('\n=== Day-type x piece du capteur (% en colonne) — lecture : composition des jours par piece ===')
ct2 = pd.crosstab(dt['daytype'], dt['room'], normalize='columns') * 100
print(ct2.round(0).to_string())

print('\n=== Jours par logement (semaine / week-end) ===')
dt['we'] = dt['DATE'].dt.dayofweek >= 5
n_days = dt.groupby(['CODELIEU','we']).size().unstack(fill_value=0)
print(n_days.describe().round(1).to_string())
