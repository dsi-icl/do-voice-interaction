from os import set_inheritable
from flask import Flask, request
import json
from model_utils import *
import spacy
import pyinflect

GRAMMATICALLY_CORRECT_CONFIDENCE = 99

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")


@app.route("/grammar-correction", methods=['POST'])
def perform_grammar_correcection():
    receivedData = json.loads(request.data)
    text_data = receivedData['transcript']

    corrections = []
    predicted_sentence = text_data

    # check grammatical correctnes of command
    # if the confidence with which the sentence is correct is < 0.96
    # then perform sentence correction
    predictions = check_GE([text_data])
    if predictions[0] < GRAMMATICALLY_CORRECT_CONFIDENCE:
        # perform parts of speech tagging
        doc = tag_parts_of_speech(text_data)

        predicted_sentence, corrections = correct_verbs(text_data, doc)

    data = {'status': 'ok', 'service': 'grammar correction service', 'response': corrections,
            'predicted_sentence': predicted_sentence}

    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

    return response


def get_verb_ids(doc):
    pos = []
    for i in range(len(doc)):
        if doc[i].pos_ == 'VERB' or doc[i].pos_ == 'AUX':
            pos.append(i)

    return pos


def correct_verbs(text_data, pos_original):
    verb_ids = get_verb_ids(pos_original)

    predicted_sentence, corrections = predict_corrections(text_data, verb_ids)

    # Check whether a completely new verb has been suggested by BERT
    # instead of just a grammatically correct version
    pos_prediction = nlp(predicted_sentence)
    for verb_id in verb_ids:

        # Check if the lemma is the same for the prediction
        if pos_original[verb_id].lemma_ != pos_prediction[verb_id].lemma_:
            # If not we compare tenses to see whether BERT just proposed
            # a 'better-fit' word or has found a mistake in the tense
            if pos_original[verb_id].tag_ == pos_prediction[verb_id].tag_:
                predicted_sentence = predicted_sentence.replace(pos_prediction[verb_id].text,
                                                                pos_original[verb_id].text, 1)
                corrections.remove(verb_id)
            else:
                inflected_verb = pos_original[verb_id]._.inflect(pos_prediction[verb_id].tag_)
                if inflected_verb is not None:
                    predicted_sentence = predicted_sentence.replace(pos_prediction[verb_id].text, inflected_verb, 1)
                else:
                    predicted_sentence = predicted_sentence.replace(pos_prediction[verb_id].text,
                                                                    pos_original[verb_id].text, 1)
                    corrections.remove(verb_id)

    return predicted_sentence, corrections

def tag_parts_of_speech(text_data):
    doc = nlp(text_data)

    # do stuff here that will manipulate the Doc object and return useful info

    return doc

# sent = "Can you provides me with your skills?"
# doc = tag_parts_of_speech(sent)
# # predictions = check_GE([sent])
# new_sent, ind = correct_verbs(sent, doc)
# # print(predictions[0])
# print(new_sent)

# if predictions[0] < GRAMMATICALLY_CORRECT_CONFIDENCE:
#     prediction, corrections = correct_verbs(sent, doc)
#     print(prediction)
#     print(corrections)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)  # set debug=False for production
