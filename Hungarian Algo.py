# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:24:29 2019

@author: Xiaopei Huang
"""

class Vertex:
    """
    vertex class
    @param: key:        String 
                        Should be unique
            group:      String
                        S or T
            neighbor:   list<Vertex>
                        Vertex connected to self from different gropu
            edges:      list<Edges>
                        The edges to connect with neighbors
                
    """
    def __init__(self,key,group):
        self.key = key
        self.group = group
        self.neighbors = []
        self.edges = []
        self.saturated = False
        self.matchingVertex = None #not null only when saturated is true
    def __str__(self):
        return self.key
    def __repr__(self):
        return self.key
    """
    insertNeighbor
    @param neighbor: Vertex
    @return: void
    @ insert a vertex as neighbor and create an edge. Edge is also put into 
    list of edges
    """
    def insertNeighbor(self,neighbor):
        if neighbor in self.neighbors:
            print("FAIL! this neighbor is already added")
        elif neighbor.group == self.group:
            print("FAIL! this vertex is in the same group as target vertex")
        else:
            self.neighbors.append(neighbor)
            edge = Edge(self,neighbor)
            self.edges.append(edge)
    """
    getEdge
    @param v:vertex - has to element of neiboughs
    @return edge - has to be element in edges
    """
    def getEdge(self, v):
        for edge in self.edges:
            if v == edge.p1 or v == edge.p2:
                return edge
    def getSaturated(self):
        return self.saturated
    def setSaturated(self,boolean):
        self.saturated = boolean
        if boolean == False:
            self.matchingVertex = None
    def makeMatch(self,v):
        self.matchingVertex = v
        v.matchingVertex = self
        self.saturated = True
        v.saturated = True

    
        
