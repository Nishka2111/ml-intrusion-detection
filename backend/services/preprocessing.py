"""Align raw feature inputs to expected 78-column model input vectors."""

from __future__ import annotations

import numpy as np
from backend.services.features import DATASET_FEATURES, normalise_feature_dict

EXPECTED_FEATURE_COUNT = 78


_NORMALISED_INDEX_MAP: dict[str, int] = {}
for i, name in enumerate(DATASET_FEATURES):
    norm = (
        name.strip()
        .lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace(".", "_")
        .replace("-", "_")
    )
    _NORMALISED_INDEX_MAP[norm] = i


def align_to_canonical_vector(features: dict) -> np.ndarray:
    """Align raw incoming feature dict to a (1, 78) NumPy float64 array."""
    vector = np.zeros((1, EXPECTED_FEATURE_COUNT), dtype=np.float64)
    norm = normalise_feature_dict(features)
    for key, val in norm.items():
        if key in _NORMALISED_INDEX_MAP:
            idx = _NORMALISED_INDEX_MAP[key]
            vector[0, idx] = val
    return vector


def reorder_to_model_features(
    vector: np.ndarray, model_feature_names: list[str]
) -> np.ndarray:
    """Reorder a canonical vector to match custom model feature names."""
    if not model_feature_names:
        return vector

    reordered = np.zeros((1, len(model_feature_names)), dtype=np.float64)
    for new_idx, name in enumerate(model_feature_names):
        norm = (
            str(name)
            .strip()
            .lower()
            .replace("/", "_")
            .replace(" ", "_")
            .replace(".", "_")
            .replace("-", "_")
        )
        if norm in _NORMALISED_INDEX_MAP:
            orig_idx = _NORMALISED_INDEX_MAP[norm]
            reordered[0, new_idx] = vector[0, orig_idx]
    return reordered


def build_model_input(features: dict, model=None) -> np.ndarray:
    """Build the final input row matrix for sklearn / XGBoost / PyTorch model."""
    canonical = align_to_canonical_vector(features)

    print("\n========== MODEL INPUT DEBUG ==========")
    print("Received feature count:", len(features))
    print("Received feature names:", list(features.keys())[:10])

    canonical = align_to_canonical_vector(features)

    print("Canonical shape:", canonical.shape)
    print("Non-zero values:", np.count_nonzero(canonical))
    print("First 10 values:", canonical[0][:10])

    feature_names = getattr(model, "feature_names_in_", None)

    if feature_names is not None:
        canonical = reorder_to_model_features(
            canonical,
            list(feature_names)
        )

    print("Final shape:", canonical.shape)
    print("Final non-zero values:", np.count_nonzero(canonical))
    print("Final first 10 values:", canonical[0][:10])

    print("=======================================\n")

    # 1. Feature names re-ordering if present on model
    feature_names = getattr(model, "feature_names_in_", None)
    if feature_names is not None:
        canonical = reorder_to_model_features(canonical, list(feature_names))

    # 2. Scaler transformation if attached
    scaler = getattr(model, "_ids_scaler", None)
    if scaler is not None and callable(getattr(scaler, "transform", None)):
        try:
            canonical = scaler.transform(canonical)
        except Exception:
            pass

    return canonical
