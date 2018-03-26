'''
Created on 13 Feb 2018

@author: Ghadah

By computing distance to the Kth nearest neighbour, we can find the range of
possible values, for DBSCAN epsilon parameter. This class works with frequency
vector class, it also normalises data before computing the distances.

Note: we used this class with and without normalising values
'''
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from FrequencyVector2 import getFreqVec
from matplotlib import pyplot as plt
import numpy as np

# Initialise variables
features = []
data = getFreqVec()

# Extract vectors in a list
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        features.append(val)


# represent data as a matrix
X = np.matrix(features)

# standardise Data
std_X = StandardScaler().fit_transform(X)

# number of neighbours
n = 8

# compute Nearest Neighbour (not normalised)
nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)

# compute Nearest Neighbour (normalised)
nbrs2 = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(std_X)
std_distances, std_indices = nbrs2.kneighbors(std_X)


# sort distances
desc_distances = sorted(distances[:, n-1], reverse=True)
std_desc_distances = sorted(std_distances[:, n-1], reverse=True)

# plot data
with plt.style.context('seaborn-whitegrid'):
    plt.subplot(211)
    plt.plot(list(range(0, len(desc_distances))), desc_distances, label='KNN')
plt.title("K-distance graph (not Normalised)")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()

# second plot
with plt.style.context('seaborn-whitegrid'):
    plt.subplot(212)
    plt.plot(list(range(0, len(std_desc_distances))), std_desc_distances,
             label='KNN', c='r')
plt.title("K-distance graph (Normalised)")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()

plt.show()
