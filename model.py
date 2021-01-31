import numpy

from tensorflow import keras
#from keras.models import Sequential
#from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
#from keras.callbacks import EarlyStopping, ModelCheckpoint

TEST_DATA = [[3,4,2,3,4,6],[3,5,7,5,3,1,5,8,9,1],[1,2,3,3,4,6,3,2,3,4,5,2,1,2],[6,2,1,4,1,1,3],[3,1,7,3,5,6,9,6,7,5,7,3,6]]
TRAINING_SIZE = 3


def create_features_and_labels(tokens):
    labels = []
    features = []

    for token in tokens:
        for i in range(TRAINING_SIZE, len(token)):
           splice = token[i - TRAINING_SIZE:i + 1]

           features.append(splice[:-1])
           labels.append(splice[-1])
    
    return (numpy.array(features), labels)
         
def one_hot_code(labels):
    num_notes = 10 # max note + 1 for index reasons
    label_array = numpy.zeros((len(features), num_notes), dtype=numpy.int8)
    
    for index, note in enumerate(labels):
        label_array[index, note] = 1
   
    return numpy.array(label_array.shape)
    

def build_network(features, labels, num_notes):

    model = keras.Sequential()

    model.add(keras.layers.Masking(mask_value=0))

    model.add(keras.layers.LSTM(
        256,
        #input_shape=(features.shape[1], features.shape[2]),
        return_sequences=True
    ))

    model.add(keras.layers.Dropout(0.4))
    model.add(keras.layers.LSTM(512, return_sequences=True))
    model.add(keras.layers.Dropout(0.2))
    model.add(keras.layers.LSTM(256))
    model.add(keras.layers.Dense(256))
    model.add(keras.layers.Dropout(0.4))
    model.add(keras.layers.Dense(128))
    model.add(keras.layers.Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    callbacks = [keras.callbacks.EarlyStopping(monitor='val_loss', patience=5),
                 keras.callbacks.ModelCheckpoint('../models/model.h5', save_best_only=True, 
                                 save_weights_only=False)]

    
    history = model.fit(features,  labels, 
                        batch_size=512, epochs=150,
                        callbacks=callbacks)


if __name__ == "__main__":
    features, labels = create_features_and_labels(TEST_DATA) 
    # print(features)
    # print(labels)
    label_array = one_hot_code(labels)
    build_network(features, label_array, 10)
    