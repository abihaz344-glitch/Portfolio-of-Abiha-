#!/usr/bin/env python3
"""Real-time face recognition using webcam and encodings.pickle

Run:
    python recognize.py
"""

import pickle
import cv2
import face_recognition
import imutils
import time
from collections import Counter

def main():
    # Load encodings
    try:
        with open("encodings.pickle", "rb") as f:
            data = pickle.load(f)
    except Exception as e:
        print("Failed to load encodings.pickle:", e)
        return
    encodings = data.get("encodings", [])
    names = data.get("names", [])
    if not encodings:
        print("No encodings found. Run encode_faces.py first.")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cannot open webcam")
        return

    print("Starting webcam. Press 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = imutils.resize(frame, width=700)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        encs = face_recognition.face_encodings(rgb, boxes)
        names_in_frame = []
        for (top, right, bottom, left), encoding in zip(boxes, encs):
            matches = face_recognition.compare_faces(encodings, encoding, tolerance=0.5)
            name = "Unknown"
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = Counter([names[i] for i in matchedIdxs])
                name = counts.most_common(1)[0][0]
            names_in_frame.append(name)
            # Draw box + label
            cv2.rectangle(frame, (left, top), (right, bottom), (0,255,0), 2)
            y = top - 10 if top - 10 > 10 else top + 10
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,255,0), 2)
        cv2.imshow("Recognition", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
