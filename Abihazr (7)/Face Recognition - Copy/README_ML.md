# 🤖 Machine Learning Emotion Detection Camera

A comprehensive machine learning-based emotion detection system using Convolutional Neural Networks (CNN) and computer vision. This project provides both traditional computer vision methods and advanced ML approaches for accurate emotion recognition.

## 🎯 Project Overview

This project implements a complete ML pipeline for emotion detection:
1. **Data Collection** - Gather training data for different emotions
2. **Model Training** - Train CNN model on collected data
3. **Real-time Detection** - Use trained model for live emotion detection
4. **Performance Analysis** - Evaluate and visualize model performance

## ✨ Features

### 🤖 Machine Learning Features
- **CNN Architecture** - Deep Convolutional Neural Network for emotion classification
- **7 Emotion Classes** - Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral
- **Real-time ML Predictions** - Live emotion detection using trained model
- **Data Augmentation** - Enhanced training with image transformations
- **Model Evaluation** - Comprehensive performance metrics and visualizations

### 🎭 Emotion Detection
- **High Accuracy** - ML-based classification with confidence scores
- **Real-time Processing** - 30 FPS camera feed with ML predictions
- **Color-coded Emotions** - Visual representation with emojis
- **Human Face Validation** - Only detects emotions on actual faces

### 📊 Training & Analysis
- **Interactive Data Collection** - Easy-to-use data gathering interface
- **Model Training Pipeline** - Automated training with callbacks
- **Performance Visualization** - Training history and confusion matrix
- **Model Persistence** - Save and load trained models

## 🚀 Quick Start

### Prerequisites
```bash
# Install Python dependencies
pip install -r requirements_ml.txt
```

### 1. Data Collection
```bash
# Collect training data
python ml_data_collector.py
```
- Press number keys 1-7 to select emotion
- Press SPACE to capture current face
- Collect at least 100 images per emotion for good results

### 2. Model Training
```bash
# Train the CNN model
python ml_model_trainer.py
```
- Automatically loads collected data
- Trains CNN with data augmentation
- Saves trained model and evaluation metrics

### 3. Real-time Detection
```bash
# Run ML emotion detection
python ml_emotion_detector.py
```
- Uses trained model for live predictions
- Shows confidence scores and emotion labels
- Real-time camera feed with ML analysis

## 🏗️ Architecture

### CNN Model Architecture
```
Input: 48x48 grayscale images
├── Conv2D(32) + BatchNorm + ReLU
├── Conv2D(32) + BatchNorm + ReLU
├── MaxPool2D + Dropout(0.25)
├── Conv2D(64) + BatchNorm + ReLU
├── Conv2D(64) + BatchNorm + ReLU
├── MaxPool2D + Dropout(0.25)
├── Conv2D(128) + BatchNorm + ReLU
├── Conv2D(128) + BatchNorm + ReLU
├── MaxPool2D + Dropout(0.25)
├── Conv2D(256) + BatchNorm + ReLU
├── Conv2D(256) + BatchNorm + ReLU
├── MaxPool2D + Dropout(0.25)
├── Flatten
├── Dense(512) + BatchNorm + Dropout(0.5)
├── Dense(256) + BatchNorm + Dropout(0.5)
└── Dense(7) + Softmax
```

### Data Pipeline
```
Raw Images → Preprocessing → Data Augmentation → CNN Training → Model Evaluation
```

## 📁 Project Structure

```
ml-emotion-detection/
├── .vscode/
│   └── launch.json              # VS Code debug configurations
├── emotion_data/                # Training data directory
│   ├── Angry/                   # Angry emotion images
│   ├── Disgust/                 # Disgust emotion images
│   ├── Fear/                    # Fear emotion images
│   ├── Happy/                   # Happy emotion images
│   ├── Sad/                     # Sad emotion images
│   ├── Surprise/                # Surprise emotion images
│   └── Neutral/                 # Neutral emotion images
├── ml_emotion_detector.py       # Main ML detection script
├── ml_data_collector.py         # Data collection script
├── ml_model_trainer.py          # Model training script
├── working_emotion_camera.py    # Traditional CV approach
├── simple_working_camera.py     # Basic face detection
├── requirements_ml.txt          # ML dependencies
├── README_ML.md                 # This file
└── README.md                    # Main project README
```

## 🎮 Usage Guide

### Data Collection (`ml_data_collector.py`)
1. **Run the script**: `python ml_data_collector.py`
2. **Select emotion**: Press 1-7 to choose emotion class
3. **Capture data**: Press SPACE to save current face
4. **Collect variety**: Make different expressions for each emotion
5. **Check statistics**: Press 's' to see collection progress

### Model Training (`ml_model_trainer.py`)
1. **Run the script**: `python ml_model_trainer.py`
2. **Automatic training**: Script loads data and trains model
3. **Monitor progress**: Watch training metrics and validation
4. **View results**: Confusion matrix and training plots
5. **Model saved**: Automatically saves trained model

### Real-time Detection (`ml_emotion_detector.py`)
1. **Run the script**: `python ml_emotion_detector.py`
2. **Point camera at face**: Only human faces get detection
3. **See ML predictions**: Real-time emotion classification
4. **Check confidence**: ML confidence scores displayed
5. **Save screenshots**: Press 's' to capture results

## 🔬 Technical Details

### Dependencies
- **TensorFlow 2.8+** - Deep learning framework
- **OpenCV 4.5+** - Computer vision
- **NumPy 1.21+** - Numerical computing
- **Scikit-learn 1.0+** - Machine learning utilities
- **Matplotlib 3.5+** - Visualization
- **Seaborn 0.11+** - Statistical visualization

### Model Parameters
- **Input Size**: 48x48 grayscale images
- **Classes**: 7 emotions
- **Batch Size**: 32
- **Epochs**: 100 (with early stopping)
- **Optimizer**: Adam (learning rate: 0.001)
- **Loss Function**: Categorical Crossentropy

### Data Augmentation
- **Rotation**: ±10 degrees
- **Translation**: ±10% width/height
- **Horizontal Flip**: Random flipping
- **Zoom**: ±10% scaling

## 📊 Performance Metrics

### Model Evaluation
- **Accuracy**: Classification accuracy on test set
- **Precision**: Per-class precision scores
- **Recall**: Per-class recall scores
- **F1-Score**: Harmonic mean of precision and recall
- **Confusion Matrix**: Visual representation of predictions

### Training Monitoring
- **Training History**: Loss and accuracy over epochs
- **Validation Metrics**: Performance on validation set
- **Early Stopping**: Prevents overfitting
- **Learning Rate Scheduling**: Adaptive learning rate

## 🎯 Emotion Classes

| Emotion | Emoji | Description | Training Tips |
|---------|-------|-------------|---------------|
| **Angry** | 😠 | Furrowed brows, tense expression | Frown, furrow eyebrows |
| **Disgust** | 🤢 | Nose wrinkled, mouth turned down | Wrinkle nose, show disgust |
| **Fear** | 😨 | Wide eyes, open mouth | Open eyes wide, show surprise |
| **Happy** | 😊 | Smile, raised cheeks | Smile broadly, show teeth |
| **Sad** | 😞 | Drooped mouth, downcast eyes | Frown, look down |
| **Surprise** | 😲 | Raised eyebrows, wide eyes | Raise eyebrows, open mouth |
| **Neutral** | 😐 | Relaxed, no strong expression | Keep normal, relaxed face |

## 🛠️ VS Code Integration

### Debug Configurations
1. **Run ML Emotion Detection (CNN)** - Main ML detection
2. **Run ML Data Collector** - Data gathering
3. **Run ML Model Trainer** - Model training
4. **Run Emotion Detection Camera (RECOMMENDED)** - Traditional CV
5. **Run Simple Face Detection** - Basic detection

### Usage in VS Code
1. **Press F5** to open debug panel
2. **Select configuration** from dropdown
3. **Click play button** to run
4. **Use integrated terminal** for output

## 🔧 Troubleshooting

### Common Issues

#### Model Not Loading
```bash
# Check if model files exist
ls -la emotion_model.h5 label_encoder.pkl

# Retrain if missing
python ml_model_trainer.py
```

#### Low Accuracy
- **Collect more data**: Aim for 200+ images per emotion
- **Improve data quality**: Ensure clear, well-lit faces
- **Increase training time**: Adjust epochs in trainer
- **Check data balance**: Ensure equal samples per class

#### Camera Issues
```bash
# Install OpenCV properly
pip install opencv-python-headless

# Check camera permissions
# Ensure no other apps using camera
```

### Performance Optimization
- **GPU Support**: Install TensorFlow with GPU support
- **Batch Size**: Adjust based on available memory
- **Image Size**: Reduce for faster processing
- **Model Architecture**: Simplify for real-time performance

## 📈 Results & Visualization

### Training Plots
- **Accuracy Curve**: Training vs validation accuracy
- **Loss Curve**: Training vs validation loss
- **Confusion Matrix**: Prediction accuracy heatmap
- **Class Distribution**: Data balance visualization

### Real-time Metrics
- **FPS**: Frames per second processing
- **Confidence Scores**: ML prediction confidence
- **Detection Count**: Number of faces detected
- **Model Status**: Loaded/not loaded indicator

## 🤝 Contributing

### Adding New Emotions
1. **Update emotion_labels** in all scripts
2. **Add new emotion directories** in data collection
3. **Retrain model** with new classes
4. **Update visualization** code

### Improving Accuracy
1. **Collect more diverse data**
2. **Experiment with model architecture**
3. **Try different augmentation strategies**
4. **Implement ensemble methods**

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **TensorFlow Team** - Deep learning framework
- **OpenCV Community** - Computer vision library
- **FER2013 Dataset** - Emotion recognition benchmark
- **Python Community** - Excellent ML ecosystem

---

**Built with ❤️ using Machine Learning and Computer Vision**
