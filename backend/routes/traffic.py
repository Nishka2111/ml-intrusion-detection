from datetime import datetime, timedelta
from flask import Blueprint, jsonify
from backend.database.models import IntrusionLog

traffic_bp = Blueprint("traffic", __name__)


@traffic_bp.get("/traffic-overview")
def traffic_overview():
    """Return time-series aggregate data for the dashboard Traffic Overview chart."""
    today = datetime.utcnow().date()
    start = today - timedelta(days=6)

    logs = (
        IntrusionLog.query
        .filter(IntrusionLog.timestamp >= start)
        .order_by(IntrusionLog.timestamp.asc())
        .all()
    )

    days: list[str] = []
    buckets: dict[str, dict[str, int]] = {}
    for i in range(7):
        day = start + timedelta(days=i)
        label = day.strftime("%a")
        days.append(label)
        buckets[label] = {"total": 0, "attacks": 0, "normal": 0}

    for log in logs:
        label = log.timestamp.strftime("%a") if log.timestamp else None
        if label not in buckets:
            continue
        buckets[label]["total"] += 1
        if log.attack_type and log.attack_type.lower() == "normal":
            buckets[label]["normal"] += 1
        else:
            buckets[label]["attacks"] += 1

    return jsonify({
        "days": days,
        "total_traffic": [buckets[d]["total"] for d in days],
        "attacks": [buckets[d]["attacks"] for d in days],
        "normal": [buckets[d]["normal"] for d in days],
    }), 200
