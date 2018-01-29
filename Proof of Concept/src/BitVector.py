'''
Created on 28 Nov 2017
@author: Ghadah
This class aim  to Extract features out of a specified directory,in this case,
a Malware family. By Iterating through samples in each malware family, and
extracting 'BINDER' SYSCALL' and 'INTENT' Saving those calls to list
and forming a bit-vector that represents each sample in the directory, it uses
values 1 if the method is found, and 0 otherwise.
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
bit_vec = {}
directory_in_str = '../../samples'


def distinct_Methods(files):
    dis_meth = []
    for f in range(len(files)):
        with open(files[f]) as data_file:
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

for key in files_in_dir:
    # list of distinct methods
    dis = distinct_Methods(files_in_dir[key])

    for f in range(0, len(files_in_dir[key])):
        json_data = readJson(files_in_dir[key][f])
        extractFeature(json_data)
        combined = Binder_methods + system_calls
        # array of zeros to determine size of vector
        vec = np.zeros(len(dis))
        for i in range(0, len(combined)):
            for j in range(0, len(dis)):
                if(combined[i] == dis[j]):
                    vec[j] = 1
        # Add results to dictionary
        bit_vec.update({files_in_dir[key][f]: vec})
        # Reset lists to empty
        Binder_methods = []
        system_calls = []
    result[key] = bit_vec
    bit_vec = {}

print(result)
print ("\nList of Distinct Methods found: ")
print (dis)


# to access results from other classes
def getBitVector():
    return result
