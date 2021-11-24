from operator import index
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs
from sklearn.cluster import AffinityPropagation
from sklearn import metrics
from kmodes.kmodes import KModes

from itertools import cycle


data = pd.read_csv("forms.csv")

    
data1=data.loc[data.Gender.isin([ 'Male', 'Masculino'])]
data1=data1.dropna(axis = 1)
data1=data1.replace('Não', 'No')
data1=data1.replace('Sim', 'Yes')
data1=data1.replace('No', '0')
data1=data1.replace('Yes', '1')
data1=data1.replace('Masculino', 'Male')
data1=data1.drop(columns=['Carimbo de data/hora'])
data1=data1.reset_index()
data1=data1.drop(columns=['index'])  
data1=data1.drop(columns=['Gender']) 
data1.to_csv('formsmasculino.csv') 


data2=data.loc[data.Gender.isin([ 'Female', 'Feminino'])]
data2=data2.dropna(axis = 1)
data2=data2.replace('Não', 'No')
data2=data2.replace('Sim', 'Yes')
data2=data2.replace('No', '0')
data2=data2.replace('Yes', '1')
data2=data2.replace('Feminino', 'Female')
data2=data2.drop(columns=['Carimbo de data/hora'])
data2=data2.reset_index()
data2=data2.drop(columns=['index']) 
data2=data2.drop(columns=['Gender'])
data2.to_csv('formsfeminino.csv') 



"""
X, data2 = make_blobs(n_samples=data2.__len__(), cluster_std=0.9, random_state=0)
afprop = AffinityPropagation(max_iter=250)
af = AffinityPropagation(preference=-50, random_state=0).fit(X)
cluster_centers_indices = af.cluster_centers_indices_
labels = af.labels_
n_clusters_ = len(cluster_centers_indices)
"""



km = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)

clusters = km.fit_predict(data2)

# Print the cluster centroids
print(km.cluster_centroids_)
print(clusters)

"""
count=0
for i in labels:
    count= count+1
    
    
print(labels)
print(count)






print("Estimated number of clusters: %d" % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(data2, labels))
print("Completeness: %0.3f" % metrics.completeness_score(data2, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(data2, labels))
print("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(data2, labels))
print(
    "Adjusted Mutual Information: %0.3f"
    % metrics.adjusted_mutual_info_score(data2, labels)
)
print(
    "Silhouette Coefficient: %0.3f"
    % metrics.silhouette_score(X, labels, metric="sqeuclidean")
)
##print("Relevância: %0.3f"
##    % metrics. )

# #############################################################################
# Plot result


plt.close("all")
plt.figure(1)
plt.clf()


colors = cycle("bgrcmykbgrcmyk")
for k, col in zip(range(n_clusters_), colors):
    class_members = labels == k
    cluster_center = X[cluster_centers_indices[k]]
    plt.plot(X[class_members, 0], X[class_members, 1], col + ".")
    plt.plot(
        cluster_center[0],
        cluster_center[1],
        "o",
        markerfacecolor=col,
        markeredgecolor="k",
        markersize=14,
    )
    for x in X[class_members]:
        plt.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col)

plt.title("Estimated number of clusters: %d" % n_clusters_)
plt.show()

"""