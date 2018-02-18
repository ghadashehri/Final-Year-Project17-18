'''
Created on 18 Feb 2018

@author: Ghadah
'''

from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from DBSCAN import PCA as pca

# Represent data as a matrix
X = pca.returnPCA()


# Compute value of neighbours
n = (2 * X.shape[1]) - 1

# Get Nearest Neighbour
nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)

distances.sort(0)
print(distances.shape)
desc_distances = distances[::-1]


# Plot the KNN distance Graph
for i in range(0, len(desc_distances)):
    # plt.scatter(i, desc_distances[i][n-1])
    plt.plot(desc_distances[i][n-1], i, 'o', 'blue',  alpha=0.5, ms=6)

plt.suptitle("K-distance graph")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()
plt.show()
