from flask import Blueprint, request, jsonify
from backend.database.database import db
from backend.database.models import IntrusionLog
from backend.schemas.prediction import PredictionRequest
from backend.services.prediction_service import predict_intrusion
from backend.services.risk_service import calculate_risk

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.post("/predict")
def predict():
    """Parse JSON -> validate -> call ML -> calculate risk -> save to SQLite -> return response."""
    try:
        payload = PredictionRequest.model_validate(request.get_json(force=True))
    except Exception as exc:
        return jsonify({
            "error": "Invalid request",
            "details": str(exc),
        }), 422

    result = predict_intrusion(payload.features)
    risk_level = calculate_risk(
        result["attack_type"],
        result["confidence"],
    )

    log = IntrusionLog(
        source_ip=payload.source_ip,
        destination_ip=payload.destination_ip,
        protocol=payload.protocol,
        attack_type=result["attack_type"],
        confidence=result["confidence"],
        risk_level=risk_level,
    )
    db.session.add(log)
    db.session.commit()

    return jsonify({
        "attack_type": result["attack_type"],
        "confidence": result["confidence"],
        "risk_level": risk_level,
    }), 200
