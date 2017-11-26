import json
import numpy as np
import collections
from pprint import pprint
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer

# list of methods called
Binder_methods = []
class_ = []
subClass = []
files_in_dir = []

directory_in_str= 'Samples/'
vec = DictVectorizer()

pathlist= Path(directory_in_str).glob('**/*.json')
for path in pathlist:
    files_in_dir.append(str(path))

for f in range(0,len(files_in_dir)):

    with open(files_in_dir[f]) as data_file:
        # takes an actual object as parameter
        data = json.load(data_file)


        # using some of data
        json_data= data["behaviors"]["dynamic"]["host"]

    n = len(json_data)
    
    for i in range(0,n):
        m = len(json_data[i]["low"])

        for j in range(0,m):
            if(json_data[i]["low"][j]["type"] == 'BINDER'):
                Binder_methods.append(json_data[i]["low"][j]["method_name"])
                class_.append(json_data[i]["class"])
                subClass.append(json_data[i]["subclass"])
              
# Change list to array
arr = np.array(Binder_methods)

# Using a counter to determine the occurance of each method
cnt = collections.Counter()
for word in arr:
    cnt[word] += 1
print cnt.values()

