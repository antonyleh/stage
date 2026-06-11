import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
from pathlib import Path
from statsmodels.tsa.stattools import acf
from sklearn.preprocessing import StandardScaler
from sklearn.mixture import GaussianMixture
from sklearn.metrics import silhouette_score
from scipy.stats import f_oneway

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')

log     = pd.read_parquet(CLEAN / 'Referentiels/logements.parquet')
co2     = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')
confort = pd.read_parquet(CLEAN / 'Mesures/confort.parquet')

# === reproduit la section 8 ===
LAGS_FULL = [1, 6, 12, 72, 144, 288, 432]
MIN_POINTS = max(LAGS_FULL) + 50

MESURES_ACF = [
    (co2,     'VALEUR',     'co2'),
    (confort, 'VALEUR_TPT', 'tpt'),
    (confort, 'VALEUR_HRE', 'hre'),
]

coverage = pd.DataFrame({'CODELIEU': log['CODELIEU']})
for df_m, col, prefix in MESURES_ACF:
    n = df_m.groupby('CODELIEU')[col].count().rename(f'n_{prefix}')
    coverage = coverage.merge(n, on='CODELIEU', how='left')
coverage = coverage.fillna(0)
coverage['n_min'] = coverage[['n_co2','n_tpt','n_hre']].min(axis=1)
codelieux_valides = coverage[coverage['n_min'] > MIN_POINTS]['CODELIEU'].tolist()

rows = []
for codelieu in codelieux_valides:
    row = {'CODELIEU': codelieu}
    for df_m, col, prefix in MESURES_ACF:
        ts = (df_m[df_m['CODELIEU'] == codelieu]
              .sort_values('DATE_HEURE')[col].dropna().values)
        try:
            vals = acf(ts, nlags=max(LAGS_FULL), fft=True)
            for lag in LAGS_FULL:
                row[f'{prefix}_acf_{lag}'] = vals[lag]
        except Exception:
            for lag in LAGS_FULL:
                row[f'{prefix}_acf_{lag}'] = np.nan
    rows.append(row)

df_full = pd.DataFrame(rows).set_index('CODELIEU')
LAGS = [1, 72, 144]
cols = [f'{p}_acf_{l}' for p in ['co2','tpt','hre'] for l in LAGS]
df_acf = df_full[cols]
X = StandardScaler().fit_transform(df_acf)

gmm = GaussianMixture(n_components=8, covariance_type='diag', random_state=42, n_init=50)
labels = gmm.fit_predict(X)

print('=== Tailles de clusters (GMM k=8) ===')
print(pd.Series(labels).value_counts().sort_index().to_string())
print(f'\nSilhouette GMM k=8 : {silhouette_score(X, labels):.3f}')

gmm3 = GaussianMixture(n_components=3, covariance_type='diag', random_state=42, n_init=50)
lbl3 = gmm3.fit_predict(X)
print(f'Silhouette GMM k=3 : {silhouette_score(X, lbl3):.3f}')
gmm4 = GaussianMixture(n_components=4, covariance_type='diag', random_state=42, n_init=50)
lbl4 = gmm4.fit_predict(X)
print(f'Silhouette GMM k=4 : {silhouette_score(X, lbl4):.3f}')

print('\n=== Variance brute de chaque feature (avant standardisation) ===')
print(df_acf.std().round(3).to_string())

print('\n=== Pouvoir discriminant par feature (ANOVA F entre les 8 clusters) ===')
res = {}
for i, c in enumerate(cols):
    groups = [X[labels == k, i] for k in sorted(set(labels)) if (labels == k).sum() > 1]
    F, p = f_oneway(*groups)
    res[c] = F
print(pd.Series(res).sort_values(ascending=False).round(1).to_string())

print('\n=== Confusion cluster x saison ===')
seg = log.set_index('CODELIEU').loc[df_acf.index]
ct = pd.crosstab(labels, seg['saison'], normalize='index')
print((ct * 100).round(0).to_string())

print('\n=== Confusion cluster x zone climatique ===')
ct2 = pd.crosstab(labels, seg['zone_climatique'], normalize='index')
print((ct2 * 100).round(0).to_string())

print('\n=== Le logement outlier C6 (singleton) ===')
sizes = pd.Series(labels).value_counts()
singletons = sizes[sizes == 1].index
for s in singletons:
    cl = df_acf.index[labels == s][0]
    print(f'Cluster {s} : {cl}')
    print(df_acf.loc[cl].round(3).to_string())
