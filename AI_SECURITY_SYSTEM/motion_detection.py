import cv2
import time
import os
import numpy as np

# Function to detect motion using a camera
def detect_motion(video_source=0, motion_threshold=25):
    # Initialize the camera (default camera is '0')
    cap = cv2.VideoCapture(video_source)

    # Allow camera to warm up
    time.sleep(2)

    # Read the first frame to use as the background (reference)
    ret, frame1 = cap.read()
    if not ret:
        print("Failed to capture the first frame.")
        cap.release()
        return False

    # Convert first frame to grayscale and blur it
    frame1_gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    frame1_gray = cv2.GaussianBlur(frame1_gray, (21, 21), 0)

    motion_detected = False

    while True:
        # Capture the next frame
        ret, frame2 = cap.read()
        if not ret:
            break

        # Convert the new frame to grayscale and blur it
        frame2_gray = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        frame2_gray = cv2.GaussianBlur(frame2_gray, (21, 21), 0)

        # Compute the absolute difference between the two frames
        frame_diff = cv2.absdiff(frame1_gray, frame2_gray)

        # Apply a threshold to the difference image to get regions with significant changes
        _, thresh = cv2.threshold(frame_diff, motion_threshold, 255, cv2.THRESH_BINARY)

        # Dilate the threshold image to fill in small holes and find contours
        thresh = cv2.dilate(thresh, None, iterations=2)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # If contours are found, motion is detected
        for contour in contours:
            if cv2.contourArea(contour) > 500:  # Ignore small contours (motion areas)
                motion_detected = True
                print("Motion detected!")
                break

        # Display the result for visual feedback
        cv2.imshow("Motion Detection", frame2)

        if motion_detected:
            break  # Exit if motion is detected

        # Update the background frame to the current frame
        frame1_gray = frame2_gray.copy()

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    return motion_detected


if __name__ == "__main__":
    # Call the motion detection function
    motion = detect_motion()

    if motion:
        print("Motion detected, returning True.")
    else:
        print("No motion detected, returning False.")

