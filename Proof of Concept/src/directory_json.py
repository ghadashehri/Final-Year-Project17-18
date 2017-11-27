import json
from pprint import pprint
from pathlib import Path

# list of methods called
Binder_methods = []
files_in_dir = []
directory_in_str= 'Samples/'

#https://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory


pathlist= Path(directory_in_str).glob('**/*.json')
for path in pathlist:
    files_in_dir.append(str(path))

for f in range(0,len(files_in_dir)):
    with open(files_in_dir[f]) as data_file:
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
