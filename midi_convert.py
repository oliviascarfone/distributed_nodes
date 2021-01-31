import glob
import music21
import numpy
import tensorflow
import tensorflow.python.keras.utils.np_utils as np_utils
from music21 import chord, converter, instrument, note
from tensorflow import keras

notes = []

for file in glob.glob("midi_me/*.mid") :
    midi = converter.parse(file)
    notes_to_parse = None

    parts = instrument.partitionByInstrument(midi)

    if parts: # file has instrument parts
        notes_to_parse = parts.parts[0].recurse()
    else: # file has notes in a flat structure
        notes_to_parse = midi.flat.notes

    for element in notes_to_parse:
        if isinstance(element, note.Note):
            notes.append(str(element.pitch))
        elif isinstance(element, chord.Chord):
            notes.append('.'.join(str(n) for n in element.normalOrder))

sequence_length = 100
# get all pitch names
pitchnames = sorted(set(notes))
# create a dictionary to map pitches to integers
note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
network_input = []
network_output = []
# create input sequences and the corresponding outputs
# network_input is all of the note/chord 'codes' (ints) from all ${sequence_length} slices of the notes array
# so if notes has 200 notes/chords in it, and sequence_length is 100, then network_input will append all the note codes for notes[0]-notes[99], then notes[1]-notes[100], etc...
# network_output is all of the note/chord 'codes' (integers) from notes array that are outside of sequence length
for i in range(0, len(notes) - sequence_length, 1):
    sequence_in = notes[i:i + sequence_length]
    sequence_out = notes[i + sequence_length]
    network_input.append([note_to_int[char] for char in sequence_in])
    network_output.append(note_to_int[sequence_out])
n_patterns = len(network_input)
# reshape the input into a format compatible with LSTM layers
# reshapes it into a list of network_input length of lists containing each individual note
# seems wrong
network_input = numpy.reshape(network_input, (n_patterns, sequence_length, 1))
# normalize input
network_input = network_input / float(n_vocab)
network_output = np_utils.to_categorical(network_output)
