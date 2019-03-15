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
    def __str__(self):
        return self.key
    def __repr__(self):
        return self.key
    def insertNeighbor(self,neighbor):
        if neighbor in self.neighbors:
            print("FAIL! this neighbor is already added")
        elif neighbor.group == self.group:
            print("FAIL! this vertex is in the same group as target vertex")
        else:
            self.neighbors.append(neighbor)
            edge = Edge(self,neighbor)
            self.edges.append(edge)
            
        
