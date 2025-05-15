import os
import cv2
import numpy as np
import time
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model


# Load dataset for training
def load_dataset(data_dir):
    images = []
    labels = []
    label_names = os.listdir(data_dir)
    label_map = {label: idx for idx, label in enumerate(label_names)}

    for label in label_names:
        label_path = os.path.join(data_dir, label)
        for img_file in os.listdir(label_path):
            img_path = os.path.join(label_path, img_file)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Load image in grayscale
            img = cv2.resize(img, (100, 100))  # Resize image to 100x100
            images.append(img)
            labels.append(label_map[label])

    images = np.array(images).reshape(-1, 100, 100, 1) / 255.0  # Normalize pixel values
    labels = np.array(labels)
    return images, labels, label_names

# Build a CNN model

def build_cnn_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    
    model.add(Dense(num_classes, activation='softmax'))
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model

# Train the CNN model
def train_model(model, images, labels):
    labels = to_categorical(labels)
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))
    model.save("trained_face_recognition_model.h5")
    return model




# Load dataset for label mapping
def load_labels(data_dir):
    label_names = os.listdir(data_dir)
    label_map = {idx: label for idx, label in enumerate(label_names)}
    return label_map

# Real-time face recognition running for 10 seconds
def real_time_face_recognition(model, label_map):
    cap = cv2.VideoCapture(0)  # Use webcam
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    start_time = time.time()
    known_face_detected = False  # Assume no known face is detected initially

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face_resized = cv2.resize(face, (100, 100)).reshape(1, 100, 100, 1) / 255.0
            
            prediction = model.predict(face_resized)
            predicted_label = np.argmax(prediction)

            if predicted_label in label_map:
                predicted_name = label_map[predicted_label]
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, predicted_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36, 255, 12), 2)
                print(f"Recognized face: {predicted_name}")
                
                # Known face detected
                known_face_detected = True
                break  # Exit the face detection loop

        # Show the video feed with rectangles around detected faces
        cv2.imshow('Real-Time Face Recognition', frame)

        # Exit the loop if a known face is detected
        if known_face_detected:
            break
 
        # End after 10 seconds
        if time.time() - start_time >= 10:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return known_face_detected




if __name__ == "__main__":
    # Load dataset
    dataset_dir = "D:\dataset"  # Path to your dataset
    images, labels, label_names = load_dataset(dataset_dir)

    # Build and train model
    input_shape = (100, 100, 1)
    num_classes = len(label_names)
    
    cnn_model = build_cnn_model(input_shape, num_classes)
    trained_model = train_model(cnn_model, images, labels)


    # Load trained CNN model
    model = load_model('trained_face_recognition_model.h5')

    # Load label mapping (e.g., from "dataset/Person1" and "dataset/Person2" folders)
    #dataset_dir = "dataset"  # Path to your dataset
    label_map = load_labels(dataset_dir)

    # Run face recognition for 10 seconds and check if any known face is recognized
    result = real_time_face_recognition(model, label_map)

    if result:
        print("Known face was detected. Returning True.")
    else:
        print("No known face was detected within 10 seconds. Returning False.")

