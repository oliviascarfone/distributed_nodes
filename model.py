import numpy

from tensorflow import keras


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
   
    return label_array.shape
    





if __name__ == "__main__":
    features, labels = create_features_and_labels(TEST_DATA) 
    # print(features)
    # print(labels)
    label_array = one_hot_code(labels)
    