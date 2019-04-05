# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 19:29:27 2019

@author: Xiaopei
"""
import networkx as nx
"""
let g be graph
node:
    g.nodes[key] return params of node key
    ex:
        g.nodes["b"] is {'bipartite': 1, 'saturated': False, 'matchingVertex': None}
        
    get and set node attribute by g.nodes[key][attributeName]
    ex:
        g.nodes["b"]["bipartite"] is 1
        this notation is same for g.graph
    
    g[key] is all the neighbor of node key
    ex:
        g[0] is {'a': {'match': False, 'path': False, 'color': 'black'}, 
                 'b': {'match': False, 'path': False, 'color': 'black'}, 
                 'c': {'match': False, 'path': False, 'color': 'black'}}
        
        g["b"] is {0: {'match': False, 'path': False, 'color': 'black'}, 
                   1: {'match': False, 'path': False, 'color': 'black'}}
    
edges:
    g[v1Key][v2Key] is the edge of (v1,v2)
    ex:
        g["b"][0] is {'match': False, 'path': False, 'color': 'black'}
"""

def createBipartiteGraph(adjacencyList):
    """
    @purpose:  created a bipartite graph using adjacencyList
               index number is set X and element in each array is set Y
    @parma: adjacencyList
    """
    g = nx.Graph() # create nx graph
    for i in range(len(adjacencyList)):
        g.add_node(i,bipartite  = 0,saturated=False,matchingVertex = None)
        #i is the key for node with param(bipartite:integer, saturated:bool, matchingVertex:node)
        for e in adjacencyList[i]:
            g.add_node(e,bipartite = 1, saturated = False, matchingVertex = None)
            g.add_edge(i,e,match = False,path = False,color = 'black') # path may or may not need
            #(i,e)are endpoints of edge with param (match:bool, path:bool, color:string)
    g.graph.update(x = nx.bipartite.sets(g)[0],y = nx.bipartite.sets(g)[1])
    # set param(x: all node with bipartite = 0, y:all nodes with bipartite = 1)
    return g
        
def hungarianAlgo(g):
    if (len(g.graph['x']) != len(g.graph['y'])):
        #may more may want to implement
        print("len x != len y impossible to have perfect match")
    initialMatching(g)#inital matching
    perfectMatchBool,unSaturatedX,unSaturatedY = isPerfectMatch(g)
    stopCondition = False # N(S) = T
    while(perfectMatchBool == False and stopCondition == False): # while not perfect match and did not reach stop condition
        SReachedT = False # find an vertex for augmenting path
        s=set() # init S
        t=set() # init Y
        """
        我在这停了
        logic有点问题
        """
        while (SReachedT == False):
            for x in unSaturatedX: # take a x in unSaturatedX
                s.add(x) # put x in s
                stopCondition,sNeighborNotInT = nsEqualT(g,s,t) # test for stop condition
                if stopCondition: #stop the inner for loop
                    break
                print(s)
                print(t)
                unSaturatedNeighbor = findUnSaturatedNeighbor(g,x)# find posible solution
                print(unSaturatedNeighbor)
                if unSaturatedNeighbor == None: # if every neighbor of x saturated
                    y = sNeighborNotInT.pop()
                    t.add(y)
                    s.add(g.nodes[y]['matchingVertex'])
                    print(s)
                    print(t)
            if stopCondition: #stop inner while
                break
            break
        if stopCondition:#stop outter while loop
            break
        break
    
        
    colors = [g[u][v]['color'] for u,v in g.edges()]
    nx.draw(g, nx.bipartite_layout(g,g.graph['x']),with_labels = True,edge_color = colors,width = 5 )
def findUnSaturatedNeighbor(g,x):
    for y in g[x]:
        if g.nodes[y]['saturated']==False:
            return y
    return None

def nsEqualT(g,s,t):
    """
    @purpose test N(S) = T condition
    @return ?N(S) = T :bool
    @sNeighbor - t : set of N(S) which not in T
    """
    sNeighbor= set() #init s neighbor
    for x in s:
        for y in g[x]:
            sNeighbor.add(y)
    return (sNeighbor == t,sNeighbor - t)
            


def initialMatching(g):
    for x in g.graph['x']:#loop through all element of x. x is only the key
                          # g.graph['x'] = {0, 1, 2, 3, 4}
        for y in g[x]: #loop through all neighbor of x. y is a key 
            if g.nodes[y]['saturated'] == False: # find a neighbor that is not saturated
                #match x and y 
                g.nodes[x]['saturated'] = True 
                g.nodes[y]['saturated'] = True
                g.nodes[y]['matchingVertex'] = x
                g.nodes[x]['matchingVertex'] = y
                g[x][y]['match']=True
                g[x][y]['color']=setEdgeColor(g[x][y]['match'],g[x][y]['path'])# set color for visual
                break


def setEdgeColor(match,path):
    if (match == True and path == True):
        return 'orange'
    elif(match==True and path == False):
        return 'red'
    elif(match ==False and path == True):
        return 'yellow'
    elif(match ==False and path == False):
        return 'black'
        
def isPerfectMatch(g):
    """
    @purpose test if graph g is perfect Match
    @return perfect:bool
            unSaturatedX: node list all vertex in x that is not saturated
            unSaturatedY: node list all vertex in y that is not saturated
            
    """
    unSaturatedX = []
    unSaturatedY = []
    perfect = False
    for x in g.graph['x']: # find all unSaturatedX
        if g.nodes[x]['saturated'] == False:
            unSaturatedX.append(x)
    for y in g.graph['y']: # find all unSaturatedY
        if g.nodes[y]['saturated'] == False:
            unSaturatedY.append(y)
    if (len(unSaturatedX) == len(unSaturatedY) == 0): # if both list is empty return true
        perfect = True
    return (perfect,unSaturatedX,unSaturatedY)

# input List - needs to find way to input. 
inputAdjacencyList = [["a","b","c"],["a","b"],["a","l","s"],["l"],["a","l"]]
g = createBipartiteGraph(inputAdjacencyList)
print(g[0])
#print(g.graph['y'])
#top = nx.bipartite.sets(g)[0]
#pos = nx.bipartite_layout(g,top)
#colors = [g[u][v]['color'] for u,v in g.edges()]
#print(colors)
#nx.draw(g,pos,with_labels = True,edge_color = colors )
#nx.draw_networkx_edges(g,pos)

#print(g.edges())
#print(list(g.nodes(data=True)))
hungarianAlgo(g)#start algorithm