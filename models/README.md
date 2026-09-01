# ML Model Integration Guide for Threat Prediction

This directory (`models/`) is where you place your trained Machine Learning model artifacts.

---

## 📁 Required Model Files

For the backend to automatically pick up and execute your trained ML model, place one of the following files in this directory:

| Preferred Filename | Format | Description |
|--------------------|--------|-------------|
| `models/model.joblib` | `.joblib` | **Recommended.** Exported using `joblib.dump()` containing model, scaler, and label map. |
| `models/model.pkl` | `.pkl` | Standard Python pickle containing fitted model object or pipeline. |

*(Optional)* You can also set a custom model path in your `.env` file:
```env
ML_MODEL_PATH=models/my_custom_ids_model.joblib
```

---

## 🧠 Supported ML Model Artifact Structures

The backend ML prediction service (`backend/services/prediction_service.py`) supports 3 model export styles:

### 1. Dictionary Bundle (Recommended Best Practice)
Export a dictionary containing your trained model, optional feature scaler, and optional class label map:

```python
import joblib

model_bundle = {
    "model": trained_clf,              # Trained XGBoost / RandomForest / Scikit-Learn model
    "scaler": fitted_scaler,            # (Optional) StandardScaler or MinMaxScaler
    "label_map": {                     # (Optional) Mapping integer labels to human display names
        0: "Normal",
        1: "DDoS",
        2: "Port Scanning",
        3: "Brute Force",
        4: "Data Exfiltration",
    }
}

joblib.dump(model_bundle, "models/model.joblib")
```

### 2. Scikit-Learn Pipeline
A single `Pipeline([("scaler", StandardScaler()), ("clf", RandomForestClassifier())])` object:

```python
import joblib

joblib.dump(pipeline, "models/model.joblib")
```

### 3. Standalone Estimator
Any fitted Scikit-Learn or XGBoost classifier with `.predict(X)` and `.predict_proba(X)` methods:

```python
import joblib

joblib.dump(trained_clf, "models/model.joblib")
```

---

## 📊 Feature Input Contract (78 Canonical Features)

The model receives a NumPy float matrix of shape `(1, 78)` matching the CICIDS2017 flow feature schema defined in `backend/services/features.py`.

### Key Features Included:
- **Flow Basics**: `Destination Port`, `Flow Duration`, `Total Fwd Packets`, `Total Backward Packets`, `Total Length of Fwd Packets`, `Total Length of Bwd Packets`
- **Packet Lengths**: Min, Max, Mean, Std across Forward & Backward packets
- **Flags**: `FIN Flag Count`, `SYN Flag Count`, `RST Flag Count`, `PSH Flag Count`, `ACK Flag Count`, `URG Flag Count`
- **Timings & Rates**: `Flow Bytes/s`, `Flow Packets/s`, `Flow IAT Mean`, `Active Mean`, `Idle Mean`

> **Note on Feature Order:** If your estimator was trained with feature names (`model.feature_names_in_`), the backend **automatically reorders** the incoming request vector to match your exact training column layout. Missing features default to `0.0`.

---

## 🔄 Automatic Mode Switching

- **When `models/model.joblib` is present**: The backend runs real ML model inference via `.predict()` & `.predict_proba()`.
- **When no model file is present**: The backend gracefully degrades to the deterministic flow-based heuristic engine so the dashboard and batch file uploads keep working end-to-end.
