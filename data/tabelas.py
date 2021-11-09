import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

data = pd.read_csv('forms.csv')


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
