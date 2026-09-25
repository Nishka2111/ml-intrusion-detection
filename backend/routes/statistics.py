from flask import Blueprint, jsonify
from backend.database.models import IntrusionLog

statistics_bp = Blueprint("statistics", __name__)


@statistics_bp.get("/statistics")
def statistics():
    """Provide dashboard counts and aggregates."""
    total = IntrusionLog.query.count()
    malicious = (
        IntrusionLog.query
        .filter(IntrusionLog.attack_type != "Normal")
        .count()
    )
    critical = (
        IntrusionLog.query
        .filter(IntrusionLog.risk_level == "CRITICAL")
        .count()
    )

    return jsonify({
        "total_traffic": total,
        "malicious_traffic": malicious,
        "normal_traffic": max(total - malicious, 0),
        "total_attacks": malicious,
        "critical_alerts": critical,
    }), 200
