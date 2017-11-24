
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math

print('Import successful')

'''This function will '''
def pre_process(file):
    data = pd.read_excel(file)
    annotation = data['Annotation']
    new_array = []
    for i in range(len(annotation)):
        if(annotation[i]<=0):
            new_array.append(0)
        else:
            new_array.append(annotation[i])
    return new_array

#Convert the pre-proccessed data to MIDI
def convert_to_midi(input_array):
    array_to_midi = []
    for i in range(len(input_array)):
        if(input_array[i] == 0):
            array_to_midi.append(input_array[i])
        else:
            midi_value = 69 + 12*math.log(input_array[i]/440,2)
            array_to_midi.append(midi_value)
    return array_to_midi

#Store the midi values as a relative sequence of numbers
def midi_to_numbers(input_array):
    midi_relative_numbers = [0]
    #import pdb;pdb.set_trace()
    for i in range(1,len(input_array)):
        if(input_array[i]==0):
            midi_relative_numbers.append(input_array[i])
        elif(input_array[i]>input_array[i-1]):
            if(abs(input_array[i]-input_array[i-1])>1):
                sequence = midi_relative_numbers[i-1] + 1
                midi_relative_numbers.append(sequence)
            else:
                midi_relative_numbers.append(midi_relative_numbers[i-1])
        elif(input_array[i]<input_array[i-1]):
            if(abs(input_array[i]-input_array[i-1])>1):
                sequence = midi_relative_numbers[i-1]-1
                midi_relative_numbers.append(sequence)
            else:
                midi_relative_numbers.append(midi_relative_numbers[i-1])
        else:
            midi_relative_numbers.append(midi_relative_numbers[i-1])
    return midi_relative_numbers

#Remove silence frames as well as negative numbers from the frames
def remove_silence(input_array):
    query_sequence = []
    for i in range(0,len(input_array)):
        if(input_array[i]!=0):
            query_sequence.append(input_array[i])
    return query_sequence




if __name__ == '__main__':
    #Process the audio file
    file_audio = r'q7_freq.xlsx'
    pre_processed_data = pre_process(file_audio)
    midi_values_audio = convert_to_midi(pre_processed_data)
    midi_relative_audio = midi_to_numbers(midi_values_audio)
    audio_without_silence = remove_silence(midi_relative_audio)

    #Process the query file
    file_query = r'q7_query.xlsx'
    pre_processed_query = pre_process(file_query)
    midi_values_query = convert_to_midi(pre_processed_query)
    midi_relative_query = midi_to_numbers(midi_values_query)
    query_without_silence = remove_silence(midi_relative_query)
    print(midi_values_query)
    print(midi_relative_query)
    print('Midi removing silence')
    print(query_without_silence)
    print('audio without silence')
    print(audio_without_silence)
    #print('main audio file')
    #print(midi_relative_audio)


