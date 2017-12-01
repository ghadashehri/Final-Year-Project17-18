'''
Created on 28 Nov 2017

@author: Ghadah


This class aim  to Extract features out of a specified directory,in this case,
a Malware family. By Iterating through samples in each malware family, and
extracting 'BINDER' SYSCALL' and 'INTENT' Saving those calls to list
and creates a dictionary that contains the name of every method found in
data set and the number of times it occurred.

note: value of directory_in_str, represents where the malware family is located

'''
import json
import numpy as np
import collections
from pathlib import Path


# list of methods called
files_in_dir = []
directory_in_str = '../../samples/'
Binder_methods = []
system_calls = []


# returns .json files found in directors
def iterateThroughDir(directory):
    files = []
    pathlist = Path(directory).glob('**/*.json')
    for path in pathlist:
        files.append(str(path))
    return files


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
for f in range(0, len(files_in_dir)):
    json_data = readJson(files_in_dir[f])
    extractFeature(json_data)

combined = Binder_methods + system_calls
arr = np.array(combined)
unique, counts = np.unique(arr, return_counts=True)
print ("\nThe methods Calls in all submitted Samples: ")
print (dict(zip(unique, counts)))
print ("\n")

# additional Counter
cnt = collections.Counter()
for word in arr:
    cnt[word] += 1
print ("Number of calls made: ")
print (cnt.values())
