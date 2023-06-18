import openai
import numpy as np
import re

openai.api_key = "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"

SYSTEM_INSTUCTIONS = """You are a emotion journal AI assistant.
Your goal is to give the user advice on their issues and help them get into a better mental state.
You will be apologetic in the first sentence if the user is dealing with an issue.
Your responses will be 1-5 sentences and your last sentence will be the advice to give the user.
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

    

    message = create_message(transcription, user_emotions)
    conversation.append({"role": "user", "content": message})
    # completion = openai.ChatCompletion.create(model="gpt-4", messages=conversation)
    # response = completion.choices[0]['message']['content']
    response = "none"
    conversation.append({"role": "assistant", "content": response})
    response = re.sub(r'\([^)]*\)', '', response)
    response = re.sub(r'\[.*?\]', '', response)
    response = re.sub(r'^"|"$', '', response)
    emotion_history = []
    
    return user_emotions
    return response