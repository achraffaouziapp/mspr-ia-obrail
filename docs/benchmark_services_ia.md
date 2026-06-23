# Benchmark des services d’intelligence artificielle — Projet ObRail

## 1. Objectif du benchmark

Dans le cadre du projet IA ObRail, un benchmark de services d’intelligence artificielle a été réalisé afin de comparer plusieurs solutions permettant de développer, entraîner, déployer ou automatiser des modèles de machine learning.

L’objectif est de déterminer si ObRail doit :

* utiliser un service IA cloud ou AutoML existant ;
* conserver un modèle interne développé avec Python et scikit-learn ;
* adopter une approche hybride combinant développement interne et services cloud.

Le cas d’usage étudié est le suivant :

```text
Identifier les liaisons ferroviaires candidates à la substitution avion → train.
```

La tâche correspond à une classification multiclasses :

```text
faible
moyen
fort
```

---

## 2. Services comparés

Les services étudiés sont :

| Service                               | Fournisseur            | Type                          |
| ------------------------------------- | ---------------------- | ----------------------------- |
| Azure Machine Learning                | Microsoft Azure        | Plateforme ML / MLOps         |
| Amazon SageMaker Autopilot            | AWS                    | AutoML / Plateforme ML        |
| Google Vertex AI AutoML               | Google Cloud           | AutoML / Plateforme ML        |
| Hugging Face AutoTrain                | Hugging Face           | AutoML simplifié              |
| IBM Watson Studio AutoAI / watsonx.ai | IBM                    | AutoML / Plateforme IA        |
| Modèle interne open source            | ObRail / équipe projet | Python, scikit-learn, FastAPI |

---

## 3. Critères d’évaluation

Les services sont comparés selon les critères suivants :

| Critère                   | Description                                                        |
| ------------------------- | ------------------------------------------------------------------ |
| Adaptation au cas d’usage | Pertinence pour une classification tabulaire                       |
| Facilité d’intégration    | Simplicité d’utilisation dans le projet ObRail                     |
| Coût                      | Niveau de coût estimé pour un prototype et une mise en production  |
| Explicabilité             | Possibilité de comprendre les résultats du modèle                  |
| Contrôle technique        | Maîtrise du code, des données et du pipeline                       |
| Reproductibilité          | Capacité à rejouer le pipeline d’entraînement                      |
| MLOps                     | Fonctionnalités de suivi, déploiement, versionnement et monitoring |
| RGPD / gouvernance        | Maîtrise des données et conformité                                 |
| Pertinence pour ObRail    | Intérêt concret dans le contexte du projet                         |

---

## 4. Azure Machine Learning

### 4.1. Présentation

Azure Machine Learning est une plateforme cloud proposée par Microsoft. Elle permet de développer, entraîner, déployer et superviser des modèles de machine learning.

Elle propose notamment :

* des notebooks ;
* des environnements de calcul ;
* des pipelines ML ;
* des fonctionnalités AutoML ;
* du suivi d’expériences ;
* du déploiement de modèles ;
* des fonctionnalités MLOps.

---

### 4.2. Avantages

| Avantage               | Explication                                         |
| ---------------------- | --------------------------------------------------- |
| Plateforme complète    | Azure ML couvre l’ensemble du cycle de vie ML       |
| Bon niveau MLOps       | Suivi des expériences, versionnement, déploiement   |
| Intégration entreprise | Bonne intégration avec l’écosystème Microsoft       |
| AutoML disponible      | Permet de tester rapidement plusieurs modèles       |
| Déploiement API        | Possibilité de déployer des endpoints de prédiction |

---

### 4.3. Limites

| Limite                     | Explication                                               |
| -------------------------- | --------------------------------------------------------- |
| Coût variable              | Le coût dépend des ressources cloud consommées            |
| Complexité initiale        | La prise en main peut être plus longue qu’un script local |
| Dépendance cloud           | Le projet dépend de l’écosystème Azure                    |
| Surdimensionné pour une V1 | Trop complet pour un prototype académique simple          |

---

### 4.4. Pertinence pour ObRail

Azure Machine Learning serait pertinent si ObRail souhaite industrialiser fortement la solution avec :

* plusieurs modèles ;
* plusieurs équipes data ;
* un besoin de monitoring avancé ;
* une infrastructure cloud déjà présente sur Azure.

Pour la version actuelle du projet, Azure ML est intéressant comme référence industrielle, mais il n’est pas indispensable.

---

## 5. Amazon SageMaker Autopilot

### 5.1. Présentation

Amazon SageMaker est la plateforme machine learning d’AWS. SageMaker Autopilot permet d’automatiser une partie du développement de modèles à partir de données tabulaires.

Il peut aider à :

* préparer les données ;
* tester plusieurs algorithmes ;
* optimiser des modèles ;
* déployer des endpoints ;
* suivre les expériences.

---

### 5.2. Avantages

| Avantage               | Explication                                            |
| ---------------------- | ------------------------------------------------------ |
| Plateforme robuste     | Service cloud mature pour le machine learning          |
| AutoML disponible      | SageMaker Autopilot automatise la recherche de modèles |
| Déploiement scalable   | Déploiement possible sous forme d’endpoint             |
| Intégration AWS        | Compatible avec S3, IAM, CloudWatch, Lambda            |
| Adapté à la production | Bon choix pour une architecture cloud complète         |

---

### 5.3. Limites

| Limite                     | Explication                                      |
| -------------------------- | ------------------------------------------------ |
| Coût potentiellement élevé | Coûts liés au calcul, stockage et endpoints      |
| Complexité AWS             | Nécessite une bonne maîtrise de l’écosystème AWS |
| Surdimensionné pour une V1 | Trop lourd pour un prototype local               |
| Dépendance fournisseur     | Verrouillage partiel dans l’écosystème AWS       |

---

### 5.4. Pertinence pour ObRail

SageMaker Autopilot est pertinent si ObRail dispose déjà d’une infrastructure AWS ou souhaite une solution industrialisée cloud.

Pour le projet actuel, il est intéressant pour comparer les capacités AutoML, mais le modèle interne reste plus simple, moins coûteux et plus maîtrisable.

---

## 6. Google Vertex AI AutoML

### 6.1. Présentation

Google Vertex AI est la plateforme IA de Google Cloud. Elle propose des fonctionnalités d’entraînement personnalisé, d’AutoML, de déploiement et de monitoring.

Vertex AI AutoML est adapté aux données tabulaires, images, texte et autres formats selon les modules utilisés.

---

### 6.2. Avantages

| Avantage                 | Explication                                             |
| ------------------------ | ------------------------------------------------------- |
| AutoML performant        | Bon niveau d’automatisation pour données tabulaires     |
| Plateforme unifiée       | Centralise entraînement, déploiement et monitoring      |
| Intégration Google Cloud | Compatible avec BigQuery, Cloud Storage et services GCP |
| Déploiement API          | Possibilité de créer des endpoints de prédiction        |
| Expérimentation rapide   | Permet de tester rapidement plusieurs modèles           |

---

### 6.3. Limites

| Limite                               | Explication                                                          |
| ------------------------------------ | -------------------------------------------------------------------- |
| Coût cloud                           | Facturation liée à l’entraînement, au déploiement et aux prédictions |
| Dépendance GCP                       | Nécessite un environnement Google Cloud                              |
| Moins transparent qu’un modèle local | AutoML peut rendre certains choix moins visibles                     |
| Complexité de gouvernance            | Les données doivent être envoyées ou stockées sur GCP                |

---

### 6.4. Pertinence pour ObRail

Vertex AI AutoML serait pertinent si ObRail souhaite automatiser une partie de la modélisation et dispose déjà de données centralisées sur Google Cloud.

Pour la version actuelle, l’approche interne reste plus adaptée car elle donne plus de contrôle sur la création de la cible, les règles métier et l’API.

---

## 7. Hugging Face AutoTrain

### 7.1. Présentation

Hugging Face AutoTrain est un outil permettant d’entraîner des modèles avec peu ou pas de code.

Il est surtout connu pour les usages liés au NLP et aux modèles open source, mais il peut aussi être utilisé pour certaines tâches tabulaires selon les configurations.

---

### 7.2. Avantages

| Avantage                        | Explication                                     |
| ------------------------------- | ----------------------------------------------- |
| Simple à utiliser               | Interface no-code ou low-code                   |
| Open source                     | Approche plus ouverte que les grands clouds     |
| Rapide pour prototypage         | Permet de tester rapidement une approche AutoML |
| Bonne intégration Hugging Face  | Compatible avec l’écosystème Hugging Face       |
| Moins lourd qu’un cloud complet | Plus simple que SageMaker ou Azure ML           |

---

### 7.3. Limites

| Limite                        | Explication                                              |
| ----------------------------- | -------------------------------------------------------- |
| Moins orienté MLOps complet   | Moins complet pour monitoring, gouvernance et production |
| Moins adapté au besoin ObRail | Le projet est principalement tabulaire et métier         |
| Personnalisation limitée      | Moins de contrôle qu’un pipeline Python interne          |
| Coût selon ressources         | Le coût dépend des ressources utilisées                  |

---

### 7.4. Pertinence pour ObRail

Hugging Face AutoTrain peut être utile pour un prototype rapide ou pour comparer une approche AutoML simple.

Cependant, pour ObRail, le besoin principal est de maîtriser les règles métier, la donnée ferroviaire, la cible construite et l’intégration API. Le modèle interne est donc plus adapté.

---

## 8. IBM Watson Studio AutoAI / watsonx.ai

### 8.1. Présentation

IBM Watson Studio AutoAI, intégré dans l’écosystème IBM watsonx.ai, permet d’automatiser plusieurs étapes de création de modèles :

* préparation des données ;
* feature engineering ;
* choix d’algorithmes ;
* optimisation ;
* comparaison de pipelines ;
* déploiement.

---

### 8.2. Avantages

| Avantage              | Explication                                            |
| --------------------- | ------------------------------------------------------ |
| AutoAI complet        | Automatisation de nombreuses étapes ML                 |
| Gouvernance IA        | IBM met l’accent sur la gouvernance et l’explicabilité |
| Adapté entreprise     | Solution pensée pour des contextes professionnels      |
| Pipelines comparables | Permet de comparer plusieurs modèles automatiquement   |
| Intégration ModelOps  | Intéressant pour une industrialisation avancée         |

---

### 8.3. Limites

| Limite                           | Explication                                      |
| -------------------------------- | ------------------------------------------------ |
| Coût potentiellement élevé       | Solution orientée entreprise                     |
| Complexité d’écosystème          | Nécessite une prise en main IBM Cloud / watsonx  |
| Surdimensionné pour le prototype | Trop complet pour une V1 académique              |
| Dépendance fournisseur           | Dépendance à IBM Cloud ou IBM Cloud Pak for Data |

---

### 8.4. Pertinence pour ObRail

IBM AutoAI est pertinent pour une organisation qui recherche une plateforme complète avec gouvernance, automatisation et suivi.

Pour la version actuelle du projet, cette solution est trop lourde par rapport au besoin. Elle peut être envisagée plus tard si ObRail souhaite une plateforme IA d’entreprise.

---

## 9. Modèle interne open source

### 9.1. Présentation

Le projet actuel utilise une approche interne basée sur des outils open source :

```text
Python
pandas
scikit-learn
joblib
FastAPI
Matplotlib
```

Le pipeline développé comprend :

```text
ETL existant
→ Dataset IA
→ Split train / validation / test
→ Entraînement de plusieurs modèles
→ Évaluation
→ Sauvegarde du modèle
→ Script predict.py
→ API REST /predict
```

---

### 9.2. Avantages

| Avantage               | Explication                                       |
| ---------------------- | ------------------------------------------------- |
| Coût faible            | Pas de coût cloud obligatoire pour la V1          |
| Maîtrise complète      | Contrôle total sur les données, règles et modèles |
| Reproductibilité       | Pipeline scripté et documenté                     |
| Transparence           | Choix méthodologiques explicites                  |
| Facilité d’intégration | API FastAPI déjà fonctionnelle                    |
| Adapté au projet       | Répond directement au besoin ObRail               |
| RGPD facilité          | Données conservées dans l’environnement projet    |
| Valorisation du MSPR 1 | Réutilisation directe du flux ETL existant        |

---

### 9.3. Limites

| Limite                  | Explication                                           |
| ----------------------- | ----------------------------------------------------- |
| Moins industrialisé     | Pas encore de plateforme MLOps complète               |
| Monitoring limité       | Pas encore de suivi automatique en production         |
| Maintenance interne     | L’équipe doit maintenir les scripts et l’API          |
| Scalabilité à prévoir   | Besoin d’adaptation pour une mise en production large |
| Gouvernance à renforcer | Versionnement et suivi des modèles à améliorer        |

---

### 9.4. Pertinence pour ObRail

Le modèle interne est le choix le plus pertinent pour cette première version.

Il permet de répondre au besoin avec une solution :

* simple ;
* maîtrisée ;
* documentée ;
* reproductible ;
* peu coûteuse ;
* adaptée aux données disponibles ;
* facilement démontrable devant un jury ou un client.

---

## 10. Tableau comparatif global

| Critère                       |      Azure ML | AWS SageMaker |     Vertex AI | Hugging Face AutoTrain |    IBM AutoAI | Modèle interne |
| ----------------------------- | ------------: | ------------: | ------------: | ---------------------: | ------------: | -------------: |
| Classification tabulaire      |      Très bon |      Très bon |      Très bon |            Moyen à bon |      Très bon |       Très bon |
| Facilité de démarrage         |       Moyenne |       Moyenne |       Moyenne |                  Bonne |       Moyenne |          Bonne |
| Coût V1                       | Moyen à élevé | Moyen à élevé | Moyen à élevé |         Faible à moyen | Moyen à élevé |         Faible |
| Contrôle du code              |         Moyen |         Moyen |         Moyen |                  Moyen |         Moyen |       Très bon |
| Explicabilité                 |         Bonne |         Bonne |         Bonne |                Moyenne |         Bonne |          Bonne |
| MLOps                         |      Très bon |      Très bon |      Très bon |                  Moyen |      Très bon |        Basique |
| Intégration API               |         Bonne |         Bonne |         Bonne |                Moyenne |         Bonne |     Très bonne |
| RGPD / maîtrise des données   |    À encadrer |    À encadrer |    À encadrer |             À encadrer |    À encadrer |       Très bon |
| Adapté au prototype MSPR      |         Moyen |         Moyen |         Moyen |                    Bon |         Moyen |       Très bon |
| Adapté à une production large |      Très bon |      Très bon |      Très bon |                  Moyen |      Très bon |    À renforcer |

---

## 11. Analyse selon le contexte ObRail

### 11.1. Données disponibles

ObRail dispose déjà d’un flux ETL produisant des données harmonisées.

Cela favorise une approche interne, car les données sont déjà structurées et prêtes à être transformées en dataset IA.

---

### 11.2. Besoin métier

Le besoin métier nécessite une forte transparence.

La cible `substitution_potential` est construite à partir d’un score métier. Il est donc important de pouvoir expliquer :

* pourquoi une liaison est classée en `faible` ;
* pourquoi une liaison est classée en `moyen` ;
* pourquoi une liaison est classée en `fort`.

Une solution interne facilite cette explicabilité.

---

### 11.3. Contraintes de coût

Pour une première version, l’usage d’un service cloud complet peut générer des coûts inutiles.

Le modèle interne permet de limiter les coûts tout en répondant aux exigences du projet.

---

### 11.4. Contraintes de reproductibilité

Le pipeline interne est entièrement scripté :

```text
build_dataset.py
split_dataset.py
train_models.py
generate_evaluation_artifacts.py
predict.py
```

Cela permet de relancer l’ensemble du processus sans dépendre d’une interface cloud.

---

### 11.5. Contraintes RGPD et gouvernance

Le projet ne manipule pas de données personnelles.

Cependant, la conservation des données dans l’environnement projet facilite :

* la traçabilité ;
* la maîtrise des traitements ;
* la documentation ;
* la conformité.

L’usage d’un cloud public nécessiterait une analyse plus complète sur l’hébergement, la localisation des données, les accès et la sécurité.

---

## 12. Recommandation finale

Pour la première version du projet ObRail, la recommandation est de conserver l’approche suivante :

```text
Modèle interne open source avec Python, scikit-learn, joblib et FastAPI.
```

Cette approche est la plus pertinente car elle offre :

* une forte maîtrise technique ;
* une bonne transparence ;
* un coût faible ;
* une intégration simple ;
* une bonne reproductibilité ;
* une cohérence avec le flux ETL existant ;
* une API déjà fonctionnelle.

Le service IA cloud n’est donc pas retenu pour la V1.

---

## 13. Positionnement des services cloud pour la suite

Même si les services cloud ne sont pas retenus pour la V1, ils restent intéressants pour une future industrialisation.

### 13.1. Azure Machine Learning

À envisager si ObRail adopte une infrastructure Microsoft Azure et souhaite mettre en place une chaîne MLOps complète.

### 13.2. AWS SageMaker

À envisager si ObRail travaille déjà sur AWS et souhaite industrialiser l’entraînement, le déploiement et le monitoring des modèles.

### 13.3. Google Vertex AI

À envisager si ObRail centralise ses données dans BigQuery ou Google Cloud Storage.

### 13.4. Hugging Face AutoTrain

À envisager pour des prototypes rapides ou pour des projets NLP complémentaires.

### 13.5. IBM AutoAI

À envisager pour une organisation recherchant une plateforme d’entreprise avec gouvernance et ModelOps.

---

## 14. Décision retenue

La décision retenue est :

| Élément                        | Décision                              |
| ------------------------------ | ------------------------------------- |
| Solution principale V1         | Modèle interne open source            |
| Bibliothèque ML                | scikit-learn                          |
| Modèle final                   | Gradient Boosting                     |
| Sauvegarde                     | joblib                                |
| API                            | FastAPI                               |
| Déploiement cloud immédiat     | Non                                   |
| Services cloud                 | Non retenus pour la V1                |
| Usage futur des services cloud | Possible pour industrialisation MLOps |

---

## 15. Justification du choix final

Le choix du modèle interne est justifié par le contexte du projet.

ObRail a besoin d’un prototype fiable, compréhensible et reproductible.
Le projet actuel dispose déjà :

* d’un dataset IA construit ;
* d’une analyse exploratoire ;
* d’un modèle entraîné ;
* d’un rapport d’évaluation ;
* d’un modèle sauvegardé ;
* d’un script de prédiction ;
* d’une API REST fonctionnelle.

Le recours immédiat à une solution cloud ajouterait de la complexité sans bénéfice majeur pour cette première version.

---

## 16. Limites de la solution interne

La solution interne doit cependant être renforcée avant une mise en production complète.

Les limites principales sont :

1. absence de monitoring automatique ;
2. absence de déploiement cloud ;
3. absence de journalisation des prédictions ;
4. absence de versionnement automatisé des modèles ;
5. absence de pipeline CI/CD complet ;
6. absence de validation métier externe des labels.

Ces points peuvent être traités dans une phase ultérieure.

---

## 17. Plan d’amélioration proposé

Pour passer d’un prototype à une solution industrialisée, les étapes suivantes sont recommandées :

1. Ajouter des tests unitaires sur les scripts ML.
2. Ajouter une journalisation des prédictions API.
3. Mettre en place un suivi des distributions des variables.
4. Ajouter un suivi du temps de réponse de l’API.
5. Versionner automatiquement les modèles.
6. Automatiser le ré-entraînement.
7. Conteneuriser l’API avec Docker.
8. Ajouter une authentification API.
9. Ajouter une route de prédiction à partir d’un `route_id`.
10. Étudier un déploiement cloud si le volume augmente.

---

## 18. Conclusion

Le benchmark montre que les solutions cloud comme Azure Machine Learning, AWS SageMaker, Google Vertex AI et IBM AutoAI sont puissantes et adaptées à des contextes industriels.

Cependant, pour la première version du projet ObRail, l’approche interne open source est la plus adaptée.

Elle répond aux besoins essentiels :

```text
préparer les données
entraîner plusieurs modèles
évaluer les performances
sauvegarder le modèle
exposer une API REST
documenter la solution
```

La solution retenue est donc :

```text
Pipeline IA interne basé sur Python, scikit-learn, joblib et FastAPI.
```

Cette décision permet à ObRail de disposer d’un prototype maîtrisé, économique, reproductible et facilement améliorable.
