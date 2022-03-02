import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize
from sklearn.cluster import AgglomerativeClustering
import seaborn               as sns                     # enhanced data viz
import numpy                 as np                      # mathematical essentials
from sklearn.preprocessing   import StandardScaler      # standard scaler
from sklearn.decomposition   import PCA                 # pca
from scipy.cluster.hierarchy import dendrogram, linkage # dendrograms
from sklearn.cluster         import KMeans              # k-means clustering


def cluster_feminino(r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15):
    data2 = pd.read_csv("formsfeminino.csv")
        
    data2=data2.set_axis(['1', '2', '3', '4', '5','6', '7', '8', '9', '10', '11', '12', '13', '14', '15'], axis=1)
    
    newline = {'1': r1, '2': r2,'3': r3,'4': r4,'5': r5,'6': r6,'7': r7,'8': r8,'9': r9,'10': r10, '11': r11, '12': r12,'13': r13,'14': r14,'15': r15}

    data2 = data2.append(newline, ignore_index = True)
    data2=data2.reset_index()
    data2=data2.drop(columns=['index'])
    data2=data2.replace('Não', 'No')
    data2=data2.replace('Sim', 'Yes')
    data2=data2.replace('No', 0)
    data2=data2.replace('Yes', 1)
    data2=data2.replace('no', 0)
    data2=data2.replace('yes', 1)

    data2.to_csv("formsfeminino.csv", index=False)

    data3=pd.DataFrame()
    columnBoho = data2["1"] + data2["2"]+ data2["12"]
    data3["boho"] = columnBoho
    columnCasual = data2["3"] + data2["4"]+ data2["5"]
    data3["casual"] = columnCasual
    columnClassico = data2["6"] + data2["7"]+ data2["8"]
    data3["classic"] = columnClassico
    columnComfy = data2["9"] + data2["10"]+ data2["11"]
    data3["comfy"] = columnComfy
    columnstreetwear = data2["13"] + data2["14"]+ data2["15"]
    data3["streetwear"] = columnstreetwear

    data3
    scaler = StandardScaler()
    datascaled = pd.DataFrame(scaler.fit_transform(data3))
    datascaled.columns = data3.columns
    datascaled
    standard_mergings_ward = linkage(y = datascaled,
                                method = 'ward',
                               optimal_ordering = True)


    # setting plot size
    fig, ax = plt.subplots(figsize=(12, 12))

    # developing a dendrogram
    dendrogram(Z = standard_mergings_ward,
        leaf_rotation = 90,
        leaf_font_size = 6)

  ##  plt.show()
    # INSTANTIATING a k-Means object 
    survey_k_pca = KMeans(n_clusters   = 3,
                        random_state = 219)

    # fitting the object to the data
    survey_k_pca.fit(datascaled)

    # converting the clusters to a DataFrame
    survey_kmeans_pca = pd.DataFrame({'Cluster': survey_k_pca.labels_})

    # checking the results
    print(survey_kmeans_pca.iloc[: , 0].value_counts().sort_index())

    # storing cluster centers
    centroids_pca = survey_k_pca.cluster_centers_


    # converting cluster centers into a DataFrame
    centroids_pca_df = pd.DataFrame(centroids_pca)


    # renaming principal components
    centroids_pca_df.columns = ['boho',                 
                        'casual',      
                        'classic',
                        'comfy',
                        'streetwear']


    # checking results (clusters = rows, pc = columns)
    centroids_pca_df.round(2)
    clst_pca_df = pd.concat([survey_kmeans_pca, data2], axis = 1)

    cluster_names = {0 : centroids_pca_df.idxmax(axis=1).loc[0],
                 1 : centroids_pca_df.idxmax(axis=1).loc[1],
                 2 : centroids_pca_df.idxmax(axis=1).loc[2]}
    #}
    clst_pca_df['Cluster'].replace(cluster_names, inplace = True)


    print(centroids_pca_df)
    print(centroids_pca_df.idxmax(axis=1))

    clst_pca_df
    last_row = clst_pca_df.iloc[-1].tolist()
    return last_row

    ########################

def cluster_masculino(r1,r2,r3,r4,r5,r6,r7,r8,r9,r10,r11,r12,r13,r14,r15):
    data1 = pd.read_csv("formsmasculino.csv") 
    
    data1.to_csv('formsmasculino.csv', index=False) 

    data1=data1.set_axis(['1', '2', '3', '4', '5','6', '7', '8', '9', '10', '11', '12', '13', '14', '15'], axis=1)
    
    newline = {'1': r1, '2': r2,'3': r3,'4': r4,'5': r5,'6': r6,'7': r7,'8': r8,'9': r9,'10': r10, '11': r11, '12': r12,'13': r13,'14': r14,'15': r15}
    data1 = data1.append(newline, ignore_index = True)

    data1=data1.reset_index()
    data1=data1.drop(columns=['index'])
    data1=data1.replace('Não', 'No')
    data1=data1.replace('Sim', 'Yes')
    data1=data1.replace('No', '0')
    data1=data1.replace('Yes', '1')
    data1=data1.replace('Masculino', 'Male')  
    data1.to_csv('formsmasculino.csv', index=False) 


    
    data3=pd.DataFrame()
    columnalterno = data1["1"] + data1["2"]+ data1["3"]
    data3["alterno"] = columnalterno
    columnclassico = data1["4"] + data1["5"]+ data1["6"]
    data3["classic"] = columnclassico
    columndesportivo = data1["7"] + data1["8"]+ data1["9"]
    data3["desportivo"] = columndesportivo
    columnflannel = data1["10"] + data1["11"]+ data1["12"]
    data3["flannel"] = columnflannel
    columnstreetwear = data1["13"] + data1["14"]+ data1["15"]
    data3["streetwear"] = columnstreetwear

    data3
    scaler = StandardScaler()
    datascaled = pd.DataFrame(scaler.fit_transform(data3))
    datascaled.columns = data3.columns
    datascaled
    standard_mergings_ward = linkage(y = datascaled,
                                method = 'ward',
                               optimal_ordering = True)


    # setting plot size
    fig, ax = plt.subplots(figsize=(12, 12))

    # developing a dendrogram
    dendrogram(Z = standard_mergings_ward,
        leaf_rotation = 90,
        leaf_font_size = 6)

  ##  plt.show()
    # INSTANTIATING a k-Means object 
    survey_k_pca = KMeans(n_clusters   = 3, random_state = 219)


    # fitting the object to the data
    survey_k_pca.fit(datascaled)


    # converting the clusters to a DataFrame
    survey_kmeans_pca = pd.DataFrame({'Cluster': survey_k_pca.labels_})
    print(survey_kmeans_pca)
    # checking the results
    print(survey_kmeans_pca.iloc[: , 0].value_counts().sort_index())

    # storing cluster centers
    centroids_pca = survey_k_pca.cluster_centers_


    # converting cluster centers into a DataFrame
    centroids_pca_df = pd.DataFrame(centroids_pca)


    # renaming principal components
    centroids_pca_df.columns = ['alterno',                 
                        'classic',      
                        'desportivo',
                        'flannel',
                        'streetwear']


    # checking results (clusters = rows, pc = columns)
    centroids_pca_df.round(2)
    clst_pca_df = pd.concat([survey_kmeans_pca, data1], axis = 1)


    cluster_names = {0 : centroids_pca_df.idxmax(axis=1).loc[0],
                 1 : centroids_pca_df.idxmax(axis=1).loc[1],
                 2 : centroids_pca_df.idxmax(axis=1).loc[2]}
   # }
    clst_pca_df['Cluster'].replace(cluster_names, inplace = True)

    clst_pca_df

    print(centroids_pca_df)
    print(centroids_pca_df.idxmax(axis=1))
    last_row = clst_pca_df.iloc[-1].tolist()
   
    return last_row