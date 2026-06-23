# ObRail Europe — ETL ferroviaire & modèle IA de substitution avion → train

## 1. Présentation du projet

**ObRail Europe** est un projet complet de traitement et d’exploitation de données ferroviaires européennes.

Le projet couvre deux grandes parties :

1. **Une chaîne ETL ferroviaire** permettant de collecter, transformer, contrôler et charger des données dans PostgreSQL.
2. **Une brique Intelligence Artificielle** permettant d’identifier les liaisons ferroviaires candidates à la substitution avion → train.

L’objectif global est de passer de sources ferroviaires hétérogènes à une solution exploitable comprenant :

- des données harmonisées ;
- un modèle relationnel PostgreSQL ;
- une API REST FastAPI ;
- un dashboard Streamlit ;
- un dataset IA construit à partir des données ETL ;
- un modèle de classification entraîné et sauvegardé ;
- une route API `/predict` permettant d’obtenir une prédiction IA.

---

## 2. Objectifs métier

ObRail Europe souhaite analyser le maillage ferroviaire européen et promouvoir le train comme alternative bas-carbone à l’avion.

Le projet permet notamment de :

- centraliser des données provenant de plusieurs sources ferroviaires ;
- distinguer les trains de jour et les trains de nuit ;
- structurer les données dans un schéma relationnel PostgreSQL ;
- contrôler la qualité des trajets transformés ;
- visualiser les volumes, les opérateurs, les sources et le réseau ferroviaire ;
- construire un dataset IA à partir des données harmonisées ;
- prédire le potentiel de substitution avion → train d’une liaison ferroviaire.

La partie IA classe chaque liaison selon trois niveaux :

```text
faible
moyen
fort
```

---

## 3. Sources de données utilisées

Le projet intègre plusieurs sources :

| Source | Format | Utilisation principale |
|---|---:|---|
| Back-on-Track Night Train Data | JSON | Trains de nuit européens |
| SNCF GTFS | GTFS ZIP | Horaires théoriques SNCF : TGV, Intercités, TER |
| Gares de voyageurs SNCF | CSV | Référentiel des gares françaises avec coordonnées |
| Wikipedia — Busiest railway stations in Europe | HTML scraping | Enrichissement des gares européennes |
| European Sleeper Timetable | HTML + CSV structuré | Trains de nuit European Sleeper |

Chaque extraction génère des fichiers bruts dans `data/raw/` ainsi qu’un fichier `metadata.json` permettant de tracer l’origine et la date d’extraction.

---

## 4. Architecture générale

Le projet suit une chaîne complète :

```text
Sources externes
      │
      ▼
Extraction
      │
      ▼
data/raw/
      │
      ▼
Transformation & contrôle qualité
      │
      ▼
data/processed/
      │
      ├── Chargement PostgreSQL
      │       ├── API FastAPI données
      │       └── Dashboard Streamlit
      │
      └── Dataset IA
              │
              ▼
        data/modeling/
              │
              ▼
        Entraînement modèles ML
              │
              ▼
        models/substitution_model.joblib
              │
              ▼
        API FastAPI /predict
```

---

## 5. Structure du projet

```text
obrail-europe/
│
├── api/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── prediction.py
│
├── dashboard/
│   ├── app.py
│   └── visualisation.py
│
├── data/
│   ├── raw/
│   │   ├── back_on_track/
│   │   ├── sncf_gtfs/
│   │   ├── gares_voyageurs/
│   │   ├── wikipedia_busiest_stations_europe/
│   │   └── european_sleeper/
│   │
│   ├── processed/
│   │   ├── country.csv
│   │   ├── city.csv
│   │   ├── station.csv
│   │   ├── operator.csv
│   │   ├── train_type.csv
│   │   ├── data_source.csv
│   │   ├── route.csv
│   │   ├── trip.csv
│   │   ├── trip_stop.csv
│   │   └── quality_check.csv
│   │
│   ├── modeling/
│   │   ├── route_substitution_dataset.csv
│   │   ├── dataset_metadata.json
│   │   ├── train.csv
│   │   ├── validation.csv
│   │   ├── test.csv
│   │   └── split_metadata.json
│   │
│   └── predictions/
│       ├── sample_input.json
│       └── last_prediction.json
│
├── docs/
│   ├── api_prediction.md
│   ├── procedure_reentrainement.md
│   ├── dictionnaire_donnees.md
│   ├── choix_methodologiques.md
│   ├── RGPD.md
│   ├── inventaire_donnees_rgpd.md
│   └── registre_traitement.md
│
├── models/
│   ├── substitution_model.joblib
│   └── model_metrics.json
│
├── notebooks/
│   └── exploration_donnees.ipynb
│
├── reports/
│   ├── benchmark_services_ia.md
│   ├── veille_risques_limites_recommandations.md
│   ├── rapport_evaluation.md
│   ├── model_comparison.csv
│   ├── feature_importance.csv
│   └── figures/
│
├── scripts/
│   ├── extraction/
│   │   ├── extract_back_on_track.py
│   │   ├── extract_gtfs.py
│   │   ├── extract_gares_voyageurs.py
│   │   ├── extract_wikipedia_busiest_stations.py
│   │   └── extract_european_sleeper.py
│   │
│   ├── transformation/
│   │   ├── transform_all_sources.py
│   │   └── check_processed_data.py
│   │
│   ├── loading/
│   │   └── load_to_postgres.py
│   │
│   └── ml/
│       ├── build_dataset.py
│       ├── split_dataset.py
│       ├── train_models.py
│       ├── generate_evaluation_artifacts.py
│       └── predict.py
│
├── sql/
│   ├── create_tables.sql
│   └── test_queries.sql
│
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 6. Prérequis

Avant de lancer le projet, il faut avoir installé :

- Python 3.10 ou une version supérieure ;
- Docker et Docker Compose ;
- PostgreSQL si vous ne souhaitez pas utiliser Docker ;
- Git, optionnel mais recommandé.

Le projet utilise notamment :

| Technologie | Rôle |
|---|---|
| Python | Langage principal |
| pandas / numpy | Manipulation et analyse des données |
| requests | Téléchargement de sources externes |
| BeautifulSoup | Scraping HTML |
| PostgreSQL | Base relationnelle |
| psycopg2 | Connexion Python/PostgreSQL |
| FastAPI | API REST |
| Uvicorn | Serveur API |
| Streamlit | Dashboard interactif |
| Plotly / NetworkX / Matplotlib | Visualisations |
| scikit-learn | Modèles de machine learning |
| joblib | Sauvegarde du modèle |
| pytest | Tests automatisés |

---

## 7. Installation

### 7.1. Cloner ou ouvrir le projet

```bash
cd obrail-europe
```

### 7.2. Créer un environnement virtuel

Sous Windows :

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Sous macOS ou Linux :

```bash
python -m venv .venv
source .venv/bin/activate
```

### 7.3. Installer les dépendances

```bash
python -m pip install -r requirements.txt
```

### 7.4. Vérifier l’installation

```bash
python -c "import pandas, sklearn, joblib, fastapi, matplotlib; print('OK dépendances principales')"
```

---

## 8. Configuration

La configuration de la base de données est placée dans le fichier `.env`.

Exemple :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=obrail
DB_USER=postgres
DB_PASSWORD=postgres
```

Ces variables sont utilisées par :

- l’API FastAPI ;
- le dashboard Streamlit ;
- les scripts de connexion à PostgreSQL.

---

## 9. Lancement de PostgreSQL avec Docker

```bash
docker compose up -d
```

Pour vérifier que le conteneur est lancé :

```bash
docker ps
```

Pour arrêter PostgreSQL :

```bash
docker compose down
```

---

## 10. Pipeline ETL complet

### 10.1. Extraction des données brutes

Les scripts d’extraction téléchargent ou construisent les fichiers bruts dans `data/raw/`.

```bash
python scripts/extraction/extract_back_on_track.py
python scripts/extraction/extract_gtfs.py
python scripts/extraction/extract_gares_voyageurs.py
python scripts/extraction/extract_wikipedia_busiest_stations.py
python scripts/extraction/extract_european_sleeper.py
```

Chaque script d’extraction produit un dossier dédié à sa source et un fichier `metadata.json`.

---

### 10.2. Transformation des données

La transformation globale fusionne les sources et génère les fichiers normalisés dans `data/processed/`.

```bash
python scripts/transformation/transform_all_sources.py
```

Cette étape produit les fichiers CSV suivants :

```text
country.csv
city.csv
station.csv
operator.csv
train_type.csv
data_source.csv
route.csv
trip.csv
trip_stop.csv
quality_check.csv
```

---

### 10.3. Vérification des fichiers transformés

```bash
python scripts/transformation/check_processed_data.py
```

Ce script contrôle notamment :

- la présence des fichiers attendus ;
- le nombre de lignes et de colonnes ;
- les valeurs manquantes ;
- l’unicité des clés primaires ;
- la validité des clés étrangères ;
- la répartition des types de train ;
- les scores qualité.

---

### 10.4. Chargement dans PostgreSQL

```bash
python scripts/loading/load_to_postgres.py
```

Le script exécute d’abord `sql/create_tables.sql`, puis charge les fichiers dans l’ordre nécessaire pour respecter les relations entre les tables.

---

## 11. Modèle relationnel

Le modèle relationnel est organisé autour des principales entités ferroviaires :

| Table | Rôle |
|---|---|
| `country` | Pays |
| `city` | Villes rattachées aux pays |
| `station` | Gares rattachées aux villes |
| `operator` | Opérateurs ferroviaires |
| `train_type` | Type de train : `day` ou `night` |
| `data_source` | Sources de données intégrées |
| `route` | Relation entre une gare de départ et une gare d’arrivée |
| `trip` | Trajet ferroviaire |
| `trip_stop` | Arrêts intermédiaires d’un trajet |
| `quality_check` | Contrôles qualité appliqués aux trajets |

Les tables `route`, `trip` et `trip_stop` constituent le cœur métier du projet.

---

## 12. Contrôle qualité ETL

La table `quality_check` est générée pendant la transformation.

Les contrôles principaux sont :

- valeurs manquantes sur des champs essentiels ;
- durée invalide ou erreur horaire ;
- doublon potentiel sur le code du trajet.

Un score qualité est calculé sur 100 :

- départ à 100 ;
- retrait de points en cas d’anomalie ;
- score minimum limité à 0.

Ce score est ensuite réutilisé dans la partie IA afin d’éviter de recommander fortement des liaisons dont les données sont peu fiables.

---

## 13. Partie IA — Objectif

La partie IA vise à développer un modèle de classification permettant d’identifier les liaisons ferroviaires candidates à la substitution avion → train.

La cible du modèle est :

```text
substitution_potential
```

Elle contient trois classes :

```text
faible
moyen
fort
```

La solution IA repose sur les données harmonisées issues du pipeline ETL.

---

## 14. Création du dataset IA

Le dataset IA est généré par le script :

```bash
python scripts/ml/build_dataset.py
```

Ce script produit :

```text
data/modeling/route_substitution_dataset.csv
data/modeling/dataset_metadata.json
```

Dans la version actuelle, le dataset contient :

```text
4101 lignes
35 colonnes
0 valeur manquante critique
```

Chaque ligne représente une liaison ferroviaire enrichie avec des indicateurs géographiques, temporels, environnementaux et qualité.

---

## 15. Variables IA utilisées

Les principales variables utilisées pour l’entraînement sont :

| Variable | Description |
|---|---|
| `is_international` | Indique si la liaison est internationale |
| `distance_km` | Distance entre gare de départ et gare d’arrivée |
| `weekly_frequency` | Fréquence hebdomadaire estimée |
| `daily_frequency_avg` | Fréquence moyenne quotidienne |
| `avg_duration_minutes` | Durée moyenne du trajet |
| `min_duration_minutes` | Durée minimale observée |
| `max_duration_minutes` | Durée maximale observée |
| `has_night_train` | Présence d’un train de nuit |
| `has_day_train` | Présence d’un train de jour |
| `avg_num_stops` | Nombre moyen d’arrêts intermédiaires |
| `avg_quality_score` | Score qualité moyen |
| `quality_issues_count` | Nombre d’anomalies qualité |
| `co2_train_kg` | Émissions CO₂ estimées en train |
| `co2_plane_kg` | Émissions CO₂ estimées en avion |
| `co2_saving_kg` | Gain CO₂ estimé |
| `co2_saving_percent` | Pourcentage de réduction des émissions |

La variable `substitution_score` est utilisée pour construire la cible métier, mais elle est volontairement exclue de l’entraînement afin d’éviter une fuite de données.

---

## 16. Analyse exploratoire

L’analyse exploratoire est réalisée dans :

```text
notebooks/exploration_donnees.ipynb
```

Elle permet de vérifier :

- la taille du dataset ;
- la répartition de la cible ;
- les valeurs manquantes ;
- les distances nulles ou négatives ;
- les durées nulles ou négatives ;
- les fréquences nulles ou négatives ;
- la distribution des distances, durées, fréquences et gains CO₂ ;
- la cohérence des classes `faible`, `moyen` et `fort`.

Répartition actuelle de la cible :

```text
moyen     2919
faible     733
fort       449
```

---

## 17. Séparation train / validation / test

La séparation est effectuée avec :

```bash
python scripts/ml/split_dataset.py
```

Fichiers générés :

```text
data/modeling/train.csv
data/modeling/validation.csv
data/modeling/test.csv
data/modeling/split_metadata.json
```

Répartition actuelle :

```text
Train      : 2870 lignes
Validation : 615 lignes
Test       : 616 lignes
```

La séparation est stratifiée afin de conserver les proportions des classes dans chaque jeu.

---

## 18. Entraînement des modèles

L’entraînement et la comparaison des modèles sont réalisés avec :

```bash
python scripts/ml/train_models.py
```

Les modèles comparés sont :

| Modèle | Rôle |
|---|---|
| Logistic Regression | Modèle simple de référence |
| Decision Tree | Modèle explicable |
| Random Forest | Modèle robuste basé sur plusieurs arbres |
| Gradient Boosting | Modèle performant sur données tabulaires |

La métrique principale retenue est le `F1 macro`, car les classes ne sont pas parfaitement équilibrées.

---

## 19. Résultats du modèle final

Le meilleur modèle sélectionné est :

```text
gradient_boosting
```

Performances sur le jeu de test :

| Métrique | Valeur |
|---|---:|
| Accuracy | 0.9919 |
| Precision macro | 0.9805 |
| Recall macro | 0.9921 |
| F1 macro | 0.9861 |
| F1 weighted | 0.9920 |

Matrice de confusion sur le jeu de test :

| Classe réelle | Prédit faible | Prédit moyen | Prédit fort |
|---|---:|---:|---:|
| faible | 110 | 0 | 0 |
| moyen | 0 | 434 | 4 |
| fort | 0 | 1 | 67 |

Le modèle final est sauvegardé dans :

```text
models/substitution_model.joblib
```

Les métriques sont sauvegardées dans :

```text
models/model_metrics.json
reports/model_comparison.csv
reports/rapport_evaluation.md
```

---

## 20. Génération des artefacts d’évaluation

```bash
python scripts/ml/generate_evaluation_artifacts.py
```

Cette commande génère notamment :

```text
reports/rapport_evaluation.md
reports/feature_importance.csv
reports/figures/model_comparison_f1_macro.png
reports/figures/confusion_matrix.png
reports/figures/feature_importance.png
```

---

## 21. Prédiction locale

Le modèle sauvegardé peut être testé localement avec :

```bash
python scripts/ml/predict.py
```

Ou avec un fichier JSON :

```bash
python scripts/ml/predict.py --input data/predictions/sample_input.json
```

Exemple d’entrée :

```json
{
  "is_international": 1,
  "distance_km": 850.0,
  "weekly_frequency": 7.0,
  "daily_frequency_avg": 1.0,
  "avg_duration_minutes": 480.0,
  "min_duration_minutes": 450.0,
  "max_duration_minutes": 520.0,
  "has_night_train": 1,
  "has_day_train": 0,
  "avg_num_stops": 6.0,
  "avg_quality_score": 85.0,
  "quality_issues_count": 0,
  "co2_train_kg": 11.9,
  "co2_plane_kg": 195.5,
  "co2_saving_kg": 183.6,
  "co2_saving_percent": 93.9
}
```

Exemple de sortie :

```json
{
  "prediction": "fort",
  "probabilities": {
    "faible": 0.0,
    "fort": 1.0,
    "moyen": 0.0
  },
  "confidence": 1.0
}
```

---

## 22. API FastAPI

L’API permet d’interroger les données transformées chargées dans PostgreSQL et d’exposer le modèle IA.

### 22.1. Lancer l’API

```bash
python -m uvicorn api.main:app --reload
```

L’API est disponible à l’adresse :

```text
http://127.0.0.1:8000
```

La documentation interactive Swagger est disponible ici :

```text
http://127.0.0.1:8000/docs
```

---

### 22.2. Principaux endpoints ETL

| Endpoint | Description |
|---|---|
| `/` | Vérifie que l’API est lancée |
| `/health` | Vérifie la connexion entre l’API et PostgreSQL |
| `/tables/counts` | Retourne le nombre de lignes par table |
| `/train-types` | Liste les types de train |
| `/sources` | Liste les sources de données |
| `/countries` | Liste les pays |
| `/stations` | Liste les gares avec filtres |
| `/operators` | Liste les opérateurs |
| `/trips` | Liste les trajets avec filtres |
| `/trips/{trip_id}` | Retourne le détail d’un trajet |
| `/trips/{trip_id}/stops` | Retourne les arrêts d’un trajet |
| `/quality` | Retourne les contrôles qualité |
| `/stats/train-types` | Statistiques par type de train |
| `/stats/sources` | Statistiques par source |
| `/stats/quality` | Statistiques qualité globales |
| `/stats/stations-by-country` | Nombre de gares par pays |

---

### 22.3. Endpoints IA

| Endpoint | Méthode | Description |
|---|---|---|
| `/model-info` | GET | Retourne les informations du modèle chargé |
| `/predict` | POST | Prédit le potentiel de substitution avion → train |

---

### 22.4. Exemple d’appel `/predict`

```json
{
  "is_international": 1,
  "distance_km": 850.0,
  "weekly_frequency": 7.0,
  "daily_frequency_avg": 1.0,
  "avg_duration_minutes": 480.0,
  "min_duration_minutes": 450.0,
  "max_duration_minutes": 520.0,
  "has_night_train": 1,
  "has_day_train": 0,
  "avg_num_stops": 6.0,
  "avg_quality_score": 85.0,
  "quality_issues_count": 0,
  "co2_train_kg": 11.9,
  "co2_plane_kg": 195.5,
  "co2_saving_kg": 183.6,
  "co2_saving_percent": 93.9
}
```

Réponse attendue :

```json
{
  "prediction": "fort",
  "probabilities": {
    "faible": 0.0,
    "fort": 1.0,
    "moyen": 0.0
  },
  "confidence": 1.0
}
```

---

## 23. Dashboard Streamlit

Le dashboard permet de visualiser les données de manière interactive.

### 23.1. Lancer le dashboard

```bash
python -m streamlit run dashboard/app.py
```

Le dashboard s’ouvre ensuite dans le navigateur.

### 23.2. Pages du dashboard

Le dashboard est organisé en trois onglets :

| Page | Contenu |
|---|---|
| Vue exécutive | Indicateurs globaux, qualité, volumes, sources |
| Analyse transport | Opérateurs, types de trains, sources |
| Réseau ferroviaire | Graphe de connexions, filtres, exploration des trajets |

---

## 24. Ordre recommandé d’exécution depuis zéro

Pour exécuter l’ensemble du projet :

```bash
# 1. Lancer PostgreSQL
docker compose up -d

# 2. Extraction
python scripts/extraction/extract_back_on_track.py
python scripts/extraction/extract_gtfs.py
python scripts/extraction/extract_gares_voyageurs.py
python scripts/extraction/extract_wikipedia_busiest_stations.py
python scripts/extraction/extract_european_sleeper.py

# 3. Transformation et contrôle qualité ETL
python scripts/transformation/transform_all_sources.py
python scripts/transformation/check_processed_data.py

# 4. Chargement PostgreSQL
python scripts/loading/load_to_postgres.py

# 5. Dataset IA
python scripts/ml/build_dataset.py

# 6. Split train / validation / test
python scripts/ml/split_dataset.py

# 7. Entraînement et évaluation
python scripts/ml/train_models.py
python scripts/ml/generate_evaluation_artifacts.py

# 8. Test de prédiction locale
python scripts/ml/predict.py

# 9. API et dashboard
python -m uvicorn api.main:app --reload
python -m streamlit run dashboard/app.py
```

Il est conseillé de lancer l’API et le dashboard dans deux terminaux séparés.

---

## 25. Tests automatisés

Des tests automatisés ont été ajoutés afin de vérifier la qualité du dataset IA et le bon fonctionnement du modèle sauvegardé.

Les tests sont situés dans le dossier :

```text
tests/
```

Les fichiers de tests principaux sont :

```text
tests/test_dataset.py
tests/test_predict.py
```

### 25.1. Objectif des tests

Les tests permettent de vérifier automatiquement plusieurs points essentiels du projet IA :

- présence du dataset final ;
- présence des fichiers de métadonnées ;
- présence des colonnes obligatoires ;
- absence de valeurs manquantes sur les variables critiques ;
- contrôle des distances, durées et fréquences strictement positives ;
- présence des trois classes cibles : `faible`, `moyen`, `fort` ;
- présence des fichiers `train.csv`, `validation.csv` et `test.csv` ;
- bon chargement du modèle sauvegardé ;
- bon chargement des variables d’entrée du modèle ;
- vérification que `substitution_score` n’est pas utilisé comme variable d’entrée ;
- bon fonctionnement d’une prédiction locale ;
- cohérence des probabilités retournées par le modèle.

---

### 25.2. Lancer les tests

Depuis la racine du projet, exécuter :

```bash
pytest -q
```

Résultat obtenu dans la version actuelle :

```text
21 passed, 36 warnings in 9.00s
```

Les warnings observés proviennent de dépendances internes liées à `joblib` et `numpy`.  
Ils ne bloquent pas l’exécution du projet, car l’ensemble des tests passe correctement.

---

### 25.3. Tests sur le dataset

Le fichier :

```text
tests/test_dataset.py
```

vérifie notamment que :

- le fichier `data/modeling/route_substitution_dataset.csv` existe ;
- le fichier `data/modeling/dataset_metadata.json` existe ;
- les colonnes indispensables sont présentes ;
- les variables critiques ne contiennent pas de valeurs manquantes ;
- les distances sont strictement positives ;
- les durées sont strictement positives ;
- les fréquences sont strictement positives ;
- les classes `faible`, `moyen` et `fort` sont présentes ;
- les fichiers `train.csv`, `validation.csv` et `test.csv` existent ;
- les jeux train, validation et test ne sont pas vides.

---

### 25.4. Tests sur le modèle et la prédiction

Le fichier :

```text
tests/test_predict.py
```

vérifie notamment que :

- le fichier `models/substitution_model.joblib` existe ;
- le fichier `models/model_metrics.json` existe ;
- le modèle peut être chargé correctement ;
- les variables d’entrée du modèle sont bien récupérées ;
- la variable `substitution_score` est exclue des variables d’entrée ;
- l’exemple de prédiction par défaut est valide ;
- la prédiction retourne une classe parmi `faible`, `moyen` ou `fort` ;
- les probabilités retournées sont cohérentes ;
- le cas métier par défaut est classé en `fort`.

---

### 25.5. Intérêt pour le projet

Ces tests renforcent la fiabilité et la reproductibilité du projet.

Ils permettent de vérifier rapidement que le dataset, le modèle sauvegardé et le script de prédiction fonctionnent correctement après une modification du code, une mise à jour des données ou un ré-entraînement du modèle.

Cette étape contribue à la qualité technique du projet et prépare une future démarche MLOps.

---

## 26. Documentation disponible

| Document | Description |
|---|---|
| `docs/api_prediction.md` | Documentation de l’API IA `/predict` |
| `docs/procedure_reentrainement.md` | Procédure de ré-entraînement du modèle |
| `docs/dictionnaire_donnees.md` | Description des tables et variables IA |
| `docs/choix_methodologiques.md` | Justification des choix projet et modèles |
| `reports/benchmark_services_ia.md` | Benchmark des services IA existants |
| `reports/veille_risques_limites_recommandations.md` | Veille, risques, limites, biais et recommandations |
| `reports/rapport_evaluation.md` | Rapport d’évaluation du modèle final |
| `docs/RGPD.md` | Analyse RGPD simplifiée |
| `docs/inventaire_donnees_rgpd.md` | Inventaire des données |
| `docs/registre_traitement.md` | Registre de traitement |

---

## 27. Tests SQL

Le fichier `sql/test_queries.sql` contient des requêtes utiles pour vérifier le contenu de la base.

Exemples de contrôles possibles :

- compter les lignes par table ;
- vérifier les trajets de nuit ;
- inspecter les trajets European Sleeper ;
- contrôler les anomalies qualité ;
- vérifier les relations entre les trajets, les routes et les gares.

---

## 28. Problèmes fréquents

### PostgreSQL n’est pas connecté

```bash
docker ps
```

Puis relancer si nécessaire :

```bash
docker compose up -d
```

---

### Erreur de connexion à la base

Vérifier les variables du fichier `.env` :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=obrail
DB_USER=postgres
DB_PASSWORD=postgres
```

---

### Les tables sont vides

```bash
python scripts/loading/load_to_postgres.py
```

---

### Les fichiers `data/processed/` sont absents

```bash
python scripts/transformation/transform_all_sources.py
```

---

### Le module `sklearn` est introuvable

```bash
python -m pip install scikit-learn
```

Ou :

```bash
python -m pip install -r requirements.txt
```

---

### L’API ne trouve pas `api.prediction`

Vérifier que les fichiers suivants existent :

```text
api/__init__.py
api/prediction.py
```

Puis relancer :

```bash
python -m uvicorn api.main:app --reload
```

---

### Le modèle IA est introuvable

Vérifier que le fichier suivant existe :

```text
models/substitution_model.joblib
```

Sinon, relancer :

```bash
python scripts/ml/train_models.py
```

---

## 29. Limites connues

### 29.1. Limites ETL

- Les noms d’opérateurs sont conservés tels qu’ils apparaissent dans les sources.
- Certaines variantes d’un même opérateur peuvent apparaître séparément.
- Certaines sources peuvent changer de structure dans le temps.
- Le scraping Wikipedia dépend de la structure HTML de la page source.
- La couverture géographique dépend des sources disponibles.

### 29.2. Limites IA

- La cible `substitution_potential` est construite à partir d’un score métier, et non à partir de labels historiques réels.
- Le modèle apprend une logique d’aide à la décision, pas un comportement réel de voyageurs.
- Les estimations CO₂ reposent sur des facteurs simplifiés.
- Les données aériennes détaillées ne sont pas encore intégrées.
- Les données de fréquentation passagers ne sont pas encore intégrées.
- Le monitoring de production n’est pas encore mis en place.

---

## 30. Axes d’amélioration

### 30.1. Améliorations ETL

- Normaliser davantage les noms d’opérateurs.
- Historiser les extractions.
- Enrichir les contrôles qualité.
- Ajouter des contrôles sur les coordonnées GPS.
- Automatiser le pipeline avec Airflow, Prefect, cron ou GitHub Actions.

### 30.2. Améliorations IA

- Faire valider le score métier par des experts ObRail.
- Ajouter des données réelles de fréquentation.
- Ajouter des données aériennes concurrentes.
- Utiliser des facteurs CO₂ plus précis.
- Tester XGBoost ou LightGBM.
- Ajouter une optimisation d’hyperparamètres.
- Ajouter des logs de prédiction.
- Ajouter une route de prédiction à partir d’un `route_id`.
- Mettre en place un monitoring de dérive des données.
- Versionner automatiquement les modèles.

---

## 31. RGPD et éthique

Le projet ne traite pas de données personnelles.

Les données utilisées concernent principalement :

- des gares ;
- des villes ;
- des pays ;
- des opérateurs ;
- des trajets ;
- des horaires ;
- des indicateurs de qualité ;
- des estimations CO₂.

Une analyse RGPD simplifiée est disponible dans le dossier `docs/` :

```text
docs/RGPD.md
docs/inventaire_donnees_rgpd.md
docs/registre_traitement.md
```

La partie IA est présentée comme un outil d’aide à la décision. Elle ne doit pas être utilisée seule pour prendre des décisions publiques ou économiques importantes sans validation humaine.

---

## 32. Conclusion

ObRail Europe met en place une chaîne complète de traitement et d’exploitation de données ferroviaires :

```text
Extraction
→ Transformation
→ Contrôle qualité
→ Chargement PostgreSQL
→ API REST
→ Dashboard
→ Dataset IA
→ Entraînement de modèles
→ Évaluation
→ Sauvegarde
→ Prédiction locale
→ API /predict
```

Le projet montre comment passer de données brutes issues de sources hétérogènes à une solution exploitable combinant data engineering, machine learning, API et documentation.

La partie IA permet d’identifier les liaisons ferroviaires à potentiel de substitution avion → train, dans une logique de mobilité durable et de réduction des émissions CO₂.

Le modèle final retenu est un **Gradient Boosting**, exposé via FastAPI et sauvegardé avec `joblib`.
