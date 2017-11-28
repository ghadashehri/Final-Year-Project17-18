import json
import numpy as np
import collections
from pprint import pprint
from pathlib import Path


# list of methods called
files_in_dir = []
directory_in_str= 'Samples/'
Binder_methods = []
system_calls= []

def iterateThroughDir(directory):
    files= []
    pathlist= Path(directory).glob('**/*.json')
    for path in pathlist:
        files.append(str(path))
    return files

def readJson(f):
    with open(f) as data_file:
        # takes an actual object as parameter
        data = json.load(data_file)

    # using some of data
    json_data= data["behaviors"]["dynamic"]["host"]
    return json_data

def extractFeature(json_data):
    n = len(json_data)
    for i in range(0,n):
        if(json_data[i]["low"][0]["type"] == 'BINDER'):
            Binder_methods.append(json_data[i]["low"][0]["method_name"])
        # retriving Intent Calls
        elif ( json_data[i]["low"][0]["type"] == 'INTENT' ):
             Binder_methods.append(json_data[i]["low"][0]["intent"])
        # retriving System Calls
        elif(json_data[i]["low"][0]["type"] == 'SYSCALL'):
            for j in range(0,len(json_data[i]["low"])):
                system_calls.append(json_data[i]["low"][j]['sysname'])



files_in_dir= iterateThroughDir(directory_in_str)
for f in range(0,len(files_in_dir)):
    json_data= readJson(files_in_dir[f])
    extractFeature(json_data)

combined = Binder_methods + system_calls
arr = np.array(combined)
unique, counts = np.unique(arr, return_counts=True)
print"\nThe methods Calls in all submited Samples: "
print dict(zip(unique, counts))
print "\n"

# additional Counter   
cnt = collections.Counter()
for word in arr:
    cnt[word] += 1
print "Number of calls made: "
print cnt.values()

