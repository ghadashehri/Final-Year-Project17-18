'''
Created on 13 Jan 2018

@author: Ghadah
'''
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
from FrequencyVector2 import getFreqVec as frecVec
import numpy as np


def returnPCA():
    return Y_sklearn


def returnLabels():
    return y


# Initialise Variables
features = []
feat_labels = []
y = []
data = frecVec()


# Extract vectors in a list
i = 1
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

print(Y_sklearn)

with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(6, 4))

    plt.scatter(Y_sklearn[:, 0],
                Y_sklearn[:, 1],
                c='black',
                alpha=0.5,
                )
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(loc=0)
    plt.tight_layout()
    plt.show()
