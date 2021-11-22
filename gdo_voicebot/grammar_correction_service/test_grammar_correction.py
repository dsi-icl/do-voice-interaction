import unittest
from model_utils import *
from grammar_utils import *
from run import *
import csv


class TestGrammar(unittest.TestCase):

    def __valid_sentences_test(self):
        sentences = open("tests/testing.tsv", "r")
        tsvreader = csv.reader(sentences, delimiter="\t")
        true_positives = 0
        false_negatives = 0
        i = 0
        for sent in tsvreader:
            if i % 100 == 0:
                print(i)
            i = i + 1
            if sent[0] == '1':
                sent = preprocess(sent[1])
                predictions = check_GE([sent])
                if predictions[0] < GRAMMATICALLY_CORRECT_CONFIDENCE:
                    false_negatives = false_negatives + 1
                else:
                    true_positives = true_positives + 1

        sentences.close()
        return true_positives, false_negatives

    def __invalid_sentences_test(self):
        sentences = open("tests/testing.tsv", "r")
        corrections = open("tests/corrections.txt", "w")
        tsvreader = csv.reader(sentences, delimiter="\t")
        false_positives = 0
        true_negatives = 0
        true_corrections = 0
        false_corrections = 0
        i = 0
        for sent in tsvreader:
            if i % 100 == 0:
                print(i)
            i = i + 1
            if sent[0] == '0':
                incorrect = preprocess(sent[1])
                predictions = check_GE([incorrect])
                if predictions[0] < GRAMMATICALLY_CORRECT_CONFIDENCE:
                    true_negatives = true_negatives + 1
                    correction, _ = correct_sentence(incorrect)
                    predictions = check_GE([correction])
                    corrections.write(correction + ' -- ' + str(predictions[0]) + '\n')
                    if predictions[0] >= GRAMMATICALLY_CORRECT_CONFIDENCE:
                        true_corrections = true_corrections + 1
                    else:
                        false_corrections = false_corrections + 1
                else:
                    false_positives = false_positives + 1

        sentences.close()
        corrections.close()
        return false_positives, true_negatives, true_corrections, false_corrections

    def test_grammar_correction(self):
        metrics = open("tests/metrics.txt", "r")
        prev_accuracy = float(metrics.readline().strip())
        prev_precision = float(metrics.readline().strip())
        prev_recall = float(metrics.readline().strip())
        prev_correction_score = float(metrics.readline().strip())
        metrics.close()

        print("Testing valid sentences...")
        true_positives, false_negatives = self.__valid_sentences_test()
        print("Testing invalid sentences...")
        false_positives, true_negatives, true_corrections, false_corrections = self.__invalid_sentences_test()
        print(true_corrections)
        print(false_corrections)

        if (true_positives + true_negatives + false_positives + false_negatives) != 0:
            new_accuracy = (true_positives + true_negatives) / (
                        true_positives + true_negatives + false_positives + false_negatives)
        else:
            new_accuracy = 0

        if (true_positives + false_positives) != 0:
            new_precision = true_positives / (true_positives + false_positives)
        else:
            new_precision = 0

        if (true_positives + false_negatives) != 0:
            new_recall = true_positives / (true_positives + false_negatives)
        else:
            new_recall = 0

        if (true_corrections + false_corrections) != 0:
            new_correction_score = true_corrections / (true_corrections + false_corrections)
        else:
            new_correction_score = 0

        print("--------------------------ACCURACY----------------------------")
        print(new_accuracy)
        print("--------------------------PRECISION---------------------------")
        print(new_precision)
        print("---------------------------RECALL-----------------------------")
        print(new_recall)
        print("----------------------CORRECTION SCORE------------------------")
        print(new_correction_score)

        metrics = open("tests/metrics.txt", "w")
        if new_accuracy > prev_accuracy:
            metrics.write(str(new_accuracy) + '\n')
        else:
            metrics.write(str(prev_accuracy) + '\n')
        if new_precision > prev_precision:
            metrics.write(str(new_precision) + '\n')
        else:
            metrics.write(str(prev_precision) + '\n')
        if new_recall > prev_recall:
            metrics.write(str(new_recall) + '\n')
        else:
            metrics.write(str(prev_recall) + '\n')
        if new_correction_score > prev_correction_score:
            metrics.write(str(new_correction_score) + '\n')
        else:
            metrics.write(str(prev_correction_score) + '\n')

        metrics.close()

        self.assertGreaterEqual(new_accuracy, prev_accuracy, "New accuracy is lower than previously achieved accuracy")
        self.assertGreaterEqual(new_precision, prev_precision,
                                "New precision is lower than previously achieved precision")
        self.assertGreaterEqual(new_recall, prev_recall, "New recall is lower than previously achieved recall")
        self.assertGreaterEqual(new_correction_score, prev_correction_score,
                                "New grammar correction score is lower than previously achieved grammar correction "
                                "score")


if __name__ == '__main__':
    unittest.main()
