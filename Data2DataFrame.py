import pickle
import os
import pandas as pd
import numpy as np
from zipfile import ZipFile

with ZipFile("ProcessedData.zip",'r') as zObject:
    zObject.extractall()

df=pd.DataFrame(columns=['size','energy','id','<roh>','<ahoh>','<roo>','<aoho>','<dhoox>',
                         '<aooo>','<q>','% HB','ASPL','Wiener','Rg',
                         '% A','% AA','% D','% AD','% AAD','% AAAD',
                         '% DD','% ADD','% AADD','% AAADD',
                         '% 3', '% 4','% 5','% 6','% 7','% 8'])

for n in range(6,26):
    print(n)
    file=open("ProcessedData/W{}_Data.pkl".format(n),'rb')
    data=pickle.load(file)
    file.close()
    for id in data.keys():
        s=data[id]['size']
        c=0
        for size in data[id]['cycles'].keys(): c+=data[id]['cycles'][size]
        temp=pd.DataFrame(data={'size':[s],
                      'energy':[data[id]['energy']],
                      'id':[id],
                      '<roh>':[np.average(data[id]['roh'])],
                      '<ahoh>':[np.average(data[id]['ahoh'])],
                      '<roo>':[np.average(data[id]['roo'])],
                      '<aoho>':[np.average(data[id]['aoho'])],
                      '<dhoox>':[ np.average(data[id]['dhoox'])],
                      '<aooo>':[ np.average(data[id]['aooo'])],
                      '<q>':[ np.average(data[id]['tet'])],
                      '% HB':[data[id]['% HB']],
                      'ASPL':[data[id]['aspl']],
                      'Wiener':[data[id]['wiener']],
                      'Rg':[data[id]['Rg']],
                      '% A':[data[id]['adjs']['A']/s],
                      '% AA':[data[id]['adjs']['AA']/s],
                      '% D':[data[id]['adjs']['D']/s],
                      '% AD':[data[id]['adjs']['AD']/s],
                      '% AAD':[data[id]['adjs']['AAD']/s],
                      '% AAAD':[data[id]['adjs']['AAAD']/s],
                      '% DD':[data[id]['adjs']['DD']/s],
                      '% ADD':[data[id]['adjs']['ADD']/s],
                      '% AADD':[data[id]['adjs']['AADD']/s],
                      '% AAADD':[data[id]['adjs']['AAADD']/s],
                      '% 3':[data[id]['cycles'][3]/c],
                      '% 4':[data[id]['cycles'][4]/c],
                      '% 5':[data[id]['cycles'][5]/c],
                      '% 6':[data[id]['cycles'][6]/c],
                      '% 7':[data[id]['cycles'][7]/c],
                      '% 8':[data[id]['cycles'][8]/c]
                      })
        df=pd.concat([df,temp])
df.to_pickle("DataFrame.pkl")
for file in os.listdir("ProcessedData"):
    os.remove("ProcessedData/"+file)
os.rmdir('ProcessedData')


