# Observatoire de la qualité des environnements intérieurs

## Documentation
**Relative aux jeux de données CNL1 mis en ligne sur data.gouv**
**NOTE FINALE | décembre 2024**
*SC-QEI-2024-170*
*anses, CSTB - le futur en construction*

---

## Préambule

L'Observatoire de la Qualité des Environnements Intérieurs (OQEI), est piloté par l'Agence Nationale de Sécurité Sanitaire de l'alimentation, de l'environnement et du travail (Anses) et par le Centre Scientifique et Technique du Bâtiment (CSTB). Dans le cadre du programme de travail de l'OQEI, l'action du présent rapport a été financée par la DGPR, l'Ademe, la DGS et la DHUP. 

* Toute utilisation ou modification de ce rapport par des tiers, sous quelque forme que ce soit, est faite sous leur seule et entière responsabilité, sans que celle de l'OQEI ne puisse être recherchée.
* Toute reproduction ou représentation intégrale ou partielle, par quelque procédé que ce soit, des pages publiées dans le présent document, faite sans l'autorisation de l'Anses et du CSTB est illicite et constitue une contrefaçon. 
* Seules sont autorisées, d'une part, les reproductions strictement réservées à l'usage du copiste et non destinées à une utilisation collective et, d'autre part, les analyses et courtes citations justifiées par le caractère scientifique ou d'information de l'œuvre dans laquelle elles sont incorporées (Loi du 1er juillet 1992 - art. L 122-4 et L 122-5 et Code Pénal art. 425). 
* L'OQEI décline toute responsabilité dans les conclusions et avis qui pourraient être associés à la réutilisation des données mises à disposition, qui n'engagent que leurs auteurs.

## Auteurs et Relecteurs

* **Auteurs :** DESVIGNES Virginie - CSTB DSC/QEI
* **Relecteurs :** RAMALHO Olivier - CSTB DSC/QEI ; GREGOIRE Anthony - CSTB DSC/QEI
* **Citation suggérée :** DESVIGNES Virginie, RAMALHO Olivier, GREGOIRE Anthony. 2024. Observatoire de la Qualité des Environnements Intérieurs - Documentation relative aux jeux de données CNL1 mis en ligne sur data.gouv. France: OQEI.
* **Mots clés :** Enquête nationale, polluant, résidentiel, COV, particules, particules fines, formaldéhyde, air intérieur, composés organiques volatils, radon, foyer. / *National survey, pollutant, dwellings, VOCs, particles, particulate matter, formaldehyde, indoor air, volatile organic compounds, radon, household*.

---

## Table des matières

| Section | Titre | Page |
| :--- | :--- | :--- |
| | Abréviations | 5 |
| 1 | Contexte et objectif de la première campagne nationale logement | 6 |
| 2 | Liste des fichiers mis à disposition | 7 |
| 3 | Description des jeux de données | 8 |
| 3.1 | Jeux de données relatif à la description des logements | 8 |
| 3.2 | Jeux de données relatifs à la mesure et aux concentrations de polluants dans l'air | 9 |
| 3.3 | Jeu de données relatif aux caractéristiques aux ménages et individus | 10 |
| 4 | Import et utilisation des jeux de données | 13 |
| 5 | Conclusions | 13 |
| 6 | Annexes | 14 |
| | Annexe 1 : Code qualité des mesures dynamiques | 14 |
| | Annexe 2 : Activité professionnelle dans l'immeuble | 15 |
| | Annexe 3 : Type de pièces | 16 |
| | Annexe 4 : Lien avec la personne de référence du ménage | 17 |
| | Annexe 5 : Codification de la nationalité | 18 |
| | Annexe 6 : Codification du niveau d'étude atteint | 20 |
| | Annexe 7 : Codification du diplôme le plus élevé obtenu | 21 |
| | Annexe 8 : Codification de la profession | 23 |

---

## Abréviations

| Acronyme | Définition |
| :--- | :--- |
| **BETA** | Budget espace-temps-activités |
| **CNLI** | Première Campagne Nationale Logement |
| **CO** | Monoxyde de carbone |
| **CQ** | Code qualité |
| **JDD** | Jeu de données |
| **OQAI** | Observatoire de la qualité de l'air intérieur |
| **ppm** | Partie par million |
| **QAI** | Qualité de l'air intérieur |

---

## 1. Contexte et objectif de la première campagne nationale logement

La campagne nationale dans les logements conduite par l'Observatoire de la Qualité de l'Air Intérieur (OQAI) sur la période allant de septembre 2003 à décembre 2005 autorise à dresser un premier état de la qualité de l'air intérieur représentatif de la situation des 24 millions de résidences principales en France métropolitaine continentale. 

* **Paramètres évalués :** Ils ont été choisis en fonction de leur impact sur la qualité de l'air ou sur le confort, de leur dangerosité et de leur fréquence d'apparition : monoxyde de carbone, composés organiques volatils, particules, radon, allergènes de chiens, de chats, d'acariens, rayonnement gamma, dioxyde de carbone, température, humidité relative (Mosqueron et Nedellec, 2002). 
* **Sources de pollution :** Ce sont des paramètres différents de ceux retenus habituellement pour caractériser la qualité de l'air extérieur car ils sont le reflet de la présence de multiples sources potentielles de pollution intérieure : matériaux, équipements, mobilier, produits ménagers, activité humaine, environnement extérieur, etc. 
* **Données collectées :** Des informations détaillées ont été collectées sur les caractéristiques techniques des logements et leur environnement ainsi que sur les ménages, leurs activités et le temps passé au contact de la pollution. Les données ont été recueillies dans 567 résidences principales (1612 individus enquêtés) réparties sur 50 départements et 74 communes de la France continentale métropolitaine, sur une durée d'une semaine, à l'intérieur des logements, dans les garages communiquant avec le logement (lorsqu'ils existaient) et à l'extérieur.

**Constats principaux :**
* Il existe une spécificité de la qualité de l'air à l'intérieur des logements par rapport à l'extérieur qui s'exprime en particulier par la présence de certaines substances non observées à l'extérieur ou par des concentrations nettement plus importantes à l'intérieur. 
* Les polluants visés sont présents à des niveaux quantifiables dans la majorité des logements du parc. 
* La répartition de la pollution chimique organique n'est pas homogène dans le parc. 
* Seule une minorité de logement (9%) présente des concentrations très élevées pour plusieurs polluants simultanément ; à l'inverse 45% des logements présentent des niveaux de concentrations très faibles pour l'ensemble des polluants mesurés. 
* Polluant par polluant, de 5 à 30% des logements présentent des valeurs nettement plus élevées que les concentrations trouvées en moyenne dans le parc.

Le détail des enquêtes, la procédure d'échantillonnage des logements, les éléments d'assurance qualité et les résultats détaillés relatifs à cette campagne sont consultables dans le rapport mis en ligne par l'OQAI (Kirchner et al., 2007) via les liens dédiés.

---

## 2. Liste des fichiers mis à disposition

Vingt-deux fichiers en dehors de la présente note sont mis à disposition :

* `20241211_CNLI_LISTE_LOGEMENT.csv` : relatif à des caractéristiques géographiques et de sondages des logements.
* `20241211_CNL1_LISTE_PIECE.csv` : relatif à la table de correspondance des pièces dans les logements.
* `20241211_CNLI_LISTE_LOGEMENT_PIECE_DICO.xlsx` : correspondant un dictionnaire commun aux fichiers `20241211_CNL1_LISTE_LOGEMENT.csv` et `20241211_CNLI_LISTE_PIECE.csv`.
* `20241211_CNLI_LISTE_PARAMETRE.csv` : relatif aux caractéristiques des paramètres mesurés.
* `20241211_CNLI_PARAMETRE.csv` : relatif aux niveaux des paramètres mesurés.
* `20241211_CNLI_PARAMETRE_LISTEPARAM_DICO.xlsx` : correspondant au dictionnaire commun aux fichiers `20241211_CNLI_LISTE_PARAMETRE.csv` et `20241211_CNLI_PARAMETRE.csv`.
* `20241211_CNLI_SERIE_CO.txt` : relatif aux mesures dynamiques de monoxyde de carbone dans les logements.
* `20241211_CNLI_SERIE_CO2.txt` : relatif aux mesures dynamiques de dioxyde de carbone dans les logements.
* `20241211_CNL1_SERIE_HRE.txt` : relatif aux mesures dynamiques de l'humidité relative dans les logements.
* `20241211_CNLI_SERIE_TPT.txt` : relatif aux mesures dynamiques de la température dans les logements.
* `20241211_CNL1_SERIE_TEMPO_DICO.xlsx` : correspondant au dictionnaire commun des fichiers relatifs aux mesures dynamiques.
* `20241211_CNLI_Q_INDIVIDU_DATA.csv` : relatif aux caractéristiques des individus.
* `20241211_CNLI_Q_LOGEMENT_MENAGE_DATA.csv` : relatif aux caractéristiques des ménages.
* `20241211_CNLI_Q_PIECE_DATA.csv` : relatif aux caractéristiques des pièces du logement.
* `20241211_CNL1_Q_TE_DATA.csv` : relatif aux caractéristiques du logement appréciés par l'enquêteur.
* `20241211_CNLI_QUESTIONNAIRE_DICO.xlsx` : correspondant au dictionnaire commun des fichiers relatifs aux questionnaires (ménages, individus, pièces et enquêteurs).
* `CNLI_JOURNALIER_DATA.csv` : relatif aux activités et produits utilisés dans la journée par les individus du logements.
* `CNLI_SEMAINIER_DATA.txt` : relatif au temps passé dans les pièces du logement.
* `CNLI_INFOS_BETA.csv` : relatif à la qualité de remplissage des semainiers et journaliers et taux de présence dans les pièces du logement.
* `CNLI_BETA_DICO.xlsx` : correspondant au dictionnaire commun des fichiers relatifs aux activités, semainiers, journalier et incluant des tables de correspondances des heures, produits et activités.
* `Fiche_10_Le_régime_de_réutilisation_des_documents_administratifs.pdf` : expliquant la pleine responsabilité du réutilisateur des données mises à disposition.

> **Note :** Les dictionnaires décrivent les variables présentes dans les jeux de données et fournissent des informations sur le code, le type, le libellé et les modalités ou l'intervalle numérique possible ainsi que l'enchainement logique amenant à la question/variable quand celle-ci est issue d'un questionnaire.

---

## 3. Description des jeux de données

Les données couvrent un échantillon de 567 logements répartis dans le parc de résidences principales en France métropolitaine continentale. 

* Les données ont été collectées dans le cadre de deux visites au domicile des occupants, espacées d'une semaine. 
* Les enquêtes ont été réalisées tout au long de l'année sans favoriser une saison plutôt qu'une autre. 
* Une seule enquête (incluant la campagne de mesures) a été menée dans chaque logement. 
* Selon les variables, les données sont exprimées à différentes échelles: le logement, une pièce du logement, un individu du logement. 
* Chaque logement ou foyer est rattaché géographiquement au niveau départemental. Le niveau infra-départemental n'est pas disponible. 
* Chaque foyer a exprimé librement son consentement écrit et signé à participer à l'enquête après présentation détaillée du processus d'enquête.

### 3.1 Jeux de données relatif à la description des logements

* `20241211_CNLT_LISTE_LOGEMENT.csv` : se compose de 568 lignes et de 7 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_LISTE_LOGEMENT_PIECE_DICO.xlsx`. Chaque observation correspond à un logement. Le jeu de données regroupe des variables relatives à/au(x) l'identification du logement: CODELOG ou CODELIEU; sondage: POIDS2006, POIDS2008; l'environnement du logement: DEPARTEMENT, REGION; l'enquête: DVISITI, DVISIT2.
* `20241211_CNL1_LISTE_PIECE.csv` : se compose de 64 lignes et de 3 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_LISTE_LOGEMENT_PIECE_DICO.xlsx`. Chaque observation correspond à une pièce. Le jeu de données regroupe des variables relatives à l'identification de la pièce.
* `20241211_CNL1_Q_PIECE_DATA.csv` : se compose de 4 692 lignes et de 42 colonnes et est au format tidy long. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_QUESTIONNAIRE_DICO.xlsx`. Chaque observation correspond à une pièce d'un logement. Le jeu de données regroupe des variables relatives à/au(x) : caractéristiques d'équipement: chauffage, ventilation, cuisson ; caractéristiques relatives au matériaux, caractéristiques relatives à l'état de condensation et moisissures ; caractéristiques relatives aux ouvrants.

### 3.2 Jeux de données relatifs à la mesure et aux concentrations de polluants dans l'air

* `20241211_CNLI_LISTE_PARAMETRE.csv` : se compose de 43 lignes et de 9 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_PARAMETRE_LISTEPARAM_DICO.xlsx`. Chaque observation correspond aux caractéristiques du polluant mesuré: nom, unité, limites analytiques et fichier dans lequel se trouve la valeur mesurée.
* `20241211_CNLI_PARAMETRE.csv` : se compose de 37 643 lignes et de 5 colonnes et est au format tidy long. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_PARAMETRE_LISTEPARAM_DICO.xlsx`. Chaque observation correspond à une mesure de polluant effectuée dans un logement et une pièce.
* **Fichiers de séries temporelles** :
    * `CNLI_SERIE_CO.txt` : se compose de 2 885 164 lignes et de 7 colonnes et est au format tidy long. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_SERIE_TEMPO_DICO.xlsx`. Chaque observation correspond à une mesure dynamique de monoxyde de carbone effectuée dans un logement et une pièce à chaque pas de temps. Le code qualité de la colonne CQ est détaillé en Annexe 1. La particularité des séries chronologiques de CO est qu'elles peuvent contenir des valeurs négatives ce qui, physiquement parlant, peut être à première vue aberrant. En fait, l'appareil de mesure ayant une précision de +/- 3 ppm sur le zéro, il faut considérer chaque donnée comme le représentant d'une classe. Laisser des valeurs négatives a ainsi pour but de ne pas perdre d'information et de laisser à chaque utilisateur le choix de traiter ces valeurs comme il le souhaite (la mise à zéro de toutes les valeurs négatives n'est pas sensée car elle modifie l'aspect des profils).
    * `CNLI_SERIE_CO2.txt` : se compose de 514 426 lignes et de 7 colonnes et est au format tidy long. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_SERIE_TEMPO_DICO.xlsx`. Chaque observation correspond à une mesure dynamique de dioxyde de carbone effectuée dans un logement et une pièce à chaque pas de temps. Le code qualité de la colonne CQ est détaillé en Annexe 1.
    * `CNLI_SERIE_HRE.txt` : se compose de 1 054 179 lignes et de 7 colonnes et est au format tidy long. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNL1_SERIE_TEMPO_DICO.xlsx`. Chaque observation correspond à une mesure dynamique de l'humidité relative effectuée dans un logement et une pièce à chaque pas de temps. Le code qualité de la colonne CQ est détaillé en Annexe 1.
    * `CNLI_SERIE_TPT.txt` : se compose de 1 056 235 lignes et de 7 colonnes et est au format tidy long. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_SERIE_TEMPO_DICO.xlsx`. Chaque observation correspond à une mesure dynamique de la température effectuée dans un logement et une pièce à chaque pas de temps. Le code qualité de la colonne CQ est détaillé en Annexe 1.

### 3.3 Jeu de données relatif aux caractéristiques aux ménages et individus

* `20241211_CNLI_Q_LOGEMENT_MENAGE_DATA.csv` : se compose de 568 lignes et de 351 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_QUESTIONNAIRE_DICO.xlsx`. Chaque observation correspond à un ménage/logement. Le jeu de données regroupe des variables relatives à/au(x) : l'identification du logement et de l'individu: CODELIEU ; caractéristiques du logement ; caractéristiques du ménage et activités ; caractéristiques de l'environnement du logement ; caractéristiques des matériaux de construction du logement ; état du logement ; caractéristiques des équipements ; caractéristiques des ouvrants et pratiques d'aération. L'Annexe 3 présente le type de pièce principale ou de service qui a contribué à l'élaboration des variables NPP et NPS.
* `20241211_CNLI_Q_TE_DATA.csv` : se compose de 1131 lignes et de 7 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_QUESTIONNAIRE_DICO.xlsx`. Chaque observation correspond à l'appréciation de l'état du logement d'un enquêteur dans chaque logement.
* `20241211_CNLI_Q_INDIVIDU_DATA.csv` : se compose de 568 lignes et de 351 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `20241211_CNLI_QUESTIONNAIRE_DICO.xlsx`. Chaque observation correspond à un individu du logement. Le jeu de données regroupe des variables relatives à/au(x) : l'identification du logement et de l'individu: CODELIEU, NUM_OCCUPANT ; caractéristiques de l'individu : LIEN (Annexe 3), MENAGE, SEXE, AGE, NATIO (Annexe 5), NIVETU (Annexe 6), DIPLOM (Annexe 7), PROFES (Annexe 8), NOCCUA, FUMO, AST, GRDI, GRD21, GRD22, GRD31, GRD32,GRD33,ASTB ; activités de l'individus ; l'utilisation de produits.
* `CNLI_JOURNALIER_DATA.csv` : se compose de 197 641 lignes et de 16 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `CNLI_BETA_DICO.xlsx`. Chaque observation correspond à une activité de chaque individu du logement à un pas de temps donné. Le jeu de données regroupe des variables relatives à/au(x) : l'identification du logement et de l'individu: CODELIEU, NUM_OCCUPANT ; pas de temps: CODE_HEURE ; aux activités ; à l'utilisation de produits.
* `CNLI_SEMAINIER_DATA.txt` : se compose de 1386001 lignes et de 5 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `CNLI_BETA_DICO.xlsx`. Chaque observation correspond à la présence de chaque individu du logement dans une pièce à un pas de temps donné. Le jeu de données regroupe des variables relatives à/au(x) : l'identification du logement et de l'individu: CODELIEU, NUM_OCCUPANT; au temps: DATE et CODE_HEURE ; la pièce: IDN_PIECE.
* `CNLI_INFOS_BETA.csv` : se compose de 1 613 lignes et de 16 colonnes et est au format tidy wide. Chaque colonne correspond à une variable décrite dans le dictionnaire de variables `CNLI_BETA_DICO.xlsx`. Chaque observation correspond à la présence de chaque individu du logement dans une pièce à un pas de temps donné. Le jeu de données regroupe des variables relatives à/au(x) : l'identification du logement et de l'individu: CODELIEU, NUM_OCCUPANT; temps: DATE et CODE_HEURE ; remplissage du journalier ; la présence dans les pièces.

---

## 4. Import et utilisation des jeux de données

L'import des fichiers `txt` dans le logiciel R est possible grâce aux ligne de code suivantes :
```R
read.table("CNL1_SERIE CO.txt", h=T, sep="1t'")
read.table("CNL1_SERIE CO2.txt", h=T, sep="1t'")
read.table("CNL1_SERIE HRE.txt", h=T, sep="(t'")
read.table("CNL1_SERIE TPT.txt", h=T, sep="(t'")