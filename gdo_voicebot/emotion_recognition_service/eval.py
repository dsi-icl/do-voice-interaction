from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
import os
from datetime import datetime
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import numpy as np

import models
import data_metrics
from data_provider import get_split
from helper import get_pathlist_from_dir, development_msg, TFRECORD_DIR

slim = tf.contrib.slim

EVAL_LOG_PATH = './log_eval.txt'

flags = tf.app.flags
flags.DEFINE_string('dataset_dir', TFRECORD_DIR, 'The tfrecords directory.')
flags.DEFINE_string('checkpoint', None, 'The checkpoint to use.')  # Required
flags.DEFINE_string('steps', None, 'The number of steps.')  # Required

flags.DEFINE_integer('batch_size', 5, 'The batch size to use.')
flags.DEFINE_integer('hidden_units', 256, 'Recurrent network hidden units.') 
flags.DEFINE_string('model', 'audio_model2', 'Which model is going to be used: audio, video, or both')
flags.DEFINE_integer('sequence_length', 100, 'Number of audio frames in one input')

flags.DEFINE_integer('eval_interval_secs', 20, 'The seconds to wait until next evaluation.')
flags.DEFINE_string('portion', None, '{devel|test} to evaluation on validation or test set.') # Required
flags.DEFINE_string('data_unit', None, '{word|sentence} as data input')
flags.DEFINE_boolean('liking', True, 'Liking dimension is calculated in the losses function or not')

# Other settings
flags.DEFINE_string('device', '0', 'CPU(-1) or GPU(0)') 
flags.DEFINE_string('min_log_level', '2', 'The min log level.') 
FLAGS = flags.FLAGS

# Use CPU when -1 and GPU when 0
os.environ["CUDA_VISIBLE_DEVICES"] = str(FLAGS.device)
# Logging setting
os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(FLAGS.min_log_level)

'''
0 = all messages are logged (default behavior)
1 = INFO messages are not printed
2 = INFO and WARNING messages are not printed
3 = INFO, WARNING, and ERROR messages are not printed
'''

def evaluate_2(file2eval, model_path):
    
    development_msg('\n******************* Enter evaluate_2() ************************')
    development_msg('file2eval = ' + str(file2eval))
    development_msg('model_path = ' + str(model_path))

    with tf.Graph().as_default():

        filename_queue = tf.FIFOQueue(capacity=1, dtypes=[tf.string])
        development_msg('\n****************** Loading dataset via get_split() **********************')
        # Load dataset
        audio_frames, word_embeddings, labels = get_split(file2eval, False,
                                                          FLAGS.batch_size, seq_length=FLAGS.sequence_length)
        
        development_msg('audio_frames = ' + str(audio_frames))
        development_msg('word_embeddings = ' + str(word_embeddings))
        development_msg('labels = ' + str(labels))
        development_msg('\n****************** Defining model graph **********************')
        # Define model graph.
        with slim.arg_scope([slim.layers.batch_norm, slim.layers.dropout], is_training=False):
            
            predictions = models.get_model(FLAGS.model)(audio_frames,
                                                       emb=tf.cast(word_embeddings, tf.float32),
                                                       hidden_units=FLAGS.hidden_units)
            

        coord = tf.train.Coordinator() # controller that maintains the set of threads and is part of tf.train.supervisor
        saver = tf.train.Saver(slim.get_variables_to_restore()) # this saver allows to get variables from a given model path

        development_msg('\n****************** Starting eval session **********************')

        with tf.Session() as sess: # 'tf.Session() as sess' initiates a TensorFlow Graph object in which tensors are processed through operations (or ops).     
            saver.restore(sess, model_path) # restores previous variables
            tf.train.start_queue_runners(sess=sess, coord=coord) # QueueRunner = when tf is reading the input, the queue serves all the workers that are responsible for executing the training step

            evaluated_predictions = []
            evaluated_labels = []

            nexamples = _get_num_examples(file2eval)
            development_msg('nexamples = ' + str(nexamples))
            num_batches = int(math.ceil(nexamples / (float(FLAGS.sequence_length))))
        
            print('Evaluating file : {}'.format(file2eval))
            development_msg('queue size = ' + str(sess.run(filename_queue.size())))
            sess.run(filename_queue.enqueue(file2eval))
            development_msg('queue size = ' + str(sess.run(filename_queue.size())))

            development_msg('Iterating through mini batches')
            for i in range(num_batches):
                development_msg('Running predictions on mini batch ' + str(i))
                development_msg('labels = ' + str(labels))
                prediction_, label_ = sess.run([predictions, labels])

                development_msg('Appending prediction')
                evaluated_predictions.append(prediction_[0])
                evaluated_labels.append(label_[0])

            development_msg(np.vstack(evaluated_predictions).shape)
            evaluated_predictions = np.vstack(evaluated_predictions)[:nexamples]
            development_msg(np.vstack(evaluated_predictions).shape)
            evaluated_labels = np.vstack(evaluated_labels)[:nexamples]
            
            
            for i in range(sess.run(filename_queue.size())):
                sess.run(filename_queue.dequeue())
            if sess.run(filename_queue.size()) != 0:
                raise ValueError('Queue not empty!')
            
            coord.request_stop()

            development_msg('queue size = ' + str(sess.run(filename_queue.size())))

        development_msg('\n****************** Ending session **********************')
        development_msg('')
    return evaluated_predictions, evaluated_labels


def _get_num_examples(tf_file):
    c = 0
    for _ in tf.python_io.tf_record_iterator(tf_file):
        c += 1

    return c


if __name__ == '__main__':

    if FLAGS.portion == None:
        print("\nPlease specify portion (e.g. --portion 'devel')\n")
        exit(-1)
    if FLAGS.checkpoint == None:
        print("\nPlease specify checkpoint (e.g. --checkpoint 'all4_after103ksteps')\n")
        exit(-1)
    if FLAGS.steps == None:
        print("\nPlease specify the number of steps (e.g. --steps '12161')\n")
        exit(-1)

    best, inx = 0.9292, 1
    cnt = 0
    model_path = FLAGS.checkpoint + '/' + 'model.ckpt-' + FLAGS.steps

    development_msg('\n**************** Setting up eval model ***************')
    predictions, labels = None, None

    eval_model = data_metrics.metric_graph()
    eval_arousal = eval_model.eval_metric_arousal # assign metric[0]
    eval_valence = eval_model.eval_metric_valence # assign metric[1]
    
    # prediction - mifu
    if FLAGS.portion == 'test':
        print('\n**************** Evaluation the test portion ***************')
        dataset_dir = FLAGS.dataset_dir + '/test'
    elif FLAGS.portion == 'devel':
        print('\n**************** Evaluating the devel portion ***************')
        dataset_dir = FLAGS.dataset_dir + '/devel'
    else:
        print('\n**************** Evaluating the ' + FLAGS.portion + ' portion ***************')
        dataset_dir = FLAGS.dataset_dir + '/' + FLAGS.portion

    portion_files = get_pathlist_from_dir(dataset_dir)
    development_msg('Below are the portion files:')
    development_msg(portion_files)
    development_msg('')

    for tf_file in portion_files:
        # prediction results
        predictions_file, labels_file = evaluate_2(str(tf_file), model_path)

        development_msg(tf_file)

        if predictions is not None and labels is not None:
            predictions = np.vstack((predictions, predictions_file))
            labels = np.vstack((labels, labels_file))
        else:
            predictions = predictions_file
            labels = labels_file

    development_msg(predictions.shape)
    development_msg(labels.shape)

    print('****************** Evaluating the prediction agaisnt label **********************')

    with tf.Session() as sess:
        e_arousal, e_valence = sess.run([eval_arousal, eval_valence],
                                                    feed_dict={
                                                        eval_model.eval_predictions: predictions,
                                                        eval_model.eval_labels: labels
                                                    })
        print('e_arousal (CCC) = ' + str(e_arousal)) # CCC for arousal
        print('e_valence (CCC) = ' + str(e_valence)) # CCC for valence
        eval_res = np.array([e_arousal, e_valence])

        if FLAGS.liking:
            eval_loss = 1 - (np.sum(eval_res) / eval_res.shape[0])
        else:
            eval_loss = (2 - eval_res[0] - eval_res[1]) / 2

        print('Evaluation: %d, loss: %.4f -- arousal: %.4f -- valence: %.4f'
                % (cnt, eval_loss, eval_res[0], eval_res[1]))

        cnt += 1

    log = open(EVAL_LOG_PATH, 'a')
    log.write('Time: ' + str(datetime.now()) + '\n')
    log.write('Portion: ' + FLAGS.portion + '\n')
    log.write('Checkpoint: ' + FLAGS.checkpoint + '\n')
    log.write('Steps: ' + FLAGS.steps + '\n')
    log.write('Checkpoint Full Path: ' + str(model_path) + '\n')
    log.write('Dataset Full Path: ' + str(dataset_dir) + '\n')
    log.write('...................................................................\n')
    log.write('batch_size=' + str(FLAGS.batch_size) + ' hidden_units='+ str(FLAGS.hidden_units) + ' model=' + str(FLAGS.model) + '\n' + 'sequence_length=' + str(FLAGS.sequence_length) + ' eval_interval_secs=' + str(FLAGS.eval_interval_secs) + ' liking=' + str(FLAGS.liking) + '\n')
    log.write('...................................................................\n')
    log.write('TotalLoss: %.4f, Arousal: %.4f, Valence: %.4f\n'
                % (eval_loss, eval_res[0], eval_res[1]))
    log.write('===================================================================\n')
    log.close()

    print('Finished evaluation!')
