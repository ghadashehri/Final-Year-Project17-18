'''
Created on 28 Mar 2018

@author: Ghadah

This class is used to plot the scores we obtained from
using different values of epsilon parameter, on frequency vector
feature set. It plots the homogeneity, completeness, and v-measure
values, depending on the Epsilon value.It also, plots precision,
recall and F-measure using the same procedure. And finally it plots the
Silhouette Coefficient, that corresponds to each epsilon value, and the
number of clusters associated with it.

NOTE: values are already assigned
'''
from sklearn.preprocessing.label import LabelEncoder
from sklearn.preprocessing import StandardScaler
from FrequencyVector2 import getFreqVec
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn import metrics
import pandas as pd
import numpy as np
import time

# from BiGrams import getBiGramVec
# initialise variables
features = []
labels_list = []

# get features from Feature Extraction classes
data = getFreqVec()
# data = getBiGramVec()

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


# convert matrix to data frame
dataframe = pd.DataFrame(std_scale)
y = encod.fit_transform(labels_list)
dataframe['labels'] = y


# Compute time
start_time = time.time()

X = dataframe.drop('labels', axis=1)
Y = dataframe['labels']

minPts = 8

# Getting data for plot method
hcv = []
prf = []
n_clust = []
silh = []
eps = []
epsilon = 0.1

for i in range(0, 30):

    eps.append(epsilon)
    model = DBSCAN(eps=epsilon, min_samples=8).fit(X)
    epsilon = epsilon + 0.5

    # add values to lists
    hcv.append(metrics.homogeneity_completeness_v_measure(Y, model.labels_))
    prf.append(metrics.precision_recall_fscore_support(Y, model.labels_,
                                                       average='micro'))
    n_clust.append(len(set(model.labels_)) -
                   (1 if -1 in model.labels_ else 0))
    silh.append(metrics.silhouette_score(X, model.labels_))


# plotting Homogeneity/Completeness/V measure graph
with plt.style.context('seaborn-whitegrid'):
    plt.subplot(211)
    plt.plot(eps, [x[0] for x in hcv], label='Homogeneity', ls='-.')
    plt.plot(eps, [x[1] for x in hcv], label='Completeness', ls='--')
    plt.plot(eps, [x[2] for x in hcv], label='V-Measure', ls=':')

plt.title('Homogeneity, Completeness, V-measure Graph')
plt.ylabel('Metric Score')
plt.xlim()
plt.ylim(0, 1)
plt.legend()


# plotting Precision, Recall, F-measure graph
with plt.style.context('seaborn-whitegrid'):
    plt.subplot(212)

    plt.plot(eps, [x[0] for x in prf], label='Precision', ls='-.')
    plt.plot(eps, [x[1] for x in prf], label='Recall', ls='--')
    plt.plot(eps, [x[2] for x in prf], label='F-Measure', ls=':')
plt.title('Precision, Recall, F-measure Graph')
plt.xlabel('Number of Clusters')
plt.ylabel('Metric Score')
plt.xlim()
plt.ylim(0, 1)
plt.legend()
plt.show()

# plotting the silhouette cof. score
fig, ax1 = plt.subplots()
ax1.set_xlabel('Epsilon Value')
ax1.set_ylabel('Silhouette Coefficient Score')
ax1.plot(eps, silh, label='Silhouette cof.', c='r', ls='--')
ax1.legend(loc=2)
with plt.style.context('seaborn-whitegrid'):
    ax2 = ax1.twinx()
    ax2.set_ylabel('Number of Clusters')
    ax2.plot(eps, n_clust, c='g', ls=':', label='number of clusters')
plt.title('Silhouette Coefficient Measure Graph')
fig.tight_layout()
plt.legend()
plt.show()
