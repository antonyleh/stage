import json, sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'c:\Users\lehmanna\Desktop\stage\projet\notebook\eda.ipynb'
with open(path, encoding='utf-8') as f:
    nb = json.load(f)

SRC = """# Choix de k : coude (inertie) + silhouette (separation) + stabilite par sous-echantillonnage (ARI)
from sklearn.metrics import adjusted_rand_score

rng = np.random.RandomState(0)
ks  = list(range(2, 21))
inerties, sils, stabs = [], [], []

for k in ks:
    km  = KMeans(n_clusters=k, random_state=42, n_init=30)
    lab = km.fit_predict(X_jour)
    inerties.append(km.inertia_)
    sils.append(silhouette_score(X_jour, lab, sample_size=2000, random_state=0))
    aris = []
    for _ in range(8):
        idx  = rng.choice(len(X_jour), int(0.8 * len(X_jour)), replace=False)
        lab2 = KMeans(n_clusters=k, random_state=rng.randint(10**6), n_init=30).fit_predict(X_jour[idx])
        aris.append(adjusted_rand_score(lab[idx], lab2))
    stabs.append(np.mean(aris))

fig, axes = plt.subplots(1, 3, figsize=(17, 4))
axes[0].plot(ks, inerties, 'o-', color='#C44E52', lw=2)
axes[0].set_xlabel('k'); axes[0].set_ylabel('Inertie intra-cluster')
axes[0].set_title('Coude', fontweight='bold')
axes[1].plot(ks, sils, 'bo-', lw=2)
axes[1].set_xlabel('k'); axes[1].set_ylabel('Silhouette')
axes[1].set_title('Séparation', fontweight='bold')
axes[2].plot(ks, stabs, 'go-', lw=2)
axes[2].set_xlabel('k'); axes[2].set_ylabel('ARI (sous-échantillons 80%)')
axes[2].set_title('Stabilité', fontweight='bold')
for ax in axes:
    ax.axvline(6, color='grey', ls='--', lw=1, alpha=0.6)
    ax.grid(True, alpha=0.3)
plt.suptitle('K-Means sur les journées — choix de k  (pointillé : k=6 retenu)',
             fontweight='bold', fontsize=12)
plt.tight_layout(); plt.show()"""

for cell in nb['cells']:
    if cell.get('id') == 's10_kselect':
        cell['source'] = SRC.splitlines(keepends=True)
        cell['outputs'] = []
        cell['execution_count'] = None

with open(path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)
print('OK')
