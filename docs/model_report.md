# ML-Based Network Intrusion Detection System

## Technical Project Report

---

# Abstract

Cybersecurity systems must continuously monitor network traffic to identify potentially malicious behavior. Manual analysis of large volumes of network traffic is impractical, while traditional rule-based approaches may have difficulty identifying complex or previously unseen patterns.

This project proposes a machine-learning-based Network Intrusion Detection System using the CICIDS2017 dataset. Network-flow information is processed into numerical features and classified using a Random Forest machine-learning model.

The final system supports seven traffic categories: BENIGN, Bot, Brute Force, DDoS, DoS, PortScan, and Web Attack.

The trained model is integrated into a Flask backend. A REST API accepts network-flow features and returns the predicted attack type, model confidence, and application-level risk level. Prediction results are also stored in SQLite for historical analysis.

---

# 1. Introduction

A Network Intrusion Detection System, or NIDS, monitors network activity and attempts to identify malicious or suspicious behavior.

With modern networks producing large volumes of traffic, automated detection is necessary. Machine-learning techniques can learn relationships between network-flow characteristics and known attack patterns.

This project applies supervised machine learning to network intrusion detection and integrates the resulting model into an application-level backend.

---

# 2. Problem Statement

The problem addressed by this project is:

> How can machine learning be used to automatically classify network traffic into benign and malicious categories and expose the resulting detection system through a usable application interface?

---

# 3. Objectives

The project objectives are:

- Analyze network intrusion data.
- Clean and preprocess the dataset.
- Develop leakage-aware features.
- Train a machine-learning classifier.
- Handle class imbalance.
- Optimize the classifier.
- Save the trained model.
- Integrate the model with a backend.
- Provide a REST API.
- Calculate intrusion risk.
- Store prediction results.

---

# 4. Dataset

The project uses the CICIDS2017 dataset.

The dataset contains network-flow information representing benign traffic and multiple attack scenarios.

The project maps the available attack labels into seven categories:

```text
BENIGN
Bot
Brute Force
DDoS
DoS
PortScan
Web Attack
```

---

# 5. Data Preprocessing

The preprocessing pipeline performs:

1. Column-name cleaning.
2. Infinite-value handling.
3. Duplicate removal.
4. Label normalization.
5. Unsupported-label filtering.
6. Class-size control.
7. Feature/target separation.

The resulting model input contains:

```text
78 numerical features
```

---

# 6. Feature Engineering

Network traffic is represented using flow-level numerical characteristics.

Examples include:

- Destination port.
- Flow duration.
- Forward packet count.
- Backward packet count.
- Forward packet length.
- Backward packet length.
- Flow inter-arrival time.
- TCP flag counts.
- Packet-length statistics.
- Flow byte rates.
- Flow packet rates.

---

# 7. Data Leakage Prevention

Data leakage can cause a model to appear more accurate during testing than it would be in real-world use.

The project therefore follows the principle that a feature must be computable from information available at prediction time.

The target label is not used as an input feature.

The train/test split is performed before training-specific operations.

Training preprocessing statistics are derived from training data rather than using information from the test set.

---

# 8. Class Imbalance

Network intrusion datasets often contain classes with very different numbers of samples.

To address this, the project uses controlled sampling and targeted SMOTE for selected minority classes during model training.

This is intended to provide the classifier with better representation of underrepresented attack categories.

---

# 9. Model Selection

The project uses a Random Forest classifier.

The final configuration is:

```python
RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)
```

---

# 10. Why Random Forest?

Random Forest was selected because:

- It performs well on structured/tabular data.
- It captures nonlinear relationships.
- It can model interactions between features.
- It does not require feature scaling for the classifier.
- It supports probability estimates.
- It provides feature importance.
- It can be serialized for backend deployment.

---

# 11. Training

The data is divided using a stratified split:

```python
test_size=0.20
random_state=42
stratify=y
```

The general workflow is:

```text
Dataset
   ↓
Preprocessing
   ↓
Train/Test Split
   ↓
Training preprocessing
   ↓
Targeted SMOTE
   ↓
Random Forest
   ↓
Evaluation
   ↓
Model Serialization
```

---

# 12. Model Serialization

The trained Random Forest is saved as:

```text
models/intrusion_model.pkl
```

The label encoder is saved as:

```text
models/label_encoder.pkl
```

Separating the model and encoder allows the backend to load the trained classifier and correctly translate encoded predictions back into attack names.

---

# 13. Backend Architecture

The Flask backend provides the integration layer between the machine-learning model and the application.

Main components:

```text
backend/app.py
backend/routes/prediction.py
backend/services/prediction_service.py
backend/services/preprocessing.py
backend/services/risk_service.py
backend/database/
```

---

# 14. Prediction Service

The prediction service:

1. Loads the trained Random Forest.
2. Loads the label encoder.
3. Builds the model input.
4. Aligns the 78 features.
5. Performs prediction.
6. Decodes the predicted class.
7. Calculates confidence.

---

# 15. Feature Alignment

The backend receives features as a dictionary.

The feature-processing service:

```text
Feature dictionary
       ↓
Name normalization
       ↓
Canonical feature mapping
       ↓
Model feature ordering
       ↓
78-feature NumPy vector
       ↓
Random Forest
```

The trained model's expected feature names are used to preserve the required feature ordering.

---

# 16. Risk Assessment

The risk service converts the model's prediction and confidence into an operational risk level.

The current logic is:

```text
BENIGN / Normal → LOW

Attack + confidence >= 0.90 → CRITICAL

Attack + confidence >= 0.75 → HIGH

Attack + confidence >= 0.50 → MEDIUM

Attack + confidence < 0.50 → LOW
```

This makes risk assessment an application-level layer separate from the machine-learning classifier.

---

# 17. API Design

The system exposes:

```text
POST /predict
```

Request:

```json
{
  "source_ip": "...",
  "destination_ip": "...",
  "protocol": "...",
  "features": {
    "78 numerical features": "..."
  }
}
```

Response:

```json
{
  "attack_type": "BENIGN",
  "confidence": 0.7867,
  "risk_level": "LOW"
}
```

---

# 18. Database

The backend uses SQLite through SQLAlchemy.

Each prediction can be stored with:

```text
Source IP
Destination IP
Protocol
Attack Type
Confidence
Risk Level
```

This provides persistent information for logs, statistics, alerts, and future analysis.

---

# 19. Testing

Testing was performed at multiple levels.

## Model loading

The backend successfully loaded:

```text
RandomForestClassifier
```

The trained model expects:

```text
78 features
```

The label encoder contains seven classes:

```text
BENIGN
Bot
Brute Force
DDoS
DoS
PortScan
Web Attack
```

## API testing

The `/predict` endpoint was tested using an HTTP request.

The endpoint returned:

```text
HTTP 200
```

with a response containing:

```text
attack_type
confidence
risk_level
```

Example:

```json
{
  "attack_type": "BENIGN",
  "confidence": 0.7866666666666666,
  "risk_level": "LOW"
}
```

---

# 20. Model Evaluation

The final model should be evaluated using a held-out test set.

The following metrics should be included:

| Metric | Result |
|---|---:|
| Accuracy | **INSERT ACTUAL VALUE** |
| Macro Precision | **INSERT ACTUAL VALUE** |
| Macro Recall | **INSERT ACTUAL VALUE** |
| Macro F1 | **INSERT ACTUAL VALUE** |

Per-class results:

| Class | Precision | Recall | F1 |
|---|---:|---:|---:|
| BENIGN | — | — | — |
| Bot | — | — | — |
| Brute Force | — | — | — |
| DDoS | — | — | — |
| DoS | — | — | — |
| PortScan | — | — | — |
| Web Attack | — | — | — |

A confusion matrix should also be included in the final report.

---

# 21. Results

The most important integration result is:

```text
Model loaded successfully
        ↓
78 features accepted
        ↓
Prediction successful
        ↓
Risk calculated
        ↓
Database logging performed
        ↓
HTTP 200 response
```

This demonstrates successful integration of the machine-learning model into the backend application.

---

# 22. Limitations

The current system has several limitations.

### Dataset limitation

CICIDS2017 represents a particular collection of network traffic and attack scenarios. Real-world traffic may differ.

### Feature dependency

The deployed model requires the same 78 feature definitions used during training.

### Confidence interpretation

The classifier's confidence should not be interpreted as absolute certainty.

### Risk rules

Risk levels are generated using predefined thresholds rather than a separate learned risk model.

### Real-time deployment

Real-time packet capture and feature extraction require additional infrastructure.

---

# 23. Future Scope

Future improvements could include:

- Real-time packet capture.
- Automated flow generation.
- Real-time prediction.
- Explainable AI.
- SHAP-based explanations.
- Model drift detection.
- Automated retraining.
- Additional datasets.
- Advanced anomaly detection.
- Authentication and authorization.
- Production deployment.
- Containerization.
- Improved alert correlation.

---

# 24. Conclusion

The project demonstrates the integration of machine learning with a practical cybersecurity application.

A Random Forest classifier was trained using network-flow data from CICIDS2017 and integrated into a Flask backend. The backend accepts network-flow features, generates an intrusion prediction, calculates confidence, assigns a risk level, stores the result, and returns the information through a REST API.

The successful HTTP test confirms that the trained model can be accessed through the backend API and is ready to be consumed by the remaining application components.
