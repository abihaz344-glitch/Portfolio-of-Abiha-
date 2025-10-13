#!/usr/bin/env python3
"""
ML Data Collector for Emotion Detection
Collects training data for machine learning model
"""

import cv2
import numpy as np
import os
import time
from datetime import datetime

class MLDataCollector:
    def __init__(self):
        self.face_cascade = None
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.current_emotion = 'Neutral'
        self.data_dir = 'emotion_data'
        self.img_size = 48
        
        # Create data directory
        self.create_data_directories()
        self.load_face_cascade()
        
    def create_data_directories(self):
        """Create directories for each emotion"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        
        for emotion in self.emotion_labels:
            emotion_dir = os.path.join(self.data_dir, emotion)
            if not os.path.exists(emotion_dir):
                os.makedirs(emotion_dir)
                print(f"Created directory: {emotion_dir}")
    
    def load_face_cascade(self):
        """Load OpenCV face cascade"""
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            print("✓ Face detection model loaded")
        except Exception as e:
            print(f"Error loading face cascade: {e}")
    
    def is_valid_face(self, face_roi, x, y, w, h):
        """Validate if the detected region is a valid face"""
        try:
            # Check size
            if w < 50 or w > 300 or h < 50 or h > 300:
                return False
            
            # Check aspect ratio
            aspect_ratio = w / h
            if aspect_ratio < 0.7 or aspect_ratio > 1.4:
                return False
            
            return True
        except:
            return False
    
    def preprocess_face(self, face_roi):
        """Preprocess face for training"""
        try:
            # Resize to standard size
            face_resized = cv2.resize(face_roi, (self.img_size, self.img_size))
            
            # Convert to grayscale if not already
            if len(face_resized.shape) == 3:
                face_resized = cv2.cvtColor(face_resized, cv2.COLOR_BGR2GRAY)
            
            return face_resized
        except:
            return None
    
    def save_face_data(self, face_roi, emotion):
        """Save face data to appropriate directory"""
        try:
            processed_face = self.preprocess_face(face_roi)
            if processed_face is None:
                return False
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = f"{emotion}_{timestamp}.jpg"
            filepath = os.path.join(self.data_dir, emotion, filename)
            
            # Save image
            cv2.imwrite(filepath, processed_face)
            return True
        except Exception as e:
            print(f"Error saving face data: {e}")
            return False
    
    def collect_data(self):
        """Main data collection function"""
        print("=" * 70)
        print("📊 ML DATA COLLECTOR FOR EMOTION DETECTION")
        print("=" * 70)
        print("📋 Instructions:")
        print("   • Press number keys 1-7 to select emotion")
        print("   • Press SPACE to capture current face")
        print("   • Press 'q' to quit")
        print("   • Press 's' to show statistics")
        print("=" * 70)
        print("📋 Emotion Keys:")
        for i, emotion in enumerate(self.emotion_labels, 1):
            print(f"   {i} - {emotion}")
        print("=" * 70)
        
        # Initialize camera
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("❌ Error: Cannot open camera")
            return
        
        # Set camera properties
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print("🎥 Data collection started!")
        print(f"Current emotion: {self.current_emotion}")
        print("Make the expression and press SPACE to capture...")
        
        frame_count = 0
        capture_count = 0
        emotion_counts = {emotion: 0 for emotion in self.emotion_labels}
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Error: Cannot read from camera")
                    break
                
                frame_count += 1
                
                # Resize frame
                frame = cv2.resize(frame, (640, 480))
                
                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Detect faces
                faces = self.face_cascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=6,
                    minSize=(40, 40),
                    flags=cv2.CASCADE_SCALE_IMAGE
                )
                
                # Process faces
                valid_faces = []
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y+h, x:x+w]
                    
                    if self.is_valid_face(face_roi, x, y, w, h):
                        valid_faces.append((x, y, w, h))
                        
                        # Draw rectangle around face
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
                        # Draw emotion label
                        cv2.putText(frame, f"Emotion: {self.current_emotion}", 
                                   (x, y - 10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Add instructions
                cv2.putText(frame, f"Current: {self.current_emotion} | Press SPACE to capture", 
                           (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                
                cv2.putText(frame, "Press 1-7 for emotion, SPACE to capture, 'q' to quit", 
                           (10, frame.shape[0] - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
                
                # Show frame
                cv2.imshow("📊 ML Data Collector", frame)
                
                # Handle key presses
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    print("🔄 Quit requested")
                    break
                elif key == ord('s'):
                    # Show statistics
                    print("\n📊 Data Collection Statistics:")
                    for emotion, count in emotion_counts.items():
                        print(f"   {emotion}: {count} images")
                    print(f"   Total captured: {capture_count}")
                elif key == ord(' '):  # Space bar
                    # Capture current face
                    if valid_faces:
                        face_roi = gray[valid_faces[0][1]:valid_faces[0][1]+valid_faces[0][3], 
                                       valid_faces[0][0]:valid_faces[0][0]+valid_faces[0][2]]
                        
                        if self.save_face_data(face_roi, self.current_emotion):
                            capture_count += 1
                            emotion_counts[self.current_emotion] += 1
                            print(f"✓ Captured {self.current_emotion} image #{emotion_counts[self.current_emotion]}")
                        else:
                            print("❌ Failed to save image")
                    else:
                        print("❌ No valid face detected")
                elif key >= ord('1') and key <= ord('7'):
                    # Change emotion
                    emotion_idx = key - ord('1')
                    if emotion_idx < len(self.emotion_labels):
                        self.current_emotion = self.emotion_labels[emotion_idx]
                        print(f"Changed emotion to: {self.current_emotion}")
                elif key == 27:  # ESC
                    print("🔄 Quit requested")
                    break
        
        except KeyboardInterrupt:
            print("\n⚠️ Interrupted by user")
        
        except Exception as e:
            print(f"❌ Error: {e}")
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
            
            # Final statistics
            print("\n" + "=" * 70)
            print("📊 FINAL DATA COLLECTION STATISTICS")
            print("=" * 70)
            for emotion, count in emotion_counts.items():
                print(f"   {emotion}: {count} images")
            print(f"   Total captured: {capture_count}")
            print("=" * 70)
            print("💡 Next steps:")
            print("   1. Collect more data for each emotion")
            print("   2. Use ml_model_trainer.py to train the model")
            print("   3. Test with ml_emotion_detector.py")
            print("=" * 70)

if __name__ == "__main__":
    collector = MLDataCollector()
    collector.collect_data()
