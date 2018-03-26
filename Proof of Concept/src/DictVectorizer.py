'''
Created on 7 Mar 2018

@author: Ghadah

This class uses Scikit-learn library for feature extraction, it produces a
pandas data frame of each sample information, along with its label.

Note: use on a small dataset.

'''
import json
import os
import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer


# Initialising Variables
Binder_methods = []
files_in_dir = []
system_calls = []

combined = []
method_list = []
labels_list = []

directory_in_str = '../../samples'


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
            Binder_methods.append(json_data[i]["low"][0]["method_name"])

        # retrieving Intent Calls
        elif (json_data[i]["low"][0]["type"] == 'INTENT'):
            Binder_methods.append(json_data[i]["low"][0]["intent"])

        # retrieving System Calls
        elif(json_data[i]["low"][0]["type"] == 'SYSCALL'):
            for j in range(0, len(json_data[i]["low"])):
                Binder_methods.append(json_data[i]["low"][j]['sysname'])


# list Files in directory
files_in_dir = iterateThroughDir(directory_in_str)
# result = files_in_dir.copy()

vectorizer = CountVectorizer()
labelEnc = LabelEncoder()


# Initialise data set
for key in files_in_dir:
    for f in range(0, len(files_in_dir[key])):

        json_data = readJson(files_in_dir[key][f])
        extractFeature(json_data)

        # sanitise system calls
        for s in range(0, len(system_calls)):
            system_calls[s] = system_calls[s].replace(" ", "_")

        combined = Binder_methods + system_calls
        labels_list.append(key)

        # remove dots from all entries (sanitise)
        for i in range(0, len(combined)):
            combined[i] = combined[i].replace(".", "_")

        method_list.append((' '.join(combined[:])))
        combined = []


X = vectorizer.fit_transform(method_list)
print('List of Distinct Methods: \n', vectorizer.get_feature_names())

y = labelEnc.fit_transform(labels_list)

samples = pd.DataFrame(X.toarray())
samples['labels'] = y

print('\n\nFeature Set: \n', samples)
