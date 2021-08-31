from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import warnings
warnings.filterwarnings('ignore',category=FutureWarning) # needed to ignore tensorflow 1x depreciation warning
import tensorflow as tf
from helper import get_pathlist_from_dir, development_msg, EMBEDDING_DIMENSION

slim = tf.contrib.slim

def get_split(dataset_dir, is_training=True, batch_size=32, seq_length=100):
    
    if is_training:
        development_msg('\n************************************ Loading training data paths ***********************************')
        paths = get_pathlist_from_dir(dataset_dir)
        development_msg(paths)
        filename_queue = tf.train.string_input_producer(paths, shuffle=True)
        development_msg('filename_queue = ' + str(filename_queue))
    else:
        development_msg('\n************************************ Loading (non-training) data paths ***********************************')
        paths = [dataset_dir]
        development_msg(paths)
        filename_queue = tf.train.string_input_producer(paths, shuffle=True)
        development_msg('filename_queue = ' + str(filename_queue))
    development_msg('\n************************************ Reader assignment ***********************************')
    reader = tf.TFRecordReader()
    development_msg('\n*************************** Reader is reading filename_queue *****************************')
    _, serialized_example = reader.read(filename_queue)
    development_msg('\n**************************** Parsing sinmgle example **************************************')
    features = tf.parse_single_example(  # take one frame
        serialized_example,
        features={
            'label': tf.FixedLenFeature([], tf.string),
            'file_name': tf.FixedLenFeature([], tf.string),
            'audio_frame': tf.FixedLenFeature([], tf.string),
            'embedding': tf.FixedLenFeature([], tf.string),
        }
    )
    development_msg('\n************************ decoding data from  single frame ********************************')
    file_name = features['file_name']  # file name
    development_msg('filename (before) = ' + file_name)
    file_name.set_shape([])
    development_msg('filename (after) = ' + file_name)
    audio_frame = tf.decode_raw(features['audio_frame'], tf.float32)  # decode the audio feature of one frame
    development_msg('audio_frame (before) = ' + str(audio_frame))
    audio_frame.set_shape([2205])  # changed from 4410 to 2205 
    development_msg('audio_frame (after) = ' + str(audio_frame))

    embedding = tf.decode_raw(features['embedding'], tf.float64)
    development_msg('embedding (before) = ' + str(embedding))
    embedding.set_shape([EMBEDDING_DIMENSION])
    development_msg('embedding (after) = ' + str(embedding))

    label = tf.decode_raw(features['label'], tf.float32)  # decode label of that frame
    development_msg('label (before) = ' + str(label))
    label.set_shape([2])  # originally 3-D label
    development_msg('label (after) = ' + str(label))

    development_msg(audio_frame)
    development_msg(embedding)
    development_msg(label)
    
    development_msg('\n****************** Creating batches of tensors in tensors (deprecated) ***********************')
    # generate sequence, num_threads = 1, guarantee the generation of sequences is correct
    # i.e. frames of a sequence are in correct order and belong to same subject
    audio_frames, embeddings, labels, file_names = tf.train.batch(
        [audio_frame, embedding, label, file_name], seq_length, num_threads=1, capacity=1000
    )
    
    labels = tf.expand_dims(labels, 0)
    audio_frames = tf.expand_dims(audio_frames, 0)
    embeddings = tf.expand_dims(embeddings, 0)
    file_names = tf.expand_dims(file_names, 0)

    development_msg(audio_frames)
    development_msg(embeddings)
    development_msg(labels)
    development_msg(file_names)

    development_msg('\n************************* Generating mini_batch of sequences *********************************')
    if is_training:  # generate mini_batch of sequences
        audio_frames, embeddings, labels, file_names = tf.train.shuffle_batch(
            [audio_frames, embeddings, labels, file_names], batch_size, 1000, 50, num_threads=1)
    else:
        audio_frames, embeddings, labels, file_names = tf.train.batch(
            [audio_frames, embeddings, labels, file_names], batch_size, num_threads=1, capacity=1000)

    development_msg(audio_frames)
    development_msg(embeddings)
    development_msg(labels)
    development_msg(file_names)
    
    development_msg('\n************************* Reshaping 1.0 *********************************')
    # 1st_dim = n_batches, 2nd_dim = 1, 3rd_dim = seq_length, 4th_dim = n_features/labels
    frames = audio_frames[:, 0, :, :]
    labels = labels[:, 0, :]
    embeddings = embeddings[:, 0, :]
    file_names = file_names[:, 0, :]

    development_msg(frames)
    development_msg(embeddings)
    development_msg(labels)
    development_msg(file_names)
    
    return frames, embeddings, labels