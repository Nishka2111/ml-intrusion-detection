"""ML prediction service supporting joblib/pkl model loading & heuristic fallback."""

from __future__ import annotations

import os
from typing import Optional
from backend.services.preprocessing import build_model_input

_DEFAULT_MODEL_PATH = os.getenv("ML_MODEL_PATH", "").strip() or "models/model.joblib"
_LOAD_CACHE: dict[str, tuple[Optional[object], Optional[str]]] = {}


def predict_intrusion(features: dict) -> dict:
    """Predict the attack type/confidence for a flow's feature dict."""
    model, scaler, label_map = _load_model()

    if model is not None:
        try:
            return _predict_with_model(features, model, scaler, label_map)
        except Exception:
            return _predict_heuristic(features)

    return _predict_heuristic(features)


def is_model_loaded() -> bool:
    """True if a trained ML model is loaded from disk."""
    return _load_model()[0] is not None


def _load_model():
    """Load (once) and return (model, scaler, label_map)."""
    path = _DEFAULT_MODEL_PATH
    if path in _LOAD_CACHE:
        model, error = _LOAD_CACHE[path]
        if error:
            return None, None, None
        return model, getattr(model, "_ids_scaler", None), getattr(model, "_ids_label_map", None)

    try:
        model, scaler, label_map = _read_artifacts(path)
        if scaler is not None and model is not None:
            model._ids_scaler = scaler
        if label_map is not None and model is not None:
            model._ids_label_map = label_map
        _LOAD_CACHE[path] = (model, None)
        return model, scaler, label_map
    except FileNotFoundError:
        _LOAD_CACHE[path] = (None, "model file not found")
        return None, None, None
    except Exception as exc:
        _LOAD_CACHE[path] = (None, str(exc))
        return None, None, None


def _read_artifacts(path: str):
    """Read a model file and return (model, scaler, label_map)."""
    if not os.path.exists(path):
        raise FileNotFoundError(path)

    if path.endswith(".joblib") or path.endswith(".pkl"):
        try:
            import joblib
            return _unpack(joblib.load(path))
        except ModuleNotFoundError:
            pass

    import pickle
    with open(path, "rb") as fh:
        return _unpack(pickle.load(fh))


def _unpack(raw):
    if isinstance(raw, dict):
        model = (
            raw.get("model")
            or raw.get("classifier")
            or raw.get("pipeline")
            or raw.get("estimator")
        )
        scaler = raw.get("scaler") or raw.get("preprocessor")
        label_map = raw.get("label_map") or raw.get("classes")
    else:
        model = raw
        scaler = None
        label_map = None

    if model is None or not callable(getattr(model, "predict", None)):
        return None, scaler, label_map
    return model, scaler, label_map


def _predict_with_model(features: dict, model, scaler, label_map) -> dict:
    import numpy as np

    row = build_model_input(features, model)
    raw_label = model.predict(row)[0]
    attack_type = _humanise_label(raw_label, model, label_map)

    try:
        proba = model.predict_proba(row)[0]
        confidence = float(np.max(proba))
    except Exception:
        confidence = 0.97 if attack_type.lower() == "normal" else 0.93

    confidence = float(max(0.0, min(1.0, confidence)))
    return {"attack_type": attack_type, "confidence": confidence}


def _humanise_label(raw_label, model, label_map) -> str:
    label = raw_label
    if hasattr(label, "item"):
        label = label.item()
    if isinstance(label, (list, tuple)) and len(label) == 1:
        label = label[0]

    if isinstance(label, (int, float)):
        classes = getattr(model, "classes_", None)
        if classes is not None and 0 <= int(label) < len(classes):
            label = classes[int(label)]

    if label_map:
        mapped = label_map.get(label) or label_map.get(str(label))
        if mapped:
            label = mapped

    text = str(label).strip().lower()
    friendly = {
        "0": "Normal", "1": "Attack",
        "benign": "Normal", "normal": "Normal",
    }
    return friendly.get(text, str(label))


def _predict_heuristic(features: dict) -> dict:
    """Feature-driven heuristic used while a real ML model file is not uploaded."""
    from backend.services.features import normalise_feature_dict

    f = normalise_feature_dict(features)

    def num(*keys: str, default: float = 0.0) -> float:
        for key in keys:
            if key in f:
                try:
                    return float(f[key])
                except (TypeError, ValueError):
                    continue
        return default

    dest_port = num("destination_port")
    duration = num("flow_duration")
    fwd_pkts = num("total_fwd_packets", "subflow_fwd_packets")
    bwd_pkts = num("total_backward_packets", "subflow_bwd_packets")
    fwd_len = num("total_length_of_fwd_packets")
    bwd_len = num("total_length_of_bwd_packets")
    syn = num("syn_flag_count")
    pkt_len_std = num("packet_length_std")
    flow_iat_mean = num("flow_iat_mean")
    flow_bytes_sec = num("flow_bytes_s")

    total_pkts = fwd_pkts + bwd_pkts
    total_len = fwd_len + bwd_len
    small_avg_payload = total_pkts > 0 and (total_len / total_pkts) < 200.0

    if syn >= 3 and dest_port >= 22 and duration < 1_000_000 and small_avg_payload:
        return {"attack_type": "Port Scanning", "confidence": 0.91}

    if dest_port in (22, 23, 3389, 445) and syn >= 1:
        return {"attack_type": "Brute Force", "confidence": 0.88}

    if total_pkts >= 50 and small_avg_payload and duration >= 2_000_000:
        if 0 < flow_bytes_sec < 50_000:
            return {"attack_type": "DoS Attack", "confidence": 0.94}
        return {"attack_type": "DDoS", "confidence": 0.96}

    if bwd_len > 1_000_000 and duration >= 1_000_000 and fwd_len > 50_000:
        return {"attack_type": "Data Exfiltration", "confidence": 0.85}

    if pkt_len_std > 1000 or (0 < flow_iat_mean < 20.0):
        return {"attack_type": "Attack", "confidence": 0.81}

    return {"attack_type": "Normal", "confidence": 0.96}
