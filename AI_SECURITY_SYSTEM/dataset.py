import cv2
import os

# Function to create a dataset folder for a person
def create_dataset(person_name, save_path="dataset", num_images=100):
    # Create directory if it doesn't exist
    person_path = os.path.join(save_path, person_name)
    if not os.path.exists(person_path):
        os.makedirs(person_path)

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    count = 0
    print(f"Capturing images for {person_name}. Please look at the camera.")

    while count < num_images:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            count += 1
            # Extract the face region
            face_img = frame[y:y+h, x:x+w]
            # Save the captured image
            img_path = os.path.join(person_path, f"{person_name}_{count}.jpg")
            cv2.imwrite(img_path, face_img)
            print(f"Saved image: {img_path}")

            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"Image {count}/{num_images}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Display the frame with a bounding box around the face
        cv2.imshow("Capturing Images", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit early
            break

        # Stop when the required number of images are captured
        if count >= num_images:
            print(f"Dataset creation for {person_name} completed!")
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    person_name = input("Enter the name of the person: ")
    create_dataset(person_name, save_path="dataset", num_images=100)
