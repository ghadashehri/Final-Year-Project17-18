
'''
Created on 1 Dec 2017

@author: Ghadah

    #### DOESNT WORK JUST TO EXPERIMENT  WITH ####
 A class to experiment with existing implementation of DBSCAN implementation
 taken from http://scikit-learn.org/stable/auto_examples/cluster/plot_dbscan.html#sphx-glr-auto-examples-cluster-plot-dbscan-py
'''


import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.datasets.samples_generator import make_blobs
# from sklearn.preprocessing import StandardScaler
from BitVector import getBitVector

data = getBitVector()
values = []
centers = [[1, 1], [-1, -1], [1, -1]]
X, labels_true = make_blobs(n_samples=208, centers=centers)

# Getting only 2 malware families from dataset, ADRD + ANVERSE
for key in data:
    values.append(data[key])
n = np.array(values)
print(n)
# n, labels_true = make_blobs(n_samples=208, centers=centers)

# Compute DBSCAN
db = DBSCAN(eps=.3, min_samples=24).fit(n)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)


# Black removed and is used for noise instead
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()
