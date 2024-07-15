import os
import bardapi
from dotenv import load_dotenv
import time
import speech_recognition as sr
import pyttsx3
import numpy as np
# from os.path import join, dirname
# import matplotlib.pyplot as plt
# ^ matplotlib is great for visualising data and for testing purposes but usually not needed for production

load_dotenv()

os.environ['_BARD_API_KEY']="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# Set up the speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voice = engine.getProperty('voices')[20]
engine.setProperty('voice', voice.id)
name = " 김동현"
greetings = [f"안녕하세요 {name} 주인님", 
             "좋은 아침이에요 주인님", 
             "어떤게 궁금하세요?",
             f"{name} 주인님! 어떤게 궁금하실까요?",
             f"{name} 주인님 저를 불러 주셨군요! 오늘은 어떤게 궁금하신가요?" ]

# Listen for the wake word "hey pos"
def listen_for_wake_word(source):
    print("Listening for '안녕'...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language = "ko-KR")
            if "안녕" in text.lower():
                print("Wake word detected.")
                engine.say(np.random.choice(greetings))
                engine.runAndWait()
                listen_and_respond(source)
                break
        except sr.UnknownValueError:
            pass

# Listen for input and respond with OpenAI API
def listen_and_respond(source):
    print("Listening...")

    while True:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio, language="ko-KR")
            print(f"You said: {text}")
            if not text:
                continue

            # Send input to OpenAI API
            response = bardapi.core.Bard().get_answer(text)['content'] 
            print(f"OpenAI response: {response}")

            # Speak the response
            engine.say(response)
            engine.runAndWait()

            if not audio:
                listen_for_wake_word(source)
        except sr.UnknownValueError:
            time.sleep(2)
            print("Silence found, shutting up, listening...")
            listen_for_wake_word(source)
            break
            
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            engine.say(f"Could not request results; {e}")
            engine.runAndWait()
            listen_for_wake_word(source)
            break

# Use the default microphone as the audio source
with sr.Microphone() as source:
    listen_for_wake_word(source)
