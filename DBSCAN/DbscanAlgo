'''
Created on 1 Dec 2017

@author: Ghadah

    #### DOESNT WORK JUST TO EXPERIMENT  WITH ####
 A class to experiment with existing implementation of DBSCAN implementation
 taken from http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
'''

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
# from FrequencyVector import getFrequencyVector
from matplotlib import pyplot as plt
from BitVector import getBitVector
import numpy as np

# Initialise Variables
features_w_labels = []
features = []

# Get extracted features from Bitvector class
data = getBitVector()
# data = getFrequencyVector()

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

# print(features)

# Represent data as a matrix
mat = np.matrix(features)

for i in range(0, 1):
    print(mat[i])


# Normalise Data
stscaler = StandardScaler().fit(mat)
matrix = stscaler.transform(mat)
# print(mat)

for i in range(0, 3):
    print(matrix[i])


# Compute DBSCAN
model = DBSCAN(eps=1.5, min_samples=8).fit(matrix)
model2 = DBSCAN(eps=1, min_samples=12).fit_predict(matrix, y=None)
# print(model2)
labels = model.labels_
print(labels)
print('\n\n')
for i in range(0, 3):
    print(labels[i])


# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# unique_labels = set(model.lab)
core = np.zeros_like(model.labels_, dtype=bool)
core[model.core_sample_indices_] = True

unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    #xy = matrix[class_member_mask & core]
    plt.plot(matrix[:, 0], matrix[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = matrix[class_member_mask & ~core]
    plt.plot(matrix[:, 0], matrix[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
#plt.show()


# Check Accuracy of Algorithm
accuracy = 0
matrix_w_labels = np.matrix(features_w_labels)
for i in range(0, len(labels)):
    if matrix_w_labels[i].item(18) == labels[i]:
        accuracy = accuracy + 1
#     else:
#         accuracy = accuracy - 1

print("DBSCAN ALGORITHM ACCURACY ", (accuracy/208)*100)





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
