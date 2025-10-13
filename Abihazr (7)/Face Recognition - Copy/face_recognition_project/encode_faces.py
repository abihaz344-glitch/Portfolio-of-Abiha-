#!/usr/bin/env python3
"""Encode faces from dataset/ and save face encodings to encodings.pickle

Dataset structure:
dataset/
  Person1/
    img1.jpg
    img2.jpg
  Person2/
    ...

Run:
    python encode_faces.py
"""

import os
import face_recognition
import pickle
import cv2

def gather_images(base="dataset"):
    images = []
    labels = []
    for person in os.listdir(base):
        person_dir = os.path.join(base, person)
        if not os.path.isdir(person_dir):
            continue
        for fname in os.listdir(person_dir):
            if not fname.lower().endswith(('.jpg','.jpeg','.png')):
                continue
            images.append(os.path.join(person_dir, fname))
            labels.append(person)
    return images, labels

def main():
    images, labels = gather_images()
    if not images:
        print("No images found in dataset/. Use capture_dataset.py or add folders manually.")
        return
    known_encodings = []
    known_names = []
    for img_path, name in zip(images, labels):
        print("Processing", img_path)
        image = cv2.imread(img_path)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')  # or 'cnn' if you have GPU and dlib built with CUDA
        encs = face_recognition.face_encodings(rgb, boxes)
        for e in encs:
            known_encodings.append(e)
            known_names.append(name)
    data = {"encodings": known_encodings, "names": known_names}
    with open("encodings.pickle", "wb") as f:
        pickle.dump(data, f)
    print("Encodings saved to encodings.pickle. Total encodings:", len(known_encodings))

if __name__ == '__main__':
    main()
