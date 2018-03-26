'''
Created on 24 Mar 2018

@author: Ghadah

This class performs DBSCAN on feature set produced by Frequency Vector
class. It performs clustering on Normalised data and by using Manhattan
distance function. Then we evaluated the quality of our clsuters

Note: parameters are already assigned
'''

from sklearn.preprocessing.label import LabelEncoder
from sklearn.preprocessing import StandardScaler
from FrequencyVector2 import getFreqVec
from sklearn.cluster import DBSCAN
from sklearn import metrics
import pandas as pd
import numpy as np
import time


# Initialise Variables
features = []
labels_list = []

# get features from Feature Extraction classes
data = getFreqVec()
encod = LabelEncoder()

# extract vectors in a list
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        features.append(val)
        labels_list.append(key)


# represent data as a matrix
mat = np.matrix(features)

# standardise data
matrix = StandardScaler().fit_transform(mat)


# convert matrix to data frame
dataframe = pd.DataFrame(matrix)
y = encod.fit_transform(labels_list)
dataframe['labels'] = y


# compute time
start_time = time.time()

# split data and labels
X = dataframe.drop('labels', axis=1)
Y = dataframe['labels']

# estimate the value of MinPts
minPts = 8

# compute DBSCAN
dbscn = DBSCAN(eps=4, min_samples=minPts, metric='manhattan').fit(X)
labels = dbscn.labels_


# number of clusters in  model labels
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# evaluation of dbscan model (using Manhattan distance)
print('\nDBSCAN results for Original data: \n')
msg = ('Clustered {:,} points to {:,} clusters, for {:.1f}% compression in '
       '{:,.2f} seconds')

print(msg.format(len(X.index), n_clusters_,
                 100*(1 - float(n_clusters_) / len(X.index)),
                 time.time()-start_time))

# Print values of cluster quality measures
print('Accuracy:', metrics.accuracy_score(Y, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(Y, labels))
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(
    X, labels)))
print('\n')
print('Precision: ', metrics.precision_score(Y, labels, average='micro'))
print('Recall: ', metrics.recall_score(Y, labels, average='micro'))
print('F-Score: ', metrics.f1_score(Y, labels, average='micro'))
print('\n')

print("Homogeneity: %0.3f" % metrics.homogeneity_score(Y, labels))
print("Completeness: %0.3f" % metrics.completeness_score(Y, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(Y, labels))
# print ('\n Confusion Matrix:\n', confusion_matrix(Y, labels))
