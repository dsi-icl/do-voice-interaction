from flask import Flask, request
import json
from grammar_utils import *

GRAMMATICALLY_CORRECT_CONFIDENCE = 96

app = Flask(__name__)


@app.route("/grammar-correction", methods=['POST'])
def perform_grammar_correction():
    receivedData = json.loads(request.data)
    text_data = receivedData['transcript']

    predicted_sentence = text_data
    corrections = []

    # check grammatical correctness of command
    # if the confidence with which the sentence is correct is < 0.96
    # then perform sentence correction
    predictions = check_GE([text_data])
    if predictions[0] < GRAMMATICALLY_CORRECT_CONFIDENCE:
        predicted_sentence, corrections = correct_sentence(text_data)

    data = {'status': 'ok', 'service': 'grammar correction service', 'response': corrections,
            'predicted_sentence': predicted_sentence}

    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)  # set debug=False for production
