from tensorflow import keras
import numpy as np
import sklearn.preprocessing as skp

'''
Use an artificial neural network for trust management.

Author: Cody Lewis
Date: 2019-04-12
'''


def create_and_train_ann(train_data, train_labels, test_data, test_labels):
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(64, input_shape=(4,)))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dense(128))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dense(128))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dense(64))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(3))
    model.add(keras.layers.Activation('sigmoid'))

    adam = keras.optimizers.Adam(lr=0.0001)
    model.compile(loss="mean_squared_error", optimizer=adam, metrics=['accuracy'])
    data = np.array(train_data + test_data)
    labels = skp.label_binarize(np.array(train_labels + test_labels), ["-1", "0", "1"])
    model.fit(x=data, y=labels, epochs=300, validation_split=0.5)

    return model


def get_trusted_list(ann, client_id, service_target, capability_target, no_of_nodes):
    trusted_list = dict()

    for i in range(no_of_nodes):
        trusted_list[i] = unbinarize(ann.predict(np.array([[client_id, i, service_target, capability_target]]))[0])

    return trusted_list


def unbinarize(arr):
    value = list(arr)
    return [-1, 0, 1][value.index(max(value))]