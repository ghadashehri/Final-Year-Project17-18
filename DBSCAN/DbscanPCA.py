'''
Created on 18 Feb 2018

@author: Ghadah
'''
from sklearn.cluster import DBSCAN
from matplotlib import pyplot as plt
from DBSCAN import PCA as pca
import numpy as np


PCA_matrix = pca.returnPCA()

# Estimate the value of MinPts as double number of dimensions
minPts = 2*len(PCA_matrix[0])

# Compute DBSCAN
dbscn = DBSCAN(eps=.26, min_samples=minPts).fit(PCA_matrix)


labels = dbscn.labels_
core_samples = np.zeros_like(labels, dtype=bool)
core_samples[dbscn.core_sample_indices_] = True


# Check Accuracy of Algorithm
def get_accuracy(labels):
    acc = 0
    data_labels = pca.returnLabels()

    for i in range(0, len(labels)):
        # print("     ", data_labels[i], labels[i])
        if data_labels[i] == labels[i]:
            acc = acc + 1
    n = len(data_labels)
    return("DBSCAN ALGORITHM ACCURACY ", (acc/n)*100)


accuracy = get_accuracy(labels)
print('\n\n')
print(accuracy)


# PLOTTTINNNNGGGG DDDDAAATTTTAAAAA #####+++++++++++++++++###############

# Display sample data
for i in range(0, PCA_matrix.shape[0]):
    plt.plot(PCA_matrix[i, :])
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
    xy = PCA_matrix[class_member_mask & core_samples]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(color),
             markeredgecolor='k', markersize=10)

    xy2 = PCA_matrix[class_member_mask & ~core_samples]
    plt.plot(xy2[:, 0], xy2[:, 1], 'o', markerfacecolor=tuple(color),
             markeredgecolor='k', markersize=6)

plt.suptitle("DBSCAN Algorithm")
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.xlabel("X (scaled)")
plt.ylabel("Y (scaled)")
plt.show()
