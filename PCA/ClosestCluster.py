import pandas as pd
import numpy as np
import pickle as pkl
import sklearn.decomposition as dcomp
import matplotlib.pyplot as plt
import sklearn.preprocessing as pp
import time

start=time.time()

np.set_printoptions(suppress=True,precision=2)
num=25
struct=0
sizes=[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]

df=pd.read_pickle("../DataFrame.pkl")
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

scaler = pp.StandardScaler().fit(df[whattolookat])
sdf=scaler.transform(df[whattolookat])

pca=pkl.load(open("PCA.pkl",'rb'))
pc=pca.transform(sdf)
df25=df[df['size']==num].sort_values('energy')
pcranges=[]
pcstd=[]
for i in range(len(pc.T)):
    pcranges.append(np.amax(pc.T[i])-np.amin(pc.T[i]))
    pcstd.append(np.std(pc.T[i]))
print(len(df25))
print(pcranges)
print(pcstd)
pc25=pca.transform(scaler.transform(df25[whattolookat]))
scale=pca.explained_variance_ratio_
print(pca.explained_variance_ratio_)
pcs=[]
for i in sizes:
    dftemp=df[df['size']==i].sort_values('energy')
    pcs.append(pca.transform(scaler.transform(dftemp[whattolookat])))

pc23=np.zeros(len(sizes),dtype=int)
pc26=np.zeros(len(sizes),dtype=int)
pcall=np.zeros(len(sizes))
pcd23=np.zeros(len(sizes))
pcd26=np.zeros(len(sizes))
pcdall=np.zeros(len(sizes))

for i in range(len(sizes)):
    dist23=10000**2
    dist26=10000**2
    distall=10000**2
    for j in range(len(pcs[i])):
        temp23=0
        for k in [1,2]:
            temp23+=(pcs[i][j][k]-pc25[struct][k])**2*scale[k]
        temp26=temp23
        for k in [3,4,6]:
            temp26+=(pcs[i][j][k]-pc25[struct][k])**2*scale[k]
        tempall=temp26
        for k in range(7,len(pc25.T)):
            tempall+=(pcs[i][j][k]-pc25[struct][k])**2*scale[k]
        if dist23>temp23:
            pc23[i]=j
            dist23=temp23
            pcd23[i]=temp23
        if dist26>temp26:
            pc26[i]=j
            dist26=temp26
            pcd26[i]=temp26
        if distall>tempall:
            pcall[i]=j
            distall=tempall
            pcdall[i]=tempall

order=np.argsort(pcd26)
print(order+6)
print(np.sqrt(pcd26[order]))
print(pc26[order])


