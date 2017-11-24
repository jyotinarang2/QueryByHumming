
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

def getCostMatrices(reference, query, compare):  
    '''
    This function takes in the reference and the query objects and returns a tuple 
    of two cost matrices where the first(costMatrix) considers the distance between the two objects in the cost
    while the other(costMatrixLCS) does not. It also returns the trace back matrice which tells us the path back
    for the best match.
    The distance is defined based on 'compare function'
    :param reference: list of the object considered as the target list
    :param query: list of the object considered as the query list
    :param compare: a funcion which returns a truple (isEqual, distance) where
        'isEqual' says if the two are close enough
        'distance' is the distance between them
    '''
    # This is the list to be seached into; normally larger than the reference
    n = len(reference)

    #This is th list of objects to be searched for normally small compare to reference
    m = len(query)

    #Initializing the matrix with size one greater than the query and refernce sizes to fill up a dummy position
    costMatrix = np.zeros((n + 1, m + 1))
    costMatrixLCS = np.zeros((n + 1, m + 1))

    for i in range(n):
        for j in range(m):
            isEqual, dist = compare.getDist(reference[i], query[j])
            if isEqual == True:
                costMatrix[i+1][j+1] = costMatrix[i][j] + (1 - dist)
                costMatrixLCS[i+1][j+1] = costMatrixLCS[i][j] + 1
            else:
                costMatrix[i+1][j+1] = max(costMatrix[i][j+1], costMatrix[i+1][j])
                costMatrixLCS[i+1][j+1] = max(costMatrixLCS[i][j+1], costMatrixLCS[i+1][j])

    return (costMatrix, costMatrixLCS)

def rlcs(query, query_audio):


if __name__ == '__main__':
    file_audio = r'q7_freq.xlsx'
    pre_processed_data = pre_process(file_audio)
    midi_values_audio = convert_to_midi(pre_processed_data)
    file_query = r'q7_query.xlsx'
    pre_processed_query = pre_process(file_query)
    midi_values_query = convert_to_midi(pre_processed_query)



