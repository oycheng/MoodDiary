from flask import request, jsonify, Blueprint
from chat import message, store_emotions
from hume import HumeStreamClient, HumeClientException
from hume.models.config import FaceConfig
import openai


HUME_API_KEY = "ad0LmsBJyv0WpfTi8GSkvrhH4ryFLcqK2YJHH9KG6pDtzMfz"
openai.api_key = "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"

bp = Blueprint('chat', __name__)

# route for Final version prediction
@bp.route('/process-frame-result', methods=['POST'])
def process_frame_result():
    global results
    try:
        print(type(request))
        frame_jpg = request.files['frame_jpg']
        results.append(frame_jpg)

        print("emotions stored:")

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


@bp.route('/transcription', methods=['POST'])
def get_transcription():
    try:
        print(type(request))
        if 'audio' not in request.files:
            return 'No audio file found', 400
        
        audio = request.files['audio']
        audio.save('./temp_file/audio.mp3')
        
        print("here")
        audio_file= open("./temp_file/audio.mp3", "rb")
        print("probaly not be here")
        transcription = openai.Audio.transcribe("whisper-1", audio_file)
        print("must be here")
        print(transcription)
        print(transcription["text"])

        end_processing()
        print("will it be here")
        response = message(transcription["text"])
        print("or maybe be here")
        print(response)
        print("??")
        
        return jsonify(response)
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
        await imageProcessor()
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

async def imageProcessor():
    global results, running
    client = HumeStreamClient(HUME_API_KEY)
    config = FaceConfig(identify_faces=True)
    async with client.connect([config]) as socket:
        print("(Connected to Hume API!)")
        while len(results) != 0:
            result = await socket.send_file(results[0])
            store_emotions(result)
            results.pop(0)
            print("emotions append:")

            if len(results) == 0 and not running:
                return

def waitForFrameProcess():
    global results, running
    while True:
        if len(results) == 0 and not running:
            return