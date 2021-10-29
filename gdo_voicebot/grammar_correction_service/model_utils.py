import torch
import numpy as np
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
from pytorch_pretrained_bert import BertForSequenceClassification
from keras.preprocessing.sequence import pad_sequences
import math
from difflib import SequenceMatcher

# credit: https://stackoverflow.com/a/39225039
import requests

# Load pre-trained model tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

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
    #download_file_from_google_drive('1M_7GJVIVEHVp2ImyHBG2xk2aw21HtHif', './bert-based-uncased-GDO-trained.pth')

    # grammar_checker =  BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)
    model = BertForMaskedLM.from_pretrained('bert-large-uncased')
    model.eval()

    # device = torch.device('cpu')
    # grammar_checker.load_state_dict(torch.load('bert-based-uncased-GDO-trained.pth', map_location=device))
    # grammar_checker.eval()

    return model

def create_mask_set(sentence, mask_ids):
  """
    For each input sentence create sentence with masked words at mask_ids
  """

  sentences = []
  sent = sentence.strip().split()
  for i in range(len(sent)):
    # [MASK] each word at mask_ids
    if i in mask_ids:
        new_sent = sent[:]
        new_sent[i] = '[MASK]'
        sentences.append('[CLS] ' + " ".join(new_sent) + ' [SEP]')

  return sentences

def check_GE(grammar_checker, sents):

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
        logits = grammar_checker(prediction_inputs, token_type_ids=None,
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

    return flat_predictions, prob_vals

def check_grammar(original_sentence, masked_sentences):
    new_sentences = []

    # what is the tokenized value of [MASK]
    text = '[MASK]'
    tokenized_text = tokenizer.tokenize(text)
    mask_token = tokenizer.convert_tokens_to_ids(tokenized_text)[0]

    for sent in masked_sentences:
        # tokenize the text
        tokenized_text = tokenizer.tokenize(sent)
        indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

        # Create the segments tensors.
        segments_ids = [0] * len(tokenized_text)

        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([indexed_tokens])
        segments_tensors = torch.tensor([segments_ids])

        # Predict all tokens
        with torch.no_grad():
            predictions = model(tokens_tensor, segments_tensors)

        # index of the masked token
        mask_index = (tokens_tensor == mask_token).nonzero()[0][1].item()
        # predicted token
        predicted_index = torch.argmax(predictions[0, mask_index]).item()
        predicted_token = tokenizer.convert_ids_to_tokens([predicted_index])[0]

        text = sent.strip().split()
        mask_index = text.index('[MASK]')

        text[mask_index] = predicted_token
        original_word = original_sentence.strip().split()[mask_index - 1]
        if original_word == predicted_token:
            continue
        
        text.remove('[SEP]')
        text.remove('[CLS]')
        new_sent = " ".join(text)

        new_sentences.append(new_sent)

        # no_error, prob_val = check_GE(model, [new_sent])
        # exps = [np.exp(i) for i in prob_val[0]]
        # sum_of_exps = sum(exps)
        # softmax = [j/sum_of_exps for j in exps]
        # if no_error and softmax[1] > 0.996:
        #     new_sentences.append(new_sent)

    result_sentences = []
    [result_sentences.append(sent) for sent in new_sentences]
    result_sentences = list(dict.fromkeys(result_sentences))
    return result_sentences

    


model = load_grammar_checker_model()
sentences = ["There are no doubt the tracking system has bring many benefits in this information age .", "I loves you.", "I has a apple.",  "I has an apple.",  "I have an apple.", 
                "I ain't there."]
# no_error, prob_val = check_GE(grammar_checker, sentences)
# #print(no_error)
# #print(prob_val)
# for i in range(len(prob_val)):
#     exps = [np.exp(i) for i in prob_val[i]]
#     sum_of_exps = sum(exps)
#     softmax = [j/sum_of_exps for j in exps]
#     print("{0} - {1:0.4f}%".format(sentences[i], softmax[1]*100))
  
# print("-"*60)
# print()

sentences = create_mask_set(sentences[0], [1, 8])
print(sentences)

corrections = check_grammar(sentences[0], sentences)

print(corrections)