"""Tests automatisés du script de prédiction locale.

Ces tests vérifient que le modèle et ses métadonnées existent, que les variables d'entrée sont correctes,
que substitution_score n'est pas utilisée comme feature et que la prédiction retourne une structure valide.
"""

from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

MODEL_PATH = PROJECT_ROOT / "models" / "substitution_model.joblib"
METRICS_PATH = PROJECT_ROOT / "models" / "model_metrics.json"

from scripts.ml.predict import (  # noqa: E402
    DEFAULT_SAMPLE,
    load_feature_columns,
    load_model,
    validate_input,
    predict,
)


def test_model_file_exists():
    """Vérifie que le fichier du modèle sauvegardé existe."""
    assert MODEL_PATH.exists(), f"Modèle introuvable : {MODEL_PATH}"


def test_metrics_file_exists():
    """Vérifie que le fichier de métriques du modèle existe."""
    assert METRICS_PATH.exists(), f"Fichier métriques introuvable : {METRICS_PATH}"


def test_load_feature_columns():
    """Vérifie que les variables du modèle sont chargées et que substitution_score est exclue."""
    feature_columns = load_feature_columns()

    assert isinstance(feature_columns, list)
    assert len(feature_columns) > 0
    assert "substitution_score" not in feature_columns, (
        "substitution_score ne doit pas être utilisé comme variable d'entrée"
    )


def test_load_model():
    """Vérifie que le modèle peut être chargé et possède une méthode predict."""
    model = load_model()

    assert model is not None
    assert hasattr(model, "predict"), "Le modèle chargé ne possède pas de méthode predict"


def test_validate_input_returns_dataframe_with_expected_columns():
    """Vérifie que l'entrée de prédiction est transformée en DataFrame conforme."""
    feature_columns = load_feature_columns()
    prediction_df = validate_input(DEFAULT_SAMPLE, feature_columns)

    assert isinstance(prediction_df, pd.DataFrame)
    assert list(prediction_df.columns) == feature_columns
    assert len(prediction_df) == 1


def test_validate_input_raises_error_when_column_missing():
    """Vérifie qu'une erreur est levée lorsqu'une variable obligatoire manque."""
    feature_columns = load_feature_columns()

    invalid_input = DEFAULT_SAMPLE.copy()
    invalid_input.pop(feature_columns[0])

    try:
        validate_input(invalid_input, feature_columns)
    except ValueError as exc:
        assert "Variables manquantes" in str(exc)
    else:
        raise AssertionError("validate_input aurait dû lever une ValueError")


def test_predict_returns_expected_structure():
    """Vérifie que la prédiction locale retourne les clés attendues."""
    result = predict(DEFAULT_SAMPLE)

    assert isinstance(result, dict)
    assert "prediction" in result
    assert "input" in result
    assert result["prediction"] in {"faible", "moyen", "fort"}


def test_predict_returns_probabilities_and_confidence():
    """Vérifie que les probabilités et la confiance sont cohérentes."""
    result = predict(DEFAULT_SAMPLE)

    assert "probabilities" in result
    assert "confidence" in result

    probabilities = result["probabilities"]

    assert set(probabilities.keys()) == {"faible", "moyen", "fort"}
    assert 0 <= result["confidence"] <= 1

    probability_sum = sum(probabilities.values())

    assert abs(probability_sum - 1.0) < 0.01, (
        f"La somme des probabilités devrait être proche de 1, obtenu : {probability_sum}"
    )


def test_default_sample_prediction_is_valid_business_case():
    """Vérifie que l'exemple métier par défaut est classé en fort potentiel."""
    result = predict(DEFAULT_SAMPLE)

    assert result["prediction"] == "fort", (
        "L'exemple métier par défaut devrait être classé en fort potentiel"
    )