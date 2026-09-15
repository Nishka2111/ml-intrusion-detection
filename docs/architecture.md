# System Architecture

## 1. Overview

The ML-Based Network Intrusion Detection System follows a modular architecture in which the machine-learning model, backend API, database, and frontend are separated into distinct components.

The architecture is designed so that:

- The ML model is responsible for intrusion classification.
- The backend provides the application and API layer.
- The database stores prediction history.
- The risk service converts predictions into operational risk levels.
- The frontend consumes the backend API.

The overall architecture is:

```text
                         ┌──────────────────────┐
                         │       FRONTEND       │
                         │   Security Dashboard │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP POST
                                    │ /predict
                                    ▼
                         ┌──────────────────────┐
                         │    FLASK BACKEND     │
                         │                      │
                         │  API / Blueprints    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  REQUEST VALIDATION  │
                         │   PredictionRequest  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │  PREDICTION SERVICE  │
                         │                      │
                         │ Model Loading        │
                         │ Feature Preparation  │
                         │ Prediction            │
                         │ Confidence            │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   RANDOM FOREST      │
                         │      CLASSIFIER      │
                         │                      │
                         │    78 Features       │
                         │     7 Classes        │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    LABEL ENCODER     │
                         │                      │
                         │ Encoded → Attack     │
                         │ Category             │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    RISK SERVICE      │
                         │                      │
                         │ Confidence + Attack  │
                         │        → Risk        │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴───────────┐
                         │                      │
                         ▼                      ▼
                ┌──────────────────┐   ┌──────────────────┐
                │      SQLite      │   │   JSON Response  │
                │   Intrusion Logs │   │                  │
                └──────────────────┘   └────────┬─────────┘
                                                │
                                                ▼
                                           FRONTEND
