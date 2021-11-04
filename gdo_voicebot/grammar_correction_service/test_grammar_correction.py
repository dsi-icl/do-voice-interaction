import unittest
from model_utils import *
from run import *

class TestGrammar(unittest.TestCase):

    def __valid_sentences_test(self):
        valid_cases = open("tests/valid_cases.txt", "r")
        true_positives = 0
        false_negatives = 0
        for sent in valid_cases:
            sent = sent.strip()
            print("CORRECT SENTENCE:")
            print(sent)
            print("\n")
            predictions = check_GE([sent])
            print("PREDICTION CONFIDENCE:")
            print(predictions[0])
            print("\n")
            if predictions[0] < GRAMMATICALLY_CORRECT_CONFIDENCE:
                print("Predicted as incorrect")
                false_negatives = false_negatives + 1
            else:
                print("Predicted as correct")
                true_positives = true_positives + 1

            print("--------------------------------------------------------------")

        valid_cases.close()
        return true_positives, false_negatives


    def __invalid_sentences_test(self):
        invalid_cases = open("tests/invalid_cases.txt", "r")
        invalid_corrections = open("tests/invalid_corrections.txt", "r")
        false_positives = 0
        true_negatives = 0
        true_corrections = 0
        false_corrections = 0
        for sent in invalid_cases:
            sent = sent.strip()
            print("INCORRECT SENTENCE:")
            print(sent)
            print("\n")
            expected_correction = invalid_corrections.readline().strip()
            predictions = check_GE([sent])
            print("PREDICTION CONFIDENCE:")
            print(predictions[0])
            print("\n")
            if predictions[0] < GRAMMATICALLY_CORRECT_CONFIDENCE:
                print("Predicted as incorrect")
                print("\n")
                true_negatives = true_negatives + 1
                doc = tag_parts_of_speech(sent)
                correction, _ = correct_verbs(sent, doc)
                print("CORRECTION:")
                print(correction)
                print("\n")
                print("EXPECTED CORRECTION:")
                print(expected_correction)
                if correction == expected_correction:
                    true_corrections = true_corrections + 1
                else:
                    false_corrections = false_corrections + 1
            else:
                print("Predicted as correct")
                false_positives = false_positives + 1
        
            print("--------------------------------------------------------------")

        invalid_cases.close()
        invalid_corrections.close()
        return false_positives, true_negatives, true_corrections, false_corrections

    def test_grammar_correction(self):
        metrics = open("tests/metrics.txt", "r")
        prev_accuracy = float(metrics.readline().strip())
        prev_precision = float(metrics.readline().strip())
        prev_recall = float(metrics.readline().strip())
        prev_correction_score = float(metrics.readline().strip())
        metrics.close()

        true_positives, false_negatives = self.__valid_sentences_test()
        false_positives, true_negatives, true_corrections, false_corrections = self.__invalid_sentences_test()

        new_accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)
        new_precision = true_positives / (true_positives + false_positives)
        new_recall = true_positives / (true_positives + false_negatives)
        new_correction_score = true_corrections / (true_corrections + false_corrections)

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
        self.assertGreaterEqual(new_precision, prev_precision, "New precision is lower than previously achieved precision")
        self.assertGreaterEqual(new_recall, prev_recall, "New recall is lower than previously achieved recall")
        self.assertGreaterEqual(new_correction_score, prev_correction_score, "New grammar correction score is lower than previously achieved grammar correction score")

if __name__ == '__main__':
    unittest.main()