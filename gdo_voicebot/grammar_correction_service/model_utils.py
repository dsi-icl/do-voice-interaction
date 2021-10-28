
# credit: https://stackoverflow.com/a/39225039


import requests
from pytorch_pretrained_bert import BertForSequenceClassification

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


def load_model():
  download_file_from_google_drive('1M_7GJVIVEHVp2ImyHBG2xk2aw21HtHif', './bert-based-uncased-GDO-trained.pth')

  grammar_checker =  BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)

  grammar_checker.load_state_dict(torch.load('bert-based-uncased-GDO-trained.pth'))
  grammar_checker.eval()

  return grammar_checker

