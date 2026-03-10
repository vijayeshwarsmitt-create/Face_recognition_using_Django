# Face Recognition System - Django Web Application

A powerful, full-featured **Face Recognition System** built with Django that allows you to register people, capture their faces, and recognize them in real-time using your webcam. Beautiful, responsive web interface with advanced features.

## 🎯 Features

### Core Features
- ✅ **Person Registration**: Add new people to the system
- ✅ **Face Upload**: Upload multiple face photos per person
- ✅ **Real-time Recognition**: Capture and recognize faces using your webcam
- ✅ **Recognition History**: View all past recognitions with confidence scores
- ✅ **Beautiful UI**: Responsive Bootstrap interface with modern design
- ✅ **Admin Panel**: Manage people and face data via Django admin

### Technical Features
- Face encoding using industry-standard `face_recognition` library
- Real-time webcam integration with JavaScript
- Database storage of face encodings
- RESTful API for face recognition
- Responsive Bootstrap 5 UI with smooth animations
- Automatic confidence level calculation
- Drag-and-drop file upload support

---

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Webcam (for recognition feature)
- Windows/macOS/Linux
- At least 2GB RAM
- Modern web browser

---

## 🚀 Quick Start

### 1. Clone/Download Project
```bash
cd Face_recognition_using_Django
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser  # Create admin account
```

### 5. Run Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000/` in your browser!

---

## 📖 Detailed Installation

### Prerequisites Setup

#### Windows
- Python 3.8+: Download from python.org
- Visual Studio Build Tools (optional, for dlib)

#### macOS
```bash
brew install python3
brew install cmake  # For dlib
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip build-essential cmake
```

### Full Installation Steps

```bash
# 1. Navigate to project
cd Face_recognition_using_Django

# 2. Create virtual environment
python -m venv venv

# 3. Activate environment (Windows)
venv\Scripts\activate
# or macOS/Linux
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Start server
python manage.py runserver
```

---

## 📱 How to Use

### Register a New Person
1. Click **Register** in the navigation
2. Enter the person's name
3. Upload at least 1 clear face photo (more = better accuracy)
4. Click "Upload Photo"
5. Repeat to add more photos

**Tips for better results:**
- Clear, well-lit photos
- Face should be clearly visible
- Multiple angles improve accuracy
- Avoid sunglasses/hats if possible

### Perform Real-Time Recognition
1. Go to **Recognize** section
2. Allow browser to access your webcam
3. Click **Start** button
4. The system will scan and identify people
5. Results shown with confidence scores

### View Recognition History
- Click **History** to see all recognitions
- Filter by person or confidence level
- View detailed statistics

### Manage People
- Click on any person card to view:
  - Their face photos
  - Recognition history
  - Confidence scores
- Add more photos for accuracy
- Delete person if needed

---

## 🗂️ Project Structure

```
Face_recognition_using_Django/
│
├── manage.py                          # Django CLI
├── requirements.txt                   # Dependencies
├── README.md                          # Documentation
│
├── face_recognition_project/          # Main project
│   ├── settings.py                    # Configuration
│   ├── urls.py                        # URL routing
│   ├── wsgi.py                        # WSGI server
│   └── asgi.py                        # ASGI server
│
├── face_app/                          # Django app
│   ├── models.py                      # Database models
│   ├── views.py                       # View logic
│   ├── urls.py                        # App URLs
│   ├── admin.py                       # Admin config
│   ├── face_utils.py                  # Recognition engine
│   ├── migrations/                    # DB migrations
│   ├── templates/face_app/            # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── register_person.html
│   │   ├── add_face_image.html
│   │   ├── recognize_webcam.html
│   │   ├── person_detail.html
│   │   ├── recognition_history.html
│   │   └── confirm_delete.html
│   └── static/face_app/css/
│       └── style.css                  # Custom styles
│
└── media/                             # User uploads
    ├── face_images/
    └── recognition_captures/
```

---

## ⚙️ Configuration

### Django Settings
Edit `face_recognition_project/settings.py`:

```python
# Model: 'hog' (fast) or 'cnn' (slower but more accurate)
FACE_ENCODING_MODEL = 'hog'

# Matching tolerance: 0 (strict) to 1 (lenient)
RECOGNITION_TOLERANCE = 0.6
```

### Database
Default: SQLite (db.sqlite3) - suitable for development
For production, migrate to PostgreSQL or MySQL

---

## 🔌 API Endpoints

### POST /api/recognize/
Recognize a face from image data

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRg..."
}
```

**Response (Match):**
```json
{
  "status": "matched",
  "person_name": "John Doe",
  "confidence": 0.95,
  "confidence_level": "high",
  "result_id": 1
}
```

**Response (Unknown):**
```json
{
  "status": "unknown",
  "confidence": 0.45,
  "result_id": 2
}
```

---

## 🐛 Troubleshooting

### Camera/Webcam Issues
```
Error: Camera not working or not detected

Solutions:
- Grant browser permission for camera
- Try different browser (Chrome, Firefox)
- Restart browser and application
- Check: chrome://flags/#unsafely-treat-insecure-origin
```

### Face Not Detected
```
Error: "No face detected in the image"

Solutions:
- Ensure good lighting
- Face should be clear and unobstructed
- Upload larger/closer face photos
- Try different angles
```

### Installation Errors

**dlib import error:**
```bash
pip install dlib --only-binary :all:
```

**OpenCV errors:**
```bash
pip install --upgrade opencv-python
```

**Pillow errors:**
```bash
pip install --upgrade Pillow
```

### Slow Performance
- Use 'hog' model instead of 'cnn'
- Reduce camera resolution
- Close background applications
- Add more RAM if available

---

## 📊 Database Models

### Person
```python
- name: Unique person identifier
- created_at: Registration timestamp
- updated_at: Last update time
```

### FaceImage
```python
- person: Foreign key to Person
- image: Image file upload
- face_encoding: Numerical face vector (JSON)
- uploaded_at: Upload timestamp
```

### RecognitionResult
```python
- matched_person: Recognized person (nullable)
- confidence: Similarity score (0-1)
- confidence_level: High/Medium/Low
- recognized_at: Recognition timestamp
```

---

## 👤 Admin Access

Access Django admin: `http://localhost:8000/admin/`

Login with superuser credentials

Features:
- Manage persons
- View face images
- See recognition results
- Manage users

---

## 🔒 Security Notes

⚠️ **Important for Production:**
1. Change `SECRET_KEY` in settings.py
2. Set `DEBUG = False`
3. Configure `ALLOWED_HOSTS`
4. Use environment variables for secrets
5. Implement SSL/HTTPS
6. Add rate limiting
7. Backup database regularly
8. Use strong admin password

---

## 💡 Tips & Best Practices

### For Better Recognition Accuracy
- Upload 3-5 clear photos per person
- Vary angles and lighting
- Include photos in different poses
- Avoid masks, sunglasses when possible
- Keep spacing consistent

### For Production Use
- Set up proper logging
- Configure email notifications
- Implement user authentication
- Add API rate limiting
- Use CDN for static files
- Configure proper media storage
- Use database backups

---

## 🚧 Troubleshooting Commands

```bash
# Check Python version
python --version

# Verify virtual environment is active
pip list | head

# Check Django installation
python -m django --version

# Test imports
python -c "import face_recognition; print('OK')"

# Reset database
python manage.py flush

# Collect static files (production)
python manage.py collectstatic --noinput

# Check for migration issues
python manage.py makemigrations --dry-run
```

---

## 📈 Future Enhancements

- [ ] Multi-face detection
- [ ] Attendance system integration
- [ ] Email notifications
- [ ] REST API export
- [ ] Mobile app
- [ ] Real-time counting
- [ ] Integration with security systems

---

## 📢 Support

Need help? Check:
1. README.md (this file)
2. Django documentation: https://docs.djangoproject.com/
3. face_recognition package: https://github.com/ageitgey/face_recognition
4. OpenCV docs: https://docs.opencv.org/

---

## 📄 License

This project is open-source and available for educational and commercial use.

---

## 🎓 Technologies Used

- **Django 4.2**: Web framework
- **Python 3.8+**: Programming language
- **face_recognition**: Face detection & recognition
- **OpenCV**: Computer vision library
- **Bootstrap 5**: UI framework
- **SQLite**: Database
- **JavaScript/HTML5**: Frontend

---

## 🎉 Enjoy Your Face Recognition System!

For issues or improvements, feel free to contribute!

**Happy Recognizing! 👋**