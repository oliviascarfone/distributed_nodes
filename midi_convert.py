import glob
import music21
import numpy
from music21 import chord, converter, instrument, note

def midi_converter():
    notes = []
    for file in glob.glob("distributed_nodes\midi_me\LeavingEarth.mid") :
        print(file)
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
    pitchnames = sorted(set(notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    #god damnit


