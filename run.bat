@echo off
echo Starting AI Intrusion Detection System...
echo.
echo =====================================================
echo   Virtual Environments Setup
echo =====================================================
echo.
echo 1. Starting Flask REST API Backend (Port 5000)...
echo    Using virtual environment: backend_venv
start "IDS Backend" cmd /k "call backend_venv\Scripts\activate.bat && python -m backend.app"

echo.
echo 2. Starting Streamlit Frontend Dashboard (Port 8501)...
echo    Using virtual environment: frontend_venv
timeout /t 2 >nul
call frontend_venv\Scripts\activate.bat && cd frontend && streamlit run app.py
