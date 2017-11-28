
import unittest
import json
from pathlib import Path
from Read_Json import iterateThroughDir,readJson,extractFeature

Binder_methods = []
system_calls = []
class Test_Read_Json(unittest.TestCase):

    def test_iterateThroughDir(self):
        files =[] 
        directory = 'Samples/'
        pathlist= Path(directory).glob('**/*.json')
        for path in pathlist:
            files.append(str(path))
        method_files = iterateThroughDir(directory)
        # Testing the method used in class
        self.assertEqual(method_files, files)

    def test_readJson(self):
        f = 'try.json'
        with open(f) as data_file:
            data = json.load(data_file)
            method_data =  readJson(f)

        data = data["behaviors"]["dynamic"]["host"]
        # Check thats the correct file is read
        self.assertEqual(method_data,data)

        # Check that readJson fails when the passed varible is file, not string.
        with self.assertRaises(TypeError):
            readJson(data_file)
            
            
    def test_extractFeature(self):
        methods = []
        f = 'try.json'
        with open(f) as data_file:
            data = json.load(data_file)
        data = data["behaviors"]["dynamic"]["host"]
        n = len(data)
        for i in range(0,n):
            if ( data[i]["low"][0]["type"] == 'INTENT' ):
                Binder_methods.append(data[i]["low"][0]["intent"])
        extractFeature(data)
        self.assertEqual(Binder_methods, methods)

'''    def test_extractBinder(self):
        methods = []
        f = 'try.json'
        with open(f) as data_file:
            data = json.load(data_file)
        data = data["behaviors"]["dynamic"]["host"]

        n = len(data)
        for i in range(0,n):
            if(data[i]["low"][0]["type"] == 'BINDER'):
                methods.append(data[i]["low"][0]["method_name"])
        extractFeature(data)
        self.assertEqual(Binder_methods, methods)'''



'''    def test_extractSysCall(self):
        sys = []
        f = 'try.json'
        with open(f) as data_file:
            data = json.load(data_file)
        data = data["behaviors"]["dynamic"]["host"]
        n = len(data)
        for i in range(0,n):
            if(data[i]["low"][0]["type"] == 'SYSCALL'):
                for j in range(0,len(data[i]["low"])):
                    sys.append(data[i]["low"][j]['sysname'])
        extractFeature(data)
        self.assertEqual(system_calls,sys)    '''

if __name__ == '__main__':
    unittest.main()
