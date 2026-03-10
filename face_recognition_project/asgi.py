"""
Asynchronous Server Gateway Interface config for face_recognition_project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_recognition_project.settings')
application = get_asgi_application()
