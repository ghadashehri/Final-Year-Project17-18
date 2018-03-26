'''
Created on 9 Mar 2018

@author: Ghadah

In this class we use the frequency vectors, to represent our feature set.
It starts by splitting up feature set to vectors and labels, then we estimate
value of Eps, using plot produced byKDistance_Freq class. We run the algorithm
on both non-normalised and normalised data, and after each computation, we
evaluate the quality of our algorithm.

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

# Get features from Feature Extraction classes
data = getFreqVec()
encod = LabelEncoder()

# Extract vectors in a list
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        features.append(val)
        labels_list.append(key)


# represent data as a matrix
matrix = np.matrix(features)

# standardise data
std_mat = StandardScaler().fit_transform(matrix)


# convert matrix to data frame
dataframe = pd.DataFrame(matrix)
y = encod.fit_transform(labels_list)
dataframe['labels'] = y

std_dataframe = pd.DataFrame(std_mat)
std_dataframe['labels'] = y


# Compute time
start_time = time.time()

X = dataframe.drop('labels', axis=1)
std_X = std_dataframe.drop('labels', axis=1)

Y = dataframe['labels']

# estimate the value of MinPts
minPts = 8

# compute DBSCAN
dbscn = DBSCAN(eps=6.89, min_samples=minPts).fit(X)
labels = dbscn.labels_

std_dbscn = DBSCAN(eps=1.15, min_samples=minPts).fit(std_X)
std_labels = std_dbscn.labels_

# number of clusters in first model labels
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = np.unique(labels)

# number of clusters in second model labels
std_n_clusters = len(set(std_labels)) - (1 if -1 in std_labels else 0)


# evaluation of first dbscan model (non normalised data)
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


# evaluation of first dbscan model (normalised data)
print('----------------------------------------------------')
print('\n\nDBSCAN results for Normalised data: \n')
msg = ('Clustered {:,} points to {:,} clusters, for {:.1f}% compression in '
       '{:,.2f} seconds')

print(msg.format(len(std_X.index), std_n_clusters,
                 100*(1 - float(std_n_clusters) / len(std_X.index)),
                 time.time()-start_time))
print('Accuracy:', metrics.accuracy_score(Y, std_labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(Y, std_labels))
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(
    std_X, std_labels)))
print('\n')
print('Precision: ', metrics.precision_score(Y, std_labels, average='micro'))
print('Recall: ', metrics.recall_score(Y, std_labels, average='micro'))
print('F-Score: ', metrics.f1_score(Y, std_labels, average='micro'))
print('\n')
print("Homogeneity: %0.3f" % metrics.homogeneity_score(Y, std_labels))
print("Completeness: %0.3f" % metrics.completeness_score(Y, std_labels))
print("V-measure: %0.3f" % metrics.v_measure_score(Y, std_labels))
# print ('\n Confusion Matrix:\n', confusion_matrix(Y, labels))
