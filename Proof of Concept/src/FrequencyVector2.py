'''
Created on 28 Nov 2017
@author: Ghadah
This class aim  to Extract features out of a specified directory,in this case,
a Malware family. By Iterating through samples in each malware family, and
extracting 'BINDER' SYSCALL' and 'INTENT' Saving those calls to list
and forming a frequency-vector that represents each sample in the directory,
it stores the number of times a method occured in a certain sample.

note: value of directory_in_str, represents where the malware family is located
'''

import json
import os
import numpy as np
from pathlib import Path


# Initialising Variables
Binder_methods = []
files_in_dir = []
system_calls = []
freq_vec = {}
directory_in_str = '../../samples'


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

                value = json_data[i]["low"][0]["type"]

                # check if value equal to binder and not in the list
                if(value == 'BINDER' and json_data[i]["low"][0]["method_name"]not in dis_meth):
                    dis_meth.append(json_data[i]["low"][0]["method_name"])

                # check if value equal to intent and not in the list
                elif (value == 'INTENT' and json_data[i]["low"][0]["intent"] not in dis_meth):
                    dis_meth.append(json_data[i]["low"][0]["intent"])

                # check if value equal to syscall and not in the list
                elif(value == 'SYSCALL'):
                    for j in range(0, len(json_data[i]["low"])):
                        if(json_data[i]["low"][j]['sysname'] not in dis_meth):
                            dis_meth.append(json_data[i]["low"][j]['sysname'])
    return dis_meth


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
        if(json_data[i]["low"][0]["type"] == 'BINDER'):
            Binder_methods.append(json_data[i]["low"][0]["method_name"])
        # retrieving Intent Calls
        elif (json_data[i]["low"][0]["type"] == 'INTENT'):
            Binder_methods.append(json_data[i]["low"][0]["intent"])
        # retrieving System Calls
        elif(json_data[i]["low"][0]["type"] == 'SYSCALL'):
            for j in range(0, len(json_data[i]["low"])):
                system_calls.append(json_data[i]["low"][j]['sysname'])


# list Files in directory
files_in_dir = iterateThroughDir(directory_in_str)
result = files_in_dir.copy()

# Get the names of different methods in all directories
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
                    count[j] += 1
        # Used from https://stackoverflow.com/questions/30024342/converting-dataframe-to-numpy-array-causes-all-numbers-to-be-printed-in-scientif?rq=1
        np.set_printoptions(formatter={'float': "{:6.5g}".format})

        # Add results to dictionary
        freq_vec.update({files_in_dir[key][f]: count})

        # Reset lists to empty
        Binder_methods = []
        system_calls = []
    result[key] = freq_vec
    freq_vec = {}

print(result.get('CoinPirate_genome_stimulated'))
print ("\nList of Distinct Methods found: ")
print (dis)


# to access results from other classes
def getFreqVec():
    return result
