from flask import Flask, request
import json
from grammar_utils import *

GRAMMATICALLY_CORRECT_CONFIDENCE = 70

app = Flask(__name__)


@app.route("/grammar-correction", methods=['POST'])
def perform_grammar_correction():
    receivedData = json.loads(request.data)
    text_data = receivedData['transcript']
    text_data = preprocess(text_data)

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

def preprocess(text):
    text = text.replace("don't", "do not")
    text = text.replace("cant't", "can not")
    text = text.replace("isn't", "is not")
    text = text.replace("aren't", "are not")
    text = text.replace("couldn't", "could not")
    text = text.replace("wouldn't", "would not")
    text = text.replace("won't", "will not")
    text = text.replace("I'm", "I am")
    text = text.replace("i'm", "i am")
    text = text.replace("she's", "she is")
    text = text.replace("he's", "he is")
    text = text.replace("we're", "we are")
    text = text.replace("they're", "they are")
    text = text.replace("you're", "you are")
    text = text.replace("it's", "it is")
    text = text.replace("that's", "that is")
    text = text.replace("wasn't", "was not")
    text = text.replace("weren't", "were not")
    text = text.replace("hasn't", "has not")
    text = text.replace("haven't", "have not")
    text = text.replace("doesn't", "does not")

    return text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)  # set debug=False for production
