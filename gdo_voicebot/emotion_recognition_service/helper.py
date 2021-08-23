import csv
import os
import numpy as np
import warnings
warnings.filterwarnings('ignore',category=FutureWarning) # needed to ignore tensorflow 1x depreciation warning
import tensorflow as tf

SPEECH2VEC_DIR = 'speech2vec/'
S2V_VEC = 's2v-processed.vec'
WORD2VEC_DIR = 'word2vec/'
W2V_VEC = '100.vec'

EMBEDDING_DIMENSION = 100
TARGET_SAMPLING_RATE = 22050
CHUNK_SIZE = 2205
MAX_DATA_LENGTH = 50
SEQUENCE_LENGTH = 100

MUSE_DIR = './MuSe-CAR/' 
AUDIO_DIR = MUSE_DIR + 'audio/'
TRANSCRIPT_DIR = MUSE_DIR + 'transcription/'
AROUSAL_DIR = MUSE_DIR + 'label/arousal/'
VALENCE_DIR = MUSE_DIR + 'label/valence/'

SYNCHRONISATION_MAPPING_DIR = './segmentation/' # Please specify your own path
PROCESSED_LABEL_DIR = MUSE_DIR + 'label/processed/' # Please specify your own path
TFRECORD_DIR = './tfrecords'  # Please specify your own path to save the tfrecords

def development_msg(content):
    #print(content)
    return

def get_filenames_from_dir(dir):
    trains, vals, tests = [], [], []

    for filename in sorted(os.listdir(dir)):
        fn = filename.split('.')[0]
        if filename.startswith('Train'):
            trains.append(fn)
        elif filename.startswith('Devel'):
            vals.append(fn)
        elif filename.startswith('Test'):
            tests.append(fn)
        else:
            print('Unknown filename: {%s}' % filename)

    return trains, vals, tests


def get_pathlist_from_dir(dir):
    pathlist = []
    for filename in os.listdir(dir):
        path = os.path.join(dir, filename)
        pathlist.append(path)

    return pathlist

class WordVectorHelper(object):
    def __init__(self, path):
        self.path = path

    def load_vec(self):
        embeddings = []
        embeddings_dict = {}

        id2word = dict()

        with open(self.path, 'r') as f:
            l1 = f.readline().split()
            vocabulary, embedding_size = int(l1[0]), int(l1[1])

            count = 0
            for line in f:
                tmp = line.split()
                try:
                    word, embed = tmp[0], np.array(tmp[1:], dtype=float)

                    if len(embed) == embedding_size:
                        embeddings.append(embed)
                        embeddings_dict[word] = embed
                        id2word[count] = word
                        count += 1
                except:
                    print('Cant process word {%s}' % tmp[0])

        word2id = dict(zip(id2word.values(), id2word.keys()))
        # print('Vocabulary size: %d, embedding size: %d' % (len(embeddings), embedding_size))

        self.embeddings_dict = embeddings_dict
        self.id2word = id2word
        self.word2id = word2id
        self.embeddings = embeddings

        return id2word, word2id, embeddings, embeddings_dict

    def check_for_synonym_in_vec(self):
        # Need to call load_vec() first
        embeddings = self.embeddings_dict

        s_embeddings = dict()
        for k, v in SYNONYM_DICT.items():
            for word in v:
                e = embeddings.get(word, None)
                found = True if e is not None else False
                # print(word, found)

                if found:
                    s_embeddings[k] = e
                    continue

        return s_embeddings

