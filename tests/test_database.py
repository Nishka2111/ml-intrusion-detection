from backend.database.database import db
from backend.database.models import IntrusionLog


def test_insert_prediction(app):
    with app.app_context():
        log = IntrusionLog(
            attack_type="DDoS",
            confidence=0.94,
            risk_level="CRITICAL",
        )
        db.session.add(log)
        db.session.commit()

        saved = IntrusionLog.query.first()
        assert saved.attack_type == "DDoS"
        assert saved.confidence == 0.94
        assert saved.risk_level == "CRITICAL"


def test_log_to_dict(app):
    with app.app_context():
        log = IntrusionLog(
            source_ip="192.168.1.10",
            destination_ip="10.0.0.5",
            protocol="TCP",
            attack_type="DDoS",
            confidence=0.94,
            risk_level="CRITICAL",
        )
        db.session.add(log)
        db.session.commit()

        data = log.to_dict()
        assert data["attack_type"] == "DDoS"
        assert data["confidence"] == 0.94
        assert data["risk_level"] == "CRITICAL"
        assert data["source_ip"] == "192.168.1.10"
