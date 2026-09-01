# AI Intrusion Detection System

A full-stack web application for network intrusion detection using machine learning.

## Project Structure

```
intrusion-detection/
├── backend/              # Flask REST API backend
│   ├── app.py           # Main Flask application
│   ├── requirements.txt # Python dependencies for backend
│   ├── routes/          # API endpoint blueprints
│   ├── services/        # Business logic (ML prediction, preprocessing)
│   └── database/        # Database models and configuration
├── frontend/            # Streamlit dashboard frontend
│   ├── app.py          # Main Streamlit application
│   ├── requirements.txt # Python dependencies for frontend
│   ├── components/      # Reusable UI components
│   ├── views/           # Page components
│   └── utils/           # Helper utilities
├── models/              # ML model artifacts directory
├── backend_venv/        # Backend Python virtual environment
├── frontend_venv/       # Frontend Python virtual environment
├── run.bat              # Startup script for both services
└── .env                 # Environment configuration
```

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Setup & Installation

The project uses separate virtual environments for backend and frontend to isolate dependencies.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd intrusion-detection
```

### 2. Create Virtual Environments (if not already present)

The startup script expects two virtual environments in the project root:

```bash
# Create backend virtual environment
python -m venv backend_venv

# Create frontend virtual environment
python -m venv frontend_venv
```

### 3. Install Dependencies

```bash
# Install backend dependencies
backend_venv\Scripts\activate
pip install -r backend\requirements.txt
deactivate

# Install frontend dependencies
frontend_venv\Scripts\activate
pip install -r frontend\requirements.txt
deactivate
```

### 4. Configure Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Backend Database
DATABASE_URL=sqlite:///intrusion_detection.db

# ML Model Configuration
ML_MODEL_PATH=models/model.joblib

# API Server Configuration
IDS_API_URL=http://127.0.0.1:5000
IDS_API_TIMEOUT=5.0
```

### 5. Add ML Model (Optional)

Place your trained ML model in the `models/` directory. The backend supports:
- `models/model.joblib` (recommended)
- `models/model.pkl`

If no model is present, the system falls back to a heuristic-based detection engine.

## Running the Application

### Quick Start (Recommended)

Use the provided batch script to start both services:

```bash
run.bat
```

This will:
1. Start the Flask backend API on `http://127.0.0.1:5000`
2. Start the Streamlit frontend dashboard on `http://localhost:8501`

### Manual Start

If you prefer to run services separately:

**Terminal 1 - Backend:**
```bash
backend_venv\Scripts\activate
python -m backend.app
```

**Terminal 2 - Frontend:**
```bash
frontend_venv\Scripts\activate
cd frontend
streamlit run app.py
```

## API Endpoints

The backend provides the following REST API endpoints:

- `GET /health` - Health check
- `POST /predict` - Predict intrusion for a single network flow
- `POST /analyze` - Analyze uploaded traffic file (CSV/TXT)
- `GET /alerts` - Get high-risk alerts
- `GET /logs` - Get historical intrusion logs
- `GET /traffic-overview` - Get traffic statistics
- `GET /statistics` - Get dashboard statistics
- `GET /performance` - Get ML model performance metrics

## Features

- **Real-time Detection**: Analyze network traffic for potential intrusions
- **Batch Analysis**: Upload CSV files for bulk traffic analysis
- **Dashboard**: Visualize attack statistics, trends, and model performance
- **Alerts**: Monitor high-risk and critical security events
- **Historical Logs**: Review past detection results
- **ML Model Integration**: Support for scikit-learn, XGBoost, and other models

## Development

### Backend Development

The backend is built with Flask and uses SQLAlchemy for database operations.

```bash
# Activate backend environment
backend_venv\Scripts\activate

# Run with auto-reload
python -m backend.app
```

### Frontend Development

The frontend is built with Streamlit.

```bash
# Activate frontend environment
frontend_venv\Scripts\activate

# Run Streamlit with auto-reload
cd frontend
streamlit run app.py
```

## Virtual Environments

The project maintains two isolated Python environments:

- **`backend_venv`**: Contains Flask, SQLAlchemy, ML libraries (numpy, pandas, joblib, etc.)
- **`frontend_venv`**: Contains Streamlit and visualization libraries (plotly, pandas, etc.)

This separation prevents dependency conflicts and allows independent updates.

## Troubleshooting

### Port Already in Use

If ports 5000 or 8501 are already in use, modify the ports in:
- Backend: `backend/app.py` (change `port=5000`)
- Frontend: Run `streamlit run app.py --server.port=8502`

### Database Issues

If you encounter database errors, delete the existing database:
```bash
del instance\intrusion_detection.db
```
The database will be recreated on the next backend startup.

### Model Not Found

If the ML model is missing, the backend will use a heuristic fallback. To use a real model, place it in `models/model.joblib`.

## License

This project is for educational and demonstration purposes.