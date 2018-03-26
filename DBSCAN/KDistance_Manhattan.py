'''
Created on 24 Mar 2018

@author: Ghadah

This class used the Manhattan Distance as a metric function to compute
Kth nearest neighbours.
The values produced are used in Experiment 3

'''
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from FrequencyVector2 import getFreqVec
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
std_scale = StandardScaler().fit_transform(X)
std_X = std_scale

# value of neighbours
n = 8

# get Nearest Neighbour
nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree',
                        metric='manhattan').fit(std_X)
distances, indices = nbrs.kneighbors(std_X)

# sort distances
desc_distances = sorted(distances[:, n-1], reverse=True)

# plot the KNN distance Graph
with plt.style.context('seaborn-whitegrid'):
    plt.plot(list(range(0, len(desc_distances))), desc_distances, label='KNN')


plt.title("K-distance graph (Using Manhattan Distance)")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()
plt.show()
