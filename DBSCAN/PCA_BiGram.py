'''
Created on 13 Jan 2018

@author: Ghadah

This class reduces the number of dimensions Bi-grams class produce,
It start by normalising data, and then splitting it into features and labels
data frames. We also plot explained variance ratio graph to compute the number
of components needed. From the graph, we concluded that we need 81 components.

returnPCA -> returns the matrix produced
returnLabels -> returns labels assigned to samples
'''
from sklearn.preprocessing.label import LabelEncoder
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
from BiGrams import getBiGramVec
import numpy as np
import pandas as pd

# returns PCA components
def returnPCA():
    return Y_sklearn

# returns labels
def returnLabels():
    return Y


# Initialise Variables
features = []
labels_list = []

# get data from feature extraction class
data = getBiGramVec()
encod = LabelEncoder()

# extract vectors in a list
for key in data:
    # dictionary of fileNames & vectors
    element = data.get(key)

    for key2 in element:
        val = element.get(key2)
        features.append(val)
        labels_list.append(key)

# represent data as a matrix
matrix = np.matrix(features)

# standardise Data
std_scale = StandardScaler().fit_transform(matrix)
matrix = std_scale

# convert matrix to data frame
dataframe = pd.DataFrame(matrix)
y = encod.fit_transform(labels_list)
dataframe['labels'] = y

# split data frame to features and labels
X = dataframe.drop('labels', axis=1)
Y = dataframe['labels']

# code available from
# https://jakevdp.github.io/PythonDataScienceHandbook/05.09-principal-component-analysis.html
# [start]

# number of components needed
pca = sklearnPCA().fit(X)
with plt.style.context('seaborn-whitegrid'):
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('number of components')
plt.ylabel('cumulative explained variance')
plt.title("Explained Variance Ratio")
plt.show()

# [end]

# produce 81 components
sklearn_pca = sklearnPCA(n_components=81)
Y_sklearn = sklearn_pca.fit_transform(X)
