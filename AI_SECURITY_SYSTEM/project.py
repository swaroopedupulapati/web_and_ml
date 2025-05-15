import cv2
import time
import os
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model
import speech_recognition as sr
import pygame
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# --------------------- Motion Detection (From motion_detection.py) ---------------------
def detect_motion(video_source=0, motion_threshold=25):
    cap = cv2.VideoCapture(video_source)
    time.sleep(2)
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to capture the first frame.")
        cap.release()
        return False
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame1_gray = cv2.GaussianBlur(frame1_gray, (21, 21), 0)
    motion_detected = False

    while True:
        ret, frame2 = cap.read()
        if not ret:
            break
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.GaussianBlur(frame2_gray, (21, 21), 0)
        frame_diff = cv2.absdiff(frame1_gray, frame2_gray)
        _, thresh = cv2.threshold(frame_diff, motion_threshold, 255, cv2.THRESH_BINARY)
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                motion_detected = True
                print("Motion detected!")
                break

        cv2.imshow("Motion Detection", frame2)

        if motion_detected:
            break

        frame1_gray = frame2_gray.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return motion_detected

# --------------------- Face Recognition (From face_recognition.py) ---------------------


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


def load_labels(data_dir):
    label_names = os.listdir(data_dir)
    label_map = {idx: label for idx, label in enumerate(label_names)}
    return label_map

def real_time_face_recognition(model, label_map):
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    start_time = time.time()
    known_face_detected = False

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
                known_face_detected = True
                break

        cv2.imshow('Real-Time Face Recognition', frame)

        if known_face_detected:
            break

        if time.time() - start_time >= 10:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return known_face_detected

# --------------------- Initialize and Play Sound before starting sentence recognition ---------------------
def init_sound():
    pygame.mixer.init()

def play_start_sound():
    pygame.mixer.music.load("start_beep.mp3")  # Path to your sound file
    pygame.mixer.music.play()
    time.sleep(1)

# --------------------- Sentence Recognition (From sentence_recognition.py) ---------------------
def sentence_recognition(authorized_sentence):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        play_start_sound()
        print("Please speak the authorized sentence...")
        audio = recognizer.listen(source)
        try:
            spoken_sentence = recognizer.recognize_google(audio)
            print(f"Spoken Sentence: {spoken_sentence}")
            if spoken_sentence.strip().lower() == authorized_sentence.strip().lower():
                print("Access Granted! Sentence matches.")
                return True
            else:
                print("Access Denied! Sentence does not match.")
                return False
        except sr.UnknownValueError:
            print("Speech Recognition could not understand the audio.")
            return False
        except sr.RequestError as e:
            print(f"Could not request results from Google Web Speech API; {e}")
            return False

# --------------------- Email Sending with Video (From email_sending.py) ---------------------
def send_email_with_video(subject, message, video_file):
    sender_email = "sender@gmail.com"
    sender_password = "password/passkey"
    recipient_email = "recevier@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Attach the video file
    with open(video_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(video_file)}")
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Alert email with video sent successfully!")
    except Exception as e:
        #print(f"Failed to send email: {e}")
        print("Failed to sent email")

# --------------------- Video Recording ---------------------
def record_video(output_file='recorded_video.mp4', duration=10):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))

    start_time = time.time()
    print(f"Recording video for {duration} seconds...")

    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording...', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# --------------------- Main Execution Flow ---------------------
if __name__ == "__main__":
    init_sound()
    # Load dataset
    dataset_dir = "dataset"  # Path to your dataset
    images, labels, label_names = load_dataset(dataset_dir)

    # Build and train model
    input_shape = (100, 100, 1)
    num_classes = len(label_names)
    
    cnn_model = build_cnn_model(input_shape, num_classes)
    trained_model = train_model(cnn_model, images, labels)

    # Detect motion
    motion = detect_motion()
    if motion:
        print("Motion detected, proceeding with face recognition.")

        # Load the facial recognition model and labels
        model = load_model('trained_face_recognition_model.h5')
        #dataset_dir = "D:\dataset" # dataset path for known faces
        label_map = load_labels(dataset_dir)

        # Perform face recognition
        face_recognition_result = real_time_face_recognition(model, label_map)
        if face_recognition_result:
            print("Known face detected. Access granted.")
        else:
            print("No known face detected. Proceeding with sentence recognition.")
            # Perform sentence recognition
            authorized_sentence = "hi i am fine"
            sentence_recognition_result = sentence_recognition(authorized_sentence)

            if sentence_recognition_result:
                print("Sentence recognized correctly. Access granted.")
            else:
                print("Unauthorized access attempt detected. Recording video and sending alert email.")
                
                # Record a 10-second video
                video_file = 'unauthorized_access.mp4'
                record_video(output_file=video_file, duration=10)
                
                # Send an alert email with the video
                send_email_with_video(
                    subject="Security Alert: Unauthorized Access Attempt",
                    message="An unknown person attempted to access the system and failed both face and sentence recognition.",
                    video_file=video_file
                )
    else:
        print("No motion detected.")
