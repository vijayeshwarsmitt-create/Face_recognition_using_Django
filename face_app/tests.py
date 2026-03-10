"""
Tests for face_app.
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Person, FaceImage, RecognitionResult


class PersonModelTests(TestCase):
    """Test Person model."""
    
    def setUp(self):
        """Set up test data."""
        self.person = Person.objects.create(name='John Doe')
    
    def test_person_creation(self):
        """Test creating a person."""
        self.assertEqual(self.person.name, 'John Doe')
        self.assertTrue(self.person.created_at)
    
    def test_person_str(self):
        """Test person string representation."""
        self.assertEqual(str(self.person), 'John Doe')


class ViewTests(TestCase):
    """Test view functions."""
    
    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.person = Person.objects.create(name='Jane Smith')
    
    def test_index_page(self):
        """Test home page loads."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('person', response.context)
    
    def test_register_person_get(self):
        """Test register person page."""
        response = self.client.get(reverse('register_person'))
        self.assertEqual(response.status_code, 200)
    
    def test_person_detail(self):
        """Test person detail page."""
        response = self.client.get(
            reverse('person_detail', args=[self.person.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['person'], self.person)
