import threading
import asyncio
import os
import cv2
import time
import traceback
import websockets
import numpy as np

from pynput import keyboard
from pvrecorder import PvRecorder
# from whispercpp import Whisper
from chat import message, store_emotions
from playsound import playsound
from hume import HumeStreamClient, HumeClientException
from hume.models.config import FaceConfig
from gtts import gTTS

# Configurations
HUME_API_KEY = "ad0LmsBJyv0WpfTi8GSkvrhH4ryFLcqK2YJHH9KG6pDtzMfz"
HUME_FACE_FPS = 1 / 3  # 3 FPS

TEMP_FILE = 'temp.jpg'
TEMP_WAV_FILE = 'temp.wav'

# Initialize whisper model, pyttsx3 engine, and pv recorder
# w = Whisper.from_pretrained("tiny.en")

# Global variables
recording = False

# Webcam setup
cam = cv2.VideoCapture(0)


async def webcam_loop():
    while True:
        try:
            client = HumeStreamClient(HUME_API_KEY)
            config = FaceConfig(identify_faces=True)
            async with client.connect([config]) as socket:
                print("(Connected to Hume API!)")
                while True:
                    if not recording:
                        # Capture frame-by-frame
                        ret, frame = cam.read()

                        if not ret:
                            print("Failed to capture frame from camera")
                            break

                        cv2.imwrite(TEMP_FILE, frame)
                        result = await socket.send_file(TEMP_FILE)
                        print(result)
                        print("emotions stored:")
                        await asyncio.sleep(3)
        except websockets.exceptions.ConnectionClosedError:
            print("Connection lost. Attempting to reconnect in 1 seconds.")
            time.sleep(1)
        except HumeClientException:
            print(traceback.format_exc())
            break
        except Exception:
            print(traceback.format_exc())


def start_asyncio_event_loop(loop, asyncio_function):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio_function)

printed = False
def on_press(key):
    global recording, printed
    if key == keyboard.Key.space:
        print("key pressed")
        if recording:
            recording = False
            printed = False
        else:
            recording = True
            if not printed:
                printed = True
                try:
                    res = message("none")
                    print(res)
                except Exception as e:
                    # Exception handling code
                    print("An exception occurred:", type(e).__name__)
                    traceback.print_exc()
                print("printed===")


new_loop = asyncio.new_event_loop()

threading.Thread(target=start_asyncio_event_loop, args=(new_loop, webcam_loop())).start()

with keyboard.Listener(on_press=on_press) as listener:
    print("Speak to Joaquin!")
    print("(Press spacebar to speak. To finish speaking, press spacebar again)")
    listener.join()
