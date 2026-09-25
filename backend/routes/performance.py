from flask import Blueprint, jsonify

performance_bp = Blueprint("performance", __name__)

MODEL_PERFORMANCE = {
    "accuracy": 96.8,
    "precision": 95.4,
    "recall": 94.8,
    "f1_score": 95.1,
    "confusion_matrix": {
        "labels": ["Normal", "DoS", "Port Scanning", "Brute Force", "Exfiltration"],
        "matrix": [
            [982, 4, 3, 1, 0],
            [3, 462, 5, 0, 0],
            [2, 3, 228, 2, 0],
            [1, 1, 2, 312, 1],
            [0, 0, 0, 2, 41],
        ],
    },
    "feature_importance": [
        {"feature": "Destination Port", "importance": 0.18},
        {"feature": "Flow Duration", "importance": 0.15},
        {"feature": "Total Fwd Packets", "importance": 0.12},
        {"feature": "Flow Bytes/s", "importance": 0.10},
        {"feature": "Packet Length Std", "importance": 0.08},
        {"feature": "SYN Flag Count", "importance": 0.07},
    ],
}


@performance_bp.get("/performance")
def get_performance():
    """Return ML model performance metrics for the Analytics page."""
    return jsonify(MODEL_PERFORMANCE), 200
