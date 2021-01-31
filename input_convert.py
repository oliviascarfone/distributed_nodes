import music21 as m21
import numpy
from music21 import chord, converter, instrument, note


deezNotes = {
    1:"A1",
    2:"A2",
    3:"A3",
    4:"B1",
    5:"B2",
    6:"B3",
    7:"C1",
    8:"C2",
    9:"C3",
    10:"D1",
    11:"D2",
    12:"D3",
    13:"E1",
    14:"E2",
    15:"E3",
    16:"F1",
    17:"F2",
    18:"F3"
}

testList1 = [[1],[7,4,15],[2,5,12],[2],[10],[8,2]]

def note_list_manager(note_list):
    res=[]
    for nte in note_list:
        res.append(m21.note.Note(deezNotes[nte]))
        print("Pitch: " +str(m21.note.Note(deezNotes[nte]).pitch))
    return res

def input_converter(input_list):
    res=[]
    for lst in input_list:
        res.append(note_list_manager(lst))
        print("Entry: ",note_list_manager(lst))
    return res

def parse_notes(notes_to_parse):
    notes=[]
    for element in notes_to_parse:
        print("Element: ", element)
        if len(element) == 1:
            print('Here')
            notes.append(str(element[0].pitch))
        elif len(element) > 1:
            # notes.append('.'.join((chord.Chord(element).normalOrder)))
            notes.append('.'.join(str(n) for n in chord.Chord(element).normalOrder))
    return notes

def do_shit_converter(input): #The shit you call boooiiii
    note_chord_list = input_converter(input)
    parsed_notes=parse_notes(note_chord_list)
    sequence_length = 100
    pitchnames = sorted(set(parsed_notes))
    note_to_int = dict((note, number) for number, note in enumerate(pitchnames))
    return note_to_int

    





