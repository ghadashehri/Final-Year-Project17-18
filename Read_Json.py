import json
import numpy as np
import collections
from pprint import pprint
from pathlib import Path
from sklearn.feature_extraction import DictVectorizer
#from sklearn.feature_extraction import CountVectorizer


vec = DictVectorizer()

# Initialising Variabels
Binder_methods = []
class_ = []
subClass = []
files_in_dir = []
system_calls= []
directory_in_str= 'Samples/'

# Adding files in directory to a list
pathlist= Path(directory_in_str).glob('**/*.json')
for path in pathlist:
    files_in_dir.append(str(path))

# Looping through Samples of each malware family
for f in range(0,len(files_in_dir)):
    with open(files_in_dir[f]) as data_file:
        # takes an actual object as parameter
        data = json.load(data_file)


    # using some of data
    json_data= data["behaviors"]["dynamic"]["host"]
    n = len(json_data)

    for i in range(0,n):
        # retriving the Binder Calls
        if(json_data[i]["low"][0]["type"] == 'BINDER'):
            Binder_methods.append(json_data[i]["low"][0]["method_name"])
            class_.append(json_data[i]["class"])
            subClass.append(json_data[i]["subclass"])
        # retriving Intent Calls
        elif ( json_data[i]["low"][0]["type"] == 'INTENT' ):
             Binder_methods.append(json_data[i]["low"][0]["intent"])
        # retriving System Calls
        elif(json_data[i]["low"][0]["type"] == 'SYSCALL'):
            for j in range(0,len(json_data[i]["low"])):
                system_calls.append(json_data[i]["low"][j]['sysname'])

# Adding both lists together
joined_list= Binder_methods + system_calls
arr = np.array(joined_list)
# Counting the number of times each method/syscall is repeated
unique, counts = np.unique(arr, return_counts=True)
print dict(zip(unique, counts))
    
# additional Counter   
cnt = collections.Counter()
for word in arr:
    cnt[word] += 1
print cnt.values()

