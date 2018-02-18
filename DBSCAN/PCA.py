'''
Created on 13 Jan 2018

@author: Ghadah
'''
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
from FrequencyVector2 import getFreqVec
import numpy as np
from cProfile import label
from matplotlib.pyplot import axis

features = []
labels = []
y = []
data = getFreqVec()

# Extract vectors in a list
i = 0
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        # i value determine a label for each array @ the last position
        val = np.insert(val, len(val), i)
        features.append(val)
        y.append(i)
    i = i + 1

# Represent data as a matrix

x = np.matrix(features)
# y = x[:, len(x[0])]

# Standardise Data
std_scale = StandardScaler().fit(x)
std_matrix = std_scale.transform(x)


# code available from https://sebastianraschka.com/Articles/2015_pca_in_3_steps.html
sklearn_pca = sklearnPCA(n_components=2)
Y_sklearn = sklearn_pca.fit_transform(std_matrix)


print(Y_sklearn)


with plt.style.context('seaborn-whitegrid'):
    plt.figure(figsize=(6, 4))
    for lab, col in zip((1, 2),
                        ('blue', 'green')):

        plt.scatter(Y_sklearn[0:20, 0],
                    Y_sklearn[20:40, 1],
                    label=lab,
                    c=col)
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(loc='lower center')
    plt.tight_layout()
    plt.show()


def returnPCA():
    return Y_sklearn


