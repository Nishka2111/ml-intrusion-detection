"""Example script showing how to export a trained ML model for the backend.

Run this script after training your model on CICIDS2017 / UNSW-NB15 dataset:
    python models/export_model_example.py
"""

import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

# 1. Create directory if needed
os.makedirs("models", exist_ok=True)

# 2. Example dummy training (Replace with your real trained model!)
X_train = np.random.rand(100, 78)
y_train = np.random.choice([0, 1, 2, 3], size=100)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_train)

model = RandomForestClassifier(n_estimators=50, random_state=42)
model.fit(X_scaled, y_train)

# 3. Define human-readable label map
label_map = {
    0: "Normal",
    1: "DDoS",
    2: "Port Scanning",
    3: "Brute Force",
}

# 4. Save artifact bundle to models/model.joblib
output_path = "models/model.joblib"
artifact_bundle = {
    "model": model,
    "scaler": scaler,
    "label_map": label_map,
}

joblib.dump(artifact_bundle, output_path)
print(f"✅ Trained model successfully saved to: {output_path}")
print("Restart the Flask backend (python -m backend.app) to enable ML threat prediction!")
