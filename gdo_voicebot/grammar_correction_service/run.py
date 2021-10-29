from flask import Flask, request
import json
from gdo_voicebot.grammar_correction_service.model_utils import * 
import spacy

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

@app.route("/grammar-correction", methods=['POST'])
def perform_grammar_correcection():
    receivedData = json.loads(request.data)
    text_data = receivedData['transcript']

    # perform parts of speech tagging
    doc = tag_parts_of_speech(text_data)

    # bert stuff

    verb_ids = get_verb_ids(doc)
    predicted_sentence, corrections = predict_corrections(text_data, verb_ids)

    data = {'status': 'ok', 'service': 'grammar correction service', 'response': corrections, 'predicted_sentence': predicted_sentence}

    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

    return response

def get_verb_ids(doc):
    pos = []
    for i in range(len(doc)):
        if doc[i].pos_ == 'VERB':
            pos.append(i)

    return pos

def tag_parts_of_speech(text_data):
    doc = nlp(text_data)

    # do stuff here that will manipulate the Doc object and return useful info

    return doc

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False) # set debug=False for production
