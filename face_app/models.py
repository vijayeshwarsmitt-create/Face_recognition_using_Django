"""
Models for the face recognition app.
"""
import json
from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    """Model to store person information."""
    name = models.CharField(max_length=255, unique=True)
    age = models.IntegerField(null=True, blank=True)
    place = models.CharField(max_length=255, null=True, blank=True, help_text="Location/City")
    work = models.CharField(max_length=255, null=True, blank=True, help_text="Job title or occupation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (ID: {self.id})"


class FaceImage(models.Model):
    """Model to store face images and their encodings."""
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='face_images')
    image = models.ImageField(upload_to='face_images/')
    face_encoding = models.TextField()  # Store as JSON string
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def set_encoding(self, encoding_array):
        """Save encoding as JSON."""
        self.face_encoding = json.dumps(encoding_array.tolist())

    def get_encoding(self):
        """Load encoding from JSON."""
        if self.face_encoding:
            return json.loads(self.face_encoding)
        return None

    def __str__(self):
        return f"Face of {self.person.name} - {self.uploaded_at}"


class RecognitionResult(models.Model):
    """Model to store recognition results."""
    CONFIDENCE_CHOICES = [
        ('high', 'High (>0.8)'),
        ('medium', 'Medium (0.5-0.8)'),
        ('low', 'Low (<0.5)'),
    ]
    
    matched_person = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recognition_results'
    )
    confidence = models.FloatField()
    confidence_level = models.CharField(
        max_length=10,
        choices=CONFIDENCE_CHOICES,
        default='low'
    )
    recognized_at = models.DateTimeField(auto_now_add=True)
    capture_image = models.ImageField(upload_to='recognition_captures/', null=True, blank=True)

    class Meta:
        ordering = ['-recognized_at']

    def __str__(self):
        if self.matched_person:
            return f"{self.matched_person.name} - {self.confidence:.2f}"
        return f"Unknown - {self.recognized_at}"

    def save(self, *args, **kwargs):
        """Automatically set confidence level based on confidence score."""
        if self.confidence >= 0.8:
            self.confidence_level = 'high'
        elif self.confidence >= 0.5:
            self.confidence_level = 'medium'
        else:
            self.confidence_level = 'low'
        super().save(*args, **kwargs)
