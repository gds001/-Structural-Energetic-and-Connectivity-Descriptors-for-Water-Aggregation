import pandas as pd
import numpy as np
import sklearn.decomposition as dcomp
import matplotlib.pyplot as plt
import matplotlib as mpl
import sklearn.preprocessing as pp
import random
np.set_printoptions(suppress=True,precision=2)

df=pd.read_pickle("../DataFrame.pkl")
print(df.keys())
whattolookat=['<roo>',
              '<aoho>',
              '<aooo>',
              '<q>',
              '% HB',
              '% AD',
              '% ADD',
              '% AAD',
              '% AADD',
              '% AAADD',
              '% 4',
              '% 6'
              ]


df=df.sample(frac=1)
scaler = pp.StandardScaler().fit(df[whattolookat])
sdf=scaler.transform(df[whattolookat])
for i in range(len(sdf.T)):
    print("Range {}: {:.2f} -> {:.2f}".format(whattolookat[i],min(sdf.T[i]),max(sdf.T[i])))
labs=[]
pca=dcomp.PCA()
pca.fit(sdf)
pca.components_.tofile("PCA.mat")
p=pca.components_

temp=np.fromfile("PCA.mat").reshape((len(p),len(p[0])))
for i in range(len(p)):
    for j in range(len(p[i])):
        if temp[i,j] !=p[i,j]: print("BAD")



