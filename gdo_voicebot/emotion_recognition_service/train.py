from __future__ import division
from __future__ import absolute_import
from __future__ import print_function

import os
from datetime import datetime
import tensorflow as tf 
from tensorflow.python.platform import tf_logging as logging
import losses
import models
from data_provider import get_split
from helper import TFRECORD_DIR

TRAIN_LOG_PATH = './log_train.txt'
SAVE_SUMMARY_SECS = 60 # calculates summary every 1 min
SAVE_INTERVAL_SECS = 120 # Saves a checkpoint every 2 mins

slim = tf.contrib.slim

# Directories
flags = tf.app.flags
flags.DEFINE_string('dataset', 'train', 'The tfrecords directory')  # tfrecord directory
flags.DEFINE_string('checkpoint_dir', './checkpoints/',
                    'Directory where to write event logs and checkpoint.')  # model save path

# Training parameters
flags.DEFINE_float('learning_rate', 0.0005, 'Initial learning rate.')
flags.DEFINE_integer('batch_size', 25, 'The batch size to use.')
flags.DEFINE_integer('hidden_units', 256, 'Recurrent network hidden units.')
flags.DEFINE_string('optimizer', 'adam', 'adam or sgd or gd')

flags.DEFINE_string('model', 'audio_model2', 'Which model is going to be used: audio, video, or both')
flags.DEFINE_integer('sequence_length', 50, 'Number of audio frames in one input')

# Other settings
flags.DEFINE_string('device', '0', 'CPU(-1) or GPU(0)') 
flags.DEFINE_string('min_log_level', '2', 'The min log level.') 
FLAGS = flags.FLAGS

# Use CPU when -1 and GPU when 0
os.environ["CUDA_VISIBLE_DEVICES"] = str(FLAGS.device)
# Logging setting
os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(FLAGS.min_log_level)


def train():
    tf.set_random_seed(1)

    g = tf.Graph()
    with g.as_default():
        # Load dataset.
        dataset_dir = TFRECORD_DIR + '/' + FLAGS.dataset
        audio_frames, word_embeddings, ground_truth = get_split(dataset_dir, True,
                                                                FLAGS.batch_size, seq_length=FLAGS.sequence_length)
        print('******************** Returning data *********************')
        print(audio_frames, word_embeddings, ground_truth)

        print('******************* Defining model **************************')
        # Define model graph.
        with slim.arg_scope([slim.layers.batch_norm, slim.layers.dropout], is_training=True):
            prediction = models.get_model(FLAGS.model)(audio_frames,
                                                       emb=tf.cast(word_embeddings, tf.float32),
                                                       hidden_units=FLAGS.hidden_units)
                                    
        if FLAGS.optimizer == 'adam':
            optimizer = tf.compat.v1.train.AdamOptimizer(FLAGS.learning_rate, beta1=0.9, beta2=0.99)
        elif FLAGS.optimizer == 'sgd':
            optimizer = tf.compat.v1.train.MomentumOptimizer(FLAGS.learning_rate, 0)
        elif FLAGS.optimizer == 'gd':
            optimizer = tf.compat.v1.train.GradientDescentOptimizer(FLAGS.learning_rate)
        else:
            print('\nInvalid optimizer name. Please provide either adam or sgd or gd\n')
            exit(-1)
            
        # Evaluate one batch
        count = 0
        for i, name in enumerate(['arousal', 'valence']):
            count += 1

            '''
            'prediction' has a shape of (batch_size, seq_length, number_of_outputs)
            Below is what 'prediction' looks like 
            This is an example with batch_size = 3
            
                         [[[a, v],         ^
                batch 1    [a, v],   sequence length 
                           [a, v]],        v 
                          [[a, v],         ^
                batch 2    [a, v],    sequence length 
                           [a, v]],        v
                          [[a, v],         ^
                batch 3    [a, v],    sequence length (which is 100 but I could not draw all obviously)
                           [a, v]]]        v
            '''

            # Strips (batch_size * sequence_len) long prediction of one feature from the above diagram
            pred_single = tf.reshape(prediction[:, :, i], (-1,)) # prediction for one batch for i feature
            gt_single = tf.reshape(ground_truth[:, :, i], (-1,))

            loss = losses.concordance_cc(pred_single, gt_single) # loss for one batch for i feature
            tf.summary.scalar('losses/{} loss'.format(name), loss)
            
            mse = tf.reduce_mean(tf.square(pred_single - gt_single))
            tf.summary.scalar('losses/mse {} loss'.format(name), mse)
            
            #tf.losses.add_loss(loss / count)
            tf.losses.add_loss(loss) # this is an attempt to happens when you add loss instead of loss/count
        
        # print(tf.get_collection(tf.GraphKeys.UPDATE_OPS))
        total_loss = tf.losses.get_total_loss()
        tf.summary.scalar('losses/total loss', total_loss)

        with tf.Session(graph=g) as sess:
            train_op = slim.learning.create_train_op(total_loss,
                                                     optimizer,
                                                     summarize_gradients=True)
            
            logging.set_verbosity(1)
            print('******************* training **************************')
            slim.learning.train(train_op,
                                FLAGS.checkpoint_dir,
                                save_summaries_secs=SAVE_SUMMARY_SECS, # compute summary every x seconds
                                save_interval_secs=SAVE_INTERVAL_SECS) # save model checkpoint every x mins


if __name__ == '__main__':
    
    log = open(TRAIN_LOG_PATH, 'a')
    log.write('Time: ' + str(datetime.now()) + '\n')
    log.write('Training Dataset: ' + TFRECORD_DIR + FLAGS.dataset + '\n')
    log.write('learning_rate = ' + str(FLAGS.learning_rate) + '\n')
    log.write('batch_size = ' + str(FLAGS.batch_size) + '\n')
    log.write('hidden_units = ' + str(FLAGS.hidden_units) + '\n')
    log.write('sequence_length = ' + str(FLAGS.sequence_length) + '\n')
    log.write('optimizer = ' + str(FLAGS.optimizer) + '\n')
    log.write('Two Features\n')
    log.write('===================================================================\n')
    log.close()

    train()
