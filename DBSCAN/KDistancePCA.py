'''
Created on 13 Feb 2018

@author: Ghadah

By computing distance to the Kth nearest neighbour, we can find the range of
possible values, for DBSCAN epsilon parameter. This class uses values produced
by PCA_Freq and PCA_BiGram, to plot the graphs.

Note: we used this class with both frequency vectors and Bi-grams
'''
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import PCA_BiGram
import PCA_Freq


# get PCA data
pca_bi = PCA_BiGram.returnPCA()
pca_freq = PCA_Freq.returnPCA()

# number of neighbours
n = 8

# compute Nearest Neighbour (Bi-Grams)
nbrs = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(pca_bi)
distances, indices = nbrs.kneighbors(pca_bi)

# compute Nearest Neighbour (Frequency)
nbrs2 = NearestNeighbors(n_neighbors=n, algorithm='ball_tree').fit(pca_freq)
freq_distances, freq_indices = nbrs2.kneighbors(pca_freq)


# sort distances
desc_distances = sorted(distances[:, n-1], reverse=True)
freq_desc_distances = sorted(freq_distances[:, n-1], reverse=True)

# plot data
with plt.style.context('seaborn-whitegrid'):
    plt.subplot(211)
    plt.plot(list(range(0, len(desc_distances))), desc_distances, label='KNN')
plt.title("K-distance graph (Bi-Grams)")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()

# second plot
with plt.style.context('seaborn-whitegrid'):
    plt.subplot(212)
    plt.plot(list(range(0, len(freq_desc_distances))), freq_desc_distances,
             label='KNN', c='r')
plt.title("K-distance graph (Frequency)")
plt.xlabel("Points in Descending Order (Eps value)")
plt.ylabel(" KNN distance")
plt.legend()
plt.tight_layout()

plt.show()
