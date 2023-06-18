import openai
import numpy as np
import re
import os
import json
from datetime import datetime

day = 18

openai.api_key = ""

SYSTEM_INSTUCTIONS = """You are a emotion journal AI assistant.
Your goal is to give the user advice on their issues and help them get into a better mental state.
You will congratulate the user if the user having a positive mental state unless the user is dealing with an issue or hardship, then you will be apologetic in the first sentence.
Your responses will be 1-5 sentences and give advice or assistance to help the user keep a positive mental attitude.
"""

EMOTIONS = np.array([
    "admiring", "adoring", "appreciative", "amused", "angry", "anxious", "awestruck", "uncomfortable", "bored", "calm",
    "focused", "contemplative", "confused", "contemptuous", "content", "hungry", "determined", "disappointed",
    "disgusted", "distressed", "doubtful", "euphoric", "embarrassed", "disturbed", "entranced", "envious", "excited",
    "fearful", "guilty", "horrified", "interested", "happy", "enamored", "nostalgic", "pained", "proud", "inspired",
    "relieved", "smitten", "sad", "satisfied", "desirous", "ashamed", "negatively surprised", "positively surprised",
    "sympathetic", "tired", "triumphant"
])

conversation = [{
    "role": "system",
    "content": SYSTEM_INSTUCTIONS
}]

emotion_history = []

def create_message(user_message=None, user_emotion=None):
    return f"The user says, '{user_message}'. The user looked {user_emotion[0]} the most, then {user_emotion[1]}."

def get_adjective(score):
    if 0.26 <= score < 0.35:
        return "slightly"
    elif 0.35 <= score < 0.44:
        return "somewhat"
    elif 0.44 <= score < 0.53:
        return "moderately"
    elif 0.53 <= score < 0.62:
        return "quite"
    elif 0.62 <= score < 0.71:
        return "very"
    elif 0.71 <= score <= 3:
        return "extremely"
    else:
        return ""
    
def process_prediction(predictions):
    emotion_predictions = []
    for frame_dict in predictions:
        if 'predictions' not in frame_dict['face']:
            continue
        frame_emo_dict = frame_dict['face']["predictions"][0]["emotions"]
        emo_dict = {x["name"]: x["score"] for x in frame_emo_dict}
        emo_frame = sorted(emo_dict.items())
        emo_frame = np.array([x[1] for x in emo_frame])
        emotion_predictions.append(emo_frame)
    if len(emotion_predictions) == 0:
        return 'calm'
    # Assuming 'emotion_predictions' is a 2D array
    mean_predictions = np.array(emotion_predictions).mean(axis=0)
    # Get the index of the highest value
    mean_emotion = dict(zip(EMOTIONS, mean_predictions))
    sorted_mean_emotion = sorted(mean_emotion.items(), key=lambda x:x[1], reverse=True)
    return sorted_mean_emotion

def find_emotion(predictions):   
    if len(predictions) == 0:
        return ["calm", "bored"]
    sorted_emotions = []
    for emotion, value in predictions:
        sorted_emotions.append(f"{get_adjective(value)} {emotion}")
    return sorted_emotions

def store_emotions(result):
    emotion_history.append(result)

def message(transcription):
    global emotion_history
    user_sorted_values = process_prediction(emotion_history)
    user_emotions = find_emotion(user_sorted_values)
    print(user_emotions[0:3])

    # Load past conversation
    #if os.path.exists("./conversation.json"):
    #    with open("./conversation.json", "r") as file:
    #        conversation = json.load(file)
    #        print("Conversation loaded")
    #else:
    #    conversation = []
    #    print("Conversation file not found. Starting with an empty conversation.")

    
    message = create_message(transcription, user_emotions)
    conversation.append({"role": "user", "content": message})
    print("creating message response")
    completion = openai.ChatCompletion.create(model="gpt-4", messages=conversation)
    response = completion.choices[0]['message']['content']
    conversation.append({"role": "assistant", "content": response})
    response = re.sub(r'\([^)]*\)', '', response)
    response = re.sub(r'\[.*?\]', '', response)
    response = re.sub(r'^"|"$', '', response)
    print(response)
    emotion_history = []


    # Save conversation
    #with open("conversation.json", "w") as file:
    #    json.dump(conversation, file)
    #    print("Conversation saved to conversation.json")

    # save data in a jason file
    print("???????")
    
    print(user_sorted_values[0][0])
    convert_data(user_sorted_values[0][0], response)
    
    return response




def convert_data(emotion, response):
    global day
    print(emotion)
    exist = True
    if os.path.exists("../my-app/src/pages/data.json"):
        with open("../my-app/src/pages/data.json", "r") as file:
            json_data = json.load(file)
            print("json_data loaded")
    else:
        json_data = [{}]
        exist = False
        print("json_data file not found. Starting with an empty json.")
        if not os.path.exists("../my-app/src/pages"):
            print("problem here")

    #current_date = datetime.now()
    print("trying to save 1")
    formatted_date = "06-" + str(day) + "-2023"
    day += 1
    #formatted_date = current_date.strftime('%m-%d-%Y')
    print("trying to save 2")
    print(emotion)
    color = get_color(emotion)
    print("trying to save 3")
    new_data = {
        formatted_date: [color, response],
    }
    
    print("trying to save 5")

    if exist:
        json_data.append(new_data)
    else:
        json_data = [new_data]

    print("trying to save")
    with open("../my-app/src/pages/data.json", 'w') as file:
        json.dump(json_data, file)
        print("json_data saved")

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
