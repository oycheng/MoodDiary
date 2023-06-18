from flask import request, jsonify, Blueprint
from chat import message, store_emotions
from hume import HumeStreamClient, HumeClientException
from hume.models.config import FaceConfig
import openai
import asyncio
import threading
import cv2
import traceback
import json
from datetime import datetime


HUME_API_KEY = "ad0LmsBJyv0WpfTi8GSkvrhH4ryFLcqK2YJHH9KG6pDtzMfz"
openai.api_key = "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"

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
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        print(transcription)

        response = message(transcription["text"])
        print(response)
        
        return jsonify(response)
    # exception
    except KeyError as e:
        # Handle missing field error
        return f'Missing field error: {e}', 400
    except Exception as e:
        # Handle other exceptions
        return f'Internal server error: {e}', 500
    

def convert_data(emotion, response, transcription):
    with open('data.json', 'r') as file:
        json_data = json.load(file)
    current_date = datetime.now()
    formatted_date = current_date.strftime('%m-%d-%Y')
    color = get_color(emotion)
    new_data = {
        formatted_date : [color, transcription, response],
    }
    json_data.append(new_data)
    
    with open('data.json', 'w') as file:
        json.dump(json_data, file)

def get_color(emotion):
    color_value = {
        "admiring" : "white", "adoring" : "pink", "appreciative" : "white", "amused" : "yellow", "angry" : "red", "anxious"  : "purple", "awestruck" : "lightblue", "uncomfortable" : "white", "bored" : "brown", "calm" : "lightblue",
        "focused" : "white", "contemplative" : "white", "confused" : "orange", "contemptuous" : "white", "content" : "white", "hungry" : "white", "determined" : "white", "disappointed" : "white",
        "disgusted" : "green", "distressed" : "white", "doubtful" : "tan", "euphoric" : "white", "embarrassed" : "white", "disturbed" : "white", "entranced" : "white", "envious" : "white", "excited" : "white",
        "fearful" : "lightpurple", "guilty" : "white", "horrified" : "white", "interested" : "white", "happy" : "white", "enamored" : "white", "nostalgic" : "white", "pained" : "maroon", "proud" : "white", "inspired" : "white",
        "relieved" : "white", "smitten" : "white", "sad" : "darkblue", "satisfied" : "white", "desirous" : "white", "ashamed" : "white", "negatively surprised" : "green", "positively surprised" : "white",
        "sympathetic" : "white", "tired" : "black", "triumphant" : "white"
    }
    return color_value[emotion]

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
    except Exception:
        print(traceback.format_exc())
        webcam_event.set()
