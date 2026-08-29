import numpy as np
from services import mock_data

def get_system_info():
    return {"status": "Online", "model_accuracy": "96.8%", "precision": "95.4%", "f1_score": "95.1%"}

def get_dashboard_data():
    return {
        "metrics": mock_data.generate_mock_dashboard_metrics(),
        "attack_dist": mock_data.generate_mock_attack_distribution(),
        "traffic_history": mock_data.generate_mock_traffic_history(),
        "recent_predictions": mock_data.generate_mock_recent_predictions()
    }

def get_alerts():
    return mock_data.generate_mock_alerts()

def predict_traffic(features_dict):
    """Simulates inference over the 78 features."""
    is_threat = np.random.choice([True, False], p=[0.3, 0.7])
    if is_threat:
        return {
            "status": "Intrusion Detected",
            "confidence": f"{np.random.uniform(90.0, 99.9):.2f}%",
            "risk_level": "Critical",
            "attack_type": np.random.choice(["DoS Attack", "Brute Force", "Port Scanning"])
        }
    return {
        "status": "Normal Traffic",
        "confidence": f"{np.random.uniform(95.0, 99.9):.2f}%",
        "risk_level": "Low",
        "attack_type": "None"
    }