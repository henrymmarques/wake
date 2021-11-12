import numpy as np
import pandas as pd


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
data2.to_csv('formsfeminino.csv') 

data2=data2.replace('No', 0)
data2=data2.replace('Yes',1)
data2




kmeans = KMeans(n_clusters=4)

y = kmeans.fit_predict(data2[['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4', 'Unnamed: 5','Unnamed: 6','Unnamed: 7','Unnamed: 8','Unnamed: 9','Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14','Unnamed: 15','Unnamed: 16']])

data2['Cluster'] = y

data2