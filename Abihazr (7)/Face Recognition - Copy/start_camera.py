#!/usr/bin/env python3
"""
Super Simple Camera Starter
Just run this to start the camera
"""

print("🚀 Starting Camera...")
print("📹 Opening Emotion Detection Camera...")

try:
    # Import and run the working camera
    import working_emotion_camera
    working_emotion_camera.main()
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔄 Trying alternative method...")
    
    # Alternative: run as subprocess
    import subprocess
    import sys
    subprocess.run([sys.executable, 'working_emotion_camera.py'])
