import networkx as nx
import sys
import numpy as np

def Wiener(G):
    nnodes=len(G.nodes)
    wiener = 0
    connect = 0
    for i in range(1, nnodes * 3 + 1, 3):
        for j in range(i + 3, nnodes * 3 + 1, 3):
            try:
                wiener += len(nx.shortest_path(G, str(i), str(j))) - 1
            except:
                continue
            connect += 1
    ASPL = wiener / connect
    return wiener,ASPL

def oneBody(waters):
    roh=[]
    ahoh=[]
    for water in waters:
        entry=water.split()
        o = np.array([float(entry[0]), float(entry[1]), float(entry[2])])
        h1 = np.array([float(entry[4]), float(entry[5]), float(entry[6])])
        h2 = np.array([float(entry[8]), float(entry[9]), float(entry[10])])
        a =o-h1
        b = o-h2
        c=np.linalg.norm(a)
        d=np.linalg.norm(b)
        if c > 2 or d> 2:
            print("Big Error.  Your bond is too long, or atoms are jumbled.",c,d)
            return [False],[False]
        roh.append(c)
        roh.append(d)
        ahoh.append(np.arccos(np.dot(a,b)/c/d)*180/np.pi)
    return roh,ahoh

def twoBody(waters,edges):
    roo=[]
    aoho=[]
    dhoox=[]

    for edge in edges:
        i1 = int((int(edge[0]) - 1) / 3)
        i2 = int((int(edge[1]) - 1) / 3)
        water1 = waters[i1]
        water2 = waters[i2]
        water1 = water1.split()
        water2 = water2.split()
        o1 = np.array([float(water1[0]), float(water1[1]), float(water1[2])])
        h11 = np.array([float(water1[4]), float(water1[5]), float(water1[6])])
        h12 = np.array([float(water1[8]), float(water1[9]), float(water1[10])])
        o2 = np.array([float(water2[0]), float(water2[1]), float(water2[2])])
        h21 = np.array([float(water2[4]), float(water2[5]), float(water2[6])])
        h22 = np.array([float(water2[8]), float(water2[9]), float(water2[10])])
        c=np.linalg.norm(o1-o2)
        roo.append(c)
        hyd=[h11,h12,h21,h22]
        ind=-1
        ang=0
        i=0
        for h in hyd:
            a=o1-h
            b=o2-h
            temp = np.arccos(np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b))
            if ang<temp:
                ang=temp
                ind=i
            i+=1
        aoho.append(ang*180/np.pi)
        if ind==0:
            f=h11-o1
            x=(h21+h22)/2-o2
            of=o2-o1
            ox=o1-o2
        elif ind==1:
            f=h12-o1
            x=(h21+h22)/2-o2
            of=o2-o1
            ox=o1-o2
        elif ind==2:
            f=h21-o2
            x=(h11-h12)/2-o1
            ox=o2-o1
            of=o1-o2
        elif ind==3:
            f=h22-o2
            x=(h11/np.linalg.norm(h11)+h12/np.linalg.norm(h12))/2-o1
            ox=o2-o1
            of=o1-o2
        don=np.cross(f,of)
        acc=np.cross(ox,x)
        dhoox.append(np.arccos(np.dot(don,acc)/np.linalg.norm(don)/np.linalg.norm(acc))*180/np.pi)
    return roo,aoho,dhoox

def threeBodyandTet(waters,G):
    aooo=[]
    tet=[]

    for i in range(len(waters)):
        oc=np.array([float(waters[i].split()[0]), float(waters[i].split()[1]), float(waters[i].split()[2])])
        atemp=[]
        neighbors=list(nx.neighbors(G,str(i*3+1)))
        k = (len(neighbors))
        on=[]
        for n in neighbors:
            j=int((int(n)-1)/3)
            on.append(np.array([float(waters[j].split()[0]), float(waters[j].split()[1]), float(waters[j].split()[2])]))
        for n in range(len(neighbors)):
            for m in range(n+1,len(neighbors)):
                a=on[n]-oc
                b=on[m]-oc
                atemp.append(np.arccos(np.dot(a,b)/np.linalg.norm(a)/np.linalg.norm(b))*180/np.pi)
        t=0
        for a in atemp:
            aooo.append(a)
            t+=(np.cos(a/180*np.pi)+1/3)**2
        if k>1: tet.append(1-9/(2*k*(k-1))*t)
    return aooo,tet

def getAdjs(G):
    adjs={'A':0,'AA':0,
          'D':0,'AD':0,'AAD':0,'AAAD':0,
          'DD':0,'ADD':0,'AADD':0,'AAADD':0}
    nodes=G['nodes']
    for node in nodes:
        label=node['label']
        if label == "a1": adjs['A'] += 1
        if label == "a2": adjs['AA'] += 1
        if label == "d1": adjs['D'] += 1
        if label == "a1d1": adjs['AD'] += 1
        if label == "a2d1": adjs['AAD'] += 1
        if label == "a3d1": adjs['AAAD'] += 1
        if label == "d2": adjs['DD'] += 1
        if label == "a1d2": adjs['ADD'] += 1
        if label == "a2d2": adjs['AADD'] += 1
        if label == "a3d2": adjs['AAADD'] += 1
    return adjs

def rg(waters,mO=15.999,mH=1.00784):
    com=np.zeros(3)
    mass=0
    for water in waters:
        entry=water.split()
        o = np.array([float(entry[0]), float(entry[1]), float(entry[2])])*mO
        h1 = np.array([float(entry[4]), float(entry[5]), float(entry[6])])*mH
        h2 = np.array([float(entry[8]), float(entry[9]), float(entry[10])])*mH
        mass+=mO+mH+mH
        com+=o+h1+h2
    com/=mass
    rg=0
    for water in waters:
        entry = water.split()
        o = np.array([float(entry[0]), float(entry[1]), float(entry[2])])
        h1 = np.array([float(entry[4]), float(entry[5]), float(entry[6])])
        h2 = np.array([float(entry[8]), float(entry[9]), float(entry[10])])
        rg += np.linalg.norm(o  - com) ** 2
        rg += np.linalg.norm(h1 - com) ** 2
        rg += np.linalg.norm(h2 - com) ** 2
    rg/=len(waters)*3
    return np.sqrt(rg)