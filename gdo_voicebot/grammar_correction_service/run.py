from flask import Flask, request
import json
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/error-correction", methods=['POST'])
def tag_parts_of_speech():
    receivedData = json.loads(request.data)
    text_data = receivedData['transcript']
    doc = nlp(text_data)

    return doc

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000, debug=False) # set debug=False for production
