from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

from helper import development_msg

slim = tf.contrib.slim

def recurrent_model(net, emb=None, hidden_units=256, number_of_outputs=2): # net = network outputed by audio_model2(audio_frames)
    development_msg('\n*************** Entering recurrent_model() in model.py ***************')

    development_msg('\n*************** Constructing the neural network ***************')

    # Fusing strategies of output of CNN model with word embeddings
    development_msg('Defining fusion of paralinguistic and semantic networks')
    # Attention aprroach  
    # # here, net = audio_model2 = paralinguistic AND 
    # emb = tf.cast(word_embeddings, tf.float32) = semantic, projected_units = 256
    fused_features = attention_model(net, emb, projected_units=1024) # fuse paralinguistic and semantic networks - mifu

    development_msg('Defining three FC layers to disentangle 3 features')
    # "We chose to use three FC layers such that the information 
    # flow per emotional dimension in the network is disentagled.
    # The intuition here is that by adding three additional dense layers, 
    # we hope that each of these projections could learn features that
    # suit best for a dimension in our emotion space." - paper
    # setting up three nets to disentangle the information - mifu
    net_1 = tf.contrib.layers.fully_connected(fused_features, num_outputs=512) # arousal - mifu
    net_2 = tf.contrib.layers.fully_connected(fused_features, num_outputs=512) # valence - mifu

    # Concat output
    # net = tf.concat([net_1, net_2, net_3], axis=2)
    development_msg('Defining the fusing of the three FC layers')
    # Self-attention
    # fuse the three layers to prep for LSTM - mifu
    net = attention_model(net_1, net_2, scope='_self12')

    #-----------------------------------------#
    # Fully connected layer approach
    # net = fully_connected_model(net, emb)
    development_msg(net)

    with tf.variable_scope('recurrent'): # 'tf.variable_scope' is a context manager for defining ops that create layers
        development_msg('Creating recurrent neural network using the defined layers')
        
        batch_size, seq_length, num_features = net.get_shape().as_list()

        # development_msg(batch_size, seq_length, num_features)

        # creating basic LSTM cell - mifu
        lstm = tf.contrib.rnn.LSTMCell(hidden_units,
                                       use_peepholes=True,
                                       cell_clip=100,
                                       state_is_tuple=True)

        outputs, states = tf.nn.dynamic_rnn(lstm, net, dtype=tf.float32) # param 1 = LSTM cell, param 2 = input data. 'tf.nn.dynamic_rnn' creates a recurrent neural network specified by RNNCell cell
        net = tf.reshape(outputs, (batch_size * seq_length, hidden_units))
        prediction = tf.nn.tanh(slim.layers.linear(net, number_of_outputs))
        development_msg('\n*************** Returning a successfully created recurrent network **************')
        return tf.reshape(prediction, (batch_size, seq_length, number_of_outputs))


# paralinguistic feature extractor - mifu
def audio_model2(audio_frames=None, conv_filters=40):
    with tf.variable_scope('audio_model'):
        development_msg('\n*************** Entering audio_model2 in model.py **************')
        development_msg('Defining the paralinguistic network')
        batch_size, seq_length, num_features = audio_frames.get_shape().as_list()
        development_msg(audio_frames.get_shape().as_list())

        audio_input = tf.reshape(audio_frames, [batch_size,  num_features * seq_length, 1])
        development_msg(audio_input)

        net = tf.layers.conv1d(audio_input, 50, 8, padding='same', activation=tf.nn.relu)
        net = tf.layers.max_pooling1d(net, 10, 10)
        net = slim.dropout(net, 0.5)
        development_msg(net)

        net = tf.layers.conv1d(net, 125, 6, padding='same', activation=tf.nn.relu)
        net = tf.layers.max_pooling1d(net, 5, 5)
        net = slim.dropout(net, 0.5)
        development_msg(net)

        net = tf.layers.conv1d(net, 250, 6, padding='same', activation=tf.nn.relu)
        net = tf.layers.max_pooling1d(net, 5, 5)
        net = slim.dropout(net, 0.5)
        development_msg(net)

        net = tf.reshape(net, [batch_size, seq_length, -1])
        development_msg(net)

        return net


def fully_connected_model(audio_frames, text_frames):
    with tf.variable_scope('FC_model'):
        audio_features = tf.contrib.layers.fully_connected(audio_frames, num_outputs=1024)
        text_features = tf.contrib.layers.fully_connected(text_frames, num_outputs=1024)

        net = tf.concat([audio_features, text_features], axis=2)
        net = tf.contrib.layers.fully_connected(net, num_outputs=512)
        return net


def attention_model(audio_frames, text_frames, projected_units=2048, scope=''): # audio_frames and text_frames should be renamed to net_1 and net_2? - mifu
    with tf.variable_scope('attn_model' + scope):
        batch_size, seq_length, num_features = audio_frames.get_shape().as_list()

        # Attention
        audio_features = tf.reshape(audio_frames, [-1, audio_frames.get_shape()[-1]])

        # NEW - check if embedding present (in evaluation sometimes there is no embedding)
        if text_frames != None:
            text_features = tf.reshape(text_frames, [-1, text_frames.get_shape()[-1]]) # Previously only this existed with no checks to wether embedding was None or not. This was giving an error when trying to run an inference without embedding
        else:
            text_features = tf.zeros((500, 100)) # NEW

        # development_msg(audio_features.get_shape().as_list(), text_features.get_shape().as_list())

        if audio_features.get_shape().as_list()[1] != text_features.get_shape().as_list()[1]:
            projected_audio = tf.contrib.layers.fully_connected(audio_features, num_outputs=projected_units)
            projected_text = tf.contrib.layers.fully_connected(text_features, num_outputs=projected_units)
        else:
            projected_audio = audio_features
            projected_text = text_features

        net = stack_attention_producer(projected_audio, projected_text, batch_size, 'attn')

        return net


def stack_attention_producer(frame1, frame2, batch_size, scope=None):

    with tf.variable_scope(scope):

        frame1 = tf.expand_dims(frame1, 1)
        frame2 = tf.expand_dims(frame2, 1)

        frames = tf.concat([frame1, frame2], axis=1)
        tmp_frames = tf.expand_dims(frames, 3)

        # development_msg(frames, tmp_frames)

        conv = tf.squeeze(conv2d(tmp_frames, 1, 1, frames.get_shape()[-1], name=scope + '_selector'), [2, 3])
        # development_msg(conv)

        conv = tf.multiply(conv, 1. / tf.sqrt(tf.cast(frames.get_shape()[-1], tf.float32)))
        # development_msg(conv)

        attention = tf.nn.softmax(conv, name=scope + '_softmax')
        attention = tf.expand_dims(attention, axis=2)
        # development_msg(attention)

        out = tf.reduce_sum(tf.multiply(frames, attention), 1, keep_dims=True)
        # development_msg(out)

        out = tf.reshape(out, (batch_size, -1, out.shape[-1]))
        return out


def conv2d(input_, output_dim, k_h, k_w, padding='VALID', name='conv2d'):
    """
         :param input_: shape = [batch_size * num_unroll_steps, 1, max_sent_length, embed_size]
         :param output_dim: [kernel_features], which is # of kernels with this width
         :param k_h: 1
         :param k_w: kernel width, n-grams
         :param name: name scope
         :return: shape = [reduced_length, output_dim]
    """

    with tf.variable_scope(name):
        w = tf.get_variable('w', [k_h, k_w, input_.get_shape()[-1], output_dim])
        b = tf.get_variable('b', [output_dim])

    return tf.nn.conv2d(input_, w, strides=[1, 1, 1, 1], padding=padding) + b


def get_model(name):
    name_to_fun = {'audio_model2': audio_model2}

    if name in name_to_fun:
        model = name_to_fun[name]
    else:
        raise ValueError('Requested name [{}] not a valid model'.format(name))

    def wrapper(*args, **kwargs):
        return recurrent_model(model(*args), **kwargs) # the first param (i.e. model) refers to audio_model2 which is the paralinguistic network

    return wrapper # returns the recurrent_model
