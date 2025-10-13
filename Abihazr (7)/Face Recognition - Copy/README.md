# 🎭 Real-Time Emotion Detection Camera

A Python-based real-time emotion detection system that uses computer vision to detect human faces and classify emotions with high accuracy. The system only shows detection squares on actual human faces, not on blank spaces or objects.

## ✨ Features

- 🎯 **Accurate Face Detection** - Only shows squares on real human faces
- 😊 **6 Emotion Detection** - Happy, Sad, Angry, Kiss, Laugh, Neutral
- 🎨 **Color-Coded Emotions** - Each emotion has a unique color
- 😀 **Emoji Indicators** - Visual emoji representation for each emotion
- 🚫 **No False Positives** - Advanced validation prevents detection on walls/objects
- 🖱️ **Easy Controls** - Red cross button to close, keyboard shortcuts
- 🪟 **Windows Compatible** - Fixed for Windows camera compatibility

## 🎯 Emotion Detection

| Emotion | Color | Emoji | Trigger |
|---------|-------|-------|---------|
| **Happy** | 🟢 Green | 😊 | Smile with teeth showing |
| **Sad** | 🔴 Red | 😞 | Frown or close eyes |
| **Angry** | 🔴 Dark Red | 😠 | Furrow eyebrows |
| **Kiss** | 🟣 Magenta | 😘 | Pout/pursed lips |
| **Laugh** | 🟡 Yellow | 😂 | Open mouth very wide |
| **Neutral** | 🟡 Cyan | 😐 | Normal expression |

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Webcam/Camera
- OpenCV

### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/emotion-detection-camera.git
cd emotion-detection-camera

# Install dependencies
pip install opencv-python numpy

# Run the camera
python working_emotion_camera.py
```

### VS Code Setup
1. Open the project in VS Code
2. Press `F5` to run with debugger
3. Select "Run Emotion Detection Camera (RECOMMENDED)"
4. Click the green play button ▶️

## 🎮 Controls

- **Click X button** (red cross) - Quit camera
- **Press 'q'** - Quit
- **Press 'ESC'** - Quit
- **Press 's'** - Save screenshot

## 🔬 How It Works

### Face Validation System
The system uses a 7-point validation system to ensure only real human faces are detected:

1. **Face Size Validation** - Must be 50-300 pixels
2. **Aspect Ratio Check** - Must be 0.7-1.4 (width/height)
3. **Eye Detection** - Must detect at least 1 eye
4. **Face Symmetry** - Analyzes left/right symmetry
5. **Texture Analysis** - Checks for human face patterns
6. **Brightness Distribution** - Validates human-like lighting
7. **Contrast Validation** - Ensures proper contrast levels

### Emotion Detection Logic
- **Happy** 😊 - Detects smiles with teeth showing
- **Laugh** 😂 - Detects very wide mouth openings
- **Kiss** 😘 - Detects pout/pursed lips
- **Sad** 😞 - Detects closed eyes or frowning
- **Angry** 😠 - Detects furrowed brows with high contrast
- **Neutral** 😐 - Default when no specific emotion detected

## 📁 Project Structure

```
emotion-detection-camera/
├── .vscode/
│   └── launch.json              # VS Code debug configurations
├── face_recognition_project/    # Original face recognition project
│   ├── capture_dataset.py
│   ├── encode_faces.py
│   ├── recognize.py
│   └── requirements.txt
├── simple_working_camera.py     # Basic face detection
├── working_emotion_camera.py    # Main emotion detection (RECOMMENDED)
└── README.md
```

## 🛠️ Technical Details

### Dependencies
- **OpenCV** - Computer vision and face detection
- **NumPy** - Numerical computing
- **Python 3.7+** - Programming language

### Camera Backend
- **DirectShow** (Windows) - Primary backend for better compatibility
- **Default** - Fallback backend if DirectShow fails

### Performance
- **Real-time processing** - 30 FPS camera feed
- **Low latency** - Immediate emotion detection
- **Stable detection** - Smooth emotion changes with history smoothing

## 🧪 Testing

### Test Different Emotions
1. **😊 Smile broadly** → Should show green "Happy"
2. **😞 Frown or close eyes** → Should show red "Sad"
3. **😠 Furrow eyebrows** → Should show dark red "Angry"
4. **😘 Pucker lips** → Should show magenta "Kiss"
5. **😂 Open mouth wide** → Should show yellow "Laugh"
6. **😐 Keep normal expression** → Should show cyan "Neutral"

### Test Face Validation
- **Point at your face** → Should show colored square with emotion
- **Point at blank wall** → Should show NO square
- **Point at objects** → Should show NO square

## 🔧 Troubleshooting

### Camera Issues
- Ensure no other apps are using the camera
- Check camera permissions in Windows settings
- Try running as administrator

### Dependencies
```bash
pip install --upgrade opencv-python numpy
```

### VS Code Issues
- Install Python extension
- Select correct Python interpreter
- Use debugger (F5) instead of terminal

## 📊 Features Comparison

| Feature | This Project | Other Projects |
|---------|-------------|----------------|
| **Human Face Only** | ✅ Advanced validation | ❌ Shows on objects |
| **6 Emotions** | ✅ Happy, Sad, Angry, Kiss, Laugh, Neutral | ⚠️ Limited emotions |
| **Emoji Indicators** | ✅ Visual emoji display | ❌ Text only |
| **Windows Compatible** | ✅ DirectShow backend | ⚠️ Camera issues |
| **Real-time Stats** | ✅ Validation counters | ❌ No feedback |
| **Easy Controls** | ✅ X button + keyboard | ⚠️ Keyboard only |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV community for computer vision tools
- Python community for excellent libraries
- Contributors and testers

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Open an issue on GitHub
3. Provide detailed error messages and system information

---

**Made with ❤️ for real-time emotion detection**
