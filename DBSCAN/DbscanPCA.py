'''
Created on 23 Mar 2018

@author: Ghadah

In this class we use values from  both PCA_BiGram and PCA_Freq,
to represents our feature set and after each computation, we evaluate
the quality of our algorithm on both models.

Note: parameters are already assigned
'''
from sklearn.cluster import DBSCAN
from sklearn import metrics
import PCA_BiGram
import PCA_Freq
import time


bi_data = PCA_BiGram.returnPCA()
freq_data = PCA_Freq.returnPCA()

bi_labels = PCA_BiGram.returnLabels()
freq_labels = PCA_Freq.returnLabels()

# compute time
start_time = time.time()

# estimate the value of MinPts
minPts = 8

# compute DBSCAN
dbscn = DBSCAN(eps=6.63, min_samples=minPts).fit(bi_data)
labels = dbscn.labels_

freq_dbscn = DBSCAN(eps=1.3, min_samples=minPts).fit(freq_data)
fq_labels = freq_dbscn.labels_

# number of clusters in first model labels
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

# number of clusters in second model labels
freq_n_clusters = len(set(fq_labels)) - (1 if -1 in fq_labels else 0)


# evaluation of first dbscan model (PCA_BiGram)
print('\nDBSCAN Results for Bi-Grams 81 Components: \n')
msg = ('Clustered {:,} points to {:,} clusters, for {:.1f}% compression in '
       '{:,.2f} seconds')

print(msg.format(len(bi_data), n_clusters_,
                 100*(1 - float(n_clusters_) / len(bi_data)),
                 time.time()-start_time))

# Print values of cluster quality measures
print('Accuracy:', metrics.accuracy_score(bi_labels, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(bi_labels, labels))
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(
    bi_data, labels)))
print('\n')
print('Precision: ', metrics.precision_score(bi_labels, labels,
                                             average='micro'))
print('Recall: ', metrics.recall_score(bi_labels, labels, average='micro'))
print('F-Score: ', metrics.f1_score(bi_labels, labels, average='micro'))
print('\n')

print("Homogeneity: %0.3f" % metrics.homogeneity_score(bi_labels, labels))
print("Completeness: %0.3f" % metrics.completeness_score(bi_labels, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(bi_labels, labels))
# print ('\n Confusion Matrix:\n', confusion_matrix(Y, labels))


# evaluation of first dbscan model (PCA_Freq)
print('----------------------------------------------------')
print('\n\nDBSCAN Results for 25 Frequency Components: \n')
msg = ('Clustered {:,} points to {:,} clusters, for {:.1f}% compression in '
       '{:,.2f} seconds')

print(msg.format(len(freq_data), freq_n_clusters,
                 100*(1 - float(freq_n_clusters) / len(freq_data)),
                 time.time()-start_time))
print('Accuracy:', metrics.accuracy_score(freq_labels, fq_labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(freq_labels, fq_labels))
print('Silhouette coefficient: {:0.03f}'.format(metrics.silhouette_score(
    freq_data, fq_labels)))
print('\n')
print('Precision: ', metrics.precision_score(freq_labels, fq_labels,
                                             average='micro'))
print('Recall: ', metrics.recall_score(freq_labels, fq_labels,
                                       average='micro'))
print('F-Score: ', metrics.f1_score(freq_labels, fq_labels, average='micro'))
print('\n')
print("Homogeneity: %0.3f" % metrics.homogeneity_score(freq_labels, fq_labels))
print("Completeness: %0.3f" % metrics.completeness_score(freq_labels,
                                                         fq_labels))
print("V-measure: %0.3f" % metrics.v_measure_score(freq_labels, fq_labels))
# print ('\n Confusion Matrix:\n', confusion_matrix(Y, labels))
