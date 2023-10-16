
import os
from re import search
import re
import time
import requests
from datetime import datetime
import pygame
from langchain.chat_models import ChatOpenAI
import cv2
import speech_recognition as sr  # required to return a string output by taking microphone input from the user
from dotenv import find_dotenv ,load_dotenv
import sounddevice as sd
import numpy as np
import wavio
import os
import keyboard
from datetime import datetime

dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
voice_id = "pNInz6obpgDQGcFmaJgB"
Vid = os.getenv("voice_id")
elevenLabsAPI = os.getenv("elevenLabsAPI")

def _approve(_input: str) -> bool:
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 0.5
            msg = (
                "Do you approve of the following input? "
                "Please say 'Yes' or 'No'  within 30 seconds."
            )
            msg += "\n\n" + _input + "\n"
            speak(msg)
            try:
                audio = r.listen(source, timeout=30, phrase_time_limit=30)
                resp = r.recognize_google(audio)
                return resp.lower() in ("yes", "y")
            except Exception as e:
                print(f"An error occurred while recognizing your response: {e}")
                return False
            
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def speak(text):
    # if current_language.lower == "english":
        voice_id = Vid
        api_key = elevenLabsAPI
        CHUNK_SIZE = 1024
        
        # filename = now.strftime("%Y-%m-%d_%H-%M-%S")
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_file = f'{timestamp}.mp3'
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            speak(f"HTTP error occurred: {err}")
            return
        except Exception as err:
            speak(f"An error occurred: {err}")
            return

        try:

            directory = datetime.now().strftime('%Y-%m-%d')
            os.makedirs(directory, exist_ok=True)

            file_path = os.path.join(directory, output_file)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)

            # Play the audio file with pygame
            pygame.mixer.init()
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

            pygame.mixer.quit()  # Release the audio file after playing

            # Delete the audio file after it's been played
            try:
                os.remove(file_path)
            except Exception as err:
                print(f"An error occurred while deleting the file: {err}")

        except Exception as err:
            print(f"An error occurred: {err}")
def speech_to_text():
    # Initialize speech recognizer
    r = sr.Recognizer()
    # Use default system microphone as source to listen to speech
    with sr.Microphone() as source:
        speak("hello, welcome.... How may i be of service....")
        # Adjust for ambient noise
        r.adjust_for_ambient_noise(source)
        # Record the user's speech
        audio = r.listen(source)
    try:
        # Use Google speech recognition to convert speech to text
        text = r.recognize_google(audio)
        speak(f"You said: {text}")
        speak("Noted.")
        return text

    except sr.UnknownValueError:
        speak("Sorry, could not understand your input.")
    except sr.RequestError:
        speak("Sorry, there was an error with the speech recognition service.")

        # Return empty string on error
        return ""
