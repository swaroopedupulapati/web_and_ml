import cv2
import numpy as np
from fer import FER

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Initialize the FER emotion detector
detector = FER()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Detect emotions in the frame
    emotion_data = detector.detect_emotions(frame)
    
    # If emotions are detected, display them
    if emotion_data:
        for emotion in emotion_data:
            (x, y, w, h) = emotion['box']
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Get the dominant emotion
            dominant_emotion = emotion['emotions']
            max_emotion = max(dominant_emotion, key=dominant_emotion.get)
            cv2.putText(frame, max_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Emotion Recognition', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
