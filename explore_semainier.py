import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
sem = pd.read_parquet(CLEAN / 'Comportement/semainier.parquet')
co2 = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')

print('=== CODE_HEURE : valeurs uniques ===')
ch = sem['CODE_HEURE'].unique()
print(f'{len(ch)} codes : {sorted(ch)[:10]} ... {sorted(ch)[-5:]}')

print('\n=== IDN_PIECE : distribution ===')
print(sem['IDN_PIECE'].value_counts(dropna=False).head(20).to_string())
print(f'\nNaN : {sem["IDN_PIECE"].isna().sum():,} ({100*sem["IDN_PIECE"].isna().mean():.1f}%)')

print('\n=== Structure par logement ===')
g = sem.groupby('CODELIEU')
print(f"dates/logement      : {g['DATE'].nunique().describe().round(1).to_string()}")
print(f"occupants/logement  : {g['NUM_OCCUPANT'].nunique().describe().round(1).to_string()}")

print('\n=== Lignes par logement x occupant x date ===')
n = sem.groupby(['CODELIEU','NUM_OCCUPANT','DATE']).size()
print(n.describe().round(1).to_string())

print('\n=== Chevauchement dates semainier vs dates mesures CO2 ===')
co2['DATE'] = co2['DATE_HEURE'].dt.normalize()
sem_dates = sem.groupby('CODELIEU')['DATE'].agg(['min','max'])
co2_dates = co2.groupby('CODELIEU')['DATE'].agg(['min','max'])
both = sem_dates.join(co2_dates, lsuffix='_sem', rsuffix='_co2', how='inner')
overlap = (both['min_sem'] <= both['max_co2']) & (both['max_sem'] >= both['min_co2'])
print(f'logements communs : {len(both)}, avec chevauchement temporel : {overlap.sum()}')
print(both.head(5).to_string())
