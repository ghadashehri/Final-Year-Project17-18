'''
Created on 8 Mar 2018

@author: Ghadah
'''
import json
import os
import numpy as np
import time
from pathlib import Path



# Initialising Variables
files_in_dir = []
system_calls = []
freq_vec = {}
directory_in_str = '../../../samples'


def distinct_Methods(dircFiles):
    dis_meth = []
    for key in dircFiles:
        for f in range(len(dircFiles[key])):
            with open(dircFiles[key][f]) as data_file:

                # takes an actual object as parameter
                data = json.load(data_file)
            json_data = data["behaviors"]["dynamic"]["host"]
            n = len(json_data)

            for i in range(0, n):

                class_value = json_data[i]["class"]
                binder_value = json_data[i]["low"][0]["type"]

                # Add values of system calls
                dis_meth.append(class_value)

                if('subclass' in json_data[i].keys()):
                    subclass_value = json_data[i]["subclass"]
                    dis_meth.append(subclass_value)

                # Add values of Binder transactions
                # check if value equal to binder and not in the list
                if(binder_value == 'BINDER'):
                    dis_meth.append(json_data[i]["low"][0]["method_name"])

                # check if value equal to intent and not in the list
                if (binder_value == 'INTENT'):
                    dis_meth.append(json_data[i]["low"][0]["intent"])

                # check if value equal to syscall and not in the list
                if(binder_value == 'SYSCALL'):
                    for j in range(0, len(json_data[i]["low"])):
                        if(json_data[i]["low"][j]['sysname']):
                            # print(json_data[i]["low"][j]['sysname'])
                            dis_meth.append(json_data[i]["low"][j]['sysname'])

    unique_list = list(set(dis_meth))
    dis_bi = list(set(get_BiGram(dis_meth)))

    return unique_list + dis_bi


# returns .json files found in directory
def iterateThroughDir(directory):
    families = {}
    files = []
    sub_directories = os.listdir(directory)
    for dirc in sub_directories:
        sub = directory + '/' + dirc
        pathlist = Path(sub).glob('**/*.json')
        for path in pathlist:
            files.append(str(path))
        families.update({dirc: files})

        files = []
    return families


# returns information extracted from each .json file
def readJson(f):
    with open(f) as data_file:
        # takes an actual object as parameter
        data = json.load(data_file)

    # using some of data
    json_data = data["behaviors"]["dynamic"]["host"]
    return json_data


# loop through data, and extract the required methods
def extractFeature(json_data):
    n = len(json_data)
    for i in range(0, n):
        system_calls.append(json_data[i]["class"])
        if('subclass' in json_data[i].keys()):
            system_calls.append(json_data[i]["subclass"])
        if(json_data[i]["low"][0]["type"] == 'BINDER'):
            system_calls.append(json_data[i]["low"][0]["method_name"])
        # retrieving Intent Calls
        elif (json_data[i]["low"][0]["type"] == 'INTENT'):
            system_calls.append(json_data[i]["low"][0]["intent"])
        # retrieving System Calls
        elif(json_data[i]["low"][0]["type"] == 'SYSCALL'):
            for j in range(0, len(json_data[i]["low"])):
                system_calls.append(json_data[i]["low"][j]['sysname'])


# Returns a 2-gram vector
def get_BiGram(methods):
    biGram = []
    j = 0
    for i in range(0, len(methods)-1):
        j = i+1
        biGram.append(methods[i] + ' ' + methods[j])

    return biGram


# Compute the required time
start = time.time()

# list Files in directory
files_in_dir = iterateThroughDir(directory_in_str)
result = files_in_dir.copy()

# Get the names of different methods in all directories
dis = distinct_Methods(files_in_dir)

for key in files_in_dir:
    for f in range(0, len(files_in_dir[key])):

        json_data = readJson(files_in_dir[key][f])
        extractFeature(json_data)
        combined = system_calls
        bi_gram = get_BiGram(combined)

        all_values = combined + bi_gram
        # array of zeros to determine size of vector
        count = np.zeros(len(dis))
        for i in range(0, len(all_values)):
            for j in range(0, len(dis)):
                if(all_values[i] == dis[j]):
                    count[j] += 1
        # Used from https://stackoverflow.com/questions/30024342/converting-dataframe-to-numpy-array-causes-all-numbers-to-be-printed-in-scientif?rq=1
        np.set_printoptions(formatter={'float': "{:6.5g}".format})

        # filtering produced feature vectors
        all_zeros = not np.any(count)
        if not all_zeros:
            # Add results to dictionary
            freq_vec.update({files_in_dir[key][f]: count})

        # Reset lists to empty
        system_calls = []
    result[key] = freq_vec
    freq_vec = {}

print(result)
print ("\nList of Distinct Methods found: ")
print (len(dis))

print(time.time() - start)


# to access results from other classes + filtering
def getBiGramVec():
    filtered_res = result.copy()
    filtered_res = dict([(k, v) for k, v in filtered_res.items() if len(v) > 6])
    return filtered_res
