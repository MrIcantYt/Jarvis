import os
import json
import queue
import sys
import webbrowser
import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer

engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

def speak(text):
    print(f"Джарвис: {text}")
    engine.say(text)
    engine.runAndWait()

def execute_command(command):
    command = command.lower()

    if "джарвис" in command:
        if "привет" in command or "здравствуй" in command:
            speak("Приветствую, сэр. Чем могу помочь?")

        elif "открой ютуб" in command or "открой youtube" in command:
            speak("Открываю YouTube, сэр.")

            webbrowser.open("https://www.youtube.com/")

        elif "сколько подписчиков" in command:
            speak("У MrIcant 183 подписчика, сэр.")

        elif "выключась" in command or "пока" in command:
            speak("Отключаю систему, сэр.")

            sys.exit()

        else:
            print("Команда не распознана, сэр.")

que = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    que.put(bytes(indata))

if not os.path.exists("model"):
    print("Пожалуйста, скачайте модель Vosk и переименуйте папку в \"model\".")
    sys.exit()

model = Model("model")
device_info = sd.query_devices(None, "input")
samplerate = int(device_info["default_samplerate"])

speak("Система \"Джарвис\" запущена. Я слушаю вас.")

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=None, dtype="int16", channels=1, callback=callback):
    rec = KaldiRecognizer(model, samplerate)

    while True:
        data = que.get()

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")

            if text:
                print(f"Вы сказали: {text}")
                execute_command(text)
