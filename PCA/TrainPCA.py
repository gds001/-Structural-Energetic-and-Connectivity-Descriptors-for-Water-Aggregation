import pandas as pd
import numpy as np
import sklearn.decomposition as dcomp
import sklearn.preprocessing as pp
import pickle as pkl
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys

np.set_printoptions(suppress=True,precision=2)

#Pulls the dataframe and selects a subset of descriptors to analize
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
df=df.sample(frac=1)

#Scale, and fit PCA to the data
scaler = pp.StandardScaler().fit(df[whattolookat])
sdf=scaler.transform(df[whattolookat])
pca=dcomp.PCA()
pca.fit(sdf)

#Write the pca matrices to a file
pkl.dump(pca,open("PCA.pkl",'wb'))

#Check that the file is properly written, as well as provides an example to in reading in the PCA.

temp=pkl.load(open("PCA.pkl",'rb'))
p=pca.components_
for i in range(len(p)):
    for j in range(len(p[i])):
        if temp.components_[i,j] !=p[i,j]:
            print("BAD")
            sys.exit()
print("Success1")

pc=pca.transform(sdf)
temp=temp.transform(sdf)
for i in range(len(pc)):
    for j in range(len(pc[i])):
        if temp[i][j] != pc[i][j]:
            print("Bad")
            sys.exit()
print("Success2")
n=7
size="Large"
fig,axes=plt.subplots(n,n,figsize=(6,6))
xmin=[-4,-7.5,-5,-2.5,-5,-5,-5,-5,-5,-5,-5]
xmax=[9,7.5,5,5,5,5,5,5,5,5,5,5,5]
comp=pca.components_
labs=[]
colors=['tab:blue','tab:orange','tab:green','tab:red','tab:purple',
        'tab:brown','tab:pink','tab:gray','tab:olive','tab:cyan',
        'royalblue','chocolate'
        ]
for i in range(len(pc.T)): labs.append("PC{}".format(i+1))
for i in range(n):
    for j in range(n):
        if j==i:
            axes[i][j].hist(pc.T[j],bins=500)
            axes[i][j].set_xlim(xmin[j], xmax[j])
        if j<i:
            axes[i][j].hist2d(pc.T[j],pc.T[i],bins=500,
                 norm=mpl.colors.LogNorm(),cmap="twilight")
            axes[i][j].set_ylim(xmin[i], xmax[i])
            axes[i][j].set_xlim(xmin[j], xmax[j])
        if i<j:
            for k in range(len(comp)):
                axes[i][j].plot([0,comp[j][k]*5],[0,comp[i][k]*5],c=colors[k])
                axes[i][j].arrow(comp[j][k]*5, comp[i][k]*5, comp[j][k], comp[i][k], shape='full', lw=0, length_includes_head=True, head_width=.75,color=colors[k])
            axes[i][j].set_ylim(-6, 6)
            axes[i][j].set_xlim(-6, 6)
        if i!=n-1:
            axes[i][j].tick_params(bottom=False,labelbottom=False)
        axes[i][j].tick_params(left=False,labelleft=False)
        if i==0:
            axes[i][j].set_title(labs[j],fontsize=10)
        elif i==n-1:
            axes[i][j].set_xticks([-3,0,3],["-3","0","3"])
        if j==0:
            axes[i][j].set_ylabel(labs[i])

plt.tight_layout()
title=""
for i in whattolookat: title+=i.replace("<",'').replace(">",'')+'_'
plt.subplots_adjust(left=0.1,bottom=0.1,top=0.9,right=0.9,hspace=0,wspace=0)
plt.savefig("SuperPlot_{}_{}.png".format(n,size),dpi=300)
plt.show()
