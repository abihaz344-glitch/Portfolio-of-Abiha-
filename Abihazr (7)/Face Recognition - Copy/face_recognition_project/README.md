# Face Recognition Project (Python - Dataset based)

This project uses `face_recognition` (dlib-based) + `opencv-python` to perform simple face recognition
from a webcam using a dataset folder of images.

--- Files included
- `capture_dataset.py` : Capture images for a person using your webcam.
- `encode_faces.py` : Process dataset and create `encodings.pickle`.
- `recognize.py` : Real-time recognition using webcam and `encodings.pickle`.
- `requirements.txt` : Python dependencies.
- `dataset/` : (empty) place subfolders named after people, or use `capture_dataset.py`.

--- Quick start (Linux / macOS / WSL / Windows with Python)
1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

> **Note:** `face_recognition` depends on `dlib`. On some systems (Windows) installing `dlib` from pip can be difficult.
If you hit issues, search for prebuilt dlib wheels or follow platform-specific install guides.

3. Capture images for each person:
   ```bash
   python capture_dataset.py --name "Alice" --count 20
   ```
   This will create `dataset/Alice/` with captured face images.

4. Encode faces:
   ```bash
   python encode_faces.py
   ```
   Produces `encodings.pickle`.

5. Run real-time recognition:
   ```bash
   python recognize.py
   ```

--- Folder structure
```
face_recognition_project/
├─ capture_dataset.py
├─ encode_faces.py
├─ recognize.py
├─ requirements.txt
├─ README.md
└─ dataset/
```

--- License
MIT
