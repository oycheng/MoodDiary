from flask import request, jsonify, Blueprint
from chat import message, store_emotions
from hume import HumeStreamClient, HumeClientException
from hume.models.config import FaceConfig
import openai
import asyncio
import threading
import cv2
import traceback


HUME_API_KEY = ""
openai.api_key = ""

bp = Blueprint('chat', __name__)

# route for Final version prediction
@bp.route('/process-frame-result', methods=['POST'])
def process_frame_result():
    global results, counter
    try:
        print(type(request))
        frame_jpg = request.files['frame_jpg']
        frame_jpg.save("./temp_file/" + str(counter) + "_" + TEMP_FILE)
        counter += 1

        print("emotions saved:")

        # unpack the request
        response_data = {}
        return jsonify(response_data)
    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500

webcam_event = asyncio.Event()

@bp.route('/transcription', methods=['POST'])
async def get_transcription():
    try:
        await asyncio.ensure_future(webcam_loop())
        await webcam_event.wait()

        if 'audio' not in request.files:
            return 'No audio file found', 400
        
        audio = request.files['audio']
        audio.save('./temp_file/audio.mp3')
        

        audio_file= open("./temp_file/audio.mp3", "rb")
        print("getting transcription")
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        print("got transcription")
        print(transcription)

        response = message(transcription["text"])
        print(response)
        
        return jsonify(response=response)
    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500
    
@bp.route('/start', methods=['POST'])
async def start_processing():
    try:
        print(type(request))
        global results, running

        results = []
        running = True
        return jsonify("started")
    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500


results = []
running = False

def end_processing():
    global results, running
    results = []
    running = False
    return


TEMP_FILE = 'temp.jpg'
counter = 0
reader = 0

async def webcam_loop():
    global counter, reader
    print("called")
    try:
        webcam_event.clear()
        client = HumeStreamClient(HUME_API_KEY)
        config = FaceConfig(identify_faces=True)
        print("trying to connect")
        async with client.connect([config]) as socket:
            print("(Connected to Hume API!)")
            while reader < counter:
                result = await socket.send_file("./temp_file/" + str(reader) + "_" + TEMP_FILE)
                store_emotions(result)
                reader += 1
                print("emotions append:")

            webcam_event.set()
    except HumeClientException:
        print(traceback.format_exc())
        webcam_event.set()
        reader = counter
    except Exception:
        print(traceback.format_exc())
        webcam_event.set()
        reader = counter
