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
        # Load OpenCV face cascade classifiers (multiple for better detection)
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        # Load alternative cascade for better detection
        alt_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml'
        self.face_cascade_alt = cv2.CascadeClassifier(alt_cascade_path)
        
        self.tolerance = settings.RECOGNITION_TOLERANCE

    def _detect_faces(self, gray, scale=1.2, min_neighbors=4):
        """
        Detect faces with optimized parameters for faster detection.
        
        Args:
            gray: grayscale image
            scale: scale factor for detection (lower = faster, more matches)
            min_neighbors: minimum neighbors for detection (lower = more detection)
            
        Returns:
            array of detected faces
        """
        # Try primary cascade with optimized parameters for speed
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=scale,
            minNeighbors=min_neighbors,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        # If no faces found, try alternative cascade
        if len(faces) == 0:
            faces = self.face_cascade_alt.detectMultiScale(
                gray,
                scaleFactor=scale,
                minNeighbors=min_neighbors,
                minSize=(30, 30),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
        
        # If still no faces, try with more lenient parameters
        if len(faces) == 0:
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=3,
                minSize=(25, 25)
            )
        
        return faces

    def _extract_face_features(self, face_roi):
        """
        Extract enhanced features from face region for better matching.
        
        Args:
            face_roi: grayscale face region
            
        Returns:
            enhanced feature vector
        """
        # Resize for consistent encoding
        face_roi = cv2.resize(face_roi, (100, 100))
        
        # Apply histogram equalization for better matching
        face_roi = cv2.equalizeHist(face_roi)
        
        # Compute histogram
        hist = cv2.calcHist([face_roi], [0], None, [256], [0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        
        # Compute edge features using Sobel
        sobelx = cv2.Sobel(face_roi, cv2.CV_32F, 1, 0, ksize=3)
        sobely = cv2.Sobel(face_roi, cv2.CV_32F, 0, 1, ksize=3)
        edges = np.sqrt(sobelx**2 + sobely**2)
        edge_hist = cv2.calcHist([edges.astype(np.uint8)], [0], None, [128], [0, 256])
        edge_hist = cv2.normalize(edge_hist, edge_hist).flatten()
        
        # Combine features
        combined = np.concatenate([hist, edge_hist])
        return combined

    def encode_face(self, image_path):
        """
        Extract face from an image using enhanced encoding.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            numpy array (enhanced features) or None if no face found
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self._detect_faces(gray)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                return self._extract_face_features(face_roi)
            
            return None
        except Exception:
            return None

    def encode_face_from_array(self, image_array):
        """
        Extract face encoding from a numpy array with fast detection.
        
        Args:
            image_array: numpy array of image in BGR format
            
        Returns:
            numpy array (enhanced features) or None if no face found
        """
        try:
            if isinstance(image_array, np.ndarray):
                if len(image_array.shape) == 3 and image_array.shape[2] == 3:
                    gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
                else:
                    gray = image_array if len(image_array.shape) == 2 else cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = cv2.cvtColor(cv2.imread(image_array), cv2.COLOR_BGR2GRAY)
            
            # Fast detection with optimized parameters
            faces = self._detect_faces(gray, scale=1.15, min_neighbors=3)
            
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                return self._extract_face_features(face_roi)
            
            return None
        except Exception:
            return None

    def face_distance(self, known_encodings, unknown_encoding):
        """
        Calculate distance between unknown and known encodings using multiple metrics.
        
        Args:
            known_encodings: list of known face encodings
            unknown_encoding: single unknown face encoding
            
        Returns:
            list of distances (lower = better match)
        """
        if not isinstance(known_encodings, list):
            return []
        
        distances = []
        for known_enc in known_encodings:
            # Normalize the encodings
            unknown_norm = unknown_encoding / (np.linalg.norm(unknown_encoding) + 1e-8)
            known_norm = known_enc / (np.linalg.norm(known_enc) + 1e-8)
            
            # Compute cosine distance (more reliable than histogram comparison)
            cosine_distance = 1 - np.dot(unknown_norm, known_norm)
            
            # Also use Bhattacharyya for robustness
            bhatta = cv2.compareHist(
                unknown_norm.reshape(-1, 1).astype(np.float32),
                known_norm.reshape(-1, 1).astype(np.float32),
                cv2.HISTCMP_BHATTACHARYYA
            )
            
            # Combine metrics (cosine is weighted more)
            combined_distance = 0.7 * cosine_distance + 0.3 * bhatta
            distances.append(combined_distance)
        
        return np.array(distances)

    def recognize_face(self, unknown_encoding, known_faces_dict):
        """
        Match a face against known faces with improved matching logic.
        
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
        
        # Convert distance to confidence (better scaling)
        # Distance 0 = perfect match (confidence 1.0)
        # Distance 1 = very different (confidence 0.0)
        confidence = max(0, 1.0 - best_distance)

        # Match if confidence is above threshold
        # tolerance 0.6 means we accept distances up to ~0.4 (confidence 0.6)
        confidence_threshold = (1.0 - self.tolerance)
        if confidence >= confidence_threshold:
            return known_ids[best_match_index], confidence
        
        return None, confidence


def get_recognition_engine():
    """Factory function to get face recognition engine."""
    return FaceRecognitionEngine()
