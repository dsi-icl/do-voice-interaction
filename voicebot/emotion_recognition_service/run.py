import base64
import json
import os
import uuid

import tensorflow as tf
import numpy as np
import librosa as lb
from flask import Flask, request
from collections import Counter
from aeneas.executetask import ExecuteTask
from aeneas.task import Task

import models
from helper import WordVectorHelper, TARGET_SAMPLING_RATE, \
                    CHUNK_SIZE, EMBEDDING_DIMENSION, SEQUENCE_LENGTH, \
                    WORD2VEC_DIR, W2V_VEC 

CKPT_PATH = './checkpoint_final/model.ckpt-8188'

app = Flask(__name__)
slim = tf.contrib.slim

def development_msg(content):
    #print(content)
    return

# equivalent to delete_segmentation() in data_generator.py
def delete_files(filename):
    development_msg('\n***************** Deleting used wav, txt and csv files *****************\n')
    for ext in ['.wav', '.txt', '.csv']: # wav and csv exceluded here
        os.remove(filename + ext)

# equivalent to execute_task() in data_generator.py
def execute_task(filename):
    # Create Task object
    config_string = u"task_language=deu|is_text_type=mplain|os_task_file_format=csv|os_task_file_levels=3"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = filename + '.wav'
    task.text_file_path_absolute = filename + '.txt'
    task.sync_map_file_path_absolute = filename + '.csv'
    
    # Process Task
    ExecuteTask(task).execute()
    
    # output sync map to file
    task.output_sync_map_file()

# equivalent to mapping_generator() in data_generator.py
def mapping_generator(filename):
    # print('\n***************** Creating synchronisation map *****************')
    
    fo = open(filename + '.csv', 'w')

    # Mapping audio with transcript
    execute_task(filename=filename)

    fo.close()

# equivalent to process_audio_frames() in data_generator.py 
def process_audio_frames(time, audio_signal, sr):
    # print('\n***************** Enter process_audio_frames(time, audio_signal, sr) *****************')
    target_interculator_audio = [np.zeros((1, 2205), dtype=np.float32) # changed from 4410 to 2205
                                 for _ in range(len(time))]  # consider interlocutor information
    
    audio_frames = []

    development_msg('audio_signal = ' + str(audio_signal))
    development_msg('audio_signal.shape = ' + str(audio_signal.shape))

    for _, t in enumerate(time):  # gather the original raw audio feature
        s = int(t * sr)
        e = s + 2205
        audio = np.reshape(audio_signal[s:e], (1, -1))
        audio_frames.append(audio.astype(np.float32))
        development_msg('Gathering raw audio_signal[' + str(s) + ':' + str(e) + '] which is 2205-bits long audio frame starting at t = ' + str(t) + 'with a shape = ' + str(audio.shape))

    for i in range(len(time)):
        if audio_frames[i].shape != (1, 2205):
            target_interculator_audio[i][0][:2205] = np.zeros((1, 2205)) # fill with zero if there is no sound
        else:
            target_interculator_audio[i][0][:2205] = audio_frames[i]  # the reviewer is speaking

    return target_interculator_audio

def process_word_mappings(time, time_mappings):
    # print('\n***************** Enter process_word_mappings(time, time_mappings) *****************')

    # Process word mappings
    start_time = time_mappings[:, 1].astype(np.float32)
    end_time = time_mappings[:, 2].astype(np.float32)
    word = time_mappings[:, 3]

    corresponding_word = [None for _ in range(len(time))]

    for i, w in enumerate(word):
        development_msg('i = ' + str(i))
        st, end = int(round(float(start_time[i]), 1) * 10), int(round(float(end_time[i]), 1) * 10)
        development_msg('st = ' + str(st))
        development_msg('end = ' + str(end))

        for t in range(st, end + 1 if end + 1 < len(time) else len(time)):
            emb = _get_embedding(w)
            corresponding_word[t] = emb.reshape((1, EMBEDDING_DIMENSION))
          
    for i in range(len(time)):
        if corresponding_word[i] is None:
            corresponding_word[i] = np.zeros((1, EMBEDDING_DIMENSION))

    corresponding_word = np.array(corresponding_word)
    return corresponding_word

# equivalent to load_metadata() in data_generator.py
def load_metadata(filename):
    # print('\n***************** Enter load_metadata *****************')
    audio_signal, sampling_rate = lb.core.load('./' + filename + '.wav', sr=TARGET_SAMPLING_RATE)
    audio_signal = np.pad(audio_signal, (0, CHUNK_SIZE - audio_signal.shape[0] % CHUNK_SIZE), 'constant')
    time_mappings = np.loadtxt('./' + filename + '.csv', delimiter=',', dtype=str, ndmin=2)
    duration = lb.core.get_duration(audio_signal, sampling_rate)
    development_msg('\naudio duration = ' + str(duration))
    time = np.arange(0.0000, duration+0.2500, 0.2500)
    return audio_signal, sampling_rate, time_mappings, time # Removed label and turns and created time


# equivalent to get_samples() in data_generator.py
def get_samples(filename):
    # print('\n***************** Getting samples *****************')
    audio_signal, sr, time_mappings, time = load_metadata(filename)
    
    # Process audio frames
    target_interculator_audio = process_audio_frames(time, audio_signal, sr)
    development_msg(len(target_interculator_audio))
    development_msg(target_interculator_audio[0].shape)

    # Process word mappings
    corresponding_word = process_word_mappings(time, time_mappings)
    development_msg(target_interculator_audio[0].shape)
    development_msg(corresponding_word[0].shape)

    # print('Returning samples foor this file')
    return target_interculator_audio, corresponding_word


vec_helper = WordVectorHelper(WORD2VEC_DIR+W2V_VEC)
_, _, _, embed_dict = vec_helper.load_vec()


def _get_embedding(word):
    global unk
    word = clean_word(word)

    if embed_dict.get(word, None) is not None:
        return embed_dict[word]
    else:
        # print('Word {%s} not in dict, so returning random embedding')
        return np.random.rand(EMBEDDING_DIMENSION)


# not used at the moment as stt service does not output these punctuations
def clean_word(word):
    word = word.lower()
    
    punctuation = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~'  # Exclude <>
    word = word.translate(str.maketrans('', '', punctuation))
    
    return word


def classifyEmotion(arousal, valence):
    if arousal<=0.5 and arousal>=-0.5 and valence<=0.5 and valence>=-0.5:
        return 'neutral'
    elif arousal>0.5 and valence>=-0.5 and valence<=0.5:
        return 'excited'
    elif arousal<-0.5 and valence>=-0.5 and valence<=0.5:
        return 'sleepy'
    elif arousal>=0 and valence>0.5:
        return 'happy'
    elif arousal<0 and valence>0.5:
        return 'relaxed'
    elif arousal>=0 and valence<-0.5:
        return 'frustrated'
    elif arousal<0 and valence<0.5:
        return 'sad'
    else:
        # print('Unclassfied emotion! This should not be happening! Check the code!')
        exit(-1)


def processPrediction(prediction):
    # print('\nCategorising detected emotion in chunks of 5 seconds (20 frames)')
    
    # classify every 5 seconds (20 frames)
    if len(prediction)%20 == 0:
        n_emotions = len(prediction) // 20
    else:
        n_emotions = len(prediction) // 20 + 1

    classifiedEmotions = []
    arousals=[]
    valences=[]
    for i in range(n_emotions):
        # print('')
        chunk = prediction[i*20:(i+1)*20]
        # print(chunk)
        mean_a, mean_v = np.mean(chunk, axis=0)
        # print('mean arousal = ' + str(mean_a))
        # print('mean valence = ' + str(mean_v))
        arousals.append(mean_a)
        valences.append(mean_v)
        emotion = classifyEmotion(mean_a, mean_v)
        classifiedEmotions.append(emotion)
        print(emotion)
    # print('\nclassfied emotions are:')
    # print(classifiedEmotions)
    # print('')

    # deduce overall emotion to apply to the bot response
    counter = Counter(classifiedEmotions) # dictionary of emotion occurances {angry: 2, neutral: 2, happy:1, sad: 1}
    most_common_emotion = counter.most_common() # a list of tuple in starting from the most common emotion [(angry, 2), (neutral, 2), (happy, 1), (sad, 1)]


    final_emotion =  most_common_emotion[0][0]
    # print('\nFinal single emotion is: ' + str(final_emotion) + '\n')
    thayers = str(sum(valences)/n_emotions)+","+str(sum(arousals)/n_emotions)
    return final_emotion, thayers


@app.route("/emotion-recognition", methods=['POST'])
def detectEmotion():

    # print("\nRecieved Audio ♪")
    receivedData = json.loads(request.data)
    base63_data = receivedData['audio']
    text_data = receivedData['transcript']
    # print('\nReceived transcript = ' + text_data)

    # print("\nDecoding Base64 into Wav") 
    wav_data = base64.b64decode(base63_data)

    # print("\nWriting audio to wav file") 
    filename = str(uuid.uuid4())
    f = open(filename + '.wav', 'wb')
    f.write(wav_data)
    f.close()
    
    # print("\nWriting transcript to txt file") 
    f = open(filename + '.txt', 'w')
    f.write(text_data)
    f.close()

    # creat s2w segmentation i.e. mapping
    mapping_generator(filename)
    
    audio_frames, embeddings = get_samples(filename)
    
    development_msg(type(audio_frames))
    audio_frames = np.array(audio_frames)
    development_msg(audio_frames.shape)
    audio_frames = audio_frames[:, 0, :]
    development_msg(audio_frames.shape)
    n_frames = len(audio_frames)
    if n_frames % SEQUENCE_LENGTH != 0:
        gap_to_fill = SEQUENCE_LENGTH - (n_frames % SEQUENCE_LENGTH)
        development_msg(gap_to_fill)
        filler = np.zeros((gap_to_fill, CHUNK_SIZE))
        audio_frames = np.vstack((audio_frames, filler))
        development_msg(audio_frames.shape)
        new_n_frames = len(audio_frames)
        n_batches = int(new_n_frames / SEQUENCE_LENGTH)
        development_msg(n_batches)
        audio_frames = audio_frames.reshape(n_batches, SEQUENCE_LENGTH, CHUNK_SIZE)
    
    audio_frames = tf.convert_to_tensor(audio_frames, dtype=np.float32)
    development_msg('\naudio_frames (tensor) = ' + str(audio_frames))

    development_msg(embeddings.shape)
    embeddings = embeddings[:, 0, :]
    n_frames = len(embeddings)
    if n_frames % SEQUENCE_LENGTH != 0:
        gap_to_fill = SEQUENCE_LENGTH - (n_frames % SEQUENCE_LENGTH)
        development_msg(gap_to_fill)
        filler = np.zeros((gap_to_fill, EMBEDDING_DIMENSION))
        embeddings = np.vstack((embeddings, filler))
        development_msg(embeddings.shape)
        new_n_frames = len(embeddings)
        n_batches = int(new_n_frames / SEQUENCE_LENGTH)
        development_msg(n_batches) # 1
        embeddings = embeddings.reshape(n_batches, SEQUENCE_LENGTH, EMBEDDING_DIMENSION)

    embeddings = tf.convert_to_tensor(embeddings)
    development_msg('\nembeddings (tensor) = ' + str(embeddings))

    with slim.arg_scope([slim.layers.batch_norm, slim.layers.dropout], is_training=False):
            
            predictions = models.get_model('audio_model2')(audio_frames,
                                                       emb=tf.cast(embeddings, tf.float32),
                                                       hidden_units=256)
    saver = tf.train.Saver(slim.get_variables_to_restore())  
    with tf.Session() as sess:
        saver.restore(sess, CKPT_PATH)
        sess.run(predictions)
        predictions = predictions.eval() # convert tensor to numpy array (1, 100, 2) n_batches, n_frames, n_outputs
    predictions = predictions[0, :(n_frames-gap_to_fill)] # discard irrelevant predictions

    # print('\n****************** Realtime Predictions ********************\n')
    # print(predictions)
    # print('\nRealtime Predictions Shape:\n')
    # print(predictions.shape)
    # print(type(predictions))
    delete_files(filename)

    (emotion, thayers) = processPrediction(predictions)

    # Send the detected emotion back to voice assistant service
    data = {'status': 'ok', 'service': 'emotion recognition service', 'emotion': emotion, 'thayers':thayers}
    
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False) # set debug=False for production
