'''
Created on 1 Dec 2017

@author: Ghadah

 A class to experiment with existing implementation of DBSCAN implementation
 taken from http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
'''

from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
#from FrequencyVector import getFrequencyVector
#from BitVector import getBitVector
from FrequencyVector2 import getFreqVec
import numpy as np

# Initialise Variables
features_w_labels = []
features = []

# Get features from Feature Extraction classes
data = getFreqVec()
#data = getBitVector()
#data = getFrequencyVector()


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


# Represent data as a matrix
mat = np.matrix(features)


# Normalise Data
std_scale = StandardScaler().fit(mat)
matrix = std_scale.transform(mat)


# Compute DBSCAN
dbscn = DBSCAN(eps=1.9, min_samples=2).fit(matrix)
# model2 = DBSCAN(eps=1, min_samples=12).fit_predict(matrix, y=None)

labels = dbscn.labels_
core_samples = np.zeros_like(labels, dtype=bool)
core_samples[dbscn.core_sample_indices_] = True


# Check Accuracy of Algorithm
def get_accuracy(labels):
    acc = 0
    matrix_w_labels = np.matrix(features_w_labels)
    last_pos = len(matrix[0])
    for i in range(0, len(labels)):
        if matrix_w_labels[i].item(last_pos) == labels[i]:
            acc = acc + 1
    return("DBSCAN ALGORITHM ACCURACY ", (acc/matrix.shape[0])*100)


accuracy = get_accuracy(labels)
print(accuracy)


# PLOTTTINNNNGGGG DDDDAAATTTTAAAAA #####+++++++++++++++++###############

# Display sample data
for i in range(0, matrix.shape[0]):
    plt.plot(matrix[i, :])
plt.xlabel("X-Axis")
plt.ylabel("Y-Axis")
plt.title("Android Sample Data ")
plt.show()

# Number of clusters in labels
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = np.unique(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

for (label, color) in zip(unique_labels, colors):
    if label == -1:
        # Black used for noise.
        color = [0, 0, 0, 1]
    class_member_mask = (labels == label)
    xy = matrix[class_member_mask & core_samples]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(color),
             markeredgecolor='k', markersize=10)

    xy2 = matrix[class_member_mask & ~core_samples]
    plt.plot(xy2[:, 0], xy2[:, 1], 'o', markerfacecolor=tuple(color),
             markeredgecolor='k', markersize=8)

plt.suptitle("DBSCAN Algorithm")
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.xlabel("X (scaled)")
plt.ylabel("Y (scaled)")

plt.show()
