from pathlib import Path
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
import tensorflow as tf
import librosa as lb
import numpy as np
from numpy.core.fromnumeric import shape

from helper import get_pathlist_from_dir, development_msg, WordVectorHelper,\
                    SPEECH2VEC_DIR, WORD2VEC_DIR, S2V_VEC, W2V_VEC, \
                    EMBEDDING_DIMENSION, PROCESSED_LABEL_DIR, AUDIO_DIR, \
                    SYNCHRONISATION_MAPPING_DIR, TFRECORD_DIR, TARGET_SAMPLING_RATE, \
                    CHUNK_SIZE

(Path(TFRECORD_DIR)).mkdir(exist_ok=True)
(Path(TFRECORD_DIR) / 'train').mkdir(exist_ok=True)
(Path(TFRECORD_DIR) / 'devel').mkdir(exist_ok=True)
(Path(TFRECORD_DIR) / 'test').mkdir(exist_ok=True)

fnames = ['Train', 'Devel', 'Test']

# Provide your partition:
TRAIN_FILES = ['23', '24', '25', '26', '27', '28', '29', '30', '31', '34', '35', '36', '37', '39', '40', '42', '43', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', '96', '97', '98', '99', '100', '101', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '122', '125', '155', '157', '159', '160', '162', '163', '165', '166', '168', '169', '171', '173', '175', '177', '178', '179', '180', '181', '183', '184', '186', '187', '188', '189', '190', '191', '192', '194', '194', '196', '198', '198', '199', '199', '201', '202', '204', '205', '207', '208', '210', '210', '211', '214', '219', '222', '225', '230', '233', '236', '240', '245', '246', '247', '248', '249', '250', '251', '252', '253', '254', '255', '256', '257', '258', '259', '261', '262', '263', '264', '266', '267', '268', '269', '270', '271', '272', '273', '274']
DEVEL_FILES = ['293', '220', '279', '229', '280', '300', '287', '275', '17', '20', '301', '286', '276', '15', '18', '289', '239', '16', '243', '217', '215', '238', '244', '241', '297', '242', '231', '234', '291', '278', '38']
TEST_FILES = ['21', '19', '302', '290', '285', '298', '303', '292', '232', '213', '221', '282', '227', '235', '288', '284', '212', '296', '283', '228', '223', '224', '22', '226', '218', '295', '237', '281', '216', '277', '294']


def serialize_sample(writer, filename):
    development_msg('Enter serialize_sample(' + filename + ')')
    for i, (audio_frame, embedding, label) in enumerate(zip(*get_samples(filename))):  # serialize every frame
        development_msg('data to serialise')
        development_msg('....................... frame ' +  str(i) + ' ......................')
        development_msg('audio_frame = ' + str(audio_frame))
        development_msg('embedding = ' + str(embedding))
        development_msg('label = ' + str(label))
    
        example = tf.train.Example(features=tf.train.Features(feature={
            'file_name': _bytes_feature(filename.encode()),
            'audio_frame': _bytes_feature(audio_frame.tobytes()),
            'embedding': _bytes_feature(embedding.tobytes()),
            'label': _bytes_feature(label.tobytes()),
        }))
        
        # write all frames of a subject to a file
        writer.write(example.SerializeToString()) 
        development_msg('successfully serialised a frame') 


def get_samples(filename):
    development_msg('Enter get_samples(' + filename + ')')
    audio_signal, sr, labels, time_mappings = load_metadata(filename)

    # Process labels
    time = labels[:, 0].astype(np.float32)
    arousal = np.reshape(labels[:, 1], (-1, 1)).astype(np.float32) # takes 1d array and makes it into 2d array with n rows and 1 col.
    valence = np.reshape(labels[:, 2], (-1, 1)).astype(np.float32)
    
    labels = np.hstack([arousal, valence]).astype(np.float32) # stacks the 1 col arrays side by side

    # Process audio frames
    target_interculator_audio = process_audio_frames(time, audio_signal, sr)

    # Process word mappings
    corresponding_word = process_word_mappings(time, time_mappings)

    development_msg('Got samples for ' + filename + ' as shown below')
    development_msg('audio_frame shape = ' + str(shape(target_interculator_audio)))
    development_msg('embedding shape = ' + str(shape(corresponding_word)))
    development_msg('label shape = ' + str(shape(labels)))
    return target_interculator_audio, corresponding_word, labels


def load_metadata(filename):
    foldername =filename.split('_')[0] # e.g. 220
    label_path = PROCESSED_LABEL_DIR + foldername + '/' + filename + '.csv'
    #turn_path = AVEC_DIR + '/turns/{}.csv'.format(filename)
    a2w_mapping_path = SYNCHRONISATION_MAPPING_DIR + foldername + '/' + filename + '.csv'

    audio_signal, sampling_rate = lb.core.load(AUDIO_DIR + foldername + '/' + filename + '.wav', sr=TARGET_SAMPLING_RATE)
    audio_signal = np.pad(audio_signal, (0, CHUNK_SIZE - audio_signal.shape[0] % CHUNK_SIZE), 'constant')

    labels = np.loadtxt(str(label_path), delimiter=';', dtype=str, ndmin=2)
    #turns = np.loadtxt(str(turn_path), delimiter=';', dtype=np.float32)
    time_mappings = np.loadtxt(str(a2w_mapping_path), delimiter=';', dtype=str, ndmin=2)

    return audio_signal, sampling_rate, labels, time_mappings


def process_audio_frames(time, audio_signal, sr):
    development_msg('Enter process_audio_frames(time, audio_signal, sr)')
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
        development_msg('Gathering raw audio_signal[' + str(s) + ':' +
        str(e) + '] which is 2205-bits long audio frame starting at t = '+
        str(t) + ' with a shape = ' + str(audio.shape))

    # Copying the content over to target_interculator_audio - this is useless in my case so I can just return audio_frames
    for i in range(len(time)):
        if audio_frames[i].shape != (1, 2205):
            target_interculator_audio[i][0][:2205] = np.zeros((1, 2205)) # fill with zero if there is no sound
        else:
            target_interculator_audio[i][0][:2205] = audio_frames[i]  # the reviewer is speaking
    development_msg('target_interculator_audio = ')
    development_msg(target_interculator_audio)

    return target_interculator_audio
    

def process_word_mappings(time, time_mappings):
    development_msg('Enter process_word_mappings(time, time_mappings)')
    development_msg('************************')
    development_msg(time_mappings)
    development_msg('************************')

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
            development_msg('t = ' + str(t))
            emb = _get_embedding(w)
            corresponding_word[t] = emb.reshape((1, EMBEDDING_DIMENSION))

    for i in range(len(time)):
        if corresponding_word[i] is None:
            corresponding_word[i] = np.zeros((1, EMBEDDING_DIMENSION))

    corresponding_word = np.array(corresponding_word)
    return corresponding_word


def _get_embeddings(space=''):
    if space == 's2v':
        d, v = SPEECH2VEC_DIR, S2V_VEC
    elif space == 'w2v':
        d, v = WORD2VEC_DIR, W2V_VEC
    else:
        print("Invalid vector space. Please choose s2v or w2v.")
        exit(-1)

    vec_helper = WordVectorHelper(d + v)
    id2word, word2id, emb, embed_dic = vec_helper.load_vec()

    return id2word, embed_dic


def _get_embedding(word):
    global unk
    word = _clean_word(word)

    if embed_dict.get(word, None) is not None:
        return embed_dict[word]
    else:
        unk.add(word)
        embed_dict[word] = np.random.rand(EMBEDDING_DIMENSION)
        print('Word {%s} not in dict, new size of embedding dict {%d}' % (word, len(embed_dict)))
        return embed_dict[word]


def _clean_word(word):
    punctuation = '!"#$%&\'()*+,-./:;=?@[\\]^_`{|}~' 
    word_clean = word.translate(str.maketrans('', '', punctuation))
    word_clean = word_clean.lower()
    return word_clean


def _bytes_feature(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def write_data():
    
    clippathlist = get_pathlist_from_dir(SYNCHRONISATION_MAPPING_DIR)
    n_clips_to_go = 239 # 303 minus 64 as there initially were 303 clips and 64 mannually removed 64 as they did not have labels
    for path in clippathlist:
        clipname = path.rsplit('/')[-1] # i.e. folder name e.g. 201
        print('Writing tfrecords for %s' % clipname) 
        
        development_msg(clipname)
        if clipname in TRAIN_FILES:
            usage = 'train'
        elif clipname in DEVEL_FILES:
            usage = 'devel'
        elif clipname in TEST_FILES:
            usage = 'test'
        else:
            print('This file does not belong to any usage')
            exit(-1)

        segmentpathlist = get_pathlist_from_dir(SYNCHRONISATION_MAPPING_DIR + clipname)

        for segmentpath in segmentpathlist:
            segmentname = segmentpath.rsplit('/')[-1][:-4] # i.e. segment name e.g. 201_1
            print('\n----------------------- Working on ' + segmentname + ' -----------------------')
            writer = tf.io.TFRecordWriter(TFRECORD_DIR + '/' + usage + '/' + segmentname + '.tfrecords')
            serialize_sample(writer, segmentname)
        n_clips_to_go -= 1
        print(str(n_clips_to_go) + ' clips to go')
    print('Successfully completed creating all tfrecords')


unk = set()

if __name__ == '__main__':
    
    # Select the embedding you want to use by setting space = 'w2v|s2v|<empty>'
    # currently word2vec vector is used
    id2word, embed_dict = _get_embeddings(space='w2v')
    write_data()