from flask import Flask
from flask import request
import whisper
import json
import base64

app = Flask(__name__)


model = whisper.load_model("base")



@app.route("/api/stt", methods=['POST'])
def speech_to_text():
    audio=request.data
    mp3_data = base64.b64decode(audio)
    with open('audio.mp3', 'wb') as f:
        f.write(mp3_data)
    result = model.transcribe("audio.mp3")
    data = {'status': 'ok', 'service': 'Speech To Text service', 'text': result['text']}
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=False)