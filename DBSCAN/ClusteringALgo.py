'''
Created on 5 Mar 2018

@author: Ghadah
'''
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
from FrequencyVector3 import getFreqVec as frecVec
from sklearn.neighbors import NearestNeighbors
from DBSCAN import PCA as pca
from sklearn.cluster import DBSCAN
import numpy as np


# PCA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Initialise Variables
features = []
feat_labels = []
y = []

# Get data from feature extraction class
data = frecVec()


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
        feat_labels.append(val)
        y.append(i)
    i = i + 1

# Represent data as a matrix
x = np.matrix(features)
x_lab = np.matrix(feat_labels)
x_lab = x_lab[:, -1]


# Standardise Data
std_scale = StandardScaler().fit(x)
std_matrix = std_scale.transform(x)


# code available from https://sebastianraschka.com/Articles/2015_pca_in_3_steps.html
sklearn_pca = sklearnPCA(n_components=2)
matrix = sklearn_pca.fit_transform(std_matrix)
Y_sklearn = matrix

# Add labels to data after standardisation
Y_sklearn = np.insert(Y_sklearn, [Y_sklearn.shape[1]], x_lab, axis=1)


# KDISTANCE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# Represent data as a matrix
X = Y_sklearn
X = X[:, 0:2]

# Compute value of neighbours
n = (2 * X.shape[1]) - 1

# Get Nearest Neighbour
nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)

# Plot the KNN distance Graph
desc_distances = sorted(distances[:, n-1], reverse=True)
plt.plot(list(range(0, len(desc_distances))), desc_distances)

plt.title("K-distance graph")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()
plt.show()


### DBSCAN ###

PCA_matrix = Y_sklearn
PCA_matrix = PCA_matrix[:, 0:2]


# Estimate the value of MinPts as double number of dimensions
minPts = 2*len(PCA_matrix[0])

# Compute DBSCAN
#.18
dbscn = DBSCAN(eps=0.20, min_samples=minPts).fit(PCA_matrix)


labels = dbscn.labels_
core_samples = np.zeros_like(labels, dtype=bool)
core_samples[dbscn.core_sample_indices_] = True

####### PROBLEM WITH ACCURAACY COMPUTATION !!!!!!!!!!!!!!!!!!!!!!!!!!
# Check Accuracy of Algorithm
def get_accuracy(labels):
    acc = 0
    data_labels = pca.returnPCA()

    labels_mat = np.matrix(data_labels)
    labels_mat = labels_mat[:, -1]

    last_pos = labels_mat.shape[1] - 1

    for i in range(0, len(labels)):

        if int(labels_mat[i, last_pos]) == labels[i]:
            acc = acc + 1

    return("DBSCAN ALGORITHM ACCURACY ", (acc/labels_mat.shape[0])*100)


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
colors = plt.cm.RdYlBu(np.linspace(0, 1, len(unique_labels)))

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

