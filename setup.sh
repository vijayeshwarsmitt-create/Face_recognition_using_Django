#!/bin/bash
# Face Recognition System - Quick Start Script for macOS/Linux

echo "============================================"
echo "Face Recognition System - Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv

echo "[2/4] Activating virtual environment..."
source venv/bin/activate

echo "[3/4] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "[4/4] Setting up database..."
python manage.py migrate
echo "Database created successfully!"
echo ""

echo "Creating superuser (admin account)..."
python manage.py createsuperuser

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://localhost:8000/"
echo "Admin panel: http://localhost:8000/admin/"
echo ""
