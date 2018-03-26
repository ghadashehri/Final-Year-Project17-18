'''
Created on 18 Feb 2018

@author: Ghadah

This class aim  to Extract features out of a specified directory,in this case,
a Malware family. By Iterating through samples in each Malware family, and
extracting 'BINDER','SYSCALL','INTENT', and high-level class information
Saving those calls to list and forming a bit-vector that represents
each sample in the directory, vectors use 1 to indicate a method occurred
0 otherwise.

note: value of directory_in_str, represents where the Malware family is located
'''
import json
import os
import time
import numpy as np
from pathlib import Path


# Initialising Variables
Binder_methods = []
files_in_dir = []
system_calls = []
bit_vec = {}
directory_in_str = '../../../samples'


# returns a list of all the distinct methods found in data set
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

                # add values of system calls
                dis_meth.append(class_value)

                if('subclass' in json_data[i].keys()):
                    subclass_value = json_data[i]["subclass"]
                    dis_meth.append(subclass_value)

                # add values of Binder transactions
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
    return unique_list


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

    json_data = data["behaviors"]["dynamic"]["host"]
    return json_data


# loop through data, and extract all methods
def extractFeature(json_data):
    n = len(json_data)
    for i in range(0, n):
        # appending class and subclass information
        system_calls.append(json_data[i]["class"])
        if('subclass' in json_data[i].keys()):
            system_calls.append(json_data[i]["subclass"])

        if(json_data[i]["low"][0]["type"] == 'BINDER'):
            Binder_methods.append(json_data[i]["low"][0]["method_name"])

        # retrieving Intent Calls
        elif (json_data[i]["low"][0]["type"] == 'INTENT'):
            Binder_methods.append(json_data[i]["low"][0]["intent"])

        # retrieving System Calls
        elif(json_data[i]["low"][0]["type"] == 'SYSCALL'):
            for j in range(0, len(json_data[i]["low"])):
                Binder_methods.append(json_data[i]["low"][j]['sysname'])


# start timer
start_time = time.time()

# list of files in directory
files_in_dir = iterateThroughDir(directory_in_str)
result = files_in_dir.copy()

# getting the names of different methods in all directories
dis = distinct_Methods(files_in_dir)

for key in files_in_dir:
    for f in range(0, len(files_in_dir[key])):
        json_data = readJson(files_in_dir[key][f])
        extractFeature(json_data)
        combined = Binder_methods + system_calls

        # array of zeros to determine size of vector
        count = np.zeros(len(dis))
        for i in range(0, len(combined)):
            for j in range(0, len(dis)):
                if(combined[i] == dis[j]):
                    count[j] = 1

        # this line used from
        # https://stackoverflow.com/questions/30024342/converting-dataframe-to-numpy-array-causes-all-numbers-to-be-printed-in-scientif?rq=1
        np.set_printoptions(formatter={'float': "{:6.5g}".format})

        # filtering feature vectors
        all_zeros = not np.any(count)
        num_of_zeros = np.count_nonzero(count == 0)
        length_req = len(dis)
        if not all_zeros and num_of_zeros < length_req-6:

            # add results to dictionary
            bit_vec.update({files_in_dir[key][f]: count})

        # reset lists to empty
        Binder_methods = []
        system_calls = []
    result[key] = bit_vec
    bit_vec = {}

print(result)
print ("\nList of Distinct Methods found: ")
print (dis)

# Print time taken
print('\nTime taken to produce Bit Vectors: %.2f s' %
      (time.time() - start_time))


# To get results from other classes
def getBitVec():
    return result
