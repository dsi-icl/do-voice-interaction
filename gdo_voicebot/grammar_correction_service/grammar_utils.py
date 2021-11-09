from enum import Enum
from model_utils import *
import spacy
import pyinflect

nlp = spacy.load("en_core_web_sm")

# possessive adjectives used in the English language
poss_adj = ['my', 'your', 'our', 'its', 'her', 'his', 'their',
            'My', 'Your', 'Our', 'Its', 'Her', 'His', 'Their']


class GrammarParts(Enum):
    ADPOS = 1
    DETERMINER = 2
    VERB = 3


# Get the ids of all words which correspond to grammar_part in doc
def get_ids(doc, grammar_part):
    pos = []

    if grammar_part is GrammarParts.ADPOS:
        for i in range(len(doc)):
            if doc[i].pos_ == 'ADP':
                pos.append(i)

    if grammar_part is GrammarParts.DETERMINER:
        for i in range(len(doc)):
            if doc[i].pos_ == 'DET' or doc[i].pos_ == 'PRON':
                pos.append(i + doc.start)

    if grammar_part is GrammarParts.VERB:
        for i in range(len(doc)):
            if doc[i].pos_ == 'VERB' or doc[i].pos_ == 'AUX':
                pos.append(i)

    return pos


def correct_verbs(text_data, pos_original):
    verb_ids = get_ids(pos_original, GrammarParts.VERB)

    predicted_sentence, corrections = predict_corrections(text_data, verb_ids)

    # Check whether a completely new verb has been suggested by BERT
    # instead of just a grammatically correct version
    pos_prediction = nlp(predicted_sentence)
    final_corrections = corrections.copy()

    for verb_id in corrections:

        # Check if the lemma is the same for the prediction
        if pos_original[verb_id].lemma_ != pos_prediction[verb_id].lemma_:
            # If not we compare tenses to see whether BERT just proposed
            # a 'better-fit' word or has found a mistake in the tense
            if pos_original[verb_id].tag_ == pos_prediction[verb_id].tag_:
                predicted_sentence = predicted_sentence.replace(pos_prediction[verb_id].text,
                                                                pos_original[verb_id].text, 1)
                final_corrections.remove(verb_id)
            else:
                inflected_verb = pos_original[verb_id]._.inflect(pos_prediction[verb_id].tag_)
                if inflected_verb is not None:
                    predicted_sentence = predicted_sentence.replace(pos_prediction[verb_id].text, inflected_verb, 1)
                else:
                    predicted_sentence = predicted_sentence.replace(pos_prediction[verb_id].text,
                                                                    pos_original[verb_id].text, 1)
                    final_corrections.remove(verb_id)

    return predicted_sentence, final_corrections


def correct_adpositions(text_data, pos_original):
    adp_ids = get_ids(pos_original, GrammarParts.ADPOS)
    corrected_sentence = text_data
    corrections = []

    if adp_ids:
        # Ensure that correct adposition was used in sentence
        corrected_sentence, corrections = predict_corrections(text_data, adp_ids)
        pos_corrected = nlp(corrected_sentence)

        for i, adp_id in enumerate(adp_ids):
            if pos_corrected[adp_id].pos_ != 'ADP':
                corrected_sentence = corrected_sentence.replace(pos_corrected[adp_id].text,
                                                                pos_original[adp_id].text, 1)

    # Check that an adposition was not missed by masking spaces
    sent = corrected_sentence.strip().split()

    i = 0

    while i < len(sent):
        new_sent = sent[:]
        new_sent[i] = "adposition {}".format(new_sent[i])

        predicted_sentence, _ = predict_corrections(" ".join(new_sent), [i])
        pos_predicted = nlp(predicted_sentence)

        if pos_predicted[i].pos_ == 'ADP':
            corrected_sentence = corrected_sentence.replace(pos_predicted[i + 1].text, "{} {}".format(
                pos_predicted[i].text, pos_predicted[i + 1].text), 1)
            i = i + 1

        sent = corrected_sentence.strip().split()
        i = i + 1

    return corrected_sentence, corrections


def correct_determiners(text_data, pos_original):
    corrected_sentence = text_data

    for noun_phrase in pos_original.noun_chunks:
        start_id = noun_phrase.start
        phrase_length = noun_phrase.end - start_id

        if phrase_length > 1 or (phrase_length == 1 and noun_phrase[0].pos_ == 'NOUN'):
            det_ids = get_ids(noun_phrase, GrammarParts.DETERMINER)
            if not det_ids:
                # there are no determiners in the noun phrase
                modified_sent = text_data.replace(noun_phrase.text,
                                                  "determiner {}".format(noun_phrase.text), 1)
                predicted_sentence, predicted_corrections = predict_corrections(modified_sent, [start_id])

                # Case where BERT suggests something other than a determiner/possessive adj
                pos_predicted = nlp(predicted_sentence)
                if pos_predicted[start_id].pos == 'DET' or pos_predicted[start_id].text in poss_adj:
                    sent = predicted_sentence.strip().split()
                    new_sent = sent[:]
                    corrected_sentence = corrected_sentence.replace(noun_phrase.text,
                                                                    "{} {}".format(new_sent[start_id],
                                                                                   noun_phrase.text), 1)
            if len(det_ids) == 1:
                # there is only one determiner
                predicted_sentence, predicted_corrections = predict_corrections(text_data, det_ids)
                pos_predicted = nlp(predicted_sentence)

                if pos_predicted[det_ids[0]].pos_ == 'DET:':
                    corrected_sentence = predicted_sentence

            if len(det_ids) > 1:
                # there are multiple determiners in a noun phrase
                sent = noun_phrase.text.strip().split()
                new_sent = sent[:]

                for i in range(1, len(det_ids)):
                    new_sent[i] = ""

                sent = " ".join(list(filter(None, new_sent)))
                corrected_sentence = corrected_sentence.replace(noun_phrase.text, sent, 1)
                det_ids.remove(det_ids[0])

        # Case we are not covering: using a/an with uncountable nouns

    return corrected_sentence


def correct_sentence(text_data):
    # perform parts of speech tagging and correct the verbs
    doc = nlp(text_data)
    predicted_sentence_v, corrections_v = correct_verbs(text_data, doc)

    # perform parts of speech tagging and correct the adpositions
    doc = nlp(predicted_sentence_v)
    predicted_sentence_adp, corrections_adp = correct_adpositions(predicted_sentence_v, doc)

    # perform parts of speech tagging and correct the determiners
    doc = nlp(predicted_sentence_adp)
    predicted_sentence_det = correct_determiners(predicted_sentence_adp, doc)

    # combine indices of all corrections in one list, remove duplicates and sort
    corrections = corrections_v + corrections_adp

    return predicted_sentence_det, corrections