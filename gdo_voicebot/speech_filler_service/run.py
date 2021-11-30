from nltk import tokenize
import preprocess as prep
import speech_filler_utils as nsf


# Generates a string to be used as input for cereproc's tts
# after naturalising the sentence by adding speech fillers and pauses
def naturalise_command(text):

    # Two lists of bigrams of words containing NSF as either the predecessor
    # or the successor to a word are constructed from the training data.
    # Data is presented in triplets in the order:
    # predecessor: NSF, word, freq
    # successor: word, NSF, freq
    predecessors, successors = prep.get_filler_dicts()

    sentences = tokenize.sent_tokenize(text)

    cereproc_command = "<speak> \n"

    for sentence in sentences:
        sentence = nsf.insert_speech_fillers(sentence, predecessors, successors)
        cereproc_command = cereproc_command + " " + nsf.add_cereproc_commands(sentence)

    cereproc_command = cereproc_command + "\n </speak>"

    return cereproc_command


# sent = "I was wondering if you would be interested in coming to the movies with me"
# print(naturalise_command(sent))
