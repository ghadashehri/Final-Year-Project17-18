import json
import numpy as np
from pprint import pprint
from pathlib import Path


def distinct_Methods(files):
    dis_meth=[]
    for f in range(len(files)):
        with open(files_in_dir[f]) as data_file:
        # takes an actual object as parameter
            data = json.load(data_file)
        json_data= data["behaviors"]["dynamic"]["host"]
        n = len(json_data)

        for i in range(0,n):
            # retriving the Binder Calls
            value = json_data[i]["low"][0]["type"]
            if( value == 'BINDER' and  json_data[i]["low"][0]["method_name"] not in dis_meth ):
                dis_meth.append(json_data[i]["low"][0]["method_name"])

            # retriving Intent Calls
            elif ( value == 'INTENT' and  json_data[i]["low"][0]["intent"] not in dis_meth):
                dis_meth.append(json_data[i]["low"][0]["intent"])

            # retriving System Calls
            elif(value == 'SYSCALL' and  json_data[i]["low"][0]['sysname'] not in dis_meth):
                for j in range(0,len(json_data[i]["low"])):
                    dis_meth.append(json_data[i]["low"][j]['sysname'])
    return dis_meth



# Initialising Variabels
Binder_methods = []
files_in_dir = []
system_calls= []
frequency = {}
directory_in_str= 'Samples/ADRD_genome_stimulated'


# Adding files in directory to a list
pathlist= Path(directory_in_str).glob('**/*.json')
for path in pathlist:
    files_in_dir.append(str(path))

    dis=distinct_Methods(files_in_dir)


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

        # retriving Intent Calls
        elif ( json_data[i]["low"][0]["type"] == 'INTENT' ):
             Binder_methods.append(json_data[i]["low"][0]["intent"])
        # retriving System Calls
        elif(json_data[i]["low"][0]["type"] == 'SYSCALL'):
            for j in range(0,len(json_data[i]["low"])):
                system_calls.append(json_data[i]["low"][j]['sysname'])

    combined = Binder_methods + system_calls
    count = np.zeros(len(dis))
    for i in range(0,len(combined)):
        for j in range(0,len(dis)):
            if(combined[i] == dis[j]):
                count[j]+=1
    frequency = {files_in_dir[f]:count}
    # Reset lists to empty
    Binder_methods = []
    system_calls = []
    print frequency

print "\nList of Distinct Methods found: "    
print dis









