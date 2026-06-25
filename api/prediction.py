"""Routes FastAPI dédiées à la prédiction IA.

Ce module charge le modèle sauvegardé, lit les métadonnées du modèle,
valide les données reçues via Pydantic et retourne la classe prédite
pour une liaison ferroviaire : faible, moyen ou fort potentiel de substitution avion-train.
"""

from pathlib import Path
import json
import pandas as pd
import joblib

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


PROJECT_ROOT = Path(__file__).resolve().parents[1]

MODELS_DIR = PROJECT_ROOT / "models"
MODEL_PATH = MODELS_DIR / "substitution_model.joblib"
METRICS_PATH = MODELS_DIR / "model_metrics.json"


router = APIRouter(tags=["Prediction IA"])


class PredictionInput(BaseModel):
    """Schéma Pydantic des variables attendues par l'endpoint /predict.
    
    Chaque champ définit à la fois le type attendu et des contraintes simples
    pour empêcher l'envoi de valeurs incohérentes à l'API.
    """
    is_international: int = Field(..., ge=0, le=1)
    distance_km: float = Field(..., gt=0)
    weekly_frequency: float = Field(..., gt=0)
    daily_frequency_avg: float = Field(..., gt=0)
    avg_duration_minutes: float = Field(..., gt=0)
    min_duration_minutes: float = Field(..., gt=0)
    max_duration_minutes: float = Field(..., gt=0)
    has_night_train: int = Field(..., ge=0, le=1)
    has_day_train: int = Field(..., ge=0, le=1)
    avg_num_stops: float = Field(..., ge=0)
    avg_quality_score: float = Field(..., ge=0, le=100)
    quality_issues_count: int = Field(..., ge=0)
    co2_train_kg: float = Field(..., ge=0)
    co2_plane_kg: float = Field(..., ge=0)
    co2_saving_kg: float
    co2_saving_percent: float

    model_config = {
        "json_schema_extra": {
            "example": {
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
        }
    }


def load_model_and_metadata():
    """Charge le modèle sauvegardé et les métadonnées associées.
    
    Cette fonction est appelée au démarrage de l'API. Elle vérifie que les fichiers existent,
    charge le modèle joblib et récupère la liste des variables attendues par le modèle.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Modèle introuvable : {MODEL_PATH}")

    if not METRICS_PATH.exists():
        raise FileNotFoundError(f"Fichier métriques introuvable : {METRICS_PATH}")

    model = joblib.load(MODEL_PATH)

    with open(METRICS_PATH, "r", encoding="utf-8") as file:
        metrics = json.load(file)

    feature_columns = metrics.get("feature_columns")

    if not feature_columns:
        raise ValueError("La liste feature_columns est absente de model_metrics.json")

    return model, metrics, feature_columns


try:
    MODEL, METRICS, FEATURE_COLUMNS = load_model_and_metadata()
except Exception as exc:
    MODEL = None
    METRICS = None
    FEATURE_COLUMNS = None
    MODEL_LOADING_ERROR = str(exc)
else:
    MODEL_LOADING_ERROR = None


@router.get("/model-info")
def get_model_info():
    """Retourne les informations principales du modèle chargé par l'API.
    
    L'endpoint est utile pour vérifier rapidement le modèle actif, les variables utilisées
    et les métriques de test sans relancer un entraînement.
    """
    if METRICS is None:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de chargement du modèle : {MODEL_LOADING_ERROR}",
        )

    return {
        "best_model": METRICS.get("best_model"),
        "target_column": METRICS.get("target_column"),
        "feature_columns": METRICS.get("feature_columns"),
        "test_metrics": METRICS.get("test_metrics"),
        "note": METRICS.get("note"),
    }


@router.post("/predict")
def predict(input_data: PredictionInput):
    """Réalise une prédiction à partir des variables envoyées à l'API.
    
    Les données sont validées par Pydantic, replacées dans l'ordre attendu par le modèle,
    puis utilisées pour produire une classe et, si disponible, des probabilités par classe.
    """
    if MODEL is None or FEATURE_COLUMNS is None:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur de chargement du modèle : {MODEL_LOADING_ERROR}",
        )

    input_dict = input_data.model_dump()

    try:
        prediction_df = pd.DataFrame([input_dict])
        prediction_df = prediction_df[FEATURE_COLUMNS]

        predicted_class = MODEL.predict(prediction_df)[0]

        response = {
            "prediction": str(predicted_class),
            "input": input_dict,
        }

        if hasattr(MODEL, "predict_proba"):
            probabilities = MODEL.predict_proba(prediction_df)[0]
            classes = MODEL.classes_

            response["probabilities"] = {
                str(class_name): round(float(probability), 4)
                for class_name, probability in zip(classes, probabilities)
            }

            response["confidence"] = round(float(max(probabilities)), 4)

        return response

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur pendant la prédiction : {str(exc)}",
        )