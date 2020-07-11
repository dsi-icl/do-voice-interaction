import requests
import sys, io, os
import time
from pydub import AudioSegment
from pydub.playback import play
from contextlib import contextmanager
import contextlib
import json

# insert at position 1 in the path, as 0 is the path of this file.
sys.path.insert(1, './deep_speech')

from deepspeech_test_prediction import record_audio
from deepspeech_test_prediction import deepspeech_predict
from test_tts import load_model

@contextlib.contextmanager
def ignore_stderr():
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(2)
    sys.stderr.flush()
    os.dup2(devnull, 2)
    os.close(devnull)
    try:
        yield
    finally:
        os.dup2(old_stderr, 2)
        os.close(old_stderr)

# response = requests.post('http://localhost:5002/webhooks/rest/webhook',json={"message":"Hello"})
#
# print("\nCHATBOT : ",end=' ')
# for i in response.json():
#     bot_message = i['text']
#     print(f"{i['text']}")
#
# welcome = AudioSegment.from_wav('./tts_audios/welcome.wav')
# with ignore_stderr():
#     play(welcome)

bot_message = ""
message = ""

while bot_message != "The Data Observatory thanks you for your presentation. I hope to see you soon :)\n":

    bot_message = ""
    
    ts = time.time()
    OUT_FILE = "./deep_speech/audio/"+str(ts)+".wav"

    record_audio(OUT_FILE)

    message = deepspeech_predict(OUT_FILE,'./deep_speech/deepspeech-0.7.4-models.pbmm','./deep_speech/deepspeech-0.7.4-models.scorer')

    print("\nYOU : {}".format(message))

    if len(message)==0:
        os.remove("./deep_speech/audio/"+str(ts)+".wav")
        continue

    print("\nSending message now...\n")

    response = requests.post('http://localhost:5002/webhooks/rest/webhook',json={"sender":"Human","message":message})
    # r = requests.get("http://localhost:5005/conversations/Human/tracker")
    # results = json.loads(r.content.decode('utf8'))
    #
    # print(results['latest_message']['intent'])

    for i in response.json():
        bot_message += i['text']+"\n"

    if 'help' in message or 'I can execute the following commands' in bot_message:
        bot_response = AudioSegment.from_wav('./tts_audios/help.wav')
    elif 'bye' in message:
        bot_response = AudioSegment.from_wav('./tts_audios/goodbye.wav')
    else:
        load_model(bot_message)
        bot_response = AudioSegment.from_wav('./tts_audios/tts_out.wav')


    print("CHATBOT : ",bot_message)

    with ignore_stderr():
        play(bot_response)


    os.remove("./deep_speech/audio/"+str(ts)+".wav")
