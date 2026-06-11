import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

# ── SECTION 8 — Signatures ACF (restauration) ────────────────────────────

s8_f089bd9a = {
    "cell_type": "code", "id": "f089bd9a", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "from statsmodels.tsa.stattools import acf\n"
        "\n"
        "LAGS = [1, 6, 12, 72, 144, 288, 432]\n"
        "LAG_LABELS = {\n"
        "    1: '10min', 6: '1h',   12: '2h',\n"
        "    72: '12h',  144: '24h', 288: '48h',\n"
        "    432: '3j',\n"
        "}\n"
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
    )
}

s8_f931d74a = {
    "cell_type": "code", "id": "f931d74a", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "rows = []\n"
        "for codelieu in codelieux_valides:\n"
        "    row = {'CODELIEU': codelieu}\n"
        "    for df_m, col, prefix in MESURES_ACF:\n"
        "        ts = (df_m[df_m['CODELIEU'] == codelieu]\n"
        "              .sort_values('DATE_HEURE')[col]\n"
        "              .dropna().values)\n"
        "        try:\n"
        "            vals = acf(ts, nlags=max(LAGS), fft=True)\n"
        "            for lag in LAGS:\n"
        "                row[f'{prefix}_acf_{lag}'] = vals[lag]\n"
        "        except Exception:\n"
        "            for lag in LAGS:\n"
        "                row[f'{prefix}_acf_{lag}'] = np.nan\n"
        "    rows.append(row)\n"
        "\n"
        "df_acf      = pd.DataFrame(rows).set_index('CODELIEU')\n"
        "df_acf_full = df_acf.copy()\n"
        "\n"
        "print(f'\\nShape : {df_acf.shape}  ({len(LAGS)} lags x 3 signaux = {len(LAGS)*3} features)')\n"
        "display(df_acf.head(3).round(3))"
    )
}

s8_0896996f = {
    "cell_type": "code", "id": "0896996f", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "def _col_to_label(col):\n"
        "    prefix, lag = col.split('_acf_')\n"
        "    m = int(lag) * 10\n"
        "    if m < 60:     ts = f'{m}min'\n"
        "    elif m < 1440: ts = f'{m//60}h'\n"
        "    else:          ts = f'{m//1440}j'\n"
        "    return f'{prefix.upper()} {ts}'\n"
        "\n"
        "col_labels = [_col_to_label(c) for c in df_acf_full.columns]\n"
        "corr = df_acf_full.corr()\n"
        "n    = len(col_labels)\n"
        "size = max(12, n * 0.65)\n"
        "\n"
        "fig, axes = plt.subplots(1, 2, figsize=(size * 2, size))\n"
        "sns.heatmap(corr, cmap='RdBu_r', center=0, vmin=-1, vmax=1,\n"
        "            xticklabels=col_labels, yticklabels=col_labels,\n"
        "            annot=True, fmt='.2f', annot_kws={'size': 7},\n"
        "            linewidths=0.3, square=True, ax=axes[0])\n"
        "axes[0].set_title('Corrélations entre features ACF', fontweight='bold')\n"
        "axes[0].tick_params(axis='x', rotation=45, labelsize=8)\n"
        "axes[0].tick_params(axis='y', rotation=0,  labelsize=8)\n"
        "\n"
        "mask = corr.abs() < 0.7\n"
        "sns.heatmap(corr, cmap='RdBu_r', center=0, vmin=-1, vmax=1,\n"
        "            xticklabels=col_labels, yticklabels=col_labels,\n"
        "            annot=True, fmt='.2f', annot_kws={'size': 7},\n"
        "            mask=mask, linewidths=0.3, square=True, ax=axes[1])\n"
        "axes[1].set_title('Corrélations fortes uniquement (|r| > 0.7)', fontweight='bold')\n"
        "axes[1].tick_params(axis='x', rotation=45, labelsize=8)\n"
        "axes[1].tick_params(axis='y', rotation=0,  labelsize=8)\n"
        "\n"
        "plt.suptitle(f'Matrice de corrélation — {n} features ACF', fontweight='bold', fontsize=13)\n"
        "plt.tight_layout(); plt.show()"
    )
}

s8_8a991e52 = {
    "cell_type": "code", "id": "8a991e52", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "LAGS       = [1, 72, 144]\n"
        "LAG_LABELS = {1: '10min', 72: '12h', 144: '24h'}\n"
        "\n"
        "cols_retenus = [f'{p}_acf_{l}' for p in ['co2', 'tpt', 'hre'] for l in LAGS]\n"
        "df_acf = df_acf_full[cols_retenus]\n"
        "X      = StandardScaler().fit_transform(df_acf)\n"
        "\n"
        "print(f'Features retenues : {df_acf.shape[1]}  ({len(LAGS)} lags x 3 signaux)')\n"
        "print(f'Logements         : {df_acf.shape[0]}')\n"
        "print(f'\\nColonnes : {df_acf.columns.tolist()}')"
    )
}

s8_77a60df3 = {
    "cell_type": "code", "id": "77a60df3", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "from sklearn.preprocessing import StandardScaler\n"
        "from sklearn.cluster import KMeans\n"
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
    )
}

s8_gmm = {
    "cell_type": "code", "id": "gmm_vs_kmeans", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "from sklearn.mixture import GaussianMixture\n"
        "\n"
        "k_range_gmm = range(2, 20)\n"
        "bic_scores, aic_scores, sil_gmm = [], [], []\n"
        "gmm_models = {}\n"
        "\n"
        "for k in k_range_gmm:\n"
        "    gmm = GaussianMixture(n_components=k, covariance_type='diag', random_state=42, n_init=50)\n"
        "    lbl = gmm.fit_predict(X)\n"
        "    bic_scores.append(gmm.bic(X))\n"
        "    aic_scores.append(gmm.aic(X))\n"
        "    sil_gmm.append(silhouette_score(X, lbl))\n"
        "    gmm_models[k] = gmm\n"
        "\n"
        "fig, axes = plt.subplots(1, 4, figsize=(24, 5))\n"
        "axes[0].plot(list(k_range), inertias, 'bo-', lw=2)\n"
        "axes[0].set_xlabel('k'); axes[0].set_ylabel('Inertie')\n"
        "axes[0].set_title('K-Means — Coude', fontweight='bold'); axes[0].grid(True, alpha=0.3)\n"
        "axes[1].plot(list(k_range),     sil_km,  'bo-', lw=2, label='K-Means')\n"
        "axes[1].plot(list(k_range_gmm), sil_gmm, 'rs-', lw=2, label='GMM')\n"
        "axes[1].set_xlabel('Nombre de clusters'); axes[1].set_ylabel('Silhouette')\n"
        "axes[1].set_title('Silhouette : K-Means vs GMM', fontweight='bold')\n"
        "axes[1].legend(); axes[1].grid(True, alpha=0.3)\n"
        "axes[2].plot(list(k_range_gmm), bic_scores, 'go-', lw=2)\n"
        "axes[2].set_xlabel('Nombre de clusters'); axes[2].set_ylabel('BIC')\n"
        "axes[2].set_title('GMM — BIC (min = optimal)', fontweight='bold'); axes[2].grid(True, alpha=0.3)\n"
        "axes[3].plot(list(k_range_gmm), aic_scores, 'mo-', lw=2)\n"
        "axes[3].set_xlabel('Nombre de clusters'); axes[3].set_ylabel('AIC')\n"
        "axes[3].set_title('GMM — AIC (min = optimal)', fontweight='bold'); axes[3].grid(True, alpha=0.3)\n"
        "plt.suptitle('K-Means vs GMM — Qualité du clustering\\n(9 features ACF normalisées, sans PCA)',\n"
        "             fontweight='bold', fontsize=12)\n"
        "plt.tight_layout(); plt.show()\n"
        "\n"
        "k_km  = list(k_range)[sil_km.index(max(sil_km))]\n"
        "k_bic = list(k_range_gmm)[bic_scores.index(min(bic_scores))]\n"
        "print(f'K-Means silhouette max : k={k_km}')\n"
        "print(f'GMM BIC minimum        : k={k_bic}')\n"
        "\n"
        "gmm_final = gmm_models[k_bic]\n"
        "labels    = gmm_final.predict(X)"
    )
}

s8_pca2d = {
    "cell_type": "code", "id": "8c034f72", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "from sklearn.decomposition import PCA\n"
        "\n"
        "pca2d   = PCA(n_components=2)\n"
        "X_2d    = pca2d.fit_transform(X)\n"
        "var_exp = sum(pca2d.explained_variance_ratio_) * 100\n"
        "\n"
        "km_final  = KMeans(n_clusters=k_km, random_state=42, n_init=50)\n"
        "labels_km = km_final.fit_predict(X)\n"
        "\n"
        "def _plot_pca_clusters(ax, x2d, lbls, n_clusters, title):\n"
        "    ax.scatter(x2d[:, 0], x2d[:, 1], c=lbls, cmap='tab10', s=40, alpha=0.7)\n"
        "    for c in range(n_clusters):\n"
        "        mask = lbls == c\n"
        "        if mask.sum() == 0: continue\n"
        "        cx, cy = x2d[mask, 0].mean(), x2d[mask, 1].mean()\n"
        "        ax.annotate(f'C{c}', (cx, cy), fontsize=9, fontweight='bold', ha='center',\n"
        "                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='grey'))\n"
        "    ax.set_xlabel(f'PC1 ({pca2d.explained_variance_ratio_[0]*100:.1f}%)')\n"
        "    ax.set_ylabel(f'PC2 ({pca2d.explained_variance_ratio_[1]*100:.1f}%)')\n"
        "    ax.set_title(title, fontweight='bold'); ax.grid(True, alpha=0.2)\n"
        "\n"
        "fig, axes = plt.subplots(1, 2, figsize=(18, 7))\n"
        "_plot_pca_clusters(axes[0], X_2d, labels_km, k_km,  f'K-Means (k={k_km}) — PCA 2D')\n"
        "_plot_pca_clusters(axes[1], X_2d, labels,    k_bic, f'GMM diag (k={k_bic}) — PCA 2D')\n"
        "plt.suptitle(f'Comparaison K-Means vs GMM — projection PCA 2D\\n(variance expliquée : {var_exp:.1f}%)',\n"
        "             fontweight='bold', fontsize=13)\n"
        "plt.tight_layout(); plt.show()"
    )
}

s8_counts = {
    "cell_type": "code", "id": "f41c1868", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "total  = len(labels)\n"
        "counts = pd.Series(labels).value_counts().sort_index()\n"
        "print(f\"{'Cluster':<10} {'N':>6}  {'%':>6}\")\n"
        "print('─' * 30)\n"
        "for c, n in counts.items():\n"
        "    flag = '  <- outlier' if n == 1 else ''\n"
        "    print(f'  C{c:<8} {n:>6}  {100*n/total:>5.1f}%{flag}')\n"
        "print('─' * 30)\n"
        "print(f\"  {'Total':<8} {total:>6}  100.0%\")"
    )
}

s8_correlogram = {
    "cell_type": "code", "id": "acf_correlogram", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "signals = [\n"
        "    ('co2', 'CO2',   '#4C72B0'),\n"
        "    ('tpt', 'Temp.', '#C44E52'),\n"
        "    ('hre', 'Humid.','#55A868'),\n"
        "]\n"
        "lag_vals   = sorted(LAG_LABELS.keys())\n"
        "lag_labels = [LAG_LABELS[l] for l in lag_vals]\n"
        "clusters_s8 = sorted(set(labels))\n"
        "n_cl_s8     = len(clusters_s8)\n"
        "\n"
        "fig, axes = plt.subplots(len(signals), n_cl_s8,\n"
        "                         figsize=(n_cl_s8 * 2.8, len(signals) * 2.8),\n"
        "                         sharey=True, sharex=True)\n"
        "idx_valides = df_acf.index\n"
        "\n"
        "for row, (prefix, sig_label, color) in enumerate(signals):\n"
        "    cols_sig = [f'{prefix}_acf_{l}' for l in lag_vals]\n"
        "    for col, c in enumerate(clusters_s8):\n"
        "        ax   = axes[row, col]\n"
        "        mask = labels == c\n"
        "        sub  = df_acf_full.loc[idx_valides[mask], cols_sig]\n"
        "        for _, profile in sub.iterrows():\n"
        "            ax.plot(range(len(lag_vals)), profile.values,\n"
        "                    color=color, alpha=0.25, lw=0.7)\n"
        "        ax.axhline(0, color='black', lw=0.8, ls='--', alpha=0.4)\n"
        "        ax.set_xticks(range(len(lag_vals)))\n"
        "        ax.set_xticklabels(lag_labels, rotation=45, fontsize=7)\n"
        "        ax.set_ylim(-1.05, 1.05); ax.grid(True, alpha=0.15)\n"
        "        if row == 0:\n"
        "            ax.set_title(f'C{c}  (n={mask.sum()})', fontweight='bold', fontsize=9)\n"
        "        if col == 0:\n"
        "            ax.set_ylabel(sig_label, fontweight='bold', color=color, fontsize=10)\n"
        "\n"
        "plt.suptitle(f'Corrélogrammes ACF par cluster GMM (k={k_bic})\\n'\n"
        "             '(chaque courbe = 1 logement  |  7 lags : 10min -> 3j)',\n"
        "             fontweight='bold', fontsize=12)\n"
        "plt.tight_layout(); plt.show()"
    )
}

s8_profiles = {
    "cell_type": "code", "id": "profiles_by_cluster", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "cluster_map = dict(zip(df_acf.index, labels))\n"
        "co2_cl     = co2_e.copy()\n"
        "confort_cl = confort_e.copy()\n"
        "co2_cl['cluster']     = co2_cl['CODELIEU'].map(cluster_map)\n"
        "confort_cl['cluster'] = confort_cl['CODELIEU'].map(cluster_map)\n"
        "co2_cl     = co2_cl.dropna(subset=['cluster']).astype({'cluster': int})\n"
        "confort_cl = confort_cl.dropna(subset=['cluster']).astype({'cluster': int})\n"
        "\n"
        "clusters = sorted(set(labels))\n"
        "n_cl     = len(clusters)\n"
        "ncols    = min(n_cl, 4)\n"
        "nrows    = (n_cl + ncols - 1) // ncols\n"
        "\n"
        "MESURES_CL = [\n"
        "    (co2_cl,     'VALEUR',     'CO2 (ppm)',  '#4C72B0'),\n"
        "    (confort_cl, 'VALEUR_TPT', 'Temp. (°C)', '#C44E52'),\n"
        "    (confort_cl, 'VALEUR_HRE', 'Humid. (%)', '#55A868'),\n"
        "]\n"
        "tick_pos_cl    = [i * 24 for i in range(8)]\n"
        "tick_labels_cl = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim','']\n"
        "\n"
        "for df_m, col_m, label_m, color_m in MESURES_CL:\n"
        "    fig, axes = plt.subplots(nrows, ncols, figsize=(ncols*5, nrows*3.5),\n"
        "                             sharey=True, sharex=True)\n"
        "    axes_flat = axes.flatten() if n_cl > 1 else [axes]\n"
        "    for i, c in enumerate(clusters):\n"
        "        ax  = axes_flat[i]\n"
        "        sub = df_m[df_m['cluster'] == c]\n"
        "        n   = sub['CODELIEU'].nunique()\n"
        "        if n == 0: ax.axis('off'); continue\n"
        "        profils = (sub.groupby(['CODELIEU','cal_pos'])[col_m].mean().unstack('cal_pos'))\n"
        "        for _, row_p in profils.iterrows():\n"
        "            ax.plot(row_p.index, row_p.values, color=color_m, alpha=0.2, lw=0.6)\n"
        "        ax.axvspan(120, 168, color='#FFD700', alpha=0.08)\n"
        "        ax.set_xticks(tick_pos_cl); ax.set_xticklabels(tick_labels_cl, fontsize=8)\n"
        "        ax.set_xlim(0, 168)\n"
        "        for xv in tick_pos_cl[1:-1]: ax.axvline(xv, color='grey', lw=0.5, ls='--', alpha=0.4)\n"
        "        ax.grid(True, alpha=0.2)\n"
        "        ax.set_title(f'C{c}  (n={n})', fontweight='bold', fontsize=10)\n"
        "        if i % ncols == 0: ax.set_ylabel(label_m, fontsize=9)\n"
        "    for i in range(len(clusters), len(axes_flat)): axes_flat[i].axis('off')\n"
        "    plt.suptitle(f'Profils {label_m} — Lundi -> Dimanche — par cluster ACF-GMM (k={k_bic})\\n'\n"
        "                 '(chaque courbe = 1 logement  |  jaune = week-end)',\n"
        "                 fontweight='bold', fontsize=12)\n"
        "    plt.tight_layout(); plt.show()"
    )
}

# ── SECTION 9 — Profils Journaliers ──────────────────────────────────────

s9_header = {
    "cell_type": "markdown", "id": "s9_header", "metadata": {},
    "source": "## 9. Clustering — Profils Journaliers"
}

# prof_build, prof_pca, prof_clustering, prof_pca2d, prof_counts already in notebook
# Add new profiles cell for section 9 (uses df_prof.index)
s9_profiles = {
    "cell_type": "code", "id": "profiles_by_cluster_prof", "metadata": {}, "outputs": [], "execution_count": None,
    "source": (
        "cluster_map_prof = dict(zip(df_prof.index, labels))\n"
        "co2_cl_p     = co2_e.copy()\n"
        "confort_cl_p = confort_e.copy()\n"
        "co2_cl_p['cluster']     = co2_cl_p['CODELIEU'].map(cluster_map_prof)\n"
        "confort_cl_p['cluster'] = confort_cl_p['CODELIEU'].map(cluster_map_prof)\n"
        "co2_cl_p     = co2_cl_p.dropna(subset=['cluster']).astype({'cluster': int})\n"
        "confort_cl_p = confort_cl_p.dropna(subset=['cluster']).astype({'cluster': int})\n"
        "\n"
        "clusters_p = sorted(set(labels))\n"
        "ncols_p    = min(len(clusters_p), 4)\n"
        "nrows_p    = (len(clusters_p) + ncols_p - 1) // ncols_p\n"
        "\n"
        "MESURES_P = [\n"
        "    (co2_cl_p,     'VALEUR',     'CO2 (ppm)',  '#4C72B0'),\n"
        "    (confort_cl_p, 'VALEUR_TPT', 'Temp. (°C)', '#C44E52'),\n"
        "    (confort_cl_p, 'VALEUR_HRE', 'Humid. (%)', '#55A868'),\n"
        "]\n"
        "tick_pos_p    = [i * 24 for i in range(8)]\n"
        "tick_labels_p = ['Lun','Mar','Mer','Jeu','Ven','Sam','Dim','']\n"
        "\n"
        "for df_m, col_m, label_m, color_m in MESURES_P:\n"
        "    fig, axes = plt.subplots(nrows_p, ncols_p, figsize=(ncols_p*5, nrows_p*3.5),\n"
        "                             sharey=True, sharex=True)\n"
        "    axes_flat = axes.flatten() if len(clusters_p) > 1 else [axes]\n"
        "    for i, c in enumerate(clusters_p):\n"
        "        ax  = axes_flat[i]\n"
        "        sub = df_m[df_m['cluster'] == c]\n"
        "        n   = sub['CODELIEU'].nunique()\n"
        "        if n == 0: ax.axis('off'); continue\n"
        "        profils = (sub.groupby(['CODELIEU','cal_pos'])[col_m].mean().unstack('cal_pos'))\n"
        "        for _, row_p in profils.iterrows():\n"
        "            ax.plot(row_p.index, row_p.values, color=color_m, alpha=0.2, lw=0.6)\n"
        "        ax.axvspan(120, 168, color='#FFD700', alpha=0.08)\n"
        "        ax.set_xticks(tick_pos_p); ax.set_xticklabels(tick_labels_p, fontsize=8)\n"
        "        ax.set_xlim(0, 168)\n"
        "        for xv in tick_pos_p[1:-1]: ax.axvline(xv, color='grey', lw=0.5, ls='--', alpha=0.4)\n"
        "        ax.grid(True, alpha=0.2)\n"
        "        ax.set_title(f'C{c}  (n={n})', fontweight='bold', fontsize=10)\n"
        "        if i % ncols_p == 0: ax.set_ylabel(label_m, fontsize=9)\n"
        "    for i in range(len(clusters_p), len(axes_flat)): axes_flat[i].axis('off')\n"
        "    plt.suptitle(f'Profils {label_m} — Lundi -> Dimanche — par cluster Profil-GMM (k={k_bic})\\n'\n"
        "                 '(chaque courbe = 1 logement  |  jaune = week-end)',\n"
        "                 fontweight='bold', fontsize=12)\n"
        "    plt.tight_layout(); plt.show()"
    )
}

# IDs currently in the notebook (from the rebuild)
S9_EXISTING = {'prof_build', 'prof_pca', 'prof_clustering', 'prof_pca2d', 'prof_counts'}
REMOVE_IDS  = {'profiles_by_cluster', 'profiles_by_cluster_prof'}

S8_CELLS = [s8_f089bd9a, s8_f931d74a, s8_0896996f, s8_8a991e52,
            s8_77a60df3, s8_gmm, s8_pca2d, s8_counts,
            s8_correlogram, s8_profiles]

new_cells = []
s9_inserted = False

for cell in nb['cells']:
    cid = cell.get('id', '')

    if cid in REMOVE_IDS:
        continue

    if cid == '183420c9':          # Section 8 header
        new_cells.append(cell)
        new_cells.extend(S8_CELLS)
        continue

    if cid == 'prof_build' and not s9_inserted:   # First section 9 cell
        new_cells.append(s9_header)
        s9_inserted = True

    if cid in S9_EXISTING:
        new_cells.append(cell)
        if cid == 'prof_counts':   # Last section 9 cell → add profiles
            new_cells.append(s9_profiles)
        continue

    new_cells.append(cell)

nb['cells'] = new_cells

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Done.")
print(f"Total cells: {len(new_cells)}")
for c in new_cells:
    cid = c.get('id','?')
    src = ''.join(c['source'])[:55].replace('\n',' ')
    print(f"  {cid:<30}  {src}")
