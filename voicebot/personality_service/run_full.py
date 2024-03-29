### This file contains code to start a Flask app and 
### load a parameterised personality.


from flask import Flask
from flask import request
import json
from personality_full import Personality
import numpy as np

app = Flask(__name__)
personality = Personality([0,0], 0, 0, 1)

def process(str):
    (x,y)=str.split(",")
    return [round(float(x), 3), round(float(y), 3)]

@app.route("/personality-service", methods=['GET'])
def updatePersonality():
    emotion = process(request.args["emotion"])
    global personality
    personality.updateThayers(emotion)
    personalityState = np.array2string(personality.getThayers(), precision=3, separator=',', suppress_small=True)
    personalityState = personalityState[1:-1]
    data = {'status': 'ok', 'service': 'personality-service', 'personalityState': personalityState}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    return response

def selectPersonality(selected):
    global personality
    if selected == "angry":
        personality  = Personality([-0.7, 0.7], -2, 3, 2)
    if selected == "neutral":
        personality = Personality([0,0],1, 10, 0.2)
    if selected == "sad":
        personality = Personality([-0.7, -0.7], 2, 3, 0.5)
    elif selected == "excited":
        personality  = Personality([0.8, 0.5], 0.2, 3, 0.5)
    

### Change the type of personality to be loaded here

selectPersonality("excited")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000, debug=False)



