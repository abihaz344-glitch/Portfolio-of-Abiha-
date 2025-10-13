#!/usr/bin/env python3
"""
ML Model Trainer for Emotion Detection
Trains CNN model on collected emotion data
"""

import os
import numpy as np
import cv2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from datetime import datetime

class MLModelTrainer:
    def __init__(self):
        self.data_dir = 'emotion_data'
        self.img_size = 48
        self.num_classes = 7
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        
        # Training parameters
        self.batch_size = 32
        self.epochs = 100
        self.validation_split = 0.2
        
        # Model
        self.model = None
        self.label_encoder = None
        self.history = None
        
    def load_data(self):
        """Load and preprocess training data"""
        print("📊 Loading training data...")
        
        X = []  # Images
        y = []  # Labels
        
        for emotion in self.emotion_labels:
            emotion_dir = os.path.join(self.data_dir, emotion)
            if not os.path.exists(emotion_dir):
                print(f"⚠️ Directory not found: {emotion_dir}")
                continue
            
            image_files = [f for f in os.listdir(emotion_dir) if f.endswith(('.jpg', '.jpeg', '.png'))]
            print(f"   {emotion}: {len(image_files)} images")
            
            for image_file in image_files:
                image_path = os.path.join(emotion_dir, image_file)
                try:
                    # Load image
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    if image is None:
                        continue
                    
                    # Resize to standard size
                    image = cv2.resize(image, (self.img_size, self.img_size))
                    
                    # Normalize pixel values
                    image = image.astype('float32') / 255.0
                    
                    X.append(image)
                    y.append(emotion)
                    
                except Exception as e:
                    print(f"Error loading {image_file}: {e}")
                    continue
        
        if len(X) == 0:
            print("❌ No training data found!")
            return None, None
        
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        
        print(f"✓ Loaded {len(X)} images")
        print(f"✓ Classes: {len(set(y))}")
        
        return X, y
    
    def preprocess_data(self, X, y):
        """Preprocess data for training"""
        print("🔄 Preprocessing data...")
        
        # Reshape X for CNN input
        X = X.reshape(X.shape[0], self.img_size, self.img_size, 1)
        
        # Encode labels
        self.label_encoder = LabelEncoder()
        y_encoded = self.label_encoder.fit_transform(y)
        y_categorical = to_categorical(y_encoded, self.num_classes)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_categorical, 
            test_size=self.validation_split, 
            random_state=42, 
            stratify=y_encoded
        )
        
        print(f"✓ Training set: {X_train.shape[0]} images")
        print(f"✓ Test set: {X_test.shape[0]} images")
        
        return X_train, X_test, y_train, y_test
    
    def create_model(self):
        """Create CNN model architecture"""
        print("🏗️ Creating CNN model...")
        
        model = Sequential([
            # First Convolutional Block
            Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_size, self.img_size, 1)),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Second Convolutional Block
            Conv2D(64, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Third Convolutional Block
            Conv2D(128, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Fourth Convolutional Block
            Conv2D(256, (3, 3), activation='relu'),
            BatchNormalization(),
            Conv2D(256, (3, 3), activation='relu'),
            MaxPooling2D(pool_size=(2, 2)),
            Dropout(0.25),
            
            # Dense Layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(self.num_classes, activation='softmax')
        ])
        
        # Compile model
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("✓ Model created successfully")
        return model
    
    def train_model(self, X_train, X_test, y_train, y_test):
        """Train the CNN model"""
        print("🚀 Starting model training...")
        
        # Create model
        self.model = self.create_model()
        
        # Print model summary
        print("\n📋 Model Architecture:")
        self.model.summary()
        
        # Callbacks
        callbacks = [
            EarlyStopping(
                monitor='val_accuracy',
                patience=10,
                restore_best_weights=True
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.0001
            )
        ]
        
        # Data augmentation
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            horizontal_flip=True,
            zoom_range=0.1
        )
        
        # Train model
        self.history = self.model.fit(
            datagen.flow(X_train, y_train, batch_size=self.batch_size),
            steps_per_epoch=len(X_train) // self.batch_size,
            epochs=self.epochs,
            validation_data=(X_test, y_test),
            callbacks=callbacks,
            verbose=1
        )
        
        print("✓ Training completed!")
        return self.history
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate model performance"""
        print("📊 Evaluating model...")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_classes = np.argmax(y_pred, axis=1)
        y_true_classes = np.argmax(y_test, axis=1)
        
        # Calculate accuracy
        accuracy = np.mean(y_pred_classes == y_true_classes)
        print(f"✓ Test Accuracy: {accuracy:.4f}")
        
        # Classification report
        print("\n📋 Classification Report:")
        print(classification_report(y_true_classes, y_pred_classes, 
                                  target_names=self.emotion_labels))
        
        # Confusion matrix
        cm = confusion_matrix(y_true_classes, y_pred_classes)
        
        # Plot confusion matrix
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.emotion_labels,
                   yticklabels=self.emotion_labels)
        plt.title('Confusion Matrix')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.tight_layout()
        plt.savefig('confusion_matrix.png')
        plt.show()
        
        return accuracy
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("❌ No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        ax1.grid(True)
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        ax2.grid(True)
        
        plt.tight_layout()
        plt.savefig('training_history.png')
        plt.show()
    
    def save_model(self):
        """Save trained model and label encoder"""
        print("💾 Saving model...")
        
        # Save model
        model_path = 'emotion_model.h5'
        self.model.save(model_path)
        print(f"✓ Model saved to: {model_path}")
        
        # Save label encoder
        encoder_path = 'label_encoder.pkl'
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        print(f"✓ Label encoder saved to: {encoder_path}")
        
        # Save training info
        info_path = 'training_info.txt'
        with open(info_path, 'w') as f:
            f.write(f"Training completed: {datetime.now()}\n")
            f.write(f"Model: {model_path}\n")
            f.write(f"Label encoder: {encoder_path}\n")
            f.write(f"Classes: {self.emotion_labels}\n")
            f.write(f"Image size: {self.img_size}x{self.img_size}\n")
        print(f"✓ Training info saved to: {info_path}")
    
    def train(self):
        """Main training function"""
        print("=" * 70)
        print("🤖 ML MODEL TRAINER FOR EMOTION DETECTION")
        print("=" * 70)
        
        # Load data
        X, y = self.load_data()
        if X is None:
            print("❌ No data to train on. Please collect data first using ml_data_collector.py")
            return
        
        # Preprocess data
        X_train, X_test, y_train, y_test = self.preprocess_data(X, y)
        
        # Train model
        self.train_model(X_train, X_test, y_train, y_test)
        
        # Evaluate model
        accuracy = self.evaluate_model(X_test, y_test)
        
        # Plot training history
        self.plot_training_history()
        
        # Save model
        self.save_model()
        
        print("\n" + "=" * 70)
        print("🎉 TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print(f"✓ Final accuracy: {accuracy:.4f}")
        print("✓ Model saved and ready for use")
        print("✓ Use ml_emotion_detector.py to test the model")
        print("=" * 70)

if __name__ == "__main__":
    trainer = MLModelTrainer()
    trainer.train()
