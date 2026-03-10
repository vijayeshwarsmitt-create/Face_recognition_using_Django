"""
Forms for face_app.
"""
from django import forms
from .models import Person, FaceImage


class PersonForm(forms.ModelForm):
    """Form for creating/editing a person."""
    
    class Meta:
        model = Person
        fields = ['name', 'age', 'place', 'work']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Full Name',
                'required': 'required'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Age',
                'min': '1',
                'max': '120'
            }),
            'place': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'City/Location (e.g., New York)',
            }),
            'work': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Job Title/Occupation',
            }),
        }


class FaceImageForm(forms.ModelForm):
    """Form for uploading face images."""
    
    image = forms.ImageField(
        label='Face Photo',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        })
    )
    
    class Meta:
        model = FaceImage
        fields = ['image']
