# ML-Based Network Intrusion Detection System

## Overview

The **ML-Based Network Intrusion Detection System** is a machine-learning-based cybersecurity application designed to identify and classify potentially malicious network traffic.

The system uses the **CICIDS2017** dataset for model development and a trained **Random Forest Classifier** to classify network flows into seven traffic categories:

- BENIGN
- Bot
- Brute Force
- DDoS
- DoS
- PortScan
- Web Attack

The trained machine-learning model is integrated into a Flask backend. The backend exposes a REST API through which network-flow features can be submitted for prediction.

For every prediction, the system returns:

- Predicted attack type
- Model confidence
- Risk level

The prediction is also stored in a SQLite database for historical monitoring and analysis.

---

## Project Objectives

The main objectives of the project are:

1. Develop a machine-learning model for network intrusion detection.
2. Classify network traffic into multiple attack categories.
3. Perform preprocessing and feature engineering without introducing data leakage.
4. Train and optimize a Random Forest classifier.
5. Save the trained model for deployment.
6. Integrate the model into a Flask backend.
7. Provide a REST API for prediction.
8. Calculate a risk level from the model prediction and confidence.
9. Store intrusion predictions in a database.
10. Provide an API that can be consumed by the project frontend.

---

## System Architecture

```text
                    Network Traffic
                           |
                           v
                 Feature Extraction
                           |
                           v
              78 Network Flow Features
                           |
                           v
                 Flask REST API
                    POST /predict
                           |
                           v
              Prediction Service
                           |
                           v
                 Random Forest
                           |
                           v
                  Label Encoder
                           |
                           v
                Attack Prediction
                           |
                           v
                    Confidence
                           |
                           v
                  Risk Assessment
                           |
                           v
                    SQLite Log
                           |
                           v
                    JSON Response
                           |
                           v
                      Frontend
```

---

## Dataset

The model was developed using the **CICIDS2017** intrusion detection dataset.

The preprocessing pipeline performs:

- Column-name cleaning
- Infinite-value handling
- Duplicate removal
- Attack-label normalization
- Unsupported-label filtering
- Class-size control
- Feature/target separation

The final model operates on **78 numerical network-flow features**.

---

## Attack Classes

The final label encoder contains seven classes:

```text
BENIGN
Bot
Brute Force
DDoS
DoS
PortScan
Web Attack
```

The label encoder is stored in:

```text
models/label_encoder.pkl
```

---

## Machine Learning Model

The project uses a **Random Forest Classifier**.

Final training configuration:

```python
RandomForestClassifier(
    n_estimators=150,
    max_depth=20,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)
```

### Why Random Forest?

Random Forest was selected because it:

- Performs well on tabular numerical data.
- Can capture nonlinear relationships.
- Can model interactions between network features.
- Does not require feature scaling for the classifier.
- Provides class probability estimates.
- Can be serialized and deployed easily.
- Is relatively interpretable through feature importance.

---

## Training Process

The dataset is divided using a stratified train/test split:

```python
train_test_split(
    test_size=0.20,
    random_state=42,
    stratify=y
)
```

The preprocessing and training pipeline includes:

```text
Raw Dataset
     |
     v
Data Cleaning
     |
     v
Label Mapping
     |
     v
Feature Processing
     |
     v
Train/Test Split
     |
     v
Training Preprocessing
     |
     v
Targeted SMOTE
     |
     v
Random Forest Training
     |
     v
Model Serialization
```

The trained model is stored as:

```text
models/intrusion_model.pkl
```

The label encoder is stored as:

```text
models/label_encoder.pkl
```

---

## Feature Engineering

The model uses network-flow characteristics such as:

- Destination port
- Flow duration
- Forward packet counts
- Backward packet counts
- Forward packet lengths
- Backward packet lengths
- Flow inter-arrival-time statistics
- TCP flag counts
- Packet-length statistics
- Flow byte rates
- Flow packet rates
- Other CICIDS2017 numerical flow features

The final model input contains:

```text
78 features
```

---

## Leakage Prevention

A major design principle of the project is avoiding data leakage.

A feature should only use information that would be available at the time the prediction is made.

The pipeline therefore avoids using:

- The target label as an input feature.
- Future information unavailable at prediction time.
- Test-set information when calculating training preprocessing statistics.

This makes the trained model more representative of how an intrusion detector would operate in practice.

---

## Backend

The backend is implemented using **Flask**.

### Main application

```text
backend/app.py
```

The Flask application:

- Initializes Flask.
- Configures the SQLite database.
- Enables CORS.
- Registers API blueprints.
- Creates database tables.

### Prediction route

```text
backend/routes/prediction.py
```

### Prediction service

```text
backend/services/prediction_service.py
```

### Feature preprocessing

```text
backend/services/preprocessing.py
```

### Risk assessment

```text
backend/services/risk_service.py
```

---

## Prediction Pipeline

The backend prediction flow is:

```text
Incoming JSON
      |
      v
PredictionRequest validation
      |
      v
Extract features
      |
      v
Build 78-feature input
      |
      v
Random Forest prediction
      |
      v
Label decoding
      |
      v
Confidence calculation
      |
      v
Risk calculation
      |
      v
SQLite logging
      |
      v
JSON response
```

---

## API

### Endpoint

```text
POST /predict
```

Local development URL:

```text
http://127.0.0.1:5000/predict
```

### Request

```json
{
  "source_ip": "192.168.1.10",
  "destination_ip": "192.168.1.20",
  "protocol": "TCP",
  "features": {
    "Destination Port": 443,
    "Flow Duration": 120000
  }
}
```

The `features` object must contain the numerical network-flow features expected by the trained model.

The model requires **78 features**.

The following fields are metadata:

```text
source_ip
destination_ip
protocol
```

They are stored in the database but are not themselves the 78 Random Forest input features.

---

## API Response

A successful request returns:

```json
{
  "attack_type": "BENIGN",
  "confidence": 0.7866666666666666,
  "risk_level": "LOW"
}
```

### Response fields

| Field | Type | Description |
|---|---|---|
| `attack_type` | string | Predicted traffic/attack category |
| `confidence` | float | Highest model probability, between 0 and 1 |
| `risk_level` | string | Application-level risk classification |

---

## Risk Assessment

Risk is calculated separately from the machine-learning prediction.

The current rules are:

| Condition | Risk |
|---|---|
| BENIGN / Normal | LOW |
| Attack confidence >= 0.90 | CRITICAL |
| Attack confidence >= 0.75 | HIGH |
| Attack confidence >= 0.50 | MEDIUM |
| Attack confidence < 0.50 | LOW |

This separates:

```text
Machine Learning
      |
      v
Prediction + Confidence
      |
      v
Application Logic
      |
      v
Risk Level
```

---

## Database

The backend uses SQLite through Flask-SQLAlchemy.

A prediction record contains information such as:

```text
source_ip
destination_ip
protocol
attack_type
confidence
risk_level
```

This provides historical records that can be used by the application's logging, statistics, and alert functionality.

---

## Project Structure

```text
ml-intrusion-detection/
│
├── backend/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── crud.py
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── alerts.py
│   │   ├── analyze.py
│   │   ├── health.py
│   │   ├── logs.py
│   │   ├── performance.py
│   │   ├── prediction.py
│   │   ├── statistics.py
│   │   └── traffic.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── alert_schema.py
│   │   ├── prediction.py
│   │   └── prediction_schema.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── features.py
│   │   ├── prediction_service.py
│   │   ├── preprocessing.py
│   │   ├── risk_service.py
│   │   └── statistics_service.py
│   │
│   ├── __init__.py
│   ├── app.py
│   ├── config.py
│   └── main.py
│
├── ml/
│   ├── evaluate.py
│   ├── feature_engineering.py
│   ├── predict.py
│   ├── preprocessing.py
│   └── train_rf.py
│
├── models/
│   ├── intrusion_model.pkl
│   └── label_encoder.pkl
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_training.ipynb
│   └── 04_model_optimization.ipynb
│
├── scripts/
│   ├── generate_sample_data.py
│   ├── preprocess_data.py
│   ├── setup_database.py
│   ├── test_model.py
│   ├── test_backend_prediction.py
│   ├── test_predict_api.py
│   ├── test_live_api.py
│   └── train_model.py
│
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_database.py
│   └── test_feature_engineering.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Installation

Create and activate the virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If required dependencies are missing:

```bash
pip install Flask Flask-Cors Flask-SQLAlchemy python-dotenv
```

ML dependencies include packages such as:

```text
numpy
pandas
scikit-learn
imbalanced-learn
joblib
```

---

## Running the Backend

From the project root:

```bash
source .venv/bin/activate
```

Run:

```bash
python -m backend.app
```

The backend runs locally on:

```text
http://127.0.0.1:5000
```

### Important

Use:

```bash
python -m backend.app
```

rather than:

```bash
python backend/app.py
```

because the project uses package imports such as:

```python
from backend.database.database import db
```

---

## Testing

The model was first tested independently.

Verified:

```text
Model: RandomForestClassifier
Features: 78
```

The label encoder was also verified:

```text
BENIGN
Bot
Brute Force
DDoS
DoS
PortScan
Web Attack
```

The complete `/predict` endpoint was then tested through HTTP.

Verified result:

```text
Status code: 200
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

## Model Evaluation

Model evaluation should be reported separately from API integration testing.

The following metrics should be included using the actual measured results:

```text
Accuracy: INSERT ACTUAL VALUE
Macro Precision: INSERT ACTUAL VALUE
Macro Recall: INSERT ACTUAL VALUE
Macro F1: INSERT ACTUAL VALUE
```

Per-class precision, recall, F1-score, support, and the confusion matrix should also be included where available.

> The API confidence value is not the same thing as model accuracy.

---

## Limitations

- CICIDS2017 may not represent every modern network environment.
- Real-world network traffic may differ from the training distribution.
- The model requires the same 78 feature definitions used during training.
- Model confidence does not guarantee that a prediction is correct.
- Risk levels are rule-based application logic.
- Real-time packet capture requires additional feature extraction infrastructure.
- The current development setup uses Flask's development server.

---

## Future Work

Possible improvements include:

- Real-time network packet capture.
- Automated network-flow generation.
- Real-time intrusion detection.
- Explainable AI.
- SHAP-based explanations.
- Improved handling of minority attack classes.
- Model drift monitoring.
- Automated model retraining.
- Production deployment.
- Authentication and authorization.
- Advanced alert correlation.

---

## Conclusion

The project demonstrates an end-to-end machine-learning intrusion detection pipeline.

The trained Random Forest model is integrated into a Flask backend that:

1. Receives network-flow features.
2. Aligns them to the required 78-feature representation.
3. Performs intrusion classification.
4. Decodes the predicted class.
5. Calculates model confidence.
6. Calculates an application-level risk level.
7. Stores the prediction.
8. Returns the result through a REST API.

The live `/predict` endpoint has been successfully tested and returned HTTP 200 with a valid prediction response.
