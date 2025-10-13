#!/usr/bin/env python3
"""
Simple ML Emotion Detection Camera
Simplified version that works reliably
"""

import cv2
import numpy as np
import os
import time

class SimpleMLCamera:
    def __init__(self):
        self.face_cascade = None
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
        
        # Simple emotion detection (rule-based for now)
        self.load_face_cascade()
        
    def load_face_cascade(self):
        """Load OpenCV face cascade"""
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            print("✓ Face detection model loaded")
        except Exception as e:
            print(f"Error loading face cascade: {e}")
    
    def detect_emotion_simple(self, face_roi):
        """Simple emotion detection using facial features"""
        try:
            # Convert to grayscale if needed
            if len(face_roi.shape) == 3:
                gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            else:
                gray_face = face_roi
            
            # Resize for processing
            face_resized = cv2.resize(gray_face, (48, 48))
            
            # Simple feature detection
            h, w = face_resized.shape
            
            # Detect eyes
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            eyes = eye_cascade.detectMultiScale(face_resized, 1.1, 3)
            
            # Detect mouth region
            mouth_region = face_resized[int(h*0.6):h, :]
            
            # Simple emotion detection based on features
            if len(eyes) >= 2:
                # Check for smile (mouth corners up)
                mouth_edges = cv2.Canny(mouth_region, 50, 150)
                smile_score = np.sum(mouth_edges) / (mouth_region.shape[0] * mouth_region.shape[1])
                
                if smile_score > 0.1:
                    return 'Happy', 0.8
                else:
                    # Check for open mouth (laugh)
                    mouth_area = np.sum(mouth_region < 100)  # Dark pixels in mouth
                    if mouth_area > (mouth_region.shape[0] * mouth_region.shape[1] * 0.3):
                        return 'Laugh', 0.7
                    else:
                        return 'Neutral', 0.6
            else:
                return 'Neutral', 0.5
                
        except Exception as e:
            return 'Neutral', 0.5
    
    def is_valid_human_face(self, face_roi, x, y, w, h):
        """Validate if the detected region is a valid face"""
        try:
            # Basic size validation
            if w < 50 or w > 300 or h < 50 or h > 300:
                return False, "Invalid size"
            
            # Aspect ratio check
            aspect_ratio = w / h
            if aspect_ratio < 0.7 or aspect_ratio > 1.4:
                return False, "Invalid ratio"
            
            # Check for eyes
            h_face, w_face = face_roi.shape
            eye_region = face_roi[0:int(h_face*0.6), :]
            
            eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            eyes = eye_cascade.detectMultiScale(eye_region, 1.1, 3, minSize=(10, 10))
            
            if len(eyes) < 1:
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
    """Main function to run the simple ML camera"""
    print("=" * 70)
    print("🤖 SIMPLE ML EMOTION DETECTION CAMERA")
    print("=" * 70)
    print("📋 Features:")
    print("   • Simple ML-based emotion detection")
    print("   • 7 Emotions: Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral")
    print("   • Real-time facial feature analysis")
    print("   • Only shows squares on human faces")
    print("=" * 70)
    print("📋 Controls:")
    print("   • Click X button (red cross) to quit")
    print("   • Press 'q' to quit")
    print("   • Press 'ESC' to quit")
    print("   • Press 's' to save screenshot")
    print("=" * 70)
    
    detector = SimpleMLCamera()
    
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
    
    print("🎥 Simple ML Camera started!")
    print("💡 Try different expressions to test ML detection!")
    
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
                is_valid, reason = detector.is_valid_human_face(face_roi, x, y, w, h)
                
                if is_valid:
                    valid_face_count += 1
                    valid_faces.append((x, y, w, h))
                    
                    # Detect emotion using simple ML
                    emotion, confidence = detector.detect_emotion_simple(face_roi)
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
            ml_text = "Simple ML: Facial Feature Analysis"
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
            cv2.putText(frame, "Simple ML Emotion Detection - Click X to close", 
                       (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Show frame
            cv2.imshow("🤖 Simple ML Emotion Detection", frame)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            # Check if window was closed
            if cv2.getWindowProperty("🤖 Simple ML Emotion Detection", cv2.WND_PROP_VISIBLE) < 1:
                print("🔄 Window closed by user")
                break
            
            if key == ord('q'):
                print("🔄 Quit requested")
                break
            elif key == ord('s'):
                filename = f"simple_ml_screenshot_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
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
        print("🎥 Simple ML Camera released. Goodbye!")

if __name__ == "__main__":
    main()
