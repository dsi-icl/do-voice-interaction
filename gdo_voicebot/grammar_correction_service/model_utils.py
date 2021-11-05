import torch
import numpy as np
from pytorch_pretrained_bert import BertTokenizer, BertForMaskedLM
from pytorch_pretrained_bert import BertForSequenceClassification
from keras.preprocessing.sequence import pad_sequences
from difflib import SequenceMatcher
import os.path
import requests

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
            if chunk: # filter out keep-alive new chunks
              f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)
    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)

def progress_bar(some_iter):
    try:
        from tqdm import tqdm
        return tqdm(some_iter)
    except ModuleNotFoundError:
        return some_iter
# --

def load_grammar_checker_model():
    # download_file_from_google_drive('1M_7GJVIVEHVp2ImyHBG2xk2aw21HtHif', './bert-based-uncased-GDO-trained.pth')
    if(not os.path.isfile('./bert-based-uncased-GDO-trained.pth')):
         download_file_from_google_drive('1sPfnUFnzSxbGA9nxvGn85Eds8wU_JyuD', './bert-based-uncased-GDO-trained.pth')

    grammar_checker =  BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

    device = torch.device('cpu')
    grammar_checker.load_state_dict(torch.load('bert-based-uncased-GDO-trained.pth', map_location=device))
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

    # Add tokens to begining and end of sentences
    sentences = ["[CLS] " + sentence + " [SEP]" for sentence in sents]
    labels = [0]

    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]

    # Padding Sentences
    MAX_LEN = 128

    predictions = []
    true_labels = []

    # Pad input tokens
    input_ids = pad_sequences(
      [tokenizer.convert_tokens_to_ids(txt) for txt in tokenized_texts],
      maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    # Index Numbers and Padding
    input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]

    # Pad sentences
    input_ids = pad_sequences(input_ids, maxlen=MAX_LEN,
                            dtype ="long", truncating="post",padding ="post")

    # Create attention masks
    attention_masks = []

    for seq in input_ids:
        seq_mask = [float(i > 0) for i in seq]
        attention_masks.append(seq_mask)

    prediction_inputs = torch.tensor(input_ids)
    prediction_masks = torch.tensor(attention_masks)
    prediction_labels = torch.tensor(labels)

    with torch.no_grad():
        # Forward pass, calculate logit predictions
        logits = checker_model(prediction_inputs, token_type_ids=None,
                          attention_mask=prediction_masks)

    # Move logits and labels to CPU
    logits = logits.detach().cpu().numpy()
    #label_ids = b_labels.to("cpu").numpy()

    # Store predictions and true labels
    predictions.append(logits)
    #true_labels.append(label_ids)

    #print(predictions)
    flat_predictions = [item for sublist in predictions for item in sublist]

    #print(flat_predictions)
    prob_vals = flat_predictions
    flat_predictions = np.argmax(flat_predictions, axis=1).flatten()
    #flat_true_labels = [item for sublist in true_labels for item in sublist]

    #print(flat_predictions)

    predictions = []
    for i in range(len(prob_vals)):
        exps = [np.exp(i) for i in prob_vals[i]]
        sum_of_exps = sum(exps)
        softmax = [j/sum_of_exps for j in exps]
        predictions.append(softmax[1]*100)

    return predictions

def check_grammar(original_sentence, masked_sentence):
    new_sentences = []

    # what is the tokenized value of [MASK]
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

# TODO
# verbs checking - use Spacy to check the tense

def predict_corrections(original_sentence, mask_ids):
    corrections = []
    sentence = original_sentence

    for i in range(len(mask_ids)):
        masked_sentence = create_mask_set(sentence, mask_ids[i])
        sentence, correct = check_grammar(sentence, masked_sentence)
        if(not correct):
            corrections.append(mask_ids[i])

    return sentence, corrections

# Load pre-trained model tokenizer
tokenizer = create_tokenizer()
checker_model = load_grammar_checker_model()
corrector_model = load_grammar_corrector_model()
