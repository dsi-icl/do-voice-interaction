import tensorflow as tf
from keras import Sequential
from keras.layers import LSTM, Dense, Input
import numpy as np
import sys
import pickle
import os
sys.path.append('../preprocessing/part2')
from process_raw_2 import get_data

character="Ross"

examples, labels = get_data(character)

batches=np.array([example for example in examples], dtype=object)
batch_labels=np.array([np.array(label) for label in labels], dtype='float64')


# Parameters
N = len(batches)
n_feats = 2
latent_dim = 32
out_dim= 2
train_split=0.9
train_no=int(np.floor(N*train_split))
p = np.random.permutation(N)  
X=batches[p]
Y=batch_labels[p]
x_train=X[:train_no]
x_test=X[train_no:]
y_train=Y[:train_no]
y_test=Y[train_no:]



model=Sequential()
model.add(Input(shape=[None, n_feats], ragged=True, batch_size=1))
# model.add(LSTM(latent_dim, return_sequences=True))
model.add(LSTM(latent_dim))
model.add(Dense(out_dim))

model.summary()
model.compile(loss='mse', metrics=[tf.keras.metrics.RootMeanSquaredError()])


x_train=tf.ragged.constant(np.ndarray.tolist(x_train))
x_test=tf.ragged.constant(np.ndarray.tolist(x_test))

class TestCallback(tf.keras.callbacks.Callback):
    def __init__(self, test_data):
        self.test_data = test_data

    def on_epoch_end(self, epoch, logs):
        x, y = self.test_data
        self.model.evaluate(x, y, verbose=2, batch_size=1)

model.fit(x_train, y_train, epochs=50, verbose=2, batch_size=1, callbacks=[TestCallback((x_test, y_test))])



from sklearn.dummy import DummyRegressor
X_train=np.zeros((len(y_train)))
dummy_train = DummyRegressor(strategy="mean")

print(np.sum(y_train[:,:1])/len(y_train))
print(np.sum(y_train[:,1:])/len(y_train))

print(dummy_train.fit(X_train, y_train))

y_predicted=dummy_train.predict(X_train)
# print(y_predicted)

from sklearn.metrics import mean_squared_error

rms = mean_squared_error(y_train, y_predicted, squared=False)

print(rms)


X_test=np.zeros((len(y_test)))

dummy_test = DummyRegressor(strategy="mean")

print(np.sum(y_test[:,:1])/len(y_test))
print(np.sum(y_test[:,1:])/len(y_test))

print(dummy_train.fit(X_test, y_test))

y_predicted=dummy_train.predict(X_test)
# print(y_predicted)

rms = mean_squared_error(y_test, y_predicted, squared=False)

print(rms)

os.chdir('/home/dodev/ben_msc_project/do-voice-interaction/voicebot/personality_service/models/type_2')


pickle.dump(model, open(character+".pickle", 'wb'))
