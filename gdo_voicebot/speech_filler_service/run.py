import string
import nltk

# Two lists of bigrams of words containing NSF as either the predecessor
# or the successor to a word are constructed from the training data.
# Data is presented in triplets in the order:
# predecessor: NSF, word, freq
# successor: word, NSF, freq
from nltk import ngrams, word_tokenize

predecessors = [("(pause)", "i", 13602), ("(pause)", "and", 8364), ("(uh)", "i", 83)]
successors = [("you", "(pause)", 4533), ("and", "(uh)", 100), ("and", "(pause)", 135)]


def insert_speech_fillers(text):
    # ASSUME: A Single Sentence Is Given - might not always be the case
    # so this will need to be a for loop

    # Clean input sentence by setting it to lower case and
    # removing punctuation; add start token in the beginning of the sentence
    # TODO: Not sure this is necessary as we are
    #  only filling in commands given by the assistant?
    sentence = text.translate(None, string.punctuation)
    sentence = "(start)" + sentence.lower()

    # Split sentence into bigrams
    tokenized_sent = word_tokenize(sentence)
    bigrams = list(ngrams(tokenized_sent, 2))

    # Find all possible insertions in the input sentence by splitting it into bigrams and
    # comparing (III) the predecessor and successor with the list of bigrams from step 1.
    draw_set = []

    for bigram in bigrams:
        pred_nsf = [nsf for nsf in predecessors if nsf[1] == bigram[1]]
        succ_nsf = [nsf for nsf in successors if nsf[0] == bigram[0]]

        if not pred_nsf:
            draw_set.extend(succ_nsf)
        # else:
        #     for nsf in pred_nsf:
        #

    # Draw a subset from D based on the degree of naturalization and a probability distribution.

    # Fallback method with POS tagging

    # Construct the output sentence by adding the bigrams (filler word included) that are
    # part of the subset of D

    return sentence

