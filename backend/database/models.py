from datetime import datetime
from backend.database.database import db


class IntrusionLog(db.Model):
    """Model representing a single intrusion detection log entry."""

    __tablename__ = "intrusion_logs"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    source_ip = db.Column(db.String(45), nullable=True)
    destination_ip = db.Column(db.String(45), nullable=True)
    protocol = db.Column(db.String(20), nullable=True)
    attack_type = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    risk_level = db.Column(db.String(20), nullable=False)

    def to_dict(self) -> dict:
        """Serialize the model instance to a dictionary."""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else "",
            "source_ip": self.source_ip or "-",
            "destination_ip": self.destination_ip or "-",
            "protocol": self.protocol or "TCP",
            "attack_type": self.attack_type,
            "confidence": float(self.confidence),
            "risk_level": self.risk_level,
        }
