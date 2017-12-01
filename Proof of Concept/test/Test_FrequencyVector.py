'''
Created on 28 Nov 2017

@author: Ghadah
'''
import unittest
import json
from pathlib import Path
from FrequencyVector import iterateThroughDir, readJson, extractFeature

Binder_methods = []
system_calls = []


class Test_FrequencyVector(unittest.TestCase):

    def test_iterateThroughDir(self):
        files = []
        directory = '../../samples/'
        pathlist = Path(directory).glob('**/*.json')
        for path in pathlist:
            files.append(str(path))
        method_files = iterateThroughDir(directory)
        # Testing the method used in class
        self.assertEqual(method_files, files)

    def test_readJson(self):
        f = 'try.json'
        with open(f) as data_file:
            data = json.load(data_file)
            method_data = readJson(f)

        data = data["behaviors"]["dynamic"]["host"]
        # Check thats the correct file is read
        self.assertEqual(method_data, data)

        # Check that readJson fails when the passed variable is file not string
        with self.assertRaises(TypeError):
            readJson(data_file)

    def test_extractFeature(self):
        methods = []
        f = 'try.json'
        with open(f) as data_file:
            data = json.load(data_file)
        data = data["behaviors"]["dynamic"]["host"]
        n = len(data)
        for i in range(0, n):
            if (data[i]["low"][0]["type"] == 'INTENT'):
                Binder_methods.append(data[i]["low"][0]["intent"])
        extractFeature(data)
        self.assertEqual(Binder_methods, methods)


if __name__ == "__main__":
    unittest.main()
