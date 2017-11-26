import json
import numpy as np
#import collections
from pprint import pprint
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
#from sklearn.feature_extraction import CountVectorizer


vec = DictVectorizer()
# list of methods called
files_in_dir = []
directory_in_str= 'Samples/'

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
    Binder_methods = []
    class_ = []
    subClass = []

    n = len(json_data)
    for i in range(0,n):
        m = len(json_data[i]["low"])

        for j in range(0,m):
            if(json_data[i]["low"][j]["type"] == 'BINDER'):
                Binder_methods.append(json_data[i]["low"][j]["method_name"])
                class_.append(json_data[i]["class"])
                subClass.append(json_data[i]["subclass"])

    arr = np.array(Binder_methods)
    unique, counts = np.unique(arr, return_counts=True)
    return dict(zip(unique, counts))


i=0
files_in_dir= iterateThroughDir(directory_in_str)
for f in range(0,len(files_in_dir)):
    json_data= readJson(files_in_dir[f])
    data[i] = np.array(extractFeature(json_data))
    i+=1
print data
    
