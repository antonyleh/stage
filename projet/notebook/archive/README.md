# Notebooks archivés

Travaux exploratoires conservés pour mémoire. Ils ne sont plus à jour et ne
doivent pas servir de référence : les résultats retenus figurent dans les
notebooks du dossier parent et dans `projet/SYNTHESE.md`.

## `clustering_datetype.ipynb`

Exploration initiale du clustering des journées CO2 — 49 cellules de code
accumulées au fil des essais. Le notebook contient une dizaine de variantes
menées en parallèle :

| Variante | Devenue |
|---|---|
| DTW sur dérivée normalisée par journée | `clustering_journees.ipynb` |
| DTW sur dérivée encodée en paliers | `clustering_paliers.ipynb` |
| Comparaison des échelles de normalisation | section 3 de `clustering_journees.ipynb` |
| DTW sur dérivée non normalisée | abandonnée — non comparable entre logements |
| DTW multivarié CO2 + température + humidité | abandonnée — reprise proprement dans `estimation_occupants.ipynb` |
| Clustering sur la distribution des valeurs | abandonnée — ne capte qu'un gradient calme/agité |
| K-means sur histogrammes de clusters | abandonnée |

Les parties utiles ont été reprises et vérifiées dans les notebooks actuels.
Ce fichier reste utile pour retrouver le détail d'un essai particulier, mais
plusieurs de ses cellules dépendent de variables supprimées depuis et ne
s'exécutent plus telles quelles.
