"""Recherche d'hyperparamètres pour le Gradient Boosting.

Ce script utilise GridSearchCV afin de tester plusieurs combinaisons de paramètres
(n_estimators, learning_rate, max_depth). Il permet de couvrir l'étape d'ajustement
du modèle attendue dans la démarche de modélisation.
"""

from pathlib import Path
import json

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.utils.class_weight import compute_sample_weight


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "modeling"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"

TRAIN_PATH = DATA_DIR / "train.csv"
VALIDATION_PATH = DATA_DIR / "validation.csv"
TEST_PATH = DATA_DIR / "test.csv"
METRICS_PATH = MODELS_DIR / "model_metrics.json"

OUTPUT_CSV = REPORTS_DIR / "gradient_boosting_gridsearch.csv"
OUTPUT_JSON = REPORTS_DIR / "gradient_boosting_gridsearch_summary.json"

TARGET_COLUMN = "substitution_potential"


def load_feature_columns():
    """Charge la liste des variables attendues par le modèle depuis model_metrics.json."""
    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        metrics = json.load(file)

    feature_columns = metrics.get("feature_columns")

    if not feature_columns:
        raise ValueError("feature_columns absent de models/model_metrics.json")

    if "substitution_score" in feature_columns:
        raise ValueError("substitution_score ne doit pas être utilisée comme variable d'entrée")

    return feature_columns


def compute_metrics(y_true, y_pred):
    """Calcule les métriques principales utilisées pour comparer les modèles."""
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="macro",
        zero_division=0,
    )

    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_true,
        y_pred,
        average="weighted",
        zero_division=0,
    )

    return {
        "accuracy": round(float(accuracy_score(y_true, y_pred)), 4),
        "precision_macro": round(float(precision_macro), 4),
        "recall_macro": round(float(recall_macro), 4),
        "f1_macro": round(float(f1_macro), 4),
        "precision_weighted": round(float(precision_weighted), 4),
        "recall_weighted": round(float(recall_weighted), 4),
        "f1_weighted": round(float(f1_weighted), 4),
    }


def main():
    """Point d'entrée du script lorsqu'il est exécuté en ligne de commande."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    feature_columns = load_feature_columns()

    train_df = pd.read_csv(TRAIN_PATH)
    validation_df = pd.read_csv(VALIDATION_PATH)
    test_df = pd.read_csv(TEST_PATH)

    X_train = train_df[feature_columns]
    y_train = train_df[TARGET_COLUMN]

    X_validation = validation_df[feature_columns]
    y_validation = validation_df[TARGET_COLUMN]

    X_test = test_df[feature_columns]
    y_test = test_df[TARGET_COLUMN]

    pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("classifier", GradientBoostingClassifier(random_state=42)),
        ]
    )

    param_grid = {
        "classifier__n_estimators": [50, 100, 150],
        "classifier__learning_rate": [0.05, 0.1],
        "classifier__max_depth": [2, 3],
    }

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=42,
    )

    sample_weight = compute_sample_weight(
        class_weight="balanced",
        y=y_train,
    )

    grid_search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring="f1_macro",
        cv=cv,
        n_jobs=-1,
        verbose=1,
        return_train_score=True,
    )

    grid_search.fit(
        X_train,
        y_train,
        classifier__sample_weight=sample_weight,
    )

    results_df = pd.DataFrame(grid_search.cv_results_)
    results_df = results_df.sort_values("rank_test_score")
    results_df.to_csv(OUTPUT_CSV, index=False)

    best_model = grid_search.best_estimator_

    validation_predictions = best_model.predict(X_validation)
    test_predictions = best_model.predict(X_test)

    validation_metrics = compute_metrics(y_validation, validation_predictions)
    test_metrics = compute_metrics(y_test, test_predictions)

    summary = {
        "best_params": grid_search.best_params_,
        "best_cv_f1_macro": round(float(grid_search.best_score_), 4),
        "validation_metrics": validation_metrics,
        "test_metrics": test_metrics,
        "note": (
            "GridSearchCV réalisé sur le Gradient Boosting afin de couvrir "
            "la recherche d'hyperparamètres. La variable substitution_score "
            "reste exclue des variables d'entrée."
        ),
    }

    with open(OUTPUT_JSON, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4, ensure_ascii=False)

    print("GridSearchCV terminé.")
    print(f"Meilleurs paramètres : {grid_search.best_params_}")
    print(f"Meilleur F1 macro CV : {grid_search.best_score_:.4f}")
    print(f"Résultats détaillés : {OUTPUT_CSV}")
    print(f"Résumé : {OUTPUT_JSON}")


if __name__ == "__main__":
    main()