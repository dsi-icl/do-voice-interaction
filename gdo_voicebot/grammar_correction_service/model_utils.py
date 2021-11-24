import torch
import numpy as np
from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM
from pytorch_pretrained_bert import BertForSequenceClassification
from keras.preprocessing.sequence import pad_sequences
from difflib import SequenceMatcher
import os.path
import requests

class CustomBERTModel(torch.nn.Module):
    def __init__(self):
          super(CustomBERTModel, self).__init__()
          self.bert = BertModel.from_pretrained('bert-base-uncased')
          ### New layer:
          self.linear = nn.Linear(768, 1)

    def forward(self, input_ids):
          outputs = self.bert(input_ids, token_type_ids=None)
          last_hidden_states = outputs.last_hidden_state

          # last_hidden_states has the following shape: (batch_size, sequence_length, hidden_size)
          linear_output = self.linear(last_hidden_states[:,0,:])

          return linear_output

# credit: https://stackoverflow.com/a/39225039
def download_file_from_google_drive(id, destination):
    print("Trying to fetch {}".format(destination))

    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in progress_bar(response.iter_content(CHUNK_SIZE)):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)
    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def progress_bar(some_iter):
    try:
        from tqdm import tqdm
        return tqdm(some_iter)
    except ModuleNotFoundError:
        return some_iter


def load_grammar_checker_model():
    if (not os.path.isfile('./bert-based-uncased-GDO-lang-8-cola-trained.pth')):
        download_file_from_google_drive('1sPfnUFnzSxbGA9nxvGn85Eds8wU_JyuD',
                                        './bert-based-uncased-GDO-lang-8-cola-trained.pth')

    device = torch.device('cpu')
    grammar_checker = CustomBERTModel()
    grammar_checker.load_state_dict(torch.load('bert-based-uncased-GDO-lang-8-cola-trained.pth', map_location=device))
    grammar_checker.eval()

    return grammar_checker


def load_grammar_corrector_model():
    grammar_corrector = BertForMaskedLM.from_pretrained('bert-large-uncased')
    grammar_corrector.eval()

    return grammar_corrector


def create_tokenizer():
    return BertTokenizer.from_pretrained('bert-base-uncased')


def create_mask_set(sentence, mask_id):
    sent = sentence.strip().split()
    new_sent = sent[:]
    if mask_id >= len(new_sent):
        print(new_sent)
        print(mask_id)
    new_sent[mask_id] = '[MASK]'
    return '[CLS] ' + " ".join(new_sent) + ' [SEP]'


def check_GE(sents):
    tokenized_texts = [tokenizer.tokenize(str(sent)) for sent in sents]

    # Padding Sentences
    padded_sequence = [tokenizer.convert_tokens_to_ids(txt) for txt in tokenized_texts]
    max_len = max([len(txt) for txt in padded_sequence])

    # Pad our input tokens
    input_ids = pad_sequences(padded_sequence, maxlen=max_len, dtype="long",
                              truncating="post", padding="post")

    prediction_inputs = torch.tensor(input_ids)
    prediction_labels = torch.tensor(labels)

    with torch.no_grad():
        # Forward pass, calculate logit predictions
        logits = checker_model(prediction_inputs, token_type_ids=None)

    # Move logits and labels to CPU
    logits = logits.detach().cpu().numpy()

    predictions = torch.round(torch.sigmoid(y_pred))

    return predictions


def check_grammar(original_sentence, masked_sentence):
    text = '[MASK]'
    tokenized_text = tokenizer.tokenize(text)
    mask_token = tokenizer.convert_tokens_to_ids(tokenized_text)[0]

    # tokenize the text
    tokenized_text = tokenizer.tokenize(masked_sentence)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

    # Create the segments tensors.
    segments_ids = [0] * len(tokenized_text)

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    # Predict all tokens
    with torch.no_grad():
        predictions = corrector_model(tokens_tensor, segments_tensors)

    # index of the masked token
    mask_index = (tokens_tensor == mask_token).nonzero()[0][1].item()
    # predicted token
    predicted_index = torch.argmax(predictions[0, mask_index]).item()
    predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]

    text = masked_sentence.strip().split()
    mask_index = text.index('[MASK]')

    text[mask_index] = predicted_token
    original_word = original_sentence.strip().split()[mask_index - 1]

    text.remove('[SEP]')
    text.remove('[CLS]')
    new_sent = " ".join(text)

    if original_word == predicted_token:
        return new_sent, True

    return new_sent, False


def predict_corrections(original_sentence, mask_ids):
    # Check grammatical correctness by masking each word
    # at position mask_id from list of mask_ids
    corrections = []
    sentence = original_sentence

    for i in range(len(mask_ids)):
        masked_sentence = create_mask_set(sentence, mask_ids[i])
        sentence, correct = check_grammar(sentence, masked_sentence)
        if not correct:
            corrections.append(mask_ids[i])

    return sentence, corrections


# Load pre-trained model tokenizer
tokenizer = create_tokenizer()
checker_model = load_grammar_checker_model()
corrector_model = load_grammar_corrector_model()
