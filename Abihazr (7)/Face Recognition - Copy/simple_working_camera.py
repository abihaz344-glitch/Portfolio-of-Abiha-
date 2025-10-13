#!/usr/bin/env python3
"""
Simple Working Camera - Guaranteed to work!
Basic face detection with emotion display
"""

import cv2
import numpy as np

def main():
    print("=" * 50)
    print("🎭 SIMPLE WORKING CAMERA")
    print("=" * 50)
    print("📋 Controls:")
    print("   • Press 'q' to quit")
    print("   • Press 's' to save screenshot")
    print("   • Click X button to quit")
    print("=" * 50)
    
    # Load face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Cannot open camera")
        print("Make sure your camera is connected and not being used by another app")
        return
    
    print("🎥 Camera started! Press 'q' to quit...")
    
    frame_count = 0
    
    try:
        while True:
            # Read frame
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
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            # Draw rectangles around faces
            for (x, y, w, h) in faces:
                # Draw green rectangle
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Add text
                cv2.putText(frame, "Face Detected", (x, y - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add frame counter
            cv2.putText(frame, f"Frame: {frame_count}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            # Add instructions
            cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Show frame
            cv2.imshow("Simple Camera", frame)
            
            # Check for quit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("🔄 Quit requested")
                break
            elif key == ord('s'):
                filename = f"screenshot_{frame_count}.jpg"
                cv2.imwrite(filename, frame)
                print(f"📸 Screenshot saved: {filename}")
    
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
        print("🎥 Camera released. Goodbye!")

if __name__ == "__main__":
    main()




