# Rapport d’évaluation du modèle IA ObRail

## Objectif

L’objectif du modèle est de classifier les liaisons ferroviaires selon leur potentiel de substitution à l’avion : faible, moyen ou fort.

## Modèles comparés

| model               |   accuracy |   precision_macro |   recall_macro |   f1_macro |   f1_weighted |
|:--------------------|-----------:|------------------:|---------------:|-----------:|--------------:|
| gradient_boosting   |     1      |            1      |         1      |     1      |        1      |
| random_forest       |     0.9902 |            0.9738 |         0.9954 |     0.9842 |        0.9904 |
| decision_tree       |     0.9886 |            0.9781 |         0.982  |     0.98   |        0.9887 |
| logistic_regression |     0.7545 |            0.7037 |         0.8744 |     0.7386 |        0.7667 |

Le meilleur modèle sélectionné est : **gradient_boosting**.

## Métriques finales sur le jeu de test

- Accuracy : 0.9919
- Precision macro : 0.9805
- Recall macro : 0.9921
- F1 macro : 0.9861
- F1 weighted : 0.992

## Rapport par classe

| classe   |   precision |   recall |   f1_score |   support |
|:---------|------------:|---------:|-----------:|----------:|
| faible   |      1      |   1      |     1      |       110 |
| moyen    |      0.9977 |   0.9909 |     0.9943 |       438 |
| fort     |      0.9437 |   0.9853 |     0.964  |        68 |

## Matrice de confusion

|             |   pred_faible |   pred_moyen |   pred_fort |
|:------------|--------------:|-------------:|------------:|
| réel_faible |           110 |            0 |           0 |
| réel_moyen  |             0 |          434 |           4 |
| réel_fort   |             0 |            1 |          67 |

## Variables les plus importantes

| feature              |   importance |
|:---------------------|-------------:|
| weekly_frequency     |   0.265887   |
| co2_train_kg         |   0.236738   |
| co2_saving_kg        |   0.159667   |
| co2_plane_kg         |   0.135868   |
| distance_km          |   0.0853119  |
| avg_duration_minutes |   0.0626326  |
| min_duration_minutes |   0.0328369  |
| max_duration_minutes |   0.0108006  |
| is_international     |   0.00419824 |
| avg_num_stops        |   0.00360674 |

## Interprétation

Les résultats montrent que le modèle Gradient Boosting reproduit très bien la logique métier de classification construite à partir des indicateurs ferroviaires et environnementaux.

La métrique principale retenue est le F1 macro, car les classes ne sont pas parfaitement équilibrées. Cette métrique permet de tenir compte de la performance sur chaque classe, et pas uniquement de la classe majoritaire.

## Limites

La cible utilisée est une cible métier construite à partir d’un score de substitution. Le modèle ne repose donc pas encore sur des labels historiques validés par des experts. Une amélioration future consisterait à valider les classes avec ObRail ou à intégrer des données réelles de report modal entre avion et train.

La variable substitution_score a été exclue des variables d’entrée afin d’éviter une fuite de données.