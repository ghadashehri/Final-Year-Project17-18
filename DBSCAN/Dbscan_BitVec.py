'''
Created on 1 Dec 2017

@author: Ghadah

** OLD VERSION **
 A class to experiment with existing implementation of DBSCAN implementation
 taken from
 http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
 This class uses Bit vectors, as feature set. It assigns all samples into one
 cluster.
 DBSCAN EPS parameters was set randomly. MinPts was set to 2*dimensions
'''
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from BitVector import getBitVec
from sklearn import metrics
import time


# Initialise Variables
features_w_labels = []
features = []

# get features from Feature Extraction classes
data = getBitVec()

# Extract vectors in a list
i = 0
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        features.append(val)
        # i value determine a label for each array @ the last position
        val = np.insert(val, len(val), i)
        # only used for testing
        features_w_labels.append(val)
    i = i + 1

# represent data as a matrix
mat = np.matrix(features)
labels_mat = np.matrix(features_w_labels)
labels_mat = labels_mat[:, -1]

# standardise Data
std_scale = StandardScaler().fit(mat)
std_matrix = std_scale.transform(mat)
matrix = std_matrix


# compute time
start_time = time.time()

# estimate the value of MinPts as double number of dimensions
minPts = 2*len(matrix[0])

# compute DBSCAN
dbscn = DBSCAN(eps=1.1, min_samples=minPts).fit(matrix)

labels = dbscn.labels_
core_samples = np.zeros_like(labels, dtype=bool)
core_samples[dbscn.core_sample_indices_] = True

# number of clusters in labels
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = np.unique(labels)


message = ('Clustered {:,} points to {:,} clusters,for {:.1f}% compression in '
           '{:,.2f} seconds')
print(message.format(len(matrix), n_clusters_,
                     100*(1 - float(n_clusters_) / len(matrix)),
                     time.time()-start_time))
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(
    matrix, labels)))
