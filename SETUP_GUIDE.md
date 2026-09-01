# Virtual Environment Setup Guide

This guide explains the virtual environment structure for the AI Intrusion Detection System.

## Overview

The project uses **two separate Python virtual environments** to isolate dependencies:

- `backend_venv` - For the Flask REST API backend
- `frontend_venv` - For the Streamlit frontend dashboard

This separation prevents dependency conflicts and allows independent updates.

## Quick Start

### 1. Run the Application

Simply run the provided batch file:

```bash
run.bat
```

This will:
1. Start the Flask backend on `http://127.0.0.1:5000`
2. Start the Streamlit frontend on `http://localhost:8501`

### 2. Access the Application

- **Frontend Dashboard**: Open `http://localhost:8501` in your browser
- **Backend API**: Access `http://127.0.0.1:5000/health` to verify the backend is running

## Manual Setup (If Needed)

If you need to recreate the virtual environments:

### Create Environments

```bash
# Create backend virtual environment
python -m venv backend_venv

# Create frontend virtual environment  
python -m venv frontend_venv
```

### Install Dependencies

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

## Project Structure

```
intrusion-detection/
├── backend/                    # Flask REST API
│   ├── app.py                 # Main Flask application
│   ├── requirements.txt       # Backend dependencies
│   ├── routes/                # API endpoints
│   ├── services/              # Business logic
│   └── database/              # Database models
├── frontend/                   # Streamlit dashboard
│   ├── app.py                 # Main Streamlit app
│   ├── requirements.txt       # Frontend dependencies
│   ├── components/            # UI components
│   ├── views/                 # Page components
│   └── utils/                 # Helper utilities
├── models/                     # ML model artifacts
├── backend_venv/               # Backend Python environment
├── frontend_venv/              # Frontend Python environment
├── run.bat                     # Startup script
├── .env                        # Environment configuration
└── README.md                   # Main documentation
```

## Backend Dependencies

The backend requires these Python packages (see `backend/requirements.txt`):

- **Flask** - Web framework
- **Flask-SQLAlchemy** - Database ORM
- **Flask-CORS** - Cross-origin resource sharing
- **python-dotenv** - Environment variables
- **joblib** - ML model serialization
- **numpy** - Numerical computing
- **pandas** - Data manipulation
- **pydantic** - Data validation

## Frontend Dependencies

The frontend requires these Python packages (see `frontend/requirements.txt`):

- **streamlit** - Web app framework
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **plotly** - Interactive visualizations
- **pillow** - Image processing

## Troubleshooting

### Port Already in Use

If ports 5000 or 8501 are already in use:

1. **Backend**: Edit `backend/app.py` and change `port=5000`
2. **Frontend**: Run with custom port:
   ```bash
   frontend_venv\Scripts\activate
   streamlit run frontend\app.py --server.port=8502
   ```

### Virtual Environment Issues

If you encounter issues with the virtual environments:

1. Delete the problematic environment folder:
   ```bash
   rmdir /s backend_venv
   rmdir /s frontend_venv
   ```

2. Recreate and reinstall:
   ```bash
   python -m venv backend_venv
   python -m venv frontend_venv
   
   backend_venv\Scripts\activate
   pip install -r backend\requirements.txt
   deactivate
   
   frontend_venv\Scripts\activate
   pip install -r frontend\requirements.txt
   deactivate
   ```

### Memory Issues

If you encounter memory errors during installation or runtime:

- Ensure you have at least 4GB of free RAM
- Close other memory-intensive applications
- Consider increasing virtual memory/page file size

### Database Issues

If you encounter database errors:

1. Delete the existing database:
   ```bash
   del instance\intrusion_detection.db
   ```

2. Restart the backend - the database will be recreated automatically.

## Development

### Running Services Separately

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

### Adding New Dependencies

When adding new packages:

1. Activate the appropriate environment
2. Install the package
3. Update the corresponding `requirements.txt`:
   ```bash
   pip freeze > backend\requirements.txt  # or frontend\requirements.txt
   ```

## Best Practices

1. **Never commit virtual environments** - They are excluded in `.gitignore`
2. **Always use the correct environment** - Backend packages in `backend_venv`, frontend in `frontend_venv`
3. **Keep environments updated** - Periodically update packages for security patches
4. **Use version pinning** - For production, pin exact versions in requirements files

## Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Python venv Documentation](https://docs.python.org/3/library/venv.html)