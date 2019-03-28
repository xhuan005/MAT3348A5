# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 19:29:27 2019

@author: lianmin 
"""
import networkx as nx
import matplotlib as plt
import time

def createBipartiteGraph(adjList):
    g = nx.Graph()
    for i in range(len(adjList)):
        g.add_node(i,bipartite  = 0,saturated=False,matchingVertex = None)
        for e in adjList[i]:
            g.add_node(e,bipartite = 1, saturated = False, matchingVertex = None)
            g.add_edge(i,e,match = False,path = False,color = 'black')
    g.graph.update(x = nx.bipartite.sets(g)[0],y = nx.bipartite.sets(g)[1])
    return g
        
def hungarianAlgo(g):
    if (len(g.graph['x'])!=len(g.graph['y'])):
        print("len x != len y impossible to have perfect match")
    initialMatching(g)
    perfectMatchBool,unSatX,unSatY = isPerfectMatch(g)
    stopCondition = False
    while(perfectMatchBool == False and stopCondition == False):
        SReachedY = False
        s=set()
        t=set()
        while (SReachedY == False):
            for x in unSatX:
                s.add(x)
                stopCondition,sNeiNotInT = nsEqualT(g,s,t)
                if stopCondition:
                    break
                print(s)
                print(t)
                unSatNei = findUnSatNei(g,x)
                print(unSatNei)
                if unSatNei == None:
                    y = sNeiNotInT.pop()
                    t.add(y)
                    s.add(g.nodes[y]['matchingVertex'])
                    print(s)
                    print(t)
                break
            if stopCondition:
                break
            break
        if stopCondition:
            break
        break
    
        
    colors = [g[u][v]['color'] for u,v in g.edges()]
    nx.draw(g, nx.bipartite_layout(g,g.graph['x']),with_labels = True,edge_color = colors,width = 5 )
def findUnSatNei(g,x):
    for y in g[x]:
        if g.nodes[y]['saturated']==False:
            return y
    return None

def nsEqualT(g,s,t):
    sNei = set()
    for x in s:
        for y in g[x]:
            sNei.add(y)
    return (sNei == t,sNei - t)
            


def initialMatching(g):
    for x in g.graph['x']:
        for y in g[x]:
            if g.nodes[y]['saturated']==False:
                g.nodes[x]['saturated'] =True
                g.nodes[y]['saturated']=True
                g.nodes[y]['matchingVertex'] = x
                g.nodes[x]['matchingVertex'] = y
                g[x][y]['match']=True
                g[x][y]['color']=setEdgeColor(g[x][y]['match'],g[x][y]['path'])
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
    unSatX = []
    unSatY = []
    perfect = False
    for x in g.graph['x']:
        if g.nodes[x]['saturated']==False:
            unSatX.append(x)
    for y in g.graph['y']:
        if g.nodes[y]['saturated']==False:
            unSatY.append(y)
    if (len(unSatX)==len(unSatY)==0):
        perfect = True
    return (perfect,unSatX,unSatY)
          
inputAdjList = [["a","b","c"],["a","b"],["a","l","s"],["l"],["a","l"]]
g = createBipartiteGraph(inputAdjList)
print(g.graph['y'])
top = nx.bipartite.sets(g)[0]
pos = nx.bipartite_layout(g,top)
colors = [g[u][v]['color'] for u,v in g.edges()]
print(colors)
#nx.draw(g,pos,with_labels = True,edge_color = colors )
#nx.draw_networkx_edges(g,pos)

#print(g.edges())
#print(list(g.nodes(data=True)))
hungarianAlgo(g)