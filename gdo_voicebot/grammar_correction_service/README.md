# Grammar Correction Service

This repository was developed to provide a grammar correction feature to the DO voicebot.
It works by checking the command input by a user for grammatical errors and then making any necesary correction.
Such modified command can then be passed to the Dialogue Manager, increasing the accuracy of the responses.
The tool uses two Bert models, one for checking the grammatical correctness of a sentence and another for correcting the mistakes in a grammatically incorrect sentence. Currently the service corrects verbs, adpositions and determiners.

## Preparation

### Installing libraries (NO need to do this if you're running from Docker)
1. Run pip install -r requirements.txt

### Get all necessary files
1. Download the files ['here'](https://imperialcollegelondon.box.com/s/okzb2csabvgn2wcm6n03cxhol6jdim57).
2. Place them all in the `tests/` folder

## Testing

To test the service and obtain metrics simply run `test_grammar_correction.py`. Make sure you have downloaded the `testing.tsv` file
from the box before. The test uses a sample from the lang-8 dataset to check the performance of the grammar correction tool. It calculates different metrics such as the accuracy, recall, precision and if they are better than the previously achieved ones overwrites the tests/metrics.txt file. The file should contain 4 lines meaning the following: accuracy, precision, recall of the grammar checking model and the percentage of well corrected sentences.

## Grammar Checker Model

The process of creating our model and how to use it can be found in the `grammar_checker_model` directory. It is used within the service in `model_utils.py`.

## Code structure

##### `run.py`

The API of the grammar correction service. Calls methods of `grammar_utils.py`and `model_utils.py` to perform grammar checking and correction if necessary.

##### `grammar_utils.py`

Contains helper functions for correcting grammatical errors. Currently verb, adposition and determiner errors are supported.

##### `model_utils.py`

Interacts with the models, checking sentence grammar/correcting mistakes.

##### `test_grammar_correction.py`

Tests for the grammar correction service (see description above).

##### `tests/`

Folder containing input and output files necessary for service testing.
