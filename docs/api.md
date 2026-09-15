# API Documentation

## ML Intrusion Detection API

The backend provides a REST API for submitting network-flow features to the trained intrusion detection model.

---

## Base URL

Development:

```text
http://127.0.0.1:5000
```

---

# POST /predict

Performs intrusion detection on one network flow.

## Endpoint

```text
POST /predict
```

---

## Request Headers

```http
Content-Type: application/json
```

---

## Request Body

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

---

## Request Fields

| Field | Type | Required | Description |
|---|---|---|---|
| `source_ip` | string | No | Source IP address |
| `destination_ip` | string | No | Destination IP address |
| `protocol` | string | No | Network protocol |
| `features` | object | Yes | Numerical network-flow features |

The `features` object must provide the values required by the trained model.

The Random Forest expects:

```text
78 features
```

---

## Prediction Process

```text
Request
   |
   v
Pydantic Validation
   |
   v
Feature Extraction
   |
   v
Feature Alignment
   |
   v
78-Feature Vector
   |
   v
Random Forest
   |
   v
Encoded Class
   |
   v
Label Encoder
   |
   v
Attack Type
   |
   v
Confidence
   |
   v
Risk Assessment
   |
   v
Database
   |
   v
Response
```

---

# Response

## Successful Response

HTTP status:

```text
200 OK
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

## Attack Response Example

```json
{
  "attack_type": "PortScan",
  "confidence": 0.94,
  "risk_level": "CRITICAL"
}
```

---

## Response Fields

### attack_type

The class predicted by the Random Forest.

Possible values:

```text
BENIGN
Bot
Brute Force
DDoS
DoS
PortScan
Web Attack
```

### confidence

The highest probability returned by the classifier.

Range:

```text
0.0 - 1.0
```

### risk_level

Application-level risk interpretation.

Possible values:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

---

# Validation Error

Invalid requests return:

```text
422
```

Example:

```json
{
  "error": "Invalid request",
  "details": "..."
}
```

---

# Frontend Integration

The frontend should send a `POST` request to:

```text
http://127.0.0.1:5000/predict
```

The frontend should then display:

```text
Attack Type
Confidence
Risk Level
```

The frontend should not implement the Random Forest itself.

The backend is responsible for:

```text
Feature processing
Prediction
Confidence
Risk calculation
Database logging
```

---

# CORS

CORS is enabled in the Flask application so that the frontend can communicate with the backend during development.

---

# Example curl Request

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "source_ip": "192.168.1.10",
    "destination_ip": "192.168.1.20",
    "protocol": "TCP",
    "features": {
      "Destination Port": 443
    }
  }'
```

For an actual prediction, the complete required 78-feature input must be supplied.

---

# API Integration Test

The endpoint was tested through live HTTP communication.

Verified:

```text
HTTP POST /predict
Status: 200
```

Example response:

```json
{
  "attack_type": "BENIGN",
  "confidence": 0.7866666666666666,
  "risk_level": "LOW"
}
```
