
from pandas import DataFrame, read_csv
import matplotlib.pyplot as plt
import rlcs as rlcs
import pandas as pd
import numpy as np
import math

print('Import successful')

'''This function will remove -ve values and convert them to 0's'''
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

def downsample_audio(input_array, sampling_rate):
    return input_array[::sampling_rate]

#Store the midi values as a relative sequence of numbers
def midi_to_numbers(input_array):
    midi_relative_numbers = [0]
    return np.diff(input_array)
    #import pdb;pdb.set_trace()
    # for i in range(1,len(input_array)):
    #     if(input_array[i]==0):
    #         midi_relative_numbers.append(input_array[i])
    #     elif(input_array[i]>input_array[i-1]):
    #         if(abs(input_array[i]-input_array[i-1])>1):
    #             #value = int(abs(input_array[i]-input_array[i-1]))
    #             sequence = midi_relative_numbers[i-1] + 1
    #             midi_relative_numbers.append(sequence)
    #         else:
    #             midi_relative_numbers.append(midi_relative_numbers[i-1])
    #     elif(input_array[i]<input_array[i-1]):
    #         if(abs(input_array[i]-input_array[i-1])>1):
    #             #value = int(abs(input_array[i]-input_array[i-1]))
    #             sequence = midi_relative_numbers[i-1]-1
    #             midi_relative_numbers.append(sequence)
    #         else:
    #             midi_relative_numbers.append(midi_relative_numbers[i-1])
    #     else:
    #         midi_relative_numbers.append(midi_relative_numbers[i-1])
    # return midi_relative_numbers

#Remove silence frames as well as negative numbers from the frames
def remove_silence(input_array):
    query_sequence = []
    for i in range(0,len(input_array)):
        if(input_array[i]!=0):
            query_sequence.append(input_array[i])
    return query_sequence

def get_continuous_numbers(input_array):
    return input_array[np.insert(np.diff(input_array).astype(np.bool),0,True)]

def process_file(file_name):
    pre_processed_query = pre_process(file_name)
    numpy_array = np.asarray(pre_processed_query)
    midi_values_query = convert_to_midi(numpy_array)
    query_without_silence = remove_silence(midi_values_query)
    downsampled = downsample_audio(query_without_silence,10)
    midi_relative_query = midi_to_numbers(downsampled)
    query_sequence = np.round(midi_relative_query)
    non_repeated = get_continuous_numbers(query_sequence)
    return non_repeated



#def segment_audio(input_array):
#    segment_to_pattern = {}
    
''' This module is not intended to run from interpreter.
        Instead, call the functions from your main script.
        from lcs import rlcs as rlcs

        score, diag, cost = rlcs.rlcs(X, Y, tau_dist,  delta)
        segment = rlcs.backtrack(X, Y, score, diag, cost)'''


if __name__ == '__main__':
    #Process the audio file
    file_audio = r'q7_freq.xlsx'

    # #Process the query file
    file_query = r'q7_query.xlsx'
    file = r'query_q1.csv'
    audio_data = process_file(file_audio)
    query_data = process_file(file_query)
    check = pre_process(file)
    np.set_printoptions(threshold=np.nan)
    print(audio_data)
    print(query_data)

    score, diag, cost = rlcs.rlcs(query_data, audio_data)
    segment = rlcs.backtrack(query_data, audio_data, score, diag, cost)
    print(segment)

