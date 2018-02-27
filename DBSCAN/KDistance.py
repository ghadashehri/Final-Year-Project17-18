'''
Created on 13 Feb 2018

@author: Ghadah
'''
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import numpy as np
import FrequencyVector3 as freqVec
from matplotlib import pyplot as plt

# Initialise variables
features = []
data = freqVec.getFreqVec()

# Extract vectors in a list
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        features.append(val)


# Represent data as a matrix
X = np.matrix(features)

# Standardise Data
std_scale = StandardScaler().fit(X)
std_X = std_scale.transform(X)


# Compute value of neighbours
n = (2 * X.shape[1]) - 1

# Get Nearest Neighbour
nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(std_X)
distances, indices = nbrs.kneighbors(std_X)

# Plot the KNN distance Graph
desc_distances = sorted(distances[:,n-1], reverse=True)
plt.plot(list(range(0,len(desc_distances))), desc_distances)


# distances.sort(0)
# desc_distances = distances[::-1]

# for i in range(0, len(desc_distances)):
# plt.scatter(i, desc_distances[i][n-1])
# plt.plot( desc_distances[i][n-1],i, 'o','blue',  alpha=0.5, ms=6)

plt.title("K-distance graph")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()
plt.show()
