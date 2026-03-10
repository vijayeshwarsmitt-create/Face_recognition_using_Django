"""
Utilities for face recognition using OpenCV.
"""
import cv2
import numpy as np
from django.conf import settings
import os


class FaceRecognitionEngine:
    """Engine for face recognition operations using OpenCV."""
    
    def __init__(self):
        # Load OpenCV face cascade classifier
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        self.tolerance = settings.RECOGNITION_TOLERANCE

    def encode_face(self, image_path):
        """
        Extract face from an image using simple histogram-based encoding.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            numpy array (histogram) or None if no face found
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                # Use histogram as simple encoding
                hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
                return hist.flatten()
            
            return None
        except Exception:
            return None

    def encode_face_from_array(self, image_array):
        """
        Extract face encoding from a numpy array (from webcam).
        
        Args:
            image_array: numpy array of image in BGR format
            
        Returns:
            numpy array (histogram) or None if no face found
        """
        try:
            if isinstance(image_array, np.ndarray):
                gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
            else:
                gray = cv2.cvtColor(cv2.imread(image_array), cv2.COLOR_BGR2GRAY)
            
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(50, 50))
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                # Resize for consistent encoding
                face_roi = cv2.resize(face_roi, (100, 100))
                hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
                return hist.flatten()
            
            return None
        except Exception:
            return None

    def face_distance(self, known_encodings, unknown_encoding):
        """
        Calculate distance between unknown and known encodings using histogram comparison.
        
        Args:
            known_encodings: list of known face encodings
            unknown_encoding: single unknown face encoding
            
        Returns:
            list of distances
        """
        if not isinstance(known_encodings, list):
            return []
        
        distances = []
        for known_enc in known_encodings:
            # Use histogram comparison (smaller is better match)
            distance = cv2.compareHist(
                unknown_encoding.reshape(-1, 1).astype(np.float32),
                known_enc.reshape(-1, 1).astype(np.float32),
                cv2.HISTCMP_BHATTACHARYYA
            )
            distances.append(distance)
        
        return np.array(distances)

    def recognize_face(self, unknown_encoding, known_faces_dict):
        """
        Match a face against known faces.
        
        Args:
            unknown_encoding: encoding of unknown face
            known_faces_dict: dict with {person_id: encoding}
            
        Returns:
            tuple: (matched_person_id, confidence_score) or (None, 0)
        """
        if not known_faces_dict or unknown_encoding is None:
            return None, 0.0

        known_ids = list(known_faces_dict.keys())
        known_encodings = list(known_faces_dict.values())

        distances = self.face_distance(known_encodings, unknown_encoding)

        if len(distances) == 0:
            return None, 0.0

        # Find best match (smallest distance)
        best_match_index = np.argmin(distances)
        best_distance = distances[best_match_index]
        
        # Convert distance to confidence (0.5 distance = 0.5 confidence)
        confidence = max(0, 1.0 - (best_distance * 2))  # Normalize

        # Match if confidence is above threshold
        if confidence >= (1.0 - self.tolerance):
            return known_ids[best_match_index], confidence
        
        return None, confidence


def get_recognition_engine():
    """Factory function to get face recognition engine."""
    return FaceRecognitionEngine()
