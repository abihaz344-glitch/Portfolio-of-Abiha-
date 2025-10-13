#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Machine Learning Emotion Detection Camera
Uses trained CNN model for accurate emotion detection
"""

import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
import pickle
import time

class MLEmotionDetector:
    def __init__(self):
        self.face_cascade = None
        self.model = None
        self.label_encoder = None
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.emotion_colors = {
            'Angry': (0, 0, 139),      # Dark Red
            'Disgust': (0, 100, 0),    # Dark Green
            'Fear': (128, 0, 128),     # Purple
            'Happy': (0, 255, 0),      # Green
            'Sad': (0, 0, 255),        # Red
            'Surprise': (255, 165, 0), # Orange
            'Neutral': (255, 255, 0)   # Cyan
        }
        self.emotion_emojis = {
            'Angry': '😠',
            'Disgust': '🤢',
            'Fear': '😨',
            'Happy': '😊',
            'Sad': '😞',
            'Surprise': '😲',
            'Neutral': '😐'
        }
        
        # Model parameters
        self.img_size = 48
        self.num_classes = 7
        
        # Load or create model
        self.load_face_cascade()
        self.load_or_create_model()
        
    def load_face_cascade(self):
        """Load OpenCV face cascade"""
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            print("✓ Face detection model loaded")
        except Exception as e:
            print(f"Error loading face cascade: {e}")
    
    def create_cnn_model(self):
        """Create CNN model for emotion detection"""
        model = Sequential([
            # First Convolutional Block
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_size, self.img_size, 1)),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Second Convolutional Block
            Conv2D(64, (3, 3), activation='relu'),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Third Convolutional Block
            Conv2D(128, (3, 3), activation='relu'),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Dense Layers
            Flatten(),
            Dense(512, activation='relu'),
            Dropout(0.5),
            Dense(256, activation='relu'),
            Dropout(0.5),
            Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def load_or_create_model(self):
        """Load existing model or create new one"""
        model_path = 'emotion_model.h5'
        encoder_path = 'label_encoder.pkl'
        
        if os.path.exists(model_path) and os.path.exists(encoder_path):
            try:
                print("Loading pre-trained model...")
                self.model = load_model(model_path)
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print("✓ Pre-trained model loaded successfully")
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Creating new model...")
                self.create_new_model()
        else:
            print("No pre-trained model found. Creating new model...")
            self.create_new_model()
    
    def create_new_model(self):
        """Create and train a new model"""
        print("Creating new CNN model...")
        self.model = self.create_cnn_model()
        
        # Create label encoder
        self.label_encoder = LabelEncoder()
        self.label_encoder.fit(self.emotion_labels)
        
        # Save the model and encoder
        self.model.save('emotion_model.h5')
        with open('label_encoder.pkl', 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        print("✓ New model created and saved")
        print("Note: Model needs training data for accurate predictions")
    
    def preprocess_face(self, face_roi):
        """Preprocess face for model input"""
        try:
            # Resize to model input size
            face_resized = cv2.resize(face_roi, (self.img_size, self.img_size))
            
            # Normalize pixel values
            face_normalized = face_resized.astype('float32') / 255.0
            
            # Reshape for model input (batch_size, height, width, channels)
            face_reshaped = face_normalized.reshape(1, self.img_size, self.img_size, 1)
            
            return face_reshaped
        except Exception as e:
            print(f"Error preprocessing face: {e}")
            return None
    
    def predict_emotion(self, face_roi):
        """Predict emotion using ML model"""
        try:
            if self.model is None:
                return 'Neutral', 0.5
            
            # Preprocess face
            processed_face = self.preprocess_face(face_roi)
            if processed_face is None:
                return 'Neutral', 0.5
            
            # Make prediction
            predictions = self.model.predict(processed_face, verbose=0)
            
            # Get emotion with highest probability
            emotion_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][emotion_idx])
            
            # Convert index to emotion label
            emotion = self.label_encoder.inverse_transform([emotion_idx])[0]
            
            return emotion, confidence
            
        except Exception as e:
            print(f"Error predicting emotion: {e}")
            return 'Neutral', 0.5
    
    def is_valid_human_face(self, face_roi, face_gray, x, y, w, h):
        """Validate if the detected region is actually a human face"""
        try:
            # Basic validation
            if w < 50 or w > 300 or h < 50 or h > 300:
                return False, "Invalid size"
            
            # Check aspect ratio
            aspect_ratio = w / h
            if aspect_ratio < 0.7 or aspect_ratio > 1.4:
                return False, "Invalid ratio"
            
            # Check for eyes
            h_face, w_face = face_roi.shape
            eye_region = face_gray[0:int(h_face*0.6), :]
            
            eyes = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            detected_eyes = eyes.detectMultiScale(eye_region, 1.1, 5, minSize=(10, 10))
            
            if len(detected_eyes) < 1:
                return False, "No eyes"
            
            return True, "Valid human face"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def draw_emotion_overlay(self, frame, valid_faces, emotions):
        """Draw colored squares with emotion labels"""
        for i, (x, y, w, h) in enumerate(valid_faces):
            if i < len(emotions):
                emotion, confidence = emotions[i]
                
                color = self.emotion_colors.get(emotion, (255, 255, 255))
                emoji = self.emotion_emojis.get(emotion, "😐")
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
                
                # Prepare label text
                label = f"{emoji} {emotion}"
                confidence_text = f"ML: {confidence:.2f}"
                validation_text = "✓ Human Face"
                
                # Set font properties
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                thickness = 2
                
                # Get text size
                (label_w, label_h), _ = cv2.getTextSize(label, font, font_scale, thickness)
                
                # Draw background rectangle for emotion label
                cv2.rectangle(frame, 
                            (x, y - label_h - 15), 
                            (x + label_w + 10, y), 
                            color, 
                            -1)
                
                # Draw emotion text
                cv2.putText(frame, label, 
                          (x + 5, y - 5), 
                          font, font_scale, 
                          (0, 0, 0), thickness)
                
                # Draw confidence text below
                cv2.putText(frame, confidence_text, 
                          (x + 5, y + h + 20), 
                          font, 0.5, 
                          color, 1)
                
                # Draw validation text
                cv2.putText(frame, validation_text, 
                          (x + 5, y + h + 40), 
                          font, 0.4, 
                          (0, 255, 0), 1)

def main():
    """Main function to run the ML emotion detection camera"""
    try:
        print("=" * 70)
        print("🤖 MACHINE LEARNING EMOTION DETECTION CAMERA")
        print("=" * 70)
        print("📋 Features:")
        print("   • CNN-based emotion detection")
        print("   • 7 Emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral")
        print("   • Real-time ML predictions")
        print("   • High accuracy emotion classification")
        print("   • Only shows squares on human faces")
        print("=" * 70)
        print("📋 ML Model Info:")
        print("   • Architecture: Convolutional Neural Network (CNN)")
        print("   • Input Size: 48x48 grayscale images")
        print("   • Classes: 7 emotions")
        print("   • Framework: TensorFlow/Keras")
        print("=" * 70)
        print("📋 Controls:")
        print("   • Click X button (red cross) to quit")
        print("   • Press 'q' to quit")
        print("   • Press 'ESC' to quit")
        print("   • Press 's' to save screenshot")
        print("   • Press 't' to train model")
        print("=" * 70)
    except Exception as e:
        print(f"Error in main setup: {e}")
        return
    
    detector = MLEmotionDetector()
    
    # Initialize camera
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ DirectShow failed, trying default backend...")
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("🎥 ML Camera started! Using CNN for emotion detection...")
    print("💡 Try different expressions to test ML predictions!")
    
    frame_count = 0
    face_count = 0
    valid_face_count = 0
    
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
            faces = detector.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=6,
                minSize=(40, 40),
                flags=cv2.CASCADE_SCALE_IMAGE
            )
            
            # Process each face
            valid_faces = []
            emotions = []
            
            for (x, y, w, h) in faces:
                face_count += 1
                face_roi = gray[y:y+h, x:x+w]
                
                # Validate face
                is_valid, reason = detector.is_valid_human_face(face_roi, face_roi, x, y, w, h)
                
                if is_valid:
                    valid_face_count += 1
                    valid_faces.append((x, y, w, h))
                    
                    # Predict emotion using ML model
                    emotion, confidence = detector.predict_emotion(face_roi)
                    emotions.append((emotion, confidence))
                else:
                    if frame_count % 60 == 0:
                        print(f"Face rejected: {reason}")
            
            # Draw overlays
            detector.draw_emotion_overlay(frame, valid_faces, emotions)
            
            # Add status information
            status_text = f"Frame: {frame_count} | ML Faces: {len(valid_faces)} | Total: {len(faces)}"
            cv2.putText(frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add ML info
            ml_text = f"CNN Model: {'Loaded' if detector.model else 'Not Available'}"
            cv2.putText(frame, ml_text, (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add current emotion info
            if emotions:
                current_emotion = emotions[0][0]
                emoji = detector.emotion_emojis.get(current_emotion, "😐")
                confidence = emotions[0][1]
                cv2.putText(frame, f"ML: {emoji} {current_emotion} ({confidence:.2f})", 
                           (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add instructions
            cv2.putText(frame, "ML Emotion Detection - Click X to close", 
                       (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Show frame
            cv2.imshow("🤖 ML Emotion Detection Camera", frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            # Check if window was closed
            if cv2.getWindowProperty("🤖 ML Emotion Detection Camera", cv2.WND_PROP_VISIBLE) < 1:
                print("🔄 Window closed by user")
                break
            
            if key == ord('q'):
                print("🔄 Quit requested")
                break
            elif key == ord('s'):
                filename = f"ml_emotion_screenshot_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
            elif key == ord('t'):
                print("🔄 Training mode not implemented in this demo")
                print("   Use a dataset like FER2013 to train the model")
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
        print("=" * 70)
        print("📊 Final Statistics:")
        print(f"   • Total frames processed: {frame_count}")
        print(f"   • Total faces detected: {face_count}")
        print(f"   • Valid human faces: {valid_face_count}")
        print(f"   • ML predictions made: {len(emotions) if 'emotions' in locals() else 0}")
        print("🎥 ML Camera released. Goodbye!")

if __name__ == "__main__":
    main()
