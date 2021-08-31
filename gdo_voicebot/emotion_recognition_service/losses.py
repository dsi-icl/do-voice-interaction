from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
import tensorflow as tf

slim = tf.contrib.slim

def concordance_cc(predictions, labels):

    pred_mean, pred_var = tf.nn.moments(predictions, (0,)) # calculates mean and variance of prediction
    gt_mean, gt_var = tf.nn.moments(labels, (0,)) # calculates mean and variance of label
    mean_cent_prod = tf.reduce_mean((predictions - pred_mean) * (labels - gt_mean))

    # returns loss for single feature for this batch = 1 - CCC
    return 1 - (2 * mean_cent_prod) / (pred_var + gt_var + tf.square(pred_mean - gt_mean))


def concordance_cc2(r1, r2):

    mean_cent_prod = ((r1 - r1.mean()) * (r2 - r2.mean())).mean()

    return (2 * mean_cent_prod) / (r1.var() + r2.var() + (r1.mean() - r2.mean()) ** 2)
