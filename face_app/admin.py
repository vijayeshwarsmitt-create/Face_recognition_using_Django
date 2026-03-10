"""
Admin configuration for face_app.
"""
from django.contrib import admin
from .models import Person, FaceImage, RecognitionResult


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(FaceImage)
class FaceImageAdmin(admin.ModelAdmin):
    list_display = ('person', 'uploaded_at')
    list_filter = ('person', 'uploaded_at')
    search_fields = ('person__name',)
    readonly_fields = ('uploaded_at',)


@admin.register(RecognitionResult)
class RecognitionResultAdmin(admin.ModelAdmin):
    list_display = ('matched_person', 'confidence', 'confidence_level', 'recognized_at')
    list_filter = ('confidence_level', 'recognized_at', 'matched_person')
    search_fields = ('matched_person__name',)
    readonly_fields = ('recognized_at',)
