import numpy as np

def checkAtomOrder(waters):
    for water in waters:
        entry = water.split()
        o = np.array([float(entry[0]), float(entry[1]), float(entry[2])])
        h1 = np.array([float(entry[4]), float(entry[5]), float(entry[6])])
        h2 = np.array([float(entry[8]), float(entry[9]), float(entry[10])])
        a = np.linalg.norm(o - h1)
        b = np.linalg.norm(o - h2)
        if a>1.25 or b>1.25:
            return reorderAtoms(waters)
    return waters

def reorderAtoms(waters):
    os=[]
    hs=[]
    for water in waters:
        entry=water.split()
        os.append(np.array([float(entry[0]), float(entry[1]), float(entry[2])]))
        hs.append(np.array([float(entry[4]), float(entry[5]), float(entry[6])]))
        hs.append(np.array([float(entry[8]), float(entry[9]), float(entry[10])]))
    taken=np.zeros(len(hs),dtype='bool')
    waters=[]
    for o in os:
        temp="{}  {}  {}\n".format(o[0],o[1],o[2])
        id1=-1
        id2=-1
        dist1=99
        dist2=100
        i=0
        for h in hs:
            if taken[i]:
                i+=1
                continue
            d=np.linalg.norm(o-h)
            if d<dist1:
                dist2=dist1
                id2=id1
                dist1=d
                id1=i
            elif d<dist2:
                dist2=d
                id2=i
            i+=1
        taken[id1]=True
        taken[id2]=True
        temp+="H  {}  {}  {}\nH  {} {} {}".format(hs[id1][0],hs[id1][1],hs[id1][2],hs[id2][0],hs[id2][1],hs[id2][2])
        waters.append(temp)
    return waters



