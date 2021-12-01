from nltk import tokenize
import preprocess as prep
import speech_filler_utils as nsf
from flask import Flask, request
import json

app = Flask(__name__)

# Generates a string to be used as input for cereproc's tts
# after naturalising the sentence by adding speech fillers and pauses
@app.route("/speech-fillers", methods=['POST'])
def naturalise_command():

    receivedData = json.loads(request.data)
    text_data = receivedData['text']

    # Two lists of bigrams of words containing NSF as either the predecessor
    # or the successor to a word are constructed from the training data.
    # Data is presented in triplets in the order:
    # predecessor: NSF, word, freq
    # successor: word, NSF, freq
    predecessors, successors = prep.get_filler_lists()

    sentences = tokenize.sent_tokenize(text_data)

    cereproc_command = "<speak> \n"

    for sentence in sentences:
        sentence = nsf.insert_speech_fillers(sentence, predecessors, successors)
        cereproc_command = cereproc_command + " " + nsf.add_cereproc_commands(sentence)

    cereproc_command = cereproc_command + "\n </speak>"

    data = {'status': 'ok', 'service': 'speech fillers service', 'response': cereproc_command}

    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )

    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)  # set debug=False for production


# sent1 = "I was wondering if you would be interested in coming to the movies with me"
# sent2 = "Can I enable emotion detection so that I can understand you better?"
# sent3 = "When we actually started recording the album we had this beautiful place that we rented."
# sent4 = "Would you like me to turn in on?"
# sent5 = "So would you be willing to read through my work?"
# sent6 = "Yes, of course, that sounds great"
# print(naturalise_command(sent1))
# print()
# print(naturalise_command(sent2))
# print()
# print(naturalise_command(sent3))
# print()
# print(naturalise_command(sent4))
# print()
# print(naturalise_command(sent5))
# print()
# print(naturalise_command(sent6))