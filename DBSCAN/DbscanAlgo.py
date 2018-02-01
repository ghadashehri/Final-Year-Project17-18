'''
Created on 1 Dec 2017

@author: Ghadah

 A class to experiment with existing implementation of DBSCAN implementation
 taken from http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
'''

from sklearn.cluster import DBSCAN
#from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from FrequencyVector import getFrequencyVector
from matplotlib import pyplot as plt
from BitVector import getBitVector
#from notInc import Bitv
import numpy as np

# Initialise Variables
features_w_labels = []
features = []

# Get extracted features from Bitvector class
#data = Bitv.getBitV()
#data = getBitVector()
data = getFrequencyVector()


# Extract vectors in a list
i = 0
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        features.append(val)
        # i value determine a label for each array @ 18th position
        val = np.insert(val, len(val), i)
        features_w_labels.append(val)
    i = i + 1


# Represent data as a matrix
mat = np.matrix(features)

for i in range(0, 1):
    print(mat[i])


# Normalise Data
stscaler = StandardScaler().fit(mat)
matrix = stscaler.transform(mat)

for i in range(0, 30):
    print(matrix[i])


# Compute DBSCAN
dbscn = DBSCAN(eps=3.8, min_samples=25).fit(matrix)
#model2 = DBSCAN(eps=1, min_samples=12).fit_predict(matrix, y=None)
labels = dbscn.labels_
core_samples = np.zeros_like(labels, dtype=bool)
core_samples[dbscn.core_sample_indices_] = True


print(labels)
print('\n\n')

for i in range(0, 3):
    print(labels[i])


# Check Accuracy of Algorithm
def get_accuracy(labels):
    acc = 0
    matrix_w_labels = np.matrix(features_w_labels)
    for i in range(0, len(labels)):
        if matrix_w_labels[i].item(18) == labels[i]:
            acc = acc + 1
    return("DBSCAN ALGORITHM ACCURACY ", (acc/208)*100)


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

n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = np.unique(labels)
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))

for (label, color) in zip(unique_labels, colors):
    class_member_mask = (labels == label)
    xy = matrix[class_member_mask & core_samples]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=color, markersize=14)

    xy2 = matrix[class_member_mask & ~core_samples]
    plt.plot(xy2[:, 0], xy2[:, 1], 'o', markerfacecolor=color, markersize=6)
plt.title("DBSCAN on Clustered data")
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.xlabel("X (scaled)")
plt.ylabel("Y (scaled)")
plt.show()


# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# # unique_labels = set(model.lab)
# 
# 
# unique_labels = set(labels)
# colors = [plt.cm.Spectral(each)
#           for each in np.linspace(0, 1, len(unique_labels))]
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = [0, 0, 0, 1]
# 
#     class_member_mask = (labels == k)
# 
#     #xy = matrix[class_member_mask & core]
#     plt.plot(matrix[:, 0], matrix[:, 1], 'o', markerfacecolor=tuple(col),
#              markeredgecolor='k', markersize=14)
# 
#     xy = matrix[class_member_mask & ~core]
#     plt.plot(matrix[:, 0], matrix[:, 1], 'o', markerfacecolor=tuple(col),
#              markeredgecolor='k', markersize=6)
# 
# plt.title('Estimated number of clusters: %d' % n_clusters_)
# #plt.show()



# for i in range(0, matrix.shape[0]):
#     if labels[i] == 0:
#         plt.plot(matrix[i, :], matrix[:, i], c='r', marker='+')
#     elif labels[i] == 1:
#         plt.plot(matrix[:, i], matrix[i, :], c='g', marker='o')
#     elif labels[i] == -1:
#         plt.plot(matrix[:, i], matrix[i, :], c='b', marker='*')
# # plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2', 'Noise'])
# plt.title('Estimated Number of Clusters: % d' % n_clusters_)
# plt.show()
