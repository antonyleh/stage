import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
co2   = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')
sem   = pd.read_parquet(CLEAN / 'Comportement/semainier.parquet')
q_ind = pd.read_parquet(CLEAN / 'Questionnaires/q_individu.parquet')
q_men = pd.read_parquet(CLEAN / 'Questionnaires/q_menage.parquet')

# ===== day-types k=4 (reproduit) =====
co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour
pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']
prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()
lab = KMeans(n_clusters=4, n_init=30, random_state=42).fit_predict(prof.values)
dtypes = pd.DataFrame({'daytype': lab}, index=prof.index).reset_index()
dtypes['we'] = dtypes['DATE'].dt.dayofweek >= 5

# ===== signature : composition en day-types, JOURS DE SEMAINE uniquement (>=3 jours) =====
semaine = dtypes[~dtypes['we']]
n_jours = semaine.groupby('CODELIEU').size()
ok = n_jours[n_jours >= 3].index
sig = (semaine[semaine['CODELIEU'].isin(ok)]
       .groupby('CODELIEU')['daytype']
       .value_counts(normalize=True).unstack(fill_value=0))
sig.columns = [f'dt{c}' for c in sig.columns]
print(f'Signatures (semaine, >=3 jours) : {len(sig)} logements x {sig.shape[1]} dims')

X = sig.values
rng = np.random.RandomState(0)
print(f"\n{'k':>2} {'silhouette':>10} {'stab. ARI':>10}  tailles")
results = {}
for k in range(2, 7):
    l = KMeans(n_clusters=k, n_init=30, random_state=42).fit_predict(X)
    sil = silhouette_score(X, l)
    aris = []
    for _ in range(8):
        idx = rng.choice(len(X), int(0.8*len(X)), replace=False)
        l2  = KMeans(n_clusters=k, n_init=30, random_state=rng.randint(1e6)).fit_predict(X[idx])
        aris.append(adjusted_rand_score(l[idx], l2))
    results[k] = l
    print(f'{k:>2} {sil:>10.3f} {np.mean(aris):>10.3f}  {np.bincount(l)}')

K = 4
lab_log = pd.Series(results[K], index=sig.index, name='cluster')
print(f'\n=== Composition moyenne par cluster (k={K}) ===')
print('DT0=plat/absent  DT1=presence continue  DT2=pic fin de nuit  DT3=plateau nocturne')
print((sig.groupby(lab_log).mean() * 100).round(0).to_string())

# ===== validation 1 : presence declaree (jours de semaine) =====
sem['present'] = sem['IDN_PIECE'].notna() & (sem['IDN_PIECE'] != 90)
sem['heure']   = (sem['CODE_HEURE'].str[2:].astype(int) - 1001) // 6
sem['we']      = sem['DATE'].dt.dayofweek >= 5
pres_h = (sem[~sem['we']].groupby(['CODELIEU','heure'])['present']
          .mean().unstack('heure'))
common = lab_log.index.intersection(pres_h.index)
heures_aff = [0, 3, 6, 9, 12, 15, 18, 21]
hdr = '  '.join(f'{h:>5}h' for h in heures_aff)
print(f'\n=== Presence declaree en semaine, par cluster ({len(common)} logements) ===')
print(f"{'cl':<4} {'n':>4}  {hdr}   jour(9-17h)")
for c in range(K):
    sel = common[lab_log.loc[common] == c]
    m = pres_h.loc[sel].mean()
    j = m[[9,10,11,12,13,14,15,16,17]].mean()
    vals = '  '.join(f'{100*m[h]:>5.0f}%' for h in heures_aff)
    print(f'C{c:<3} {len(sel):>4}  {vals}   {100*j:>5.0f}%')

# ===== validation 2 : composition du menage =====
q_ind['actif']   = q_ind['profes_label'].astype(str).str.contains('actif|Actif', na=False)
occ = q_ind.groupby('CODELIEU').agg(
    n_occ   = ('NUM_OCCUPANT','nunique'),
    age_moy = ('AGE','mean'),
    n_enfants = ('AGE', lambda s: (s < 18).sum()),
)
print('\n=== profes_label : valeurs ===')
print(q_ind['profes_label'].value_counts(dropna=False).head(10).to_string())

prof_counts = (q_ind.groupby(['CODELIEU','profes_label']).size().unstack(fill_value=0))
occ = occ.join(prof_counts, how='left')

common2 = lab_log.index.intersection(occ.index)
print(f'\n=== Caracteristiques menage par cluster ({len(common2)} logements) ===')
agg = occ.loc[common2].groupby(lab_log.loc[common2]).mean().round(2)
print(agg.to_string())
