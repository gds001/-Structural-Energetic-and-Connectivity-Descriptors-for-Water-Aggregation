import time as time
import json
import CycleSearching.FindCycles as cyc
from ComputeDescriptors import *
from Useful import sec2time
from zipfile import ZipFile
import pickle
from CheckStructures import *
import os

start=time.time()
try:
    for file in os.listdir("ProcessedData"):
        os.remove("ProcessedData/"+file)
    os.rmdir('ProcessedData')
except: pass
try: os.remove("ProcessedData.zip")
except: pass
os.mkdir("ProcessedData")

with ZipFile("Database.zip",'r') as zObject:
    zObject.extractall()

for n in range(6,26):
    data={}
    st=time.time()
    file=open("Database/W{}_projected_grpahs_5kcal_orderd.txt".format(n),'r')
    graphs=file.read()
    file.close()
    graphs=graphs.split("---")[:-1]
    file=open("Database/W{}_geoms_5kcal_ordered.xyz".format(n),'r')
    geom=file.read()
    geom=geom.split('\n{}\n'.format(n*3))
    geoms=[]
    for i in geom:
        geoms.extend(i.split(" {}\n".format(n*3)))
    geoms=geoms[1:]
    mid=time.time()
    print("ReadTime",sec2time(mid-st))
    for i in range(len(graphs)):
        data[i]={}
        G=nx.json_graph.adjacency_graph(json.loads(graphs[i]))
        js=json.loads(graphs[i])
        S=geoms[i]
        s=S.find("rgy") - 3
        S=S[s:]
        e=S.split()[1]
        s=S.find("O") - 2
        S=S[s:]
        waters = S.split("O")[1:]
        waters=checkAtomOrder(waters)
        roh, ahoh = oneBody(waters)
        if roh[0]==False:
            print("Size, id, energy\n",n,i,e)
            print("This will be removed from the dataset.")
            break
        data[i]['energy']=e
        nnodes=len(G.nodes)
        nedges=len(G.edges)
        data[i]['size']=nnodes
        data[i]['% HB']=float(nedges)/2/nnodes
        wiener,ASPL=Wiener(G)
        data[i]['wiener']=wiener
        data[i]['aspl']=ASPL


        data[i]['Rg']=rg(waters)


        roo,aoho,dhoox=twoBody(waters,G.edges)
        aooo,tet=threeBodyandTet(waters,G)
        data[i]['roh']=roh
        data[i]['ahoh']=ahoh

        data[i]['roo'] = roo
        data[i]['aoho'] = aoho
        data[i]['dhoox'] = dhoox
        data[i]['aooo'] = aooo
        data[i]['tet'] = tet

        cycles=cyc.CountNonShortCircuitedCycles(G)
        for j in range(3,9):
            try: cycles[j]
            except: cycles[j]=0
        data[i]['cycles']=cycles
        adjs=getAdjs(json.loads(graphs[i]))
        data[i]['adjs']=adjs

    file=open("ProcessedData/W{}_Data.pkl".format(n),'wb')
    pickle.dump(data,file,protocol=pickle.HIGHEST_PROTOCOL)
    file.close()
    nd=time.time()
    print(n,sec2time(nd-st))

with ZipFile("ProcessedData.zip",'w') as zObject:
    for root, dirs, files in os.walk("ProcessedData/"):
        for file in files:
            zObject.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join("ProcessedData", '..')))
for file in os.listdir("ProcessedData"):
    os.remove("ProcessedData/"+file)
os.rmdir('ProcessedData')

for file in os.listdir("Database"):
    os.remove("Database/"+file)
os.rmdir("Database")

end=time.time()
print(sec2time(end-start))

