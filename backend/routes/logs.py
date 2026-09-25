from flask import Blueprint, jsonify, request
from backend.database.models import IntrusionLog

logs_bp = Blueprint("logs", __name__)


@logs_bp.get("/logs")
def get_logs():
    """Return raw historical records, optionally filtered by attack_type or risk_level."""
    query = IntrusionLog.query

    attack_type = request.args.get("attack_type")
    risk_level = request.args.get("risk_level")

    if attack_type:
        query = query.filter_by(attack_type=attack_type)
    if risk_level:
        query = query.filter_by(risk_level=risk_level)

    logs = query.order_by(IntrusionLog.timestamp.desc()).all()
    return jsonify([item.to_dict() for item in logs]), 200
