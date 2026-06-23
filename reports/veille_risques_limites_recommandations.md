# Veille, risques, limites, biais et recommandations — Projet IA ObRail

## 1. Objectif de la section

Cette section présente les éléments de veille, les risques, les limites, les biais potentiels et les recommandations associés au modèle IA développé pour ObRail.

Le modèle vise à identifier les liaisons ferroviaires candidates à la substitution avion → train.

Il s’agit d’un prototype d’aide à la décision basé sur des données ferroviaires harmonisées et enrichies par des indicateurs métier, environnementaux et qualité.

---

## 2. Veille technique

### 2.1. Modèles de machine learning pour données tabulaires

Le projet repose sur des données tabulaires structurées : distance, durée, fréquence, type de train, score qualité, gain CO₂, etc.

Pour ce type de données, les modèles à base d’arbres sont généralement pertinents. Ils permettent de bien gérer les relations non linéaires entre variables et offrent une meilleure interprétabilité qu’un réseau de neurones complexe.

Les modèles comparés dans le projet sont :

```text
Logistic Regression
Decision Tree
Random Forest
Gradient Boosting
```

Le modèle final retenu est :

```text
Gradient Boosting
```

Ce choix est justifié par ses très bonnes performances sur le jeu de test et sa capacité à traiter efficacement des variables numériques issues d’un dataset tabulaire.

---

### 2.2. Pourquoi Gradient Boosting ?

Le Gradient Boosting combine plusieurs arbres de décision de manière séquentielle. Chaque nouvel arbre corrige les erreurs des arbres précédents.

Dans le cadre du projet ObRail, ce modèle présente plusieurs avantages :

* bonnes performances sur données tabulaires ;
* capacité à gérer des relations non linéaires ;
* bonne robustesse ;
* importance des variables exploitable ;
* meilleure performance que les modèles de référence testés.

Les résultats obtenus sur le jeu de test sont :

| Métrique        | Valeur |
| --------------- | -----: |
| Accuracy        | 0.9919 |
| Precision macro | 0.9805 |
| Recall macro    | 0.9921 |
| F1 macro        | 0.9861 |
| F1 weighted     | 0.9920 |

Le modèle réalise seulement 5 erreurs sur 616 exemples de test.

---

### 2.3. Veille sur les outils IA et MLOps

Plusieurs outils et approches ont été étudiés dans le cadre du benchmark :

| Solution               | Intérêt                                                     |
| ---------------------- | ----------------------------------------------------------- |
| Azure Machine Learning | Plateforme complète pour entraînement, déploiement et MLOps |
| AWS SageMaker          | Solution cloud robuste pour industrialiser des modèles ML   |
| Google Vertex AI       | AutoML et déploiement IA dans l’écosystème Google Cloud     |
| Hugging Face AutoTrain | Prototypage AutoML simplifié                                |
| IBM AutoAI             | Automatisation de pipelines IA orientée entreprise          |
| scikit-learn + FastAPI | Solution interne simple, maîtrisée et reproductible         |

Pour la version actuelle, le choix retenu est une solution interne open source :

```text
Python
pandas
scikit-learn
joblib
FastAPI
```

Cette solution est adaptée au contexte MSPR car elle est :

* simple à exécuter localement ;
* peu coûteuse ;
* reproductible ;
* documentée ;
* facilement présentable au jury ;
* cohérente avec le flux ETL déjà développé.

---

## 3. Veille réglementaire et éthique

### 3.1. RGPD

Le projet ne traite pas directement de données personnelles. Les données utilisées concernent principalement :

* des gares ;
* des villes ;
* des pays ;
* des trajets ferroviaires ;
* des horaires ;
* des types de trains ;
* des indicateurs de qualité ;
* des estimations CO₂.

Cependant, même sans données personnelles, il est important de respecter une démarche responsable :

* documentation des sources ;
* traçabilité des traitements ;
* minimisation des données utilisées ;
* justification des variables retenues ;
* transparence sur la méthode de création de la cible ;
* contrôle des résultats ;
* sécurisation de l’environnement projet.

---

### 3.2. IA Act européen

Le règlement européen sur l’intelligence artificielle introduit une approche fondée sur les risques.

Le modèle développé dans ce projet est un outil d’aide à l’analyse ferroviaire. Il ne prend pas de décision automatique sur des individus et ne manipule pas de données personnelles sensibles.

Le niveau de risque est donc limité dans le cadre actuel du prototype.

Cependant, si le modèle était utilisé plus tard pour orienter des décisions publiques importantes d’investissement ou d’aménagement du territoire, il faudrait renforcer :

* la documentation ;
* la gouvernance ;
* l’explicabilité ;
* la validation métier ;
* la supervision humaine ;
* le suivi des performances ;
* la gestion des biais territoriaux.

---

### 3.3. Principes d’IA digne de confiance

Le projet applique plusieurs principes d’IA responsable :

| Principe            | Application dans le projet                                                 |
| ------------------- | -------------------------------------------------------------------------- |
| Transparence        | Documentation du dataset, des variables, des règles et du modèle           |
| Robustesse          | Séparation train / validation / test et évaluation sur données non vues    |
| Supervision humaine | Le modèle est présenté comme une aide à la décision                        |
| Qualité des données | Contrôle des valeurs manquantes, distances, durées et fréquences           |
| Explicabilité       | Importance des variables et justification des critères métier              |
| Reproductibilité    | Scripts dédiés pour dataset, split, entraînement, évaluation et prédiction |
| Sécurité            | Modèle sauvegardé, API contrôlée, validation des entrées via FastAPI       |

---

## 4. Risques identifiés

### 4.1. Risque lié à la cible construite

Le principal risque méthodologique concerne la variable cible :

```text
substitution_potential
```

Cette cible n’existe pas directement dans les données sources. Elle a été construite à partir d’un score métier nommé :

```text
substitution_score
```

Ce score repose sur plusieurs critères :

* distance ;
* durée ;
* fréquence ;
* train de nuit ;
* gain CO₂ ;
* qualité des données ;
* caractère international.

Le risque est que le modèle apprenne à reproduire une logique métier construite, plutôt qu’une réalité historique observée.

Ce point doit être clairement présenté dans le rapport et à l’oral.

---

### 4.2. Risque de surinterprétation des résultats

Les performances du modèle sont très élevées.

Cela peut donner l’impression que le modèle est parfaitement fiable. Or, ces résultats doivent être interprétés avec prudence.

Le modèle apprend une classification issue d’un score métier. Il ne prédit pas encore un comportement réel de voyageurs ni un report modal observé entre avion et train.

Le risque serait de présenter les résultats comme une vérité opérationnelle définitive.

La bonne formulation est :

```text
Le modèle constitue un prototype d’aide à la décision permettant de prioriser les liaisons selon des critères ferroviaires et environnementaux.
```

---

### 4.3. Risque lié à la qualité des données

Le modèle dépend directement de la qualité du flux ETL.

Si les données sources sont incomplètes, mal harmonisées ou obsolètes, les prédictions peuvent être faussées.

Les risques principaux sont :

* coordonnées de gares manquantes ou incorrectes ;
* durées incohérentes ;
* fréquences mal estimées ;
* doublons de trajets ;
* erreurs de classification jour/nuit ;
* sources hétérogènes selon les pays ;
* couverture géographique inégale.

Pour limiter ce risque, un score qualité a été intégré dans le dataset IA.

---

### 4.4. Risque de biais géographique

Les données disponibles ne couvrent pas forcément tous les pays européens de manière équivalente.

Certaines zones peuvent être mieux représentées que d’autres, notamment si les sources utilisées sont plus riches pour certains pays ou opérateurs.

Cela peut créer un biais géographique :

* surreprésentation de la France ;
* sous-représentation de certaines zones d’Europe centrale ou orientale ;
* faible nombre de liaisons internationales ;
* faible visibilité de certains opérateurs.

Ce biais peut influencer le modèle et réduire sa généralisation à l’ensemble du réseau européen.

---

### 4.5. Risque de biais en faveur des liaisons fréquentes

La fréquence est un critère important dans le score métier.

Une liaison très fréquente a donc plus de chances d’être classée comme pertinente.

Cela est logique d’un point de vue opérationnel, mais peut pénaliser des liaisons émergentes ou stratégiques qui sont peu fréquentes aujourd’hui mais pourraient être développées demain.

Le modèle peut donc favoriser l’existant au détriment du potentiel futur.

---

### 4.6. Risque de biais en faveur des liaisons courtes ou moyennes

La substitution avion → train est particulièrement pertinente sur les distances intermédiaires.

Cependant, les longues distances peuvent aussi être intéressantes si elles disposent d’un train de nuit.

Il existe donc un risque de sous-évaluer certaines longues liaisons si les données sur les trains de nuit sont incomplètes.

---

### 4.7. Risque lié aux estimations CO₂

Les émissions CO₂ sont estimées à partir de facteurs simplifiés.

Ces estimations permettent d’intégrer une dimension environnementale, mais elles restent approximatives.

Les émissions réelles peuvent varier selon :

* le mix électrique du pays ;
* le type de train ;
* le taux d’occupation ;
* la distance réelle parcourue ;
* les correspondances ;
* les phases de décollage et d’atterrissage pour l’avion.

Le risque est donc de donner une précision apparente supérieure à la précision réelle.

---

### 4.8. Risque API

L’API `/predict` fonctionne avec des valeurs fournies en entrée.

Si l’utilisateur envoie des valeurs incohérentes mais techniquement valides, le modèle peut retourner une prédiction peu pertinente.

Exemple :

```text
distance très faible
durée irréaliste
fréquence anormalement élevée
CO₂ incohérent
```

FastAPI valide les types et certaines contraintes, mais ne garantit pas encore une cohérence métier complète.

---

### 4.9. Risque de dérive des données

En production, les données ferroviaires peuvent évoluer :

* nouvelles lignes ;
* nouveaux horaires ;
* nouvelles fréquences ;
* nouveaux trains de nuit ;
* modification des opérateurs ;
* fermeture temporaire de lignes ;
* changement des facteurs CO₂.

Si le modèle n’est pas réentraîné régulièrement, ses prédictions peuvent devenir moins fiables.

---

## 5. Limites actuelles du projet

### 5.1. Absence de labels réels

La limite principale est l’absence de données historiques indiquant réellement si une liaison aérienne a été remplacée par une liaison ferroviaire.

Le modèle utilise donc une cible construite à partir d’une logique métier.

Cette approche est acceptable pour un prototype, mais une version industrielle devrait intégrer des labels validés par des experts ou des données réelles de report modal.

---

### 5.2. Absence de données passagers

Le modèle ne tient pas compte de la fréquentation réelle des liaisons.

Il ne sait pas si une liaison est très utilisée ou peu utilisée par les voyageurs.

Cela limite la capacité du modèle à prédire l’impact réel d’une substitution avion → train.

---

### 5.3. Absence de données aériennes détaillées

Le modèle ne compare pas directement les liaisons ferroviaires à des vols réels.

Il ne prend pas en compte :

* le nombre de vols ;
* les aéroports concernés ;
* le prix des billets ;
* la durée totale porte-à-porte ;
* les temps de sécurité et d’embarquement ;
* les correspondances aériennes.

Cela limite la précision de l’analyse de concurrence train/avion.

---

### 5.4. Estimation simplifiée de la distance

La distance est calculée principalement à partir des coordonnées géographiques des gares.

Il s’agit d’une distance approximative, qui peut différer de la distance ferroviaire réelle parcourue.

---

### 5.5. Estimation simplifiée des émissions CO₂

Les émissions CO₂ sont calculées à partir de facteurs simplifiés.

Elles donnent un ordre de grandeur utile, mais ne remplacent pas un calcul carbone complet.

---

### 5.6. Modèle non encore monitoré

L’API expose le modèle, mais aucun système de monitoring complet n’est encore mis en place.

Il manque notamment :

* logs des prédictions ;
* suivi du temps de réponse ;
* suivi des erreurs API ;
* suivi des distributions des variables ;
* détection de dérive des données ;
* suivi de la performance réelle après déploiement.

---

### 5.7. Pas encore d’optimisation avancée des hyperparamètres

Les modèles ont été comparés avec des paramètres raisonnables, mais une recherche d’hyperparamètres plus poussée pourrait améliorer ou confirmer les performances.

Des méthodes comme GridSearchCV ou RandomizedSearchCV pourraient être ajoutées dans une version ultérieure.

---

## 6. Biais potentiels

### 6.1. Biais de couverture des sources

Le dataset dépend des sources intégrées dans l’ETL.

Si certains pays, opérateurs ou types de trains sont moins présents, le modèle sera moins représentatif pour ces cas.

---

### 6.2. Biais de disponibilité des données

Les liaisons avec des données plus complètes peuvent être mieux évaluées que les liaisons avec des données partielles.

Cela peut favoriser les opérateurs ou pays qui publient des données plus propres et plus détaillées.

---

### 6.3. Biais du score métier

Le score métier reflète les choix de pondération définis dans le projet.

Par exemple, accorder beaucoup de poids à la fréquence favorise les lignes déjà bien desservies.

Accorder beaucoup de poids au CO₂ favorise les longues distances avec fort gain environnemental.

Ces choix sont justifiables, mais doivent être documentés et idéalement validés par des experts métier.

---

### 6.4. Biais temporel

Les données utilisées correspondent à une période donnée.

Les horaires et fréquences ferroviaires peuvent changer selon les saisons, les travaux, les politiques d’offre ou les évolutions commerciales.

Un modèle entraîné sur une période donnée peut devenir moins pertinent dans le temps.

---

### 6.5. Biais d’interprétation

Une classe `fort` ne signifie pas automatiquement qu’une liaison doit être financée ou développée.

Elle signifie seulement que, selon les critères du modèle, la liaison présente un fort potentiel de substitution.

La décision finale doit rester humaine et intégrer d’autres critères :

* coût d’investissement ;
* faisabilité infrastructurelle ;
* demande réelle ;
* politique publique ;
* acceptabilité sociale ;
* contraintes transfrontalières.

---

## 7. Mesures déjà mises en place

Plusieurs mesures ont été mises en place pour réduire les risques.

### 7.1. Contrôle qualité des données

Les données ont été contrôlées avant l’entraînement :

```text
valeurs manquantes critiques : 0
distances <= 0 : 0
durées <= 0 : 0
fréquences <= 0 : 0
```

Une liaison incohérente avec une distance de 0 km a été supprimée.

---

### 7.2. Séparation train / validation / test

Le dataset a été séparé en trois jeux :

```text
train
validation
test
```

Cette séparation permet d’évaluer le modèle sur des données non vues pendant l’entraînement.

---

### 7.3. Séparation stratifiée

La séparation est stratifiée afin de conserver les proportions des classes dans chaque jeu.

Cela permet une évaluation plus fiable, notamment pour les classes minoritaires.

---

### 7.4. Exclusion de `substitution_score`

La variable `substitution_score` a été exclue de l’entraînement.

Cette décision évite une fuite de données, car la cible `substitution_potential` est construite à partir de ce score.

---

### 7.5. Comparaison de plusieurs modèles

Plusieurs modèles ont été testés :

```text
Logistic Regression
Decision Tree
Random Forest
Gradient Boosting
```

Cette comparaison permet de justifier le choix du modèle final.

---

### 7.6. Documentation

Plusieurs documents ont été produits :

```text
docs/api_prediction.md
docs/procedure_reentrainement.md
docs/dictionnaire_donnees.md
docs/choix_methodologiques.md
reports/benchmark_services_ia.md
reports/rapport_evaluation.md
```

Cette documentation renforce la transparence et la reproductibilité.

---

### 7.7. API contrôlée

L’API FastAPI valide les types et certaines contraintes d’entrée :

* distance strictement positive ;
* durée strictement positive ;
* fréquence strictement positive ;
* score qualité entre 0 et 100 ;
* variables binaires limitées à 0 ou 1.

---

## 8. Recommandations techniques

### 8.1. Ajouter une route de prédiction par `route_id`

Actuellement, l’API `/predict` attend toutes les variables en entrée.

Une amélioration importante serait d’ajouter une route :

```text
POST /predict/{route_id}
```

ou :

```text
GET /routes/{route_id}/prediction
```

Cette route récupérerait automatiquement les variables depuis PostgreSQL avant d’appeler le modèle.

---

### 8.2. Ajouter des logs de prédiction

Il est recommandé d’enregistrer chaque prédiction dans une table ou un fichier de logs.

Les informations à conserver sont :

| Élément            | Description                  |
| ------------------ | ---------------------------- |
| Date de prédiction | Moment de l’appel API        |
| Données d’entrée   | Variables envoyées au modèle |
| Prédiction         | Classe retournée             |
| Probabilités       | Probabilités par classe      |
| Confiance          | Score de confiance           |
| Version du modèle  | Modèle utilisé               |
| Temps de réponse   | Durée de traitement          |

Ces logs permettraient d’alimenter une boucle de retour et de préparer le monitoring.

---

### 8.3. Ajouter un monitoring des données

Il est recommandé de suivre les distributions des variables principales :

```text
distance_km
avg_duration_minutes
weekly_frequency
co2_saving_kg
avg_quality_score
```

Si les distributions changent fortement, cela peut indiquer une dérive des données.

---

### 8.4. Versionner les modèles

Chaque modèle sauvegardé devrait être versionné.

Exemple :

```text
substitution_model_2026_01.joblib
model_metrics_2026_01.json
```

Cela permettrait de revenir à une version précédente en cas de problème.

---

### 8.5. Automatiser le ré-entraînement

La procédure de ré-entraînement est documentée, mais elle reste manuelle.

Une amélioration future serait d’automatiser le pipeline :

```text
build_dataset.py
split_dataset.py
train_models.py
generate_evaluation_artifacts.py
tests API
déploiement
```

---

### 8.6. Ajouter des tests unitaires

Des tests unitaires pourraient être ajoutés sur :

* calcul des distances ;
* création du score métier ;
* création de la cible ;
* absence de valeurs manquantes ;
* format du dataset ;
* chargement du modèle ;
* route API `/predict`.

---

## 9. Recommandations métier

### 9.1. Faire valider le score par des experts ObRail

Le score métier doit être présenté à des experts du ferroviaire.

Ils pourront valider ou ajuster :

* les seuils de distance ;
* les seuils de durée ;
* le poids de la fréquence ;
* le poids des trains de nuit ;
* le poids du gain CO₂ ;
* le rôle du caractère international.

---

### 9.2. Ajouter des données de demande réelle

Pour améliorer la pertinence métier, il faudrait ajouter des données de fréquentation :

* nombre de voyageurs par liaison ;
* évolution de la demande ;
* taux d’occupation ;
* saisonnalité ;
* demande transfrontalière.

Ces données permettraient de mieux estimer le potentiel réel de report modal.

---

### 9.3. Ajouter des données aériennes

Le modèle serait plus complet avec des données sur les vols concurrents :

* existence d’une liaison aérienne équivalente ;
* nombre de vols hebdomadaires ;
* durée du vol ;
* temps moyen porte-à-porte ;
* émissions CO₂ aériennes plus précises ;
* prix moyen.

Cela permettrait de comparer plus directement train et avion.

---

### 9.4. Ajouter des critères socio-économiques

Certaines liaisons peuvent être stratégiques même si leur potentiel actuel semble moyen.

Il serait utile d’ajouter :

* population des villes ;
* attractivité économique ;
* tourisme ;
* présence d’universités ;
* bassins d’emploi ;
* politiques publiques locales.

---

### 9.5. Utiliser le modèle comme outil d’aide, pas comme décision automatique

Le modèle ne doit pas décider seul.

Il doit aider à prioriser les analyses, mais la décision finale doit rester humaine.

La recommandation est donc d’utiliser le modèle comme un outil d’aide à la décision pour :

* identifier des liaisons prometteuses ;
* alimenter des études ;
* orienter les analyses environnementales ;
* préparer des recommandations politiques.

---

## 10. Recommandations réglementaires et éthiques

### 10.1. Maintenir la transparence

Chaque prédiction doit pouvoir être expliquée.

Il est recommandé de fournir au moins :

* la classe prédite ;
* la probabilité associée ;
* les principales variables ayant influencé le modèle ;
* les limites de la prédiction.

---

### 10.2. Garder une documentation à jour

La documentation doit être mise à jour à chaque évolution :

* nouvelle source de données ;
* changement de règles métier ;
* modification des facteurs CO₂ ;
* changement de modèle ;
* nouvelle version API.

---

### 10.3. Renforcer la gouvernance

Avant une mise en production, ObRail devrait définir :

* qui valide les données ;
* qui valide les modèles ;
* qui autorise un nouveau déploiement ;
* qui surveille les performances ;
* qui peut consulter les prédictions ;
* qui est responsable en cas d’erreur.

---

### 10.4. Éviter les décisions automatisées non supervisées

Le modèle ne doit pas être utilisé seul pour prendre des décisions publiques ou économiques importantes.

Les résultats doivent être interprétés par des experts et croisés avec d’autres analyses.

---

## 11. Plan d’amélioration priorisé

| Priorité | Action                                   | Objectif                             |
| -------- | ---------------------------------------- | ------------------------------------ |
| Haute    | Valider le score métier avec des experts | Réduire le risque méthodologique     |
| Haute    | Ajouter des logs de prédiction           | Préparer le monitoring               |
| Haute    | Versionner les modèles                   | Sécuriser les déploiements           |
| Haute    | Ajouter une route par `route_id`         | Faciliter l’intégration applicative  |
| Moyenne  | Ajouter des données aériennes            | Améliorer la comparaison train/avion |
| Moyenne  | Ajouter des données de fréquentation     | Améliorer la pertinence métier       |
| Moyenne  | Ajouter un monitoring de dérive          | Suivre la stabilité du modèle        |
| Moyenne  | Optimiser les hyperparamètres            | Confirmer les performances           |
| Basse    | Tester des modèles XGBoost / LightGBM    | Comparer avec des modèles avancés    |
| Basse    | Déploiement cloud                        | Industrialisation future             |

---

## 12. Conclusion

Le projet ObRail propose une première solution IA complète permettant de classifier les liaisons ferroviaires selon leur potentiel de substitution avion → train.

La solution est techniquement fonctionnelle :

```text
dataset IA généré
analyse exploratoire réalisée
modèles comparés
modèle final sauvegardé
prédiction locale opérationnelle
API REST fonctionnelle
documentation produite
```

Les principaux risques concernent surtout :

* la cible métier construite ;
* la couverture inégale des données ;
* les estimations CO₂ simplifiées ;
* l’absence de labels réels ;
* l’absence de monitoring en production.

Ces limites sont acceptables pour une première version, à condition de présenter le modèle comme un prototype d’aide à la décision.

La priorité pour une version future est de faire valider les règles métier par des experts ObRail, d’ajouter des données réelles de demande et de mettre en place un monitoring des prédictions.
