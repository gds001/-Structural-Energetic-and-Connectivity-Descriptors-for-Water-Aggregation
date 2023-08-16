import networkx as nx
import json
import pandas as pd
import numpy as np
import sklearn.decomposition as dcomp
import matplotlib.pyplot as plt
import sklearn.preprocessing as pp
from mpl_toolkits import mplot3d
import sklearn.cluster as clu
import time as time
from scipy.stats import gaussian_kde
import sys
import sklearn.model_selection as ms
#import kneed
import sklearn.metrics as metrics
from Useful import sec2time

start=time.time()

for n in range(6,26):
    st=time.time()
    file=open("W{}_projected_grpahs_5kcal_orderd.txt".format(n),'r')
    graphs=file.read()
    file.close()
    graphs=graphs.split("---")[:-1]
    file=open("W{}_geoms_5kcal_ordered.xyz".format(n),'r')
    geoms=file.read()
    geoms=geoms.split('\n{}\n'.format(n*3))
    geom=[]
    for i in geoms:
        geom.extend(i.split(" {}\n".format(n*3)))
    nd=time.time()
    print(n,sec2time(nd-st))

end=time.time()

print(sec2time(end-start))