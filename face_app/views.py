"""
Views for face recognition app.
"""
import json
import base64
from io import BytesIO
from PIL import Image
import numpy as np

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .models import Person, FaceImage, RecognitionResult
from .face_utils import get_recognition_engine
from .forms import PersonForm


def index(request):
    """Home page with navigation."""
    persons = Person.objects.all()
    recent_recognitions = RecognitionResult.objects.all()[:10]
    
    context = {
        'persons': persons,
        'recent_recognitions': recent_recognitions,
        'total_persons': persons.count(),
    }
    return render(request, 'face_app/index.html', context)


def register_person(request):
    """Register a new person."""
    if request.method == 'POST':
        form = PersonForm(request.POST)
        
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            
            messages.success(request, f'Person "{person.name}" registered successfully!')
            return redirect('add_face_image', person_id=person.id)
        else:
            messages.error(request, 'Please fill in the required fields correctly.')
    else:
        form = PersonForm()
    
    context = {'form': form}
    return render(request, 'face_app/register_person.html', context)


def add_face_image(request, person_id):
    """Upload face images for a person."""
    person = get_object_or_404(Person, pk=person_id)
    engine = get_recognition_engine()
    
    if request.method == 'POST':
        if 'image' not in request.FILES:
            messages.error(request, 'No image provided.')
            return redirect('add_face_image', person_id=person_id)
        
        image_file = request.FILES['image']
        
        try:
            # Verify it's a valid image
            img = Image.open(image_file)
            img_array = np.array(img)
            
            # Convert to RGB if needed
            if len(img_array.shape) == 2:  # Grayscale
                img_array = np.stack([img_array] * 3, axis=-1)
            elif img_array.shape[2] == 4:  # RGBA
                img_array = img_array[:, :, :3]
            
            # Extract face encoding
            encoding = engine.encode_face_from_array(img_array)
            
            if encoding is None:
                messages.error(request, 'No face detected in the image. Please upload a clear photo.')
                return redirect('add_face_image', person_id=person_id)
            
            # Save face image
            face_image = FaceImage.objects.create(person=person, image=image_file)
            face_image.set_encoding(encoding)
            face_image.save()
            
            messages.success(request, f'Face image added to {person.name}.')
            
        except Exception as e:
            messages.error(request, f'Error processing image: {str(e)}')
        
        return redirect('add_face_image', person_id=person_id)
    
    face_images = person.face_images.all()
    context = {
        'person': person,
        'face_images': face_images,
    }
    return render(request, 'face_app/add_face_image.html', context)


def recognize_webcam(request):
    """Real-time face recognition from webcam."""
    persons = Person.objects.prefetch_related('face_images')
    context = {'persons': persons}
    return render(request, 'face_app/recognize_webcam.html', context)


@csrf_exempt
@require_POST
def api_recognize_face(request):
    """API endpoint for real-time face recognition."""
    try:
        data = json.loads(request.body)
        image_data = data.get('image')
        
        if not image_data:
            return JsonResponse({'error': 'No image provided'}, status=400)
        
        # Decode base64 image
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        image = Image.open(BytesIO(image_bytes))
        image_array = np.array(image.convert('RGB'))
        
        # Get face encoding
        engine = get_recognition_engine()
        unknown_encoding = engine.encode_face_from_array(image_array)
        
        if unknown_encoding is None:
            return JsonResponse({
                'status': 'no_face',
                'message': 'No face detected'
            })
        
        # Load all known faces
        known_faces_dict = {}
        for person in Person.objects.prefetch_related('face_images'):
            person_encodings = []
            for face_img in person.face_images.all():
                encoding = face_img.get_encoding()
                if encoding:
                    person_encodings.append(np.array(encoding))
            
            if person_encodings:
                # Use average encoding
                known_faces_dict[person.id] = np.mean(person_encodings, axis=0)
        
        # Recognize face
        matched_id, confidence = engine.recognize_face(unknown_encoding, known_faces_dict)
        
        # Save result
        result_obj = RecognitionResult.objects.create(
            matched_person_id=matched_id,
            confidence=confidence
        )
        
        if matched_id:
            matched_person = Person.objects.get(id=matched_id)
            return JsonResponse({
                'status': 'matched',
                'person_name': matched_person.name,
                'confidence': round(confidence, 4),
                'confidence_level': result_obj.confidence_level,
                'result_id': result_obj.id,
            })
        else:
            return JsonResponse({
                'status': 'unknown',
                'message': 'Face not recognized',
                'confidence': round(confidence, 4),
                'result_id': result_obj.id,
            })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def recognition_history(request):
    """View recognition history."""
    results = RecognitionResult.objects.all()
    
    # Filter by person if specified
    person_id = request.GET.get('person_id')
    if person_id:
        results = results.filter(matched_person_id=person_id)
    
    # Stats
    total_recognitions = results.count()
    matched_count = results.exclude(matched_person__isnull=True).count()
    unknown_count = results.filter(matched_person__isnull=True).count()
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(results, 20)
    page_num = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_num)
    
    context = {
        'page_obj': page_obj,
        'total_recognitions': total_recognitions,
        'matched_count': matched_count,
        'unknown_count': unknown_count,
    }
    return render(request, 'face_app/recognition_history.html', context)


def person_detail(request, person_id):
    """View person details and their faces."""
    person = get_object_or_404(Person, pk=person_id)
    face_images = person.face_images.all()
    recognitions = person.recognition_results.all()[:10]
    
    context = {
        'person': person,
        'face_images': face_images,
        'recognitions': recognitions,
    }
    return render(request, 'face_app/person_detail.html', context)


def delete_person(request, person_id):
    """Delete a person and their faces."""
    person = get_object_or_404(Person, pk=person_id)
    
    if request.method == 'POST':
        person_name = person.name
        person.delete()
        messages.success(request, f'Person "{person_name}" deleted successfully.')
        return redirect('index')
    
    context = {'person': person}
    return render(request, 'face_app/confirm_delete.html', context)
