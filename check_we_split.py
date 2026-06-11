import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
co2 = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')

co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour
pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']
prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()

lab6 = KMeans(n_clusters=6, random_state=42, n_init=30).fit_predict(prof.values)
we = prof.index.get_level_values('DATE').dayofweek >= 5
DT_NOMS = {0:'Présence diurne',1:'Pic du soir',2:'Plat/absence',
           3:'Plateau nocturne',4:'Pic du matin',5:'Pic nocturne intense'}

print('=== Test 1 : au sein de chaque day-type, forme semaine vs week-end ===')
print('(correlation des profils moyens + ecart max en z)')
for c in range(6):
    sub = prof[lab6 == c]
    m_sem = sub[~we[lab6 == c]].mean()
    m_we  = sub[we[lab6 == c]].mean()
    r = np.corrcoef(m_sem, m_we)[0, 1]
    dmax = (m_sem - m_we).abs().max()
    print(f'DT{c} {DT_NOMS[c]:<22} r={r:.3f}  écart max={dmax:.2f}σ  (n_sem={(~we[lab6==c]).sum()}, n_we={we[lab6==c].sum()})')

print('\n=== Test 2 : clustering separe des seuls week-ends — formes nouvelles ? ===')
X_we = prof[we].values
print(f'{len(X_we)} journées de week-end')
for k in [3, 4, 5, 6]:
    l = KMeans(n_clusters=k, random_state=42, n_init=30).fit_predict(X_we)
    sil = silhouette_score(X_we, l)
    print(f'  k={k} : silhouette {sil:.3f}, tailles {np.bincount(l)}')

km_we = KMeans(n_clusters=4, random_state=42, n_init=30).fit(X_we)
cent6 = np.array([prof.values[lab6 == c].mean(0) for c in range(6)])

print('\nCorrélation max de chaque centroide week-end avec les 6 day-types joints :')
for i, cw in enumerate(km_we.cluster_centers_):
    cors = [np.corrcoef(cw, c6)[0, 1] for c6 in cent6]
    j = int(np.argmax(cors))
    print(f'  WE-{i} (n={np.bincount(km_we.labels_)[i]:>4}) -> DT{j} {DT_NOMS[j]:<22} r={cors[j]:.3f}')
