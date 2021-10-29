import torch
import numpy as np
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
from pytorch_pretrained_bert import BertForSequenceClassification
from keras.preprocessing.sequence import pad_sequences
import os.path
# credit: https://stackoverflow.com/a/39225039
import requests

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
    if(not os.path.isfile('./bert-based-uncased-GDO-trained.pth')):
        download_file_from_google_drive('1sPfnUFnzSxbGA9nxvGn85Eds8wU_JyuD', './bert-based-uncased-GDO-trained.pth')
    
    grammar_checker =  BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

    device = torch.device('cpu')
    grammar_checker.load_state_dict(torch.load('bert-based-uncased-GDO-trained.pth', map_location=device))
    grammar_checker.eval()

    return grammar_checker

def check_GE(grammar_checker, sents):
    # Load pre-trained model tokenizer
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

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

grammar_checker = load_grammar_checker_model()
sentences = ["I love you", "I loves you.", "I has a apple.",  "I has an apple.",  "I have an apple.", 
            "I ain't there."]
no_error, prob_val = check_GE(grammar_checker, sentences)
print(no_error)
print(prob_val)
for i in range(len(prob_val)):
    exps = [np.exp(i) for i in prob_val[i]]
    sum_of_exps = sum(exps)
    softmax = [j/sum_of_exps for j in exps]
    print("{0} - {1:0.4f}%".format(sentences[i], softmax[1]*100))
  
print("-"*60)
print()