from flask import Flask, render_template, Response
import cv2
from fer import FER
app = Flask(__name__)
# Initialize the FER emotion detector
detector = FER()
def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
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
        # Encode the frame in JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(debug=True)