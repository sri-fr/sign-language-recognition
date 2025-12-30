import pyttsx3
import threading

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak_async(text):
    def run():
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=run, daemon=True).start()
