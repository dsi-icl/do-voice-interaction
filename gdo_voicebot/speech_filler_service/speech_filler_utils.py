import string
import nltk
import numpy as np
from numpy.random import choice

# TODO: Add to docker-compose files/requirements?
# nltk.download('punkt')

# Parameter that controls the degree of naturalisation
DEGREE_OF_NAT = 0.15
EXTRA_TOKENS = 2


# Calculates number of speech fillers to be inserted
# based on the degree of naturalisation and the length of the sentence
def speech_filler_num(input_text):
    return int(DEGREE_OF_NAT * (len(input_text) - EXTRA_TOKENS))


# Checks whether a word is one of the approved natural speech fillers
def is_nsf(word):
    return word == "(um)" or \
           word == "(uh)" or \
           word == "(pause)"


# Adds the vocal gesture IDs needed by cereproc
# corresponding to the approved natural speech fillers
def add_cereproc_commands(sentence):
    sentence = sentence.replace("(um)", "<spurt audio=\"g0001_015\">umm</spurt>")
    sentence = sentence.replace("(uh)", "spurt audio=\"g0001_014\">hmm thinking</spurt>")
    sentence = sentence.replace("(pause)", "...")

    sentence = sentence.replace("START", "")
    sentence = sentence.replace("END", "")

    return sentence


# Creates a set of the probabilities P with which a bigram appears
# in a subset of the draw set based on the formula
# P = frequency of the bigram in the data / size of draw set
def create_nsf_distribution(draw_set):
    set_of_prob = []

    draw_set_size = sum(n for ((_, n), _) in draw_set)
    for i in range(len(draw_set)):
        set_of_prob.append(draw_set[i][0][1] / draw_set_size)

    return set_of_prob


# Adds the natural speech fillers into the sentence from the
# chosen set of bigrams
def generate_nsf_sentence(sentence, draw_set):
    new_sent = sentence.split()
    for (bigram, pos) in draw_set:
        if is_nsf(bigram[0][0]):
            new_sent = new_sent[:(pos - 1)] + [bigram[0][0]] + new_sent[(pos - 1):]
        else:
            new_sent = new_sent[:pos] + [bigram[0][1]] + new_sent[pos:]

    return ' '.join(word for word in new_sent)


# A sentence as well as two lists of bigrams of words containing NSF
# is passed as input. Produces a transformed sentence with
# inserted pauses and natural speech fillers.
def insert_speech_fillers(text, predecessors, successors):

    # Clean input sentence by setting it to lower case and
    # removing punctuation; add start token in the beginning of the sentence
    # TODO: Not sure this is necessary as we are
    #  only filling in commands given by the assistant?
    sentence = text.translate(string.punctuation)
    sentence = "START " + sentence.lower() + " END"

    # Split sentence into bigrams
    tokenized_sent = nltk.word_tokenize(sentence)
    bigrams = list(nltk.ngrams(tokenized_sent, 2))

    # Find all possible insertions in the input sentence by splitting it into bigrams and
    # comparing the predecessor and successor with the list of bigrams from step 1.
    draw_set = []

    pos = 0
    for bigram in bigrams:
        pred_nsf = [(nsf, pos) for nsf in predecessors if nsf[0][1] == bigram[1]]
        succ_nsf = [(nsf, pos) for nsf in successors if nsf[0][0] == bigram[0]]

        draw_set.extend(pred_nsf)
        draw_set.extend(succ_nsf)
        pos += 1

    # Draw a subset from D based on the degree of naturalization and a probability distribution.
    possible_fillers = speech_filler_num(tokenized_sent)
    draw_subset = np.array(draw_set, dtype=object)
    draw_subset = draw_subset[choice(draw_subset.shape[0], possible_fillers, p=create_nsf_distribution(draw_set))]

    # Construct the output sentence by adding the bigrams (filler word included) that are
    # part of the subset of D
    draw_subset = sorted(draw_subset, key=lambda tup: tup[1], reverse=True)

    return generate_nsf_sentence(sentence, draw_subset)

