# Configuration Hints for Face Recognition System

## Environment Variables (Optional)

Create a `.env` file in the project root for sensitive data:

```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
FACE_ENCODING_MODEL=hog
RECOGNITION_TOLERANCE=0.6
```

## Database Backup & Restore

```bash
# Backup database
python manage.py dumpdata > backup.json

# Restore database
python manage.py loaddata backup.json

# Export specific model
python manage.py dumpdata face_app.Person > persons.json
```

## Deployment Checklist

### Before Going Live

- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Configure ALLOWED_HOSTS
- [ ] Setup HTTPS/SSL
- [ ] Configure proper logging
- [ ] Setup database backups
- [ ] Configure media file storage (AWS S3/etc)
- [ ] Setup email for notifications
- [ ] Add rate limiting
- [ ] Implement user authentication
- [ ] Setup monitoring/alerts
- [ ] Configure CDN for static files

### Production Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {...}
```

## Performance Optimization

### Database
```bash
# Create indexes
python manage.py sqlsequencereset face_app | python manage.py dbshell

# Vacuum SQLite
sqlite3 db.sqlite3 "VACUUM;"
```

### Caching
Add to settings.py:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'face-recognition-cache',
    }
}
```

### Static Files
```bash
# Collect static files
python manage.py collectstatic --noinput

# Minify CSS/JS
npm install -g minify
```

## Face Recognition Tuning

### Model Selection
- **'hog'**: Fast (~100ms), lower accuracy, works on CPU
- **'cnn'**: Slower (~2-5s), higher accuracy, needs GPU

### Tolerance Adjustment
- Lower (0.3): Stricter matching, fewer false positives
- Higher (0.7): Lenient matching, more false positives

```python
# In settings.py
FACE_ENCODING_MODEL = 'hog'
RECOGNITION_TOLERANCE = 0.6
```

## Troubleshooting Advanced Issues

### Memory Issues
```bash
# Monitor memory usage
python -m memory_profiler manage.py

# Optimize: Batch processing, caching, cleanup
```

### GPU Acceleration (Optional)

Install CUDA for CNN model:
```bash
# NVIDIA CUDA Toolkit
# cuDNN library
pip install tensorflow  # or pytorch
```

Then use:
```python
FACE_ENCODING_MODEL = 'cnn'
```

## Logging Configuration

Add to settings.py:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'face_recognition.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'INFO',
    },
}
```

## API Rate Limiting

Install django-ratelimit:
```bash
pip install django-ratelimit
```

Usage:
```python
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='100/h', method='POST')
def api_recognize_face(request):
    ...
```

---

**For more help, check README.md or QUICKSTART.md**
