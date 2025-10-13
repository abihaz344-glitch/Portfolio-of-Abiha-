#!/usr/bin/env python3
"""Capture face images from webcam into dataset/<name>/ folder.

Usage:
    python capture_dataset.py --name "Person Name" --count 30
"""

import os
import cv2
import argparse
import imutils

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def main(name, count):
    save_dir = os.path.join("dataset", name)
    ensure_dir(save_dir)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return
    print("Press 'q' to quit early. Capturing will start in 2 seconds...")
    import time; time.sleep(2)
    taken = 0
    while taken < count:
        ret, frame = cap.read()
        if not ret:
            break
        frame = imutils.resize(frame, width=600)
        cv2.putText(frame, f"Capturing for: {name} ({taken}/{count})", (10,30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
        cv2.imshow("Capture - Press 'c' to capture, 'q' to quit", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('c'):
            fname = os.path.join(save_dir, f"{name}_{taken:03d}.jpg")
            cv2.imwrite(fname, frame)
            print("Saved", fname)
            taken += 1
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    print("Done. Captured", taken, "images.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True, help='Person name (folder will be created)')
    parser.add_argument('--count', type=int, default=20, help='Number of images to capture')
    args = parser.parse_args()
    main(args.name, args.count)
