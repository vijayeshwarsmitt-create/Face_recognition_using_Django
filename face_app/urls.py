"""
URL configuration for face_app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_person, name='register_person'),
    path('person/<int:person_id>/add-face/', views.add_face_image, name='add_face_image'),
    path('person/<int:person_id>/', views.person_detail, name='person_detail'),
    path('person/<int:person_id>/delete/', views.delete_person, name='delete_person'),
    path('recognize/', views.recognize_webcam, name='recognize_webcam'),
    path('api/recognize/', views.api_recognize_face, name='api_recognize_face'),
    path('history/', views.recognition_history, name='recognition_history'),
]
