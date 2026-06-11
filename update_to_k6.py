import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

MD_WHY_K6 = """### Pourquoi k=6 et pas k=4 ?

Les courbes ci-dessus ne donnent pas de k « évident » : silhouette et stabilité décroissent de façon
quasi monotone (structure en continuum). Deux candidats se détachent : **k=4** (stabilité 0.91) et
**k=6**, petit rebond local (silhouette 0.161, stabilité 0.924 — meilleur que k=5 sur les deux critères).

On retient **k=6** pour trois raisons :

1. **Le passage k=4 → k=6 est emboîté** : chaque type de k=4 se subdivise proprement (pas de remélange).
   « Présence continue » se sépare en *présence diurne* (pic l'après-midi) et *pic du soir* ;
   « pic fin de nuit » se sépare en *pic du matin* (6-9h) et *pic nocturne intense* (3-6h).
2. **k=6 discrimine mieux la vérité terrain** : l'écart de présence diurne déclarée entre types passe
   de [34–50%] à [35–54%]. Le nouveau type « présence diurne » est le mieux validé (54% de présence
   déclarée en journée, record du parc — et 46% de jours de week-end).
3. **C'est la classe la plus utile pour la suite** : pour prédire l'activité des occupants, distinguer
   « quelqu'un est à la maison en journée » est précisément l'information cible — k=4 la noyait dans
   un type fourre-tout."""

DAYTYPES_K6 = """# k=6 : rebond local de silhouette/stabilite + subdivisions interpretables (cf. markdown ci-dessus)
K_JOUR    = 6
km_jour   = KMeans(n_clusters=K_JOUR, random_state=42, n_init=30)
dt_labels = km_jour.fit_predict(X_jour)

# noms etablis a partir des profils moyens (valables pour random_state=42)
DT_NOMS = {0: 'Présence diurne',      # pic l'apres-midi, 46% WE
           1: 'Pic du soir',          # absence la journee, pic 21h
           2: 'Plat / absence',       # aucune accumulation
           3: 'Plateau nocturne',     # nuit haute, chute a 9h (actifs)
           4: 'Pic du matin',         # accumulation fin de nuit, pic 6-9h
           5: 'Pic nocturne intense'} # tres forte accumulation 3-6h

prof_dt = prof_jour.copy()
prof_dt['daytype'] = dt_labels
prof_dt['we']      = prof_dt.index.get_level_values('DATE').dayofweek >= 5

fig, ax = plt.subplots(figsize=(13, 6))
for c in range(K_JOUR):
    sub  = prof_dt[prof_dt['daytype'] == c]
    m    = sub[list(range(24))].mean()
    s    = sub[list(range(24))].std()
    line, = ax.plot(range(24), m, lw=2.2, marker='o', ms=3,
                    label=f'DT{c} — {DT_NOMS[c]}  (n={len(sub)}, {100*sub["we"].mean():.0f}% WE)')
    ax.fill_between(range(24), m - s, m + s, alpha=0.06, color=line.get_color())

ax.axhline(0, color='grey', lw=0.8, ls='--', alpha=0.6)
ax.set_xticks(range(0, 24, 3)); ax.set_xticklabels([f'{h}h' for h in range(0, 24, 3)])
ax.set_xlabel('Heure'); ax.set_ylabel('CO₂ (z-score du logement)')
ax.set_title('6 types de journées — profil CO₂ moyen ± 1σ\\n'
             '(rappel : 28.6% des journées sont des jours de week-end)',
             fontweight='bold')
ax.legend(fontsize=10); ax.grid(True, alpha=0.25)
plt.tight_layout(); plt.show()"""

BILAN_K6 = """### Bilan de la section 9

- Les **6 types de journées** sont robustes (stabilité ARI ≈ 0.92) et **validés par le semainier** :
  la présence diurne déclarée s'étale de 35% (« plateau nocturne ») à 54% (« présence diurne »),
  la présence nocturne de 73% (« plat/absence ») à 92% (« plateau nocturne »).
- La **signature logement** (composition en day-types, jours de semaine) donne 4 clusters logement stables
  (ARI ≈ 0.98, silhouette ≈ 0.37) : dominante « plateau nocturne » (actifs), dominante « pic du matin »,
  dominante « pic du soir », et un cluster mixte à dominante « absence ».
- **Limites** : le capteur CO₂ est en chambre (95% des cas) → on mesure surtout l'occupation de la chambre ;
  une seule semaine de mesure → la composition week-end (2 jours) est inexploitable telle quelle ;
  les types rares (« présence diurne », 6% des journées) ne dominent aucun cluster logement.
- **Suite logique** : le semainier fournit des labels de présence par créneau → base d'un futur **modèle supervisé**
  capteurs → présence (les features ACF de la section 8 et les day-types ci-dessus sont des entrées candidates)."""

new_cells = []
for cell in nb['cells']:
    cid = cell.get('id')
    if cid == 's10_daytypes':
        # markdown d'explication insere AVANT la cellule k=6
        new_cells.append({'id': 's10_why_k6', 'cell_type': 'markdown', 'metadata': {},
                          'source': MD_WHY_K6.splitlines(keepends=True)})
        cell['source'] = DAYTYPES_K6.splitlines(keepends=True)
        cell['outputs'] = []
        cell['execution_count'] = None
    if cid == 's10_bilan':
        cell['source'] = BILAN_K6.splitlines(keepends=True)
    new_cells.append(cell)

nb['cells'] = new_cells
with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print(f'OK. {len(new_cells)} cellules.')
