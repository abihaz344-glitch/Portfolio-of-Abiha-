#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Camera Launcher
Easy way to run different camera versions
"""

import sys
import os

def show_menu():
    """Show camera selection menu"""
    print("=" * 60)
    print("🎥 CAMERA LAUNCHER - CHOOSE YOUR CAMERA")
    print("=" * 60)
    print("1. Working Emotion Camera (RECOMMENDED)")
    print("   • 6 Emotions: Happy, Sad, Angry, Kiss, Laugh, Neutral")
    print("   • Fixed emotion detection")
    print("   • Only shows squares on human faces")
    print()
    print("2. Simple ML Camera")
    print("   • 7 Emotions with ML analysis")
    print("   • Facial feature detection")
    print("   • Confidence scores")
    print()
    print("3. Simple Face Detection")
    print("   • Basic face detection only")
    print("   • No emotion detection")
    print()
    print("4. Exit")
    print("=" * 60)

def run_working_camera():
    """Run the working emotion camera"""
    print("🚀 Starting Working Emotion Camera...")
    try:
        import subprocess
        subprocess.run([sys.executable, 'working_emotion_camera.py'])
    except Exception as e:
        print(f"❌ Error: {e}")

def run_simple_ml_camera():
    """Run the simple ML camera"""
    print("🚀 Starting Simple ML Camera...")
    try:
        import subprocess
        subprocess.run([sys.executable, 'simple_ml_camera.py'])
    except Exception as e:
        print(f"❌ Error: {e}")

def run_simple_face_camera():
    """Run the simple face detection camera"""
    print("🚀 Starting Simple Face Detection...")
    try:
        import subprocess
        subprocess.run([sys.executable, 'simple_working_camera.py'])
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main launcher function"""
    while True:
        show_menu()
        
        try:
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == '1':
                run_working_camera()
            elif choice == '2':
                run_simple_ml_camera()
            elif choice == '3':
                run_simple_face_camera()
            elif choice == '4':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
