import speech_recognition as sr
import pygame
import time

# Initialize Pygame for playing sound
def init_sound():
    pygame.mixer.init()

# Function to play a sound (e.g., a beep) for start intimation
def play_start_sound():
    pygame.mixer.music.load("start_beep.mp3")  # Path to start beep sound
    pygame.mixer.music.play()
    time.sleep(1)  # Wait for 1 second to let the sound finish

# Function for sentence recognition using microphone
def sentence_recognition(authorized_sentence):
    recognizer = sr.Recognizer()

    # Use the microphone for input
    with sr.Microphone() as source:
        # Play the start sound to indicate that the system is ready
        play_start_sound()

        print("Please speak the authorized sentence...")
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google Web Speech API
            spoken_sentence = recognizer.recognize_google(audio)
            print(f"Spoken Sentence: {spoken_sentence}")

            # Check if spoken sentence matches the authorized sentence
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

if __name__ == "__main__":
    # Initialize sound system
    init_sound()

    # Define the authorized sentence
    authorized_sentence = "hi i am fine"

    # Run sentence recognition
    result = sentence_recognition(authorized_sentence)

    if result:
        print("Sentence recognized correctly!")
    else:
        print("Sentence not recognized or incorrect.")
