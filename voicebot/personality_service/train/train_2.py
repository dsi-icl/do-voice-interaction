### This file contains code to train an LSTM to model emotional 
### transitions in the characters from the Friends Dataset 
### according to approach 2 from the report. Please change the 
### variable 'character' below to train for a different character.
### There are options below to train using masking or using a 
### batch size of 1.

character="Joey"


import tensorflow as tf
from tensorflow.keras import Sequential, optimizers
from tensorflow.keras.layers import LSTM, Dense, Masking
from tensorflow.keras.metrics import RootMeanSquaredError
import numpy as np
import sys
import pickle
import os
from matplotlib import pyplot as plt
from scikeras.wrappers import KerasRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_squared_error


sys.path.append('../preprocessing/process_emotions')
from process_raw_2 import get_data
tf.compat.v1.enable_eager_execution()


class TestCallback(tf.keras.callbacks.Callback):
    def __init__(self, test_data):
        self.test_data = test_data

    def on_epoch_end(self, epoch, logs):
        x, y = self.test_data
        self.model.evaluate(x, y, verbose=2, batch_size=1)


examples, labels = get_data(character)

####### Batch_size = 1 Approach ##########


# batches=np.array([example for example in examples], dtype=object)
# batch_labels=np.array([np.array(label) for label in labels], dtype='float64')


##### Parameters  #####
# N = len(batches)
# n_feats = 2
# latent_dim = 32
# out_dim= 2
# train_split=0.9


###### Train split  #######
# train_no=int(np.floor(N*train_split))
# p = np.random.permutation(N)  
# X=batches[p]
# Y=batch_labels[p]
# x_train=X[:train_no]
# x_test=X[train_no:]
# y_train=Y[:train_no]
# y_test=Y[train_no:]
# x_train=tf.ragged.constant(np.ndarray.tolist(x_train))
# x_test=tf.ragged.constant(np.ndarray.tolist(x_test))


# model=Sequential()
# model.add(Input(shape=[None, n_feats], ragged=True, batch_size=1))
# model.add(LSTM(latent_dim))
# model.add(Dense(out_dim, activation='tanh'))
# model.summary()
# model.compile(loss='mse', metrics=[tf.keras.metrics.RootMeanSquaredError()])


# # model.fit(x_train, y_train, epochs=5, verbose=2, batch_size=1, callbacks=[TestCallback((x_test, y_test))])






####### Masking Approach #########



mask_value=5
padded_x = tf.keras.preprocessing.sequence.pad_sequences(examples, padding="pre", value=mask_value, dtype='float32')
y= tf.convert_to_tensor(labels, dtype='float32').numpy()

x_train, x_test, y_train, y_test = train_test_split(padded_x,
                                                    y,
                                                    test_size=0.1,
                                                    random_state=42)

input_shape=tf.shape(x_train)[1:]


def create_model(neurons):
    model=Sequential()
    model.add(Masking(mask_value=mask_value, input_shape=input_shape))
    model.add(LSTM(neurons))
    model.add(Dense(2, activation='tanh'))
    model.compile(optimizer=optimizers.Adam(learning_rate=0.01),loss='mse', metrics=[RootMeanSquaredError()])
    model.summary()
    return model

######   Grid Search   #######
# param_grid = dict(epochs=[20, 30], batch_size=[30, 100], optimizer__learning_rate= [0.01, 0.1, 0.2], model__neurons=[32, 64])
# grid = GridSearchCV(scoring='neg_mean_squared_error', verbose=2, estimator=KerasRegressor(create_model), param_grid=param_grid, cv=10 )
# grid_result = grid.fit(x_train, y_train)
## print out configurations
# print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
# means = grid_result.cv_results_['mean_test_score']
# stds = grid_result.cv_results_['std_test_score']
# params = grid_result.cv_results_['params']
# for mean, stdev, param in zip(means, stds, params):
#     print("%f (%f) with: %r" % (mean, stdev, param))

##### Train without grid seaarch  #######

model=create_model(32)
history = model.fit(x_train, y_train, epochs=20, verbose=1, batch_size=100)
print(history.history)
print(model.evaluate(x_test, y_test))
# plt.plot(history.history['root_mean_squared_error'])
# plt.plot(history.history['val_root_mean_squared_error'])
# plt.title('model accuracy')
# plt.ylabel('accuracy')
# plt.xlabel('epoch')
# plt.legend(['train', 'val'], loc='upper left')
# plt.show()

######## Compare with dummy regressor  ##########


# X_train=np.zeros((len(y_train)))
# X_test=np.zeros((len(y_test)))
# dummy_train = DummyRegressor(strategy="mean")
# dummy_train.fit(X_train, y_train)
# y_predicted=dummy_train.predict(X_test)
# rms = mean_squared_error(y_test, y_predicted, squared=False)
# print(rms)



########   Save model   ########

# os.chdir('/home/dodev/ben_msc_project/do-voice-interaction/voicebot/personality_service/models/type_2')


# pickle.dump(model, open(character+".pickle", 'wb'))