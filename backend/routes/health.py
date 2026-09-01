from flask import Blueprint, jsonify
from backend.services.prediction_service import _DEFAULT_MODEL_PATH, is_model_loaded

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health():
    """Backend availability check + active inference mode."""
    return jsonify({
        "status": "ok",
        "mode": "ml" if is_model_loaded() else "demo",
        "model_path": _DEFAULT_MODEL_PATH,
    }), 200
