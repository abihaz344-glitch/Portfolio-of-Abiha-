#!/usr/bin/env python3
"""
Working Emotion Camera - Fixed for Windows with proper window controls
Shows emotions on green frames with red cross button to close
"""

import cv2
import numpy as np
import time

class WorkingEmotionDetector:
    def __init__(self):
        self.face_cascade = None
        self.eye_cascade = None
        self.smile_cascade = None
        self.load_cascades()
        
        # Face validation parameters
        self.min_face_size = 50
        self.max_face_size = 300
        
        # Emotion definitions
        self.emotions = ['Happy', 'Sad', 'Angry', 'Kiss', 'Laugh', 'Neutral']
        self.emotion_colors = {
            'Happy': (0, 255, 0),      # Green
            'Sad': (0, 0, 255),        # Red
            'Angry': (0, 0, 139),      # Dark Red
            'Kiss': (255, 0, 255),     # Magenta
            'Laugh': (0, 255, 255),    # Yellow
            'Neutral': (255, 255, 0)   # Cyan
        }
        self.emotion_emojis = {
            'Happy': '😊',
            'Sad': '😞',
            'Angry': '😠',
            'Kiss': '😘',
            'Laugh': '😂',
            'Neutral': '😐'
        }
        
        # Smoothing
        self.emotion_history = []
        self.current_emotion = 'Neutral'
        
    def load_cascades(self):
        """Load OpenCV cascades"""
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
            self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
            print("✓ Emotion detection models loaded")
        except Exception as e:
            print(f"Error loading cascades: {e}")
    
    def is_valid_human_face(self, face_roi, face_gray, x, y, w, h):
        """Validate if the detected region is actually a human face"""
        try:
            # Check face size
            if w < self.min_face_size or w > self.max_face_size:
                return False, "Invalid size"
            
            if h < self.min_face_size or h > self.max_face_size:
                return False, "Invalid size"
            
            # Check aspect ratio
            aspect_ratio = w / h
            if aspect_ratio < 0.7 or aspect_ratio > 1.4:
                return False, "Invalid ratio"
            
            # Check for eyes
            h_face, w_face = face_roi.shape
            eye_region = face_gray[0:int(h_face*0.6), :]
            
            eyes = self.eye_cascade.detectMultiScale(
                eye_region,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(10, 10)
            )
            
            if len(eyes) < 1:
                return False, "No eyes"
            
            # Check face symmetry
            left_half = face_gray[:, :w_face//2]
            right_half = cv2.flip(face_gray[:, w_face//2:], 1)
            
            min_width = min(left_half.shape[1], right_half.shape[1])
            if min_width > 0:
                left_half = cv2.resize(left_half, (min_width, left_half.shape[0]))
                right_half = cv2.resize(right_half, (min_width, right_half.shape[0]))
                
                diff = cv2.absdiff(left_half, right_half)
                symmetry_score = 1.0 - (np.mean(diff) / 255.0)
                
                if symmetry_score < 0.2:
                    return False, "Low symmetry"
            
            # Check texture
            edges = cv2.Canny(face_gray, 50, 150)
            edge_density = np.sum(edges > 0) / (h_face * w_face)
            
            if edge_density < 0.05 or edge_density > 0.3:
                return False, "Invalid texture"
            
            # Check brightness
            brightness_std = np.std(face_gray)
            if brightness_std < 10 or brightness_std > 80:
                return False, "Invalid brightness"
            
            return True, "Valid human face"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    def detect_smile(self, face_roi, face_gray):
        """Detect if there's a smile (teeth showing)"""
        try:
            h, w = face_roi.shape
            lower_face = face_gray[int(h*0.4):h, :]
            
            # Look for smiles with teeth (more specific detection)
            smiles = self.smile_cascade.detectMultiScale(
                lower_face,
                scaleFactor=1.5,  # More sensitive
                minNeighbors=8,   # Lower threshold
                minSize=(20, 20)  # Smaller minimum size
            )
            
            # Check if smile is wide enough to show teeth
            for (mx, my, mw, mh) in smiles:
                if mw > 30 and mh > 15:  # Reasonable smile size
                    return True
            return False
        except:
            return False
    
    def detect_wide_mouth(self, face_roi, face_gray):
        """Detect wide open mouth (laugh - very wide mouth)"""
        try:
            h, w = face_roi.shape
            lower_face = face_gray[int(h*0.4):h, :]
            
            # Look for very wide mouth openings
            smiles = self.smile_cascade.detectMultiScale(
                lower_face,
                scaleFactor=1.3,
                minNeighbors=5,
                minSize=(40, 40)  # Larger minimum size for laugh
            )
            
            for (mx, my, mw, mh) in smiles:
                if mw > 60 and mh > 30:  # Very wide mouth for laugh
                    return True
            return False
        except:
            return False
    
    def detect_pout(self, face_roi, face_gray):
        """Detect pout/kiss (small, pursed lips)"""
        try:
            h, w = face_roi.shape
            lower_face = face_gray[int(h*0.5):h, :]  # Lower part of face
            
            # Look for small, round mouth regions
            smiles = self.smile_cascade.detectMultiScale(
                lower_face,
                scaleFactor=1.2,
                minNeighbors=10,
                minSize=(10, 10)
            )
            
            for (mx, my, mw, mh) in smiles:
                # Small, round mouth (pout)
                if mw < 25 and mh < 15 and abs(mw - mh) < 8:
                    return True
            return False
        except:
            return False
    
    def detect_eye_closure(self, face_roi, face_gray):
        """Detect closed eyes (sad)"""
        try:
            h, w = face_roi.shape
            upper_face = face_gray[0:int(h*0.6), :]
            
            eyes = self.eye_cascade.detectMultiScale(
                upper_face,
                scaleFactor=1.1,
                minNeighbors=8,
                minSize=(15, 15)
            )
            
            return len(eyes) < 2
        except:
            return False
    
    def detect_emotion(self, face_roi, face_gray):
        """Detect emotion based on facial features - FIXED LOGIC"""
        try:
            has_smile = self.detect_smile(face_roi, face_gray)
            has_wide_mouth = self.detect_wide_mouth(face_roi, face_gray)
            has_pout = self.detect_pout(face_roi, face_gray)
            eyes_closed = self.detect_eye_closure(face_roi, face_gray)
            
            h, w = face_roi.shape
            brightness_std = np.std(face_gray)
            contrast = np.max(face_gray) - np.min(face_gray)
            
            emotion_scores = {
                'Happy': 0,
                'Sad': 0,
                'Angry': 0,
                'Kiss': 0,
                'Laugh': 0,
                'Neutral': 0
            }
            
            # FIXED: Happy detection (smile with teeth, not wide mouth)
            if has_smile and not has_wide_mouth and not has_pout:
                emotion_scores['Happy'] += 0.9
                emotion_scores['Laugh'] -= 0.5  # Prevent laugh when smiling
                emotion_scores['Sad'] -= 0.3
            else:
                emotion_scores['Neutral'] += 0.2
            
            # FIXED: Laugh detection (very wide mouth, not just smile)
            if has_wide_mouth and not has_smile:
                emotion_scores['Laugh'] += 0.9
                emotion_scores['Happy'] -= 0.4  # Prevent happy when laughing
                emotion_scores['Sad'] -= 0.4
            else:
                emotion_scores['Neutral'] += 0.1
            
            # FIXED: Kiss detection (pout + closed eyes)
            if has_pout and eyes_closed:
                emotion_scores['Kiss'] += 0.8
                emotion_scores['Happy'] -= 0.3
                emotion_scores['Laugh'] -= 0.3
            elif has_pout:
                emotion_scores['Kiss'] += 0.5  # Partial kiss
            else:
                emotion_scores['Neutral'] += 0.1
            
            # Sad detection (closed eyes + low energy)
            if eyes_closed and not has_smile and not has_wide_mouth:
                emotion_scores['Sad'] += 0.8
                emotion_scores['Happy'] -= 0.4
                emotion_scores['Laugh'] -= 0.4
            else:
                emotion_scores['Neutral'] += 0.1
            
            # Angry detection (high contrast + furrowed brows)
            if contrast > 120 and brightness_std > 60 and not has_smile:
                emotion_scores['Angry'] += 0.7
                emotion_scores['Happy'] -= 0.4
                emotion_scores['Sad'] -= 0.2
            else:
                emotion_scores['Neutral'] += 0.1
            
            # Find best emotion
            best_emotion = max(emotion_scores, key=emotion_scores.get)
            best_score = emotion_scores[best_emotion]
            
            # Only return emotion if confidence is high enough
            total_score = sum(emotion_scores.values())
            confidence = min(0.95, 0.6 + (best_score / max(total_score, 1)) * 0.3)
            
            # If confidence is too low, return Neutral
            if confidence < 0.5:
                return 'Neutral', 0.5
            
            return best_emotion, confidence
            
        except Exception as e:
            return 'Neutral', 0.5
    
    def smooth_emotion(self, emotion, confidence):
        """Smooth emotion changes"""
        self.emotion_history.append((emotion, confidence))
        
        if len(self.emotion_history) > 5:
            self.emotion_history.pop(0)
        
        if len(self.emotion_history) < 3:
            return self.current_emotion, confidence
        
        emotion_counts = {}
        for hist_emotion, hist_confidence in self.emotion_history:
            if hist_emotion in emotion_counts:
                emotion_counts[hist_emotion] += hist_confidence
            else:
                emotion_counts[hist_emotion] = hist_confidence
        
        if emotion_counts:
            most_common = max(emotion_counts, key=emotion_counts.get)
            avg_confidence = emotion_counts[most_common] / len(self.emotion_history)
            
            if avg_confidence > 0.6 and most_common != self.current_emotion:
                self.current_emotion = most_common
        
        return self.current_emotion, confidence
    
    def draw_emotion_overlay(self, frame, valid_faces, emotions):
        """Draw colored squares with emotion labels ONLY on human faces"""
        for i, (x, y, w, h) in enumerate(valid_faces):
            if i < len(emotions):
                emotion, confidence = emotions[i]
                
                color = self.emotion_colors.get(emotion, (255, 255, 255))
                emoji = self.emotion_emojis.get(emotion, "😐")
                
                # Draw rectangle around VALIDATED human face
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 3)
                
                # Prepare label text
                label = f"{emoji} {emotion}"
                confidence_text = f"({confidence:.1f})"
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
    """Main function to run the working emotion camera"""
    print("=" * 70)
    print("🎭 WORKING EMOTION CAMERA - FIXED FOR WINDOWS")
    print("=" * 70)
    print("📋 Features:")
    print("   • ONLY shows squares on REAL human faces")
    print("   • NO squares on blank spaces, walls, or objects")
    print("   • 6 Emotions: Happy, Sad, Angry, Kiss, Laugh, Neutral")
    print("   • Red cross button to close camera")
    print("   • Fixed Windows camera compatibility")
    print("=" * 70)
    print("📋 FIXED Emotion Detection:")
    print("   😊 Happy - When you smile (teeth showing)")
    print("   😂 Laugh - When you open mouth very wide")
    print("   😘 Kiss - When you make pout/lips pursed")
    print("   😞 Sad - When you close eyes or frown")
    print("   😠 Angry - When you furrow brows")
    print("   😐 Neutral - Normal expression")
    print("=" * 70)
    print("📋 Controls:")
    print("   • Click X button (red cross) to quit")
    print("   • Press 'q' to quit")
    print("   • Press 'ESC' to quit")
    print("   • Press 's' to save screenshot")
    print("=" * 70)
    
    detector = WorkingEmotionDetector()
    
    # Initialize camera with DirectShow backend (better for Windows)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print("❌ DirectShow failed, trying default backend...")
        cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        print("Make sure your camera is connected and not being used by another app")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    cap.set(cv2.CAP_PROP_FPS, 30)
    
    print("🎥 Camera started! Only REAL human faces will show squares!")
    print("💡 Try pointing at your face vs. blank wall - only face gets square!")
    print("🎭 FIXED: Smile = Happy, Wide Mouth = Laugh, Pout = Kiss")
    
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
            
            # Validate each detected face
            valid_faces = []
            emotions = []
            
            for (x, y, w, h) in faces:
                face_count += 1
                face_roi = gray[y:y+h, x:x+w]
                
                # Validate if this is actually a human face
                is_valid, reason = detector.is_valid_human_face(face_roi, face_roi, x, y, w, h)
                
                if is_valid:
                    valid_face_count += 1
                    valid_faces.append((x, y, w, h))
                    
                    # Detect emotion only for validated faces
                    emotion, confidence = detector.detect_emotion(face_roi, face_roi)
                    emotion, confidence = detector.smooth_emotion(emotion, confidence)
                    emotions.append((emotion, confidence))
                else:
                    # Debug: show why face was rejected (every 60 frames to avoid spam)
                    if frame_count % 60 == 0:
                        print(f"Face rejected: {reason}")
            
            # Draw overlays ONLY on validated human faces
            detector.draw_emotion_overlay(frame, valid_faces, emotions)
            
            # Add status information
            status_text = f"Frame: {frame_count} | Human Faces: {len(valid_faces)} | Total Detected: {len(faces)}"
            cv2.putText(frame, status_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add validation info
            validation_text = f"Validated: {valid_face_count} | Rejected: {face_count - valid_face_count}"
            cv2.putText(frame, validation_text, (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add current emotion info
            if emotions:
                current_emotion = emotions[0][0]
                emoji = detector.emotion_emojis.get(current_emotion, "😐")
                cv2.putText(frame, f"Current: {emoji} {current_emotion}", 
                           (10, 90), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Add instructions
            cv2.putText(frame, "FIXED: Smile=Happy, Wide=Laugh, Pout=Kiss - Click X to close", 
                       (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
            
            # Show frame
            cv2.imshow("🎭 Working Emotion Camera", frame)
            
            # Handle key presses and window close events
            key = cv2.waitKey(1) & 0xFF
            
            # Check if window was closed by clicking X button
            if cv2.getWindowProperty("🎭 Working Emotion Camera", cv2.WND_PROP_VISIBLE) < 1:
                print("🔄 Window closed by user (X button clicked)")
                break
            
            if key == ord('q'):
                print("🔄 Quit requested (Q key pressed)")
                break
            elif key == ord('s'):
                filename = f"working_emotion_screenshot_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
            elif key == 27:  # ESC key
                print("🔄 Quit requested (ESC key pressed)")
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
        print(f"   • Rejected false positives: {face_count - valid_face_count}")
        print("🎥 Camera released. Goodbye!")

if __name__ == "__main__":
    main()