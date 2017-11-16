import json
from pprint import pprint

# list of methods called
binder_methods = []

with open('try.json') as data_file:
    # takes an actual object as parameter
    data = json.load(data_file)

# Number of elemnts in host
n = len(data["behaviors"]["dynamic"]["host"])
for i in range(0,n):
    m = len(data["behaviors"]["dynamic"]["host"][i]["low"])
    for j in range(0,m):
        if(data["behaviors"]["dynamic"]["host"][i]["low"][j]["type"] == 'BINDER'):
            binder_methods.append( data["behaviors"]["dynamic"]["host"][i]["low"][j]["method_name"])
print(binder_methods)
    

