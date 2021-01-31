import numpy
import music21
import glob
import pickle

from tensorflow import keras
#from keras.models import Sequential
#from keras.layers import LSTM, Dense, Dropout, Masking, Embedding
#from keras.callbacks import EarlyStopping, ModelCheckpoint

def get_notes():
    """ Get all the notes and chords from the midi files in the ./midi_songs directory """
    notes = []

    for file in glob.glob("midi_me/*.mid"):
        print(file)
        midi = music21.converter.parse(file)

        print("Parsing %s" % file)

        notes_to_parse = None

        try: # file has instrument parts
            s2 = music21.instrument.partitionByInstrument(midi)
            notes_to_parse = s2.parts[0].recurse() 
        except: # file has notes in a flat structure
            notes_to_parse = midi.flat.notes

        for element in notes_to_parse:
            if isinstance(element, music21.note.Note):
                notes.append(str(element.pitch))
            elif isinstance(element, music21.chord.Chord):
                notes.append('.'.join(str(n) for n in element.normalOrder))

    with open('data/notes', 'wb') as filepath:
        pickle.dump(notes, filepath)

    return notes


def create_input_and_output(sequence):
    network_input = []
    network_output = []
    note_to_int = {}
    sequence_length = 10
    pitchnames = sorted(set(item for item in notes))
    
    for number, note in enumerate(pitchnames):
        note_to_int[note] = number

    for i in range(0, len(notes) - sequence_length, 1):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])
    n_patterns = len(network_input)
    
    network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))

    network_input = network_input / float(len(pitchnames))

    try:
        network_output = keras.utils.to_categorical(network_output)
    except ValueError:
        pass

    return (network_input, network_output, len(pitchnames))
    

def build_network(network_input, network_output, num_notes):

    model = keras.Sequential()

    model.add(keras.layers.LSTM(
        512,
        input_shape=(network_input.shape[1], network_input.shape[2]),
        recurrent_dropout=0.3,
        return_sequences=True
    ))
    model.add(keras.layers.LSTM(512, return_sequences=True, recurrent_dropout=0.3,))
    model.add(keras.layers.LSTM(512))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(256))
    model.add(keras.layers.Activation('relu'))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(num_notes))
    model.add(keras.layers.Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

    return model


def thomas_the_train(model, network_input, network_output):
    filepath = "weights-improvement-{epoch:02d}-{loss:.4f}-bigger.hdf5"
    checkpoint = keras.callbacks.ModelCheckpoint(
        filepath,
        monitor='loss',
        verbose=0,
        save_best_only=True,
        mode='min'
    )
    callbacks_list = [checkpoint]

    model.fit(network_input, network_output, epochs=10, batch_size=128, callbacks=callbacks_list)


if __name__ == "__main__":
    notes = get_notes()
    network_input, network_output, num_notes = create_input_and_output(notes) 
    model = build_network(network_input, network_output, num_notes)
    thomas_the_train(model, network_input, network_output)

    