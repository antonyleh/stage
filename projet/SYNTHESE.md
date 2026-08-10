# Détecter l'occupation d'un logement à partir du CO2

**Données OQAI CNL1** — synthèse des travaux

---

## 1. La question

Le CO2 intérieur est produit par la respiration des occupants. On cherche à
savoir dans quelle mesure ce signal permet de retrouver leur **présence**, et
au-delà, leur activité.

Les données proviennent de la campagne nationale logements CNL1 : 535 logements
équipés d'un capteur CO2 relevant une mesure toutes les 10 minutes, sur des
périodes d'environ une semaine par logement, réparties entre octobre 2003 et
décembre 2005. Le capteur se trouve dans une **chambre** dans 95 % des cas.

Deux sources déclaratives accompagnent ces mesures :

| Source | Contenu | Couverture |
|---|---|---|
| Semainier | pièce occupée par chaque occupant, par tranche de 10 min | 7 jours par logement |
| Carnet journalier | activités déclarées (dormir, cuisiner, aérer…) | **1 seule journée** par logement |

---

## 2. Préparation du signal

Trois choix structurent tout le travail qui suit.

**Travailler sur la dérivée du CO2.** Le niveau absolu dépend surtout du
logement — volume, ventilation, occupation de fond. Sa variation traduit les
événements : arrivée d'un occupant, aération, départ.

**Calculer cette dérivée sur la série continue**, avant tout découpage en
journées. Le filtre de lissage (Savitzky-Golay, fenêtre de 13 points, ordre 2)
a besoin de points de part et d'autre de chaque instant ; découper d'abord
créerait un artefact à minuit, aux deux bords de chaque journée.

**Normaliser par journée.** Une vérification à quatre échelles emboîtées le
justifie :

| Échelle | Amplitude observée |
|---|---|
| Une journée d'un logement | ± 150 ppm/h |
| Toutes les journées de ce logement | ± 200 ppm/h |
| **16 logements, une même journée** | **± 1 600 ppm/h** |
| Tous logements, toutes journées | ± 3 500 ppm/h |

Le saut se produit **en changeant de logement, pas en ajoutant des jours** :
certains varient dix fois plus que d'autres et dominent tout si l'on ne remet
pas à l'échelle. Chaque journée est donc ramenée à sa propre moyenne et à son
propre écart-type, ce qui conserve la forme et efface l'amplitude.

---

## 3. Première approche : le clustering

**Principe** — regrouper les journées qui se ressemblent, sans hypothèse
préalable, en espérant voir émerger des types interprétables.

Plusieurs variantes ont été testées : signal continu contre signal discrétisé
en cinq paliers, distance DTW (tolérant un décalage temporel de ±1 h) contre
distance euclidienne, différentes valeurs du nombre de groupes.

**Résultat** — les partitions obtenues sont instables. Deux méthodes appliquées
aux *mêmes* données avec le *même* nombre de groupes produisent des découpages
presque indépendants : **ARI = 0.21** (1 signifierait des partitions identiques,
0 aucun rapport).

Le croisement avec les caractéristiques des ménages ne montre aucun contraste :

| Cluster | Logements | Surface médiane | Occupants | % avec actif |
|---|---|---|---|---|
| 0 | 28 | 91 m² | 2 | 67.9 |
| 1 | 113 | 98 m² | 3 | 77.9 |
| 2 | 78 | 95 m² | 3 | 73.1 |
| 3 | 190 | 110 m² | 3 | 77.9 |
| 4 | 70 | 80 m² | 2 | 67.1 |
| 5 | 34 | 78 m² | 2 | 64.7 |

**Pourquoi cette approche ne pouvait pas trancher** — le clustering ne dispose
d'aucun critère extérieur permettant de juger un résultat. Chaque modification
de la normalisation, de l'encodage ou du nombre de groupes redistribuait les
clusters sans qu'on puisse dire si le résultat s'améliorait.

---

## 4. Basculement : approche supervisée

**Le constat** — le semainier fournit une vérité terrain à la même résolution
temporelle que le CO2. La question posée n'est donc pas « quels types de
journées existe-t-il ? » mais « peut-on retrouver la présence à partir du
signal ? », qui admet une réponse vérifiable.

### Construction du jeu de données

| Étape | Observations | Journées | Logements |
|---|---|---|---|
| Croisement CO2 × semainier | 391 248 | 2 717 | 471 |
| Sans journées saturées (≥ 6000 ppm) | 389 952 | 2 708 | 471 |
| **Semainier intégralement renseigné** | **342 698** | **2 488** | **451** |

Deux précautions importantes :

- **Traitement des déclarations manquantes.** 8.2 % des cases du semainier ne
  sont pas remplies. Une comparaison directe les compterait comme des
  *absences*, alors que la position y est seulement *inconnue* — un biais qui ne
  fabrique que de fausses absences. Seules les tranches où **tous** les occupants
  ont renseigné leur position sont conservées. Le jeu final ne contient aucune
  valeur manquante.

- **Découpe train/test par logement.** Si des journées d'un même logement se
  trouvaient des deux côtés, le modèle apprendrait à reconnaître *ce logement*
  plutôt que la relation générale, et le score serait trompeur.

### Résultats

| Modèle | AUC | Exactitude |
|---|---|---|
| Référence (classe majoritaire) | 0.500 | 0.567 |
| Régression logistique | 0.922 | 0.869 |
| **Gradient boosting** | **0.936** | 0.876 |

---

## 5. Le résultat, correctement énoncé

Une AUC de 0.936 ne se rapporte pas telle quelle. Le capteur étant en chambre,
la règle « la nuit quelqu'un dort ici, la journée non » fonctionne déjà très
bien **sans jamais regarder le CO2** :

| Créneau | Présence réelle |
|---|---|
| 0-4h | 92.2 % |
| 16-20h | 8.1 % |

Un modèle n'utilisant **que l'heure** atteint 0.902. Une large part de la
performance globale tient donc à la régularité du rythme, non au signal.

La mesure honnête est le **gain à heure comparable** :

| Créneau | Heure seule | Avec le CO2 | Gain |
|---|---|---|---|
| 0-4h | 0.569 | 0.886 | **+0.32** |
| 4-8h | 0.733 | 0.878 | +0.15 |
| 8-12h | 0.710 | 0.818 | +0.11 |
| 12-16h | 0.536 | 0.782 | **+0.25** |
| 16-20h | 0.524 | 0.724 | **+0.20** |
| 20-24h | 0.778 | 0.838 | +0.06 |

**En pleine nuit, savoir qu'il est 2 h ne distingue plus rien** (0.569, à peine
mieux que le hasard) — et le CO2 fait passer à 0.886. Même constat l'après-midi.
Le signal apporte l'information précisément là où le rythme moyen est muet.

### Trois enseignements complémentaires

**Le niveau prime sur la dérivée** — 0.849 contre 0.706 pris séparément. C'est
contre-intuitif au vu du travail consacré à la dérivée : celle-ci signale les
*événements*, mais c'est l'accumulation qui traduit la *présence*.

**Le signal réagit avec 30 minutes de retard.** Le CO2 reflète la présence
passée, le temps que le gaz s'accumule.

**Les transitions restent mal détectées** — +0.05 seulement sur les débuts de
plage. Le CO2 s'accumule et se dissipe lentement : l'instant précis d'une
arrivée ou d'un départ est intrinsèquement flou dans ce signal.

---

## 6. Pourquoi le modèle réussit ici et échoue là

La performance varie fortement d'un logement à l'autre (AUC médiane 0.97, mais
10 % des logements sous 0.88). Le croisement avec les caractéristiques déclarées
donne un résultat net.

**La ventilation ne joue aucun rôle** — c'était l'hypothèse la plus intuitive
(un renouvellement d'air rapide devrait brouiller le lien), elle est infirmée :
0.012 d'écart entre types de ventilation, non significatif (p = 0.22).

**Le facteur déterminant est la régularité du rythme.** En mesurant, pour chaque
logement, ce qu'un modèle n'utilisant que l'heure parvient à prédire, on obtient
un indicateur de régularité. Sa corrélation avec la performance est de **+0.77**,
sans commune mesure avec le reste :

| Facteur | Corrélation avec l'AUC |
|---|---|
| **Régularité du rythme** | **+0.77** |
| Surface | +0.33 |
| Taux de présence | −0.31 |
| Nombre de pièces | +0.23 |

Le seul groupe nettement distinct est celui des **studios** (0.791 contre 0.971,
sur 14 logements) : dans une pièce unique, l'occupant présent chez lui s'y trouve
nécessairement, à toute heure. Le rythme « chambre » disparaît, et avec lui le
principal repère du modèle. Une fois la régularité neutralisée, l'effet de la
surface chute de +0.33 à +0.16 — plus de la moitié transite par elle.

**L'hypothèse du statut professionnel est infirmée, et même inversée.** On
attendait des ménages d'actifs, aux horaires contraints, une occupation plus
régulière. C'est l'inverse :

| Profil du ménage | Logements | Régularité | Contraste jour/nuit |
|---|---|---|---|
| **Aucun horaire contraint** | 97 | **0.975** | **0.958** |
| Majorité contrainte | 312 | 0.954 | 0.917 |
| Minorité contrainte | 38 | 0.949 | 0.828 |

L'écart est significatif (p = 0.0001), et la part d'occupants contraints corrèle
négativement avec la régularité (rho = −0.175).

L'explication envisagée — une alternance semaine/week-end propre aux actifs —
**a été testée et écartée** :

| Profil du ménage | Semaine | Week-end | Écart |
|---|---|---|---|
| Aucun horaire contraint | 0.981 | 0.980 | 0.002 |
| Majorité contrainte | 0.968 | 0.958 | 0.006 |
| Minorité contrainte | 0.964 | 0.948 | 0.012 |

Les écarts sont négligeables et ne diffèrent pas selon le profil (p = 0.37) ; la
hiérarchie se retrouve à l'identique dans les deux périodes. Ce n'est donc pas
l'alternance travail/repos qui est en cause, mais une stabilité d'habitudes plus
générale, dont le mécanisme reste à élucider. La taille du ménage est écartée
(rho = +0.047, p = 0.32) ; l'âge des occupants et la présence d'enfants
constituent des pistes non testées ici.

**Ce que cela dit des tentatives de clustering** — aucune caractéristique
*structurelle* n'explique la performance, et le statut professionnel ne prédit la
régularité que faiblement, dans un sens contre-intuitif. Ce qui compte est un
trait d'*usage* — la stabilité des habitudes — que ne capture aucun
questionnaire. Il n'existe pas de « types de logements » lisibles dans la
dynamique du CO2 : les logements se distinguent par la manière dont ils sont
habités.

---

## 7. Pistes explorées sans succès

**Estimer le nombre d'occupants** — distinguer une personne de deux atteint
0.65-0.68 d'AUC, contre 0.93 pour la simple présence. Les moyennes expliquent
pourquoi : le premier occupant fait bondir le CO2 normalisé de 0.93, le second
de 0.32 seulement. Cet effet marginal décroissant est attendu — le CO2 résulte
d'un équilibre entre production et renouvellement d'air, et sature. S'y ajoutent
deux facteurs confondus avec le nombre : l'activité des occupants et le taux de
ventilation.

**Ajouter température et humidité** — mesurées par la même sonde, aux mêmes
instants. Gain nul sur la présence (+0.001) et négatif sur le dénombrement
(−0.024). Prises isolément elles valent mieux que le hasard (0.696), mais leur
information est **redondante** avec celle du CO2 : les trois capteurs occupent
la même pièce et réagissent aux mêmes causes.

**Détecter les activités** — le carnet journalier ne couvre qu'une journée par
logement, soit 416 journées croisant un CO2 complet. Surtout, les activités les
plus visibles physiquement sont les plus rares :

| Activité | Tranches déclarées |
|---|---|
| Je dors | 48 895 |
| Je sors | 10 243 |
| Je fais la cuisine | 3 027 |
| **J'aère** | **166** |

L'aération produit la signature la plus nette dans le CO2 — une chute brutale —
mais 166 observations ne permettent aucun apprentissage fiable. C'est une limite
des données, pas de la méthode.

---

## 8. Limites

**La vérité terrain est déclarative.** Le semainier est rempli de mémoire, avec
les approximations que cela suppose : horaires arrondis, oublis. Une part de
l'erreur mesurée relève de la déclaration et non du signal, ce qui rend les
scores obtenus plutôt conservateurs.

**Le capteur mesure une pièce, pas le logement.** Dans 95 % des cas une chambre.
Ce que l'on détecte est donc largement « quelqu'un dort ici », et non
l'occupation du logement au sens large.

**La campagne est ancienne** (2003-2005) et les logements observés une semaine
seulement. Aucune conclusion ne peut être tirée sur les variations saisonnières
d'un même logement.

---

## 9. Perspectives

**Estimer le taux de renouvellement d'air** à partir des phases de décroissance
du CO2, puis le comparer au type de ventilation déclaré. C'est la piste la plus
riche scientifiquement, et directement pertinente pour un travail sur la qualité
de l'air intérieur. Elle permettrait aussi de retirer ce facteur de l'équation
du dénombrement, où il se confond aujourd'hui avec l'effet du nombre d'occupants.

**Exploiter la régularité du rythme comme variable à part entière.** Elle
explique la performance mieux que toute caractéristique déclarée ; en faire un
objet d'étude plutôt qu'un facteur explicatif ouvrirait une lecture des modes
d'habiter.

---

## Notebooks

| Fichier | Contenu | État |
|---|---|---|
| `detection_occupation.ipynb` | **Résultat principal** — détection de présence | à jour |
| `analyse_erreurs.ipynb` | Pourquoi le modèle réussit ou échoue | à jour |
| `estimation_occupants.ipynb` | Dénombrement · apport température/humidité | à jour |
| `clustering_journees.ipynb` | Clustering sur signal continu | conservé |
| `clustering_paliers.ipynb` | Clustering sur signal discrétisé | conservé |
| `clustering_datetype.ipynb` | Exploration initiale (49 cellules) | à archiver |
| `eda.ipynb`, `preparation.ipynb` | Exploration et mise en forme des données | — |

Les paramètres communs (fenêtre de lissage, seuils, graines aléatoires) sont
fixés en tête de chaque notebook ; tous les résultats sont reproductibles.
