"""ML prediction service for the intrusion detection model."""

from __future__ import annotations

import os
from pathlib import Path

import joblib
import numpy as np

from backend.services.preprocessing import build_model_input

BASE_DIR = Path(__file__).resolve().parents[2]

DEFAULT_MODEL_PATH = BASE_DIR / "models" / "intrusion_model.pkl"

DEFAULT_ENCODER_PATH = BASE_DIR / "models" / "label_encoder.pkl"

MODEL_PATH = Path(
    os.getenv(
        "ML_MODEL_PATH",
        str(DEFAULT_MODEL_PATH)
    )
)


ENCODER_PATH = Path(
    os.getenv(
        "ML_ENCODER_PATH",
        str(DEFAULT_ENCODER_PATH)
    )
)


_MODEL = None
_ENCODER = None



def _load_model():
    """Load the trained Random Forest model."""

    global _MODEL

    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"ML model not found: {MODEL_PATH}"
            )

        _MODEL = joblib.load(MODEL_PATH)

    return _MODEL


def _load_encoder():
    """Load the label encoder used during training."""

    global _ENCODER

    if _ENCODER is None:
        if not ENCODER_PATH.exists():
            raise FileNotFoundError(
                f"Label encoder not found: {ENCODER_PATH}"
            )

        _ENCODER = joblib.load(ENCODER_PATH)

    return _ENCODER


def is_model_loaded() -> bool:
    """Return True if the trained ML model can be loaded."""

    try:
        _load_model()
        _load_encoder()
        return True
    except Exception:
        return False

def predict_intrusion(features: dict) -> dict:
    """
    Run intrusion detection on one network flow.

    Parameters
    ----------
    features:
        Dictionary containing network flow features.

    Returns
    -------
    dict
        {
            "attack_type": str,
            "confidence": float
        }
    """

    model = _load_model()
    encoder = _load_encoder()

    # Build the exact 78-feature input expected by
    # the trained Random Forest.
    row = build_model_input(
        features,
        model
    )

    # Sanity check
    if row.shape[1] != 78:
        raise ValueError(
            f"Expected 78 features, got {row.shape[1]}"
        )


    encoded_prediction = model.predict(row)[0]

    # Decode numeric prediction back to attack name
    attack_type = encoder.inverse_transform(
        [int(encoded_prediction)]
    )[0]


    try:
        probabilities = model.predict_proba(row)[0]

        confidence = float(
            np.max(probabilities)
        )

    except Exception:
        confidence = 0.0

    confidence = max(
        0.0,
        min(1.0, confidence)
    )

    return {
        "attack_type": str(attack_type),
        "confidence": confidence
    }