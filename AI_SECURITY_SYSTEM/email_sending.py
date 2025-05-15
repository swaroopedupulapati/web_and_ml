
import cv2
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from datetime import datetime

# Function to record video
def record_video(filename, duration=10):
    cap = cv2.VideoCapture(0)  # Use the default camera
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use 'mp4v' for MP4 format
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = datetime.now()
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        
        # Display the recording frame
        cv2.imshow('Recording...', frame)
        
        # Stop recording after the specified duration
        if (datetime.now() - start_time).seconds >= duration:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Function to send email
def send_email(subject, body, filename, to_email):
    from_email = "swaroopqis@gmail.com"
    password = "qihb sgty ysew ikes"

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Attach the video file
    with open(filename, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(filename)}')
        msg.attach(part)

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)

# Main execution
if __name__ == "__main__":
    video_filename = "live_video.mp4"  # Change extension to .mp4
    record_video(video_filename, duration=10)
    
    subject = "10 Seconds Live Video"
    body = "Here is a 10 seconds live video recording."
    to_email = "recevier1@gmail.com" #receiver mail id

    send_email(subject, body, video_filename, to_email)
    
    # Optionally, remove the video file after sending
    os.remove(video_filename)
