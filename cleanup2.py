import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

PLOT_PCA_CLUSTERS = (
    "\n\n"
    "def _plot_pca_clusters(ax, x2d, lbls, n_clusters, title, ev_ratio):\n"
    "    ax.scatter(x2d[:, 0], x2d[:, 1], c=lbls, cmap='tab10', s=40, alpha=0.7)\n"
    "    for c in range(n_clusters):\n"
    "        mask = lbls == c\n"
    "        if mask.sum() == 0: continue\n"
    "        cx, cy = x2d[mask, 0].mean(), x2d[mask, 1].mean()\n"
    "        ax.annotate(f'C{c}', (cx, cy), fontsize=9, fontweight='bold', ha='center',\n"
    "                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='grey'))\n"
    "    ax.set_xlabel(f'PC1 ({ev_ratio[0]*100:.1f}%)')\n"
    "    ax.set_ylabel(f'PC2 ({ev_ratio[1]*100:.1f}%)')\n"
    "    ax.set_title(title, fontweight='bold'); ax.grid(True, alpha=0.2)"
)

EDITS = {
    'f089bd9a': (
        "from statsmodels.tsa.stattools import acf\n"
        "\n"
        "LAGS = [1, 6, 12, 72, 144, 288, 432]\n"
        "MIN_POINTS = max(LAGS) + 50\n"
        "\n"
        "MESURES_ACF = [\n"
        "    (co2_e,     'VALEUR',     'co2'),\n"
        "    (confort_e, 'VALEUR_TPT', 'tpt'),\n"
        "    (confort_e, 'VALEUR_HRE', 'hre'),\n"
        "]\n"
        "\n"
        "coverage = pd.DataFrame({'CODELIEU': log['CODELIEU']})\n"
        "for df_m, col, prefix in MESURES_ACF:\n"
        "    n = df_m.groupby('CODELIEU')[col].count().rename(f'n_{prefix}')\n"
        "    coverage = coverage.merge(n, on='CODELIEU', how='left')\n"
        "\n"
        "coverage = coverage.fillna(0).astype({'n_co2': int, 'n_tpt': int, 'n_hre': int})\n"
        "coverage['n_min'] = coverage[['n_co2','n_tpt','n_hre']].min(axis=1)\n"
        "\n"
        "codelieux_valides = coverage[coverage['n_min'] > MIN_POINTS]['CODELIEU'].tolist()\n"
        "print(f'Lag max : {max(LAGS)} x 10 min = {max(LAGS)*10//60}h  |  Seuil minimum : {MIN_POINTS} points')\n"
        "print(f'Logements retenus : {len(codelieux_valides)} / {len(log)}  ({100*len(codelieux_valides)/len(log):.1f}%)')"
    ),
    '8a991e52': (
        "LAGS = [1, 72, 144]\n"
        "\n"
        "cols_retenus = [f'{p}_acf_{l}' for p in ['co2', 'tpt', 'hre'] for l in LAGS]\n"
        "df_acf = df_acf_full[cols_retenus]\n"
        "X      = StandardScaler().fit_transform(df_acf)\n"
        "\n"
        "print(f'Features retenues : {df_acf.shape[1]}  ({len(LAGS)} lags x 3 signaux)')\n"
        "print(f'Logements         : {df_acf.shape[0]}')\n"
        "print(f'\\nColonnes : {df_acf.columns.tolist()}')"
    ),
    '77a60df3': (
        "from sklearn.metrics import silhouette_score\n"
        "\n"
        "k_range  = range(2, 20)\n"
        "inertias = []\n"
        "sil_km   = []\n"
        "\n"
        "for k in k_range:\n"
        "    km  = KMeans(n_clusters=k, random_state=42, n_init=50)\n"
        "    lbl = km.fit_predict(X)\n"
        "    inertias.append(km.inertia_)\n"
        "    sil_km.append(silhouette_score(X, lbl))\n"
        "\n"
        "fig, axes = plt.subplots(1, 2, figsize=(12, 4))\n"
        "axes[0].plot(list(k_range), inertias, 'bo-', lw=2)\n"
        "axes[0].set_xlabel('k'); axes[0].set_ylabel('Inertie')\n"
        "axes[0].set_title('K-Means — Coude', fontweight='bold')\n"
        "axes[0].grid(True, alpha=0.3)\n"
        "axes[1].plot(list(k_range), sil_km, 'bo-', lw=2)\n"
        "axes[1].set_xlabel('k'); axes[1].set_ylabel('Silhouette')\n"
        "axes[1].set_title('K-Means — Silhouette', fontweight='bold')\n"
        "axes[1].grid(True, alpha=0.3)\n"
        "plt.suptitle('K-Means — Sélection du nombre de clusters\\n(9 features ACF normalisées, sans PCA)',\n"
        "             fontweight='bold', fontsize=12)\n"
        "plt.tight_layout(); plt.show()\n"
        "\n"
        "k_km = list(k_range)[sil_km.index(max(sil_km))]\n"
        "print(f'K-Means silhouette max : k={k_km}')"
    ),
    '8c034f72': (
        "pca2d   = PCA(n_components=2)\n"
        "X_2d    = pca2d.fit_transform(X)\n"
        "var_exp = sum(pca2d.explained_variance_ratio_) * 100\n"
        "\n"
        "km_final  = KMeans(n_clusters=k_km, random_state=42, n_init=50)\n"
        "labels_km = km_final.fit_predict(X)\n"
        "\n"
        "fig, axes = plt.subplots(1, 2, figsize=(18, 7))\n"
        "_plot_pca_clusters(axes[0], X_2d, labels_km, k_km,  f'K-Means (k={k_km}) — PCA 2D', pca2d.explained_variance_ratio_)\n"
        "_plot_pca_clusters(axes[1], X_2d, labels,    k_bic, f'GMM diag (k={k_bic}) — PCA 2D', pca2d.explained_variance_ratio_)\n"
        "plt.suptitle(f'Comparaison K-Means vs GMM — projection PCA 2D\\n(variance expliquée : {var_exp:.1f}%)',\n"
        "             fontweight='bold', fontsize=13)\n"
        "plt.tight_layout(); plt.show()"
    ),
    'prof_pca2d': (
        "pca2d    = PCA(n_components=2)\n"
        "X_2d     = pca2d.fit_transform(X_pca)\n"
        "var_exp  = sum(pca2d.explained_variance_ratio_) * 100\n"
        "\n"
        "km_final  = KMeans(n_clusters=k_km, random_state=42, n_init=50)\n"
        "labels_km = km_final.fit_predict(X_pca)\n"
        "\n"
        "fig, axes = plt.subplots(1, 2, figsize=(18, 7))\n"
        "_plot_pca_clusters(axes[0], X_2d, labels_km, k_km,  f'K-Means (k={k_km}) — PCA 2D', pca2d.explained_variance_ratio_)\n"
        "_plot_pca_clusters(axes[1], X_2d, labels,    k_bic, f'GMM diag (k={k_bic}) — PCA 2D', pca2d.explained_variance_ratio_)\n"
        "plt.suptitle(f'Comparaison K-Means vs GMM — projection PCA 2D\\n(variance expliquée : {var_exp:.1f}%)',\n"
        "             fontweight='bold', fontsize=13)\n"
        "plt.tight_layout(); plt.show()"
    ),
    'prof_build': (
        "# Profil hebdomadaire moyen par logement — aligné calendaire\n"
        "# cal_pos = jour_semaine * 24 + heure (0–167), déjà calculé en section 7\n"
        "co2_prof = (co2_e.groupby(['CODELIEU', 'cal_pos'])['VALEUR']\n"
        "            .mean().unstack('cal_pos').add_prefix('co2_'))\n"
        "tpt_prof = (confort_e.groupby(['CODELIEU', 'cal_pos'])['VALEUR_TPT']\n"
        "            .mean().unstack('cal_pos').add_prefix('tpt_'))\n"
        "hre_prof = (confort_e.groupby(['CODELIEU', 'cal_pos'])['VALEUR_HRE']\n"
        "            .mean().unstack('cal_pos').add_prefix('hre_'))\n"
        "\n"
        "df_prof = co2_prof.join(tpt_prof, how='inner').join(hre_prof, how='inner').dropna()\n"
        "\n"
        "# Filtre : réutilisation de coverage (section 8) — au moins 1 semaine complète\n"
        "MIN_MESURES = 7 * 144\n"
        "lieux_valides = coverage.loc[coverage['n_min'] >= MIN_MESURES, 'CODELIEU']\n"
        "df_prof = df_prof.loc[df_prof.index.isin(lieux_valides)]\n"
        "\n"
        "print(f'Logements retenus : {len(df_prof)} / {len(log)}')\n"
        "print(f'Features          : {df_prof.shape[1]}  (168 positions cal. × 3 signaux)')\n"
        "display(df_prof.iloc[:3, :6].round(2))"
    ),
}

new_cells = []
for cell in nb['cells']:
    cid = cell.get('id')

    if cid == '92fd8754':
        continue  # cellule vide -> supprimée

    if cid in EDITS:
        cell['source'] = EDITS[cid]
        cell['outputs'] = []
        cell['execution_count'] = None

    if cid == 'plot_helper':
        cell['source'] = ''.join(cell['source']) + PLOT_PCA_CLUSTERS
        cell['outputs'] = []
        cell['execution_count'] = None

    new_cells.append(cell)

nb['cells'] = new_cells

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print(f"Done. {len(new_cells)} cellules.")
