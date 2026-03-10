@echo off
REM Face Recognition System - Quick Start Script for Windows

echo ============================================
echo Face Recognition System - Setup
echo ============================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv

echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/4] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo [4/4] Setting up database...
python manage.py migrate
echo.
echo Database created successfully!
echo.

echo Creating superuser (admin account)...
python manage.py createsuperuser

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Then visit: http://localhost:8000/
echo Admin panel: http://localhost:8000/admin/
echo.
pause
