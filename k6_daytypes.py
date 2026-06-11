import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pathlib import Path
from sklearn.cluster import KMeans

CLEAN = Path(r'c:\Users\lehmanna\Desktop\stage\projet\data\cln1\Clean')
co2 = pd.read_parquet(CLEAN / 'Mesures/co2.parquet')
sem = pd.read_parquet(CLEAN / 'Comportement/semainier.parquet')

# ===== profils journaliers (identique a la section 9) =====
co2['DATE']  = co2['DATE_HEURE'].dt.normalize()
co2['heure'] = co2['DATE_HEURE'].dt.hour
pts = co2.groupby(['CODELIEU','DATE']).size()
co2c = co2.set_index(['CODELIEU','DATE']).loc[pts[pts >= 138].index].reset_index()
stats = co2c.groupby('CODELIEU')['VALEUR'].agg(['mean','std'])
co2c = co2c.merge(stats, on='CODELIEU')
co2c['z'] = (co2c['VALEUR'] - co2c['mean']) / co2c['std']
prof = co2c.groupby(['CODELIEU','DATE','heure'])['z'].mean().unstack('heure').dropna()
X = prof.values

lab4 = KMeans(n_clusters=4, random_state=42, n_init=30).fit_predict(X)
lab6 = KMeans(n_clusters=6, random_state=42, n_init=30).fit_predict(X)

DT4 = {0:'Plat/absence', 1:'Présence continue', 2:'Pic fin de nuit', 3:'Plateau nocturne'}

print('=== Correspondance k=4 -> k=6 (% en ligne) ===')
ct = pd.crosstab(pd.Series(lab4).map(lambda c: f'k4-{c} {DT4[c]}'),
                 pd.Series(lab6, name='k6'), normalize='index') * 100
print(ct.round(0).to_string())

we = prof.index.get_level_values('DATE').dayofweek >= 5

# ===== presence declaree =====
sem['present'] = sem['IDN_PIECE'].notna() & (sem['IDN_PIECE'] != 90)
sem['heure']   = (sem['CODE_HEURE'].str[2:].astype(int) - 1001) // 6
pres = sem.groupby(['CODELIEU','DATE','heure'])['present'].mean().unstack('heure')
common = prof.index.intersection(pres.index)
pres_c  = pres.loc[common]
lab6_c  = pd.Series(lab6, index=prof.index).loc[common]

print('\n=== k=6 : effectifs, %WE, presence declaree nuit (0-6h) / jour (9-17h) ===')
print(f"{'type':<5} {'n':>5} {'%WE':>5} {'nuit':>6} {'jour':>6}")
for c in range(6):
    mask = lab6 == c
    p = pres_c[lab6_c == c]
    n_ = p[[0,1,2,3,4,5]].mean().mean()
    j_ = p[[9,10,11,12,13,14,15,16,17]].mean().mean()
    print(f'C{c:<4} {mask.sum():>5} {100*we[mask].mean():>4.0f}% {100*n_:>5.0f}% {100*j_:>5.0f}%')

# ===== figure : profils moyens + presence =====
fig, axes = plt.subplots(1, 2, figsize=(18, 6))
colors = plt.cm.tab10(np.linspace(0, 1, 10))
for c in range(6):
    sub = prof.values[lab6 == c]
    m = sub.mean(0)
    axes[0].plot(range(24), m, lw=2.2, marker='o', ms=3, color=colors[c],
                 label=f'C{c} (n={(lab6==c).sum()}, {100*we[lab6==c].mean():.0f}% WE)')
    mp = pres_c[lab6_c == c].mean() * 100
    axes[1].plot(range(24), mp, lw=2.2, marker='o', ms=3, color=colors[c], label=f'C{c}')

axes[0].axhline(0, color='grey', lw=0.8, ls='--', alpha=0.6)
axes[0].set_title('k=6 — profil CO2 moyen (z-score)', fontweight='bold')
axes[0].set_ylabel('CO2 (z)'); axes[0].legend(fontsize=9)
axes[1].set_title('k=6 — présence déclarée (semainier)', fontweight='bold')
axes[1].set_ylabel('Présence (%)'); axes[1].set_ylim(0, 100); axes[1].legend(fontsize=9)
for ax in axes:
    ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels([f'{h}h' for h in range(0, 24, 3)])
    ax.set_xlabel('Heure'); ax.grid(True, alpha=0.25)
plt.tight_layout()
out = r'c:\Users\lehmanna\Desktop\stage\k6_daytypes.png'
plt.savefig(out, dpi=110)
print(f'\nFigure : {out}')
