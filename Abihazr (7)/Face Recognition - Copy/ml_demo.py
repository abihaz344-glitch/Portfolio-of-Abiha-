#!/usr/bin/env python3
"""
ML Emotion Detection Demo
Quick demo of the machine learning emotion detection system
"""

import cv2
import numpy as np
import os
import time

def check_ml_setup():
    """Check if ML setup is complete"""
    print("🔍 Checking ML Setup...")
    
    # Check dependencies
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow: {tf.__version__}")
    except ImportError:
        print("❌ TensorFlow not installed")
        return False
    
    try:
        import cv2
        print(f"✓ OpenCV: {cv2.__version__}")
    except ImportError:
        print("❌ OpenCV not installed")
        return False
    
    try:
        import numpy as np
        print(f"✓ NumPy: {np.__version__}")
    except ImportError:
        print("❌ NumPy not installed")
        return False
    
    # Check model files
    model_files = ['emotion_model.h5', 'label_encoder.pkl']
    for file in model_files:
        if os.path.exists(file):
            print(f"✓ {file} found")
        else:
            print(f"⚠️ {file} not found (will create new model)")
    
    # Check data directory
    if os.path.exists('emotion_data'):
        print("✓ Training data directory found")
        # Count images
        total_images = 0
        for emotion in ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']:
            emotion_dir = os.path.join('emotion_data', emotion)
            if os.path.exists(emotion_dir):
                count = len([f for f in os.listdir(emotion_dir) if f.endswith(('.jpg', '.jpeg', '.png'))])
                total_images += count
                print(f"   {emotion}: {count} images")
        print(f"✓ Total training images: {total_images}")
    else:
        print("⚠️ Training data directory not found")
    
    return True

def show_ml_menu():
    """Show ML project menu"""
    print("\n" + "=" * 70)
    print("🤖 MACHINE LEARNING EMOTION DETECTION PROJECT")
    print("=" * 70)
    print("📋 Available Scripts:")
    print("   1. ml_emotion_detector.py    - Real-time ML emotion detection")
    print("   2. ml_data_collector.py      - Collect training data")
    print("   3. ml_model_trainer.py       - Train CNN model")
    print("   4. working_emotion_camera.py - Traditional CV approach")
    print("   5. simple_working_camera.py  - Basic face detection")
    print("=" * 70)
    print("📋 Quick Start Guide:")
    print("   1. First run: ml_data_collector.py (collect data)")
    print("   2. Then run: ml_model_trainer.py (train model)")
    print("   3. Finally run: ml_emotion_detector.py (use ML model)")
    print("=" * 70)
    print("📋 VS Code Usage:")
    print("   • Press F5 to open debug panel")
    print("   • Select 'Run ML Emotion Detection (CNN)'")
    print("   • Click play button to run")
    print("=" * 70)

def run_ml_detector():
    """Run the ML emotion detector"""
    print("🚀 Starting ML Emotion Detection...")
    try:
        import subprocess
        subprocess.run(['python', 'ml_emotion_detector.py'])
    except Exception as e:
        print(f"❌ Error running ML detector: {e}")

def run_data_collector():
    """Run the data collector"""
    print("📊 Starting Data Collection...")
    try:
        import subprocess
        subprocess.run(['python', 'ml_data_collector.py'])
    except Exception as e:
        print(f"❌ Error running data collector: {e}")

def run_model_trainer():
    """Run the model trainer"""
    print("🏗️ Starting Model Training...")
    try:
        import subprocess
        subprocess.run(['python', 'ml_model_trainer.py'])
    except Exception as e:
        print(f"❌ Error running model trainer: {e}")

def main():
    """Main demo function"""
    print("🎭 ML Emotion Detection Demo")
    print("=" * 50)
    
    # Check setup
    if not check_ml_setup():
        print("❌ ML setup incomplete. Please install dependencies first.")
        print("Run: pip install -r requirements_ml.txt")
        return
    
    # Show menu
    show_ml_menu()
    
    # Interactive menu
    while True:
        print("\n📋 What would you like to do?")
        print("   1. Run ML Emotion Detection (CNN)")
        print("   2. Collect Training Data")
        print("   3. Train ML Model")
        print("   4. Run Traditional CV Detection")
        print("   5. Run Basic Face Detection")
        print("   6. Check Setup Again")
        print("   7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            run_ml_detector()
        elif choice == '2':
            run_data_collector()
        elif choice == '3':
            run_model_trainer()
        elif choice == '4':
            print("🚀 Starting Traditional CV Detection...")
            try:
                import subprocess
                subprocess.run(['python', 'working_emotion_camera.py'])
            except Exception as e:
                print(f"❌ Error: {e}")
        elif choice == '5':
            print("🚀 Starting Basic Face Detection...")
            try:
                import subprocess
                subprocess.run(['python', 'simple_working_camera.py'])
            except Exception as e:
                print(f"❌ Error: {e}")
        elif choice == '6':
            check_ml_setup()
        elif choice == '7':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-7.")

if __name__ == "__main__":
    main()
