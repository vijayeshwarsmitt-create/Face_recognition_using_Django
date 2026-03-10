# Quick Start Guide - Face Recognition System

## 🚀 Super Quick Start (3 Minutes)

### Windows
```bash
# Double-click setup.bat
setup.bat

# Follow the prompts to create admin account
# Then run:
python manage.py runserver
```

### macOS/Linux
```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh

# Then run:
python manage.py runserver
```

**That's it! Visit http://localhost:8000/**

---

## 📖 Manual Setup Steps

### 1. Python & Virtual Environment
```bash
# Create environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Install Packages
```bash
pip install -r requirements.txt
```

### 3. Database
```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Run
```bash
python manage.py runserver
```

---

## 🎯 First Time Use

1. **Register a Person**
   - Click "Register" → Enter Name → Upload Face Photo
   - Tip: Upload 2-3 clear photos for better accuracy

2. **Recognize Faces**
   - Click "Recognize" → Click "Start"
   - Allow webcam access → System scans and identifies people

3. **View Results**
   - Click "History" → See all recognitions
   - Click person to see their details

---

## 🔧 Common Commands

```bash
# Start server
python manage.py runserver

# Admin panel
http://localhost:8000/admin/
# Username/Password: created during superuser setup

# Reset database
python manage.py flush

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run tests
python manage.py test

# Create superuser again
python manage.py createsuperuser

# Collect static files (production)
python manage.py collectstatic
```

---

## 🐛 Quick Fixes

**Camera not showing?**
- Check browser permissions
- Try Chrome or Firefox
- Refresh the page

**Face not detected?**
- Ensure good lighting
- Clear, unobstructed face
- Larger/closer face photo

**Installation error?**
```bash
# Reinstall requirements
pip install --force-reinstall -r requirements.txt

# Fix dlib specifically
pip install dlib --only-binary :all:
```

---

## 📱 URLs

- **Home**: http://localhost:8000/
- **Register**: http://localhost:8000/register/
- **Recognition**: http://localhost:8000/recognize/
- **History**: http://localhost:8000/history/
- **Admin**: http://localhost:8000/admin/

---

## 💾 Project Files

```
✅ manage.py                    - Django CLI
✅ requirements.txt              - All dependencies
✅ setup.bat / setup.sh         - Quick setup scripts
✅ .gitignore                   - Git ignore rules
✅ face_recognition_project/    - Django project settings
✅ face_app/                    - Main application
   ✅ models.py                 - Database models
   ✅ views.py                  - View logic
   ✅ urls.py                   - URL routing
   ✅ admin.py                  - Admin config
   ✅ face_utils.py             - Recognition engine
   ✅ forms.py                  - Form validation
   ✅ tests.py                  - Unit tests
   ✅ templates/                - HTML templates
   ✅ static/                   - CSS/JS files
   ✅ migrations/               - Database migrations
✅ README.md                     - Full documentation
✅ QUICKSTART.md                 - This file
```

---

## 🎓 Learn More

- Full README: See README.md
- Django: https://docs.djangoproject.com/
- face_recognition: https://github.com/ageitgey/face_recognition
- Bootstrap: https://getbootstrap.com/

---

**Happy Face Recognition! 👋**
