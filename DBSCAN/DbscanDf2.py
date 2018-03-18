'''
Created on 9 Mar 2018

@author: Ghadah
'''

import numpy as np
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from BiGrams import getBiGramVec
from sklearn import metrics
from sklearn.metrics import accuracy_score, f1_score, precision_score
from sklearn.metrics import recall_score, confusion_matrix
import pandas as pd
import time
from sklearn.preprocessing.label import LabelEncoder

# Initialise Variables
features = []
labels_list = []
lessthanten = 0

# Get features from Feature Extraction classes
data = getBiGramVec()

encod = LabelEncoder()

# Extract vectors in a list
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)
    if len(element) < 4:
        lessthanten = lessthanten + 1

    for key2 in element:
        val = element.get(key2)
        features.append(val)
        labels_list.append(key)


# Represent data as a matrix
matrix = np.matrix(features)
print('less than ten', lessthanten)

# Standardise Data
#std_scale = StandardScaler().fit_transform(matrix)
# std_matrix = std_scale.transform(matrix)
#matrix = std_scale

# Convert matrix to data frame
dataframe = pd.DataFrame(matrix)
y = encod.fit_transform(labels_list)
dataframe['labels'] = y


# Compute time
start_time = time.time()

X = dataframe.drop('labels', axis=1)
Y = dataframe['labels']

# Estimate the value of MinPts as double number of dimensions ln(1230)= 7.5
minPts = len(X.columns) * 2

# Compute DBSCAN
dbscn = DBSCAN(eps=120, min_samples=10, metric='manhattan').fit(X)
labels = dbscn.labels_

core_samples = np.zeros_like(labels, dtype=bool)
core_samples[dbscn.core_sample_indices_] = True

# Add the predicted labels, and the ground truth
X['clusterID'] = labels
X['labels'] = list(y)

# Compute noise
noise = 0
for label in labels:
    if label == -1:
        noise = noise + 1
print('noise ', noise)

# Number of clusters in labels
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = np.unique(labels)


message = 'Clustered {:,} points to {:,} clusters, for {:.1f}% compression in {:,.2f} seconds'
print(message.format(len(X.index), n_clusters_,
                     100*(1 - float(n_clusters_) / len(X.index)),
                     time.time()-start_time))

# Print values of cluster quality measures
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(
    X, labels)))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(Y, labels))
print("Homogeneity: %0.3f" % metrics.homogeneity_score(Y, labels))
print('Accuracy:', accuracy_score(Y, labels))
print('Precision: ', precision_score(Y, labels, average='macro',
                                     labels=np.unique(labels)))
print('Recall: ', recall_score(Y, labels, average='macro', labels=np.unique(labels)))
print('F-Score: ', f1_score(Y, labels, average='macro', labels=np.unique(labels)))
# print ('\n Confusion Matrix:\n', confusion_matrix(Y, labels))
