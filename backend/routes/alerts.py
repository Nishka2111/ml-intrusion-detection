from flask import Blueprint, jsonify
from backend.database.models import IntrusionLog

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.get("/alerts")
def get_alerts():
    """Return relevant malicious/high-risk events."""
    alerts = (
        IntrusionLog.query
        .filter(IntrusionLog.risk_level.in_(["HIGH", "CRITICAL"]))
        .order_by(IntrusionLog.timestamp.desc())
        .all()
    )
    return jsonify([item.to_dict() for item in alerts]), 200
