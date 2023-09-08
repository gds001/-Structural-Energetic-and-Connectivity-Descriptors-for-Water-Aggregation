import networkx as nx

def GetNonSortCircuitedCycles(G):
    """
    This method wraps all the bits and pieces to return non-short circuited cycles.

    :param G: networkx, graph to analyze
    :return: list, returns a list with all non-short-circuited cycles in G
    """
    _PruneDeadEnds(G)
    cycles=_FindCycles(G)
    cycles=_ReduceCycles(cycles)
    cycles=_ShortCircuitCycles(cycles, G)
    return cycles

def CountNonShortCircuitedCycles(G):
    """
    This method returns the counts of the sizes of cycles in G.


    :param G: networkx, graph to be analyzed
    :return: list: list of the number of non-repeating cycles in G.
    """
    cycles=GetNonSortCircuitedCycles(G)
    max=0
    for cycle in cycles:
        if len(cycle)>max: max=len(cycle)
    return CountCycles(cycles)

def CountCycles(cycles):
    """
    This method counts the sizes of cycles from a list of cycles.

    :param cycles: list of cycles to count
    :param max: int, max size of the cycle to count to.
    :return: list: the number of each cycle of each size
    """
    sizes={}
    for i in range(len(cycles)):
        temp=len(cycles[i])
        if temp in sizes: sizes[temp]+=1
        else: sizes[temp]=1
    return sizes


def _PruneDeadEnds(G):
    """
    This method modifies G to remove any nodes with one edge.
    This decreases further computational cost, since these nodes cannot be in a cycle.

    :param G: networkx, graph to be pruned.
    :return: None
    """
    prune=[]
    for node in nx.nodes(G):
        if len(list(G[node].keys()))==1:
            prune.append(node)
    for item in prune:
        G.remove_node(item)

def _FindCycles(G):
    """
    This method takes a graph and returns all the cycles in the graph.

    :param G: networkx, graph to be analyzed
    :return: list, list of cycles.
    """
    cycles=[]
    for node in list(G.nodes()):
        _CycleSearch(G, cycles, node)
    return cycles

def _CycleSearch(G, cycles, start):
    """
    This method appends the cycle parameter with any cycles coming from the starting node in graph G

    :param G: networkx, the graph you are searching cylces for
    :param cycles: list, container for the cycles
    :param start: key/node, the identity of the node you are going to start each cycle from.
    :return: None
    """
    neighbors=list(G[start].keys())
    for i in range(len(neighbors)): #O(5)
        for j in range(i+1,len(neighbors)): #O(5)
            paths=_ShortPath(G, i, j, neighbors, start)
            for path in paths:
                cycles.append(path)

def _ShortPath(G, start, end, pieces, origin):
    """
    This method sets up the BFS to find the shortest path from the starting
    node to the ending node without going through the origin.

    :param G: networkx graph to be analyzed
    :param start: int, index of starting node in pieces
    :param end: int, index of ending node in pieces
    :param pieces: list of nodes, nodes of neighbors to origin.
    :param origin: node, origin of the cycle.
    :return: list: all paths that are likely non-short-circuited cycles
             (cause there can be two or more)!
    """
    H=G.copy()
    H.remove_node(origin)
    source=pieces[start]
    sink=pieces[end]
    paths=_BfsPath(H, source, sink, pieces)
    for i in range(len(paths)):
        paths[i]=paths[i]+[origin]
        for j in range(len(paths[i])):
            if paths[i][j]==pieces[start] or paths[i][j]==pieces[end]: continue
            elif paths[i][j] in pieces:
                paths[i]=[]
                break
    return paths

def _BfsPath(G, source, sink, pieces):
    """
    This recursive BFS algorithm finds the shortest path between source and sink
    via a BFS that breaks when the sink is found.

    :param G: networkx, graph of interest
    :param source: node, beginning of the BFS
    :param sink: node, end goal of the BFS
    :param pieces: list of nodes connected to the origin
    :return: list: the list of all potential paths for this cycle.
    """
    tree={}
    tree[0]={source:[]}
    leaves=list(G[source])
    if sink in leaves: return [[source,sink]]
    tree[1]={}
    for leaf in leaves:
        tree[1][leaf]=[source]
    trunk=[source]
    return _BfsPathRec(G, source, sink, tree, trunk)

def _BfsPathRec(G, source, sink, tree, trunk, level=2):
    """
    This is the recursive part of the BFS for shortest paths.
    BASE 1: BFS exhausts itself and doesn't find the sink.  No paths are returned.
    BASE 2: The sink is found, so one or more paths are returned.

    :param G: networkx, graph of interest
    :param source: node, source of the BFS
    :param sink: node, sink goal of the BFS
    :param tree: dict, stores the paths taken by the BFS
    :param trunk: list of nodes, all previously visited nodes to prevent double visits.
    :param level: int, level of the BFS from the origin you've taken.
    :return: list: a list of path from source to sink.
    """
    branches=tree[level-1]
    paths=[]
    if not branches:  #Base Case 1: Nothing left, return nothing
        return []
    tree[level]={}
    for branch in branches:
        trunk.append(branch)
        leaves=list(G[branch].keys())
        for wood in trunk:
            if wood in leaves: leaves.remove(wood)
        for leaf in leaves:
            if leaf==sink:
                paths.append([leaf,branch]+branches[branch])
            else:
                tree[level][leaf]=[branch]+branches[branch]
    if not paths: # Base Case not satisfied, do the recursive thing.
        return _BfsPathRec(G, source, sink, tree, trunk, level=level + 1)
    return paths # Base Case 2: There is a path so return it.

def _ReduceCycles(cycles):
    """
    This method eliminates multiple copies of a cycle in the list cycles.

    :param cycles: list of cycles
    :return: list: list of unique cycles.  (eliminates repeats)
    """
    for i in range(len(cycles)):
        cycles[i].sort()
    unique=[]
    for i in cycles:
        if i not in unique and len(i)>=3:
            unique.append(i)
    return unique

def _ShortCircuitCycles(cycles, G):
    """
    This method loops through all cycles and removes the cycle if it is short-circuited by other edges in G.

    :param cycles: list of cycles to check for short-circuitousness
    :param G: networkx, graph of the environment of the cycles
    :return: list: all the non-short-circuited cycles.
    """
    temp=[]
    for cycle in cycles: temp.append(cycle)
    for i in range(len(temp)):
        if _ShortCirciutedCycle(temp[i], G):
            cycles.remove(temp[i])
    return cycles


def _ShortCirciutedCycle(cycle, G):
    """
    This method checks to see if a cycle is short-circuited by other edges in G.

    :param cycle: list, the cycle in question
    :param G: networkx, graph of interest
    :return: boolean whether the cycle is short-circuited by graph G.
    """
    nodes=G.nodes()
    H=G.copy()
    for node in nodes:
        if node not in cycle:
            H.remove_node(node)
    nodes=list(H.nodes())

    for i in range(len(nodes)):
        for j in range(i+1,len(nodes)):
            a=nodes[i]
            b=nodes[j]
            lenG=nx.shortest_path_length(G,a,b)
            lenH=nx.shortest_path_length(H,a,b)
            if lenG<lenH: return True
    return False