import json
from pprint import pprint
from pathlib import Path

# list of methods called
Binder_methods = []

directory_in_str= 'Samples/'
pathlist = Path(directory_in_str).glob('**/*.json')
for path in pathlist:
    # because path is object not string
    path_in_str = str(path)
    # print(path_in_str)

with open(path_in_str) as data_file:
    # takes an actual object as parameter
    data = json.load(data_file)

# Number of elemnts in host
n = len(data["behaviors"]["dynamic"]["host"])
for i in range(0,n):
    m = len(data["behaviors"]["dynamic"]["host"][i]["low"])
    for j in range(0,m):
        if(data["behaviors"]["dynamic"]["host"][i]["low"][j]["type"] == 'BINDER'):
            Binder_methods.append( data["behaviors"]["dynamic"]["host"][i]["low"][j]["method_name"])
print(Binder_methods)
