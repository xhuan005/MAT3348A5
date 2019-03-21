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

    def __init__(self, key, group):
        self.key = key
        self.group = group
        self.neighbors = []
        self.edges = []
        self.saturated = False
        self.matchingVertex = None  # not null only when saturated is true

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return str(self.key)

    """
    insertNeighbor
    @param neighbor: Vertex
    @return: void
    @ insert a vertex as neighbor and create an edge. Edge is also put into 
    list of edges
    """

    def insertNeighbor(self, neighbor):
        if neighbor in self.neighbors:
            print("FAIL! this neighbor is already added")
        elif neighbor.group == self.group:
            print("FAIL! this vertex is in the same group as target vertex")
        else:
            self.neighbors.append(neighbor)
            edge = Edge(self, neighbor)
            self.edges.append(edge)
            # add self to neighbor's neighbor list
            neighbor.neighbors.append(self)
            neighbor.edges.append(edge)

    """
    getEdge
    @param v:vertex - has to element of neiboughs
    @return edge - has to be element in edges
    """

    def getEdge(self, v):
        for edge in self.edges:
            if v == edge.v1 or v == edge.v2:
                return edge

    def getSaturated(self):
        return self.saturated

    def setSaturated(self, boolean):
        self.saturated = boolean
        if boolean == False:
            self.matchingVertex = None  # if we set saturted to false we have to null out the matching Vertex

    # Match 2 vertex
    def makeMatch(self, v):
        if v not in self.neighbors:
            print("v is not in neighbors")
        self.matchingVertex = v
        v.matchingVertex = self
        self.saturated = True
        v.saturated = True


class Edge:
    """
    @params
        v1:Vertex
        v2:Vertex
        isMatch:boolean
    """

    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2
        self.isMatch = False

    def __str__(self):
        return "(" + str(self.v1) + "," + str(self.v2) + ")"

    def __repr__(self):
        return "(" + str(self.v1) + "," + str(self.v2) + ")"


class BipartiteGraph:
    """
    @param adjList:List List
            index of out list is key for vertex group is S
            value in inniner list is key for vertex Group T
            
            Example[["a","b","c"],["a","d","e"]] 
            v0 is connect with va,vb,vc
            v1 is connected with vd,ve
            
            
    """

    def __init__(self, adjList):
        self.S = []  # set S
        self.T = []  # set T
        self.edges = []  # set of Edges consider removing
        self.initSets(adjList)

    def initSets(self, adjList):
        for i in range(len(adjList)):
            vertex = Vertex(i, "S")
            self.S.append(vertex)
            print("evaluating S " + str(vertex))

            for neighborStr in adjList[i]:
                vertNei = None
                # check if neighbor already in list T
                for t in self.T:
                    if neighborStr == t.key:
                        print(neighborStr + " vertex already in T ")
                        vertNei = t
                        break
                if vertNei == None:
                    print(neighborStr + " is not in T adding vertex")
                    vertNei = Vertex(neighborStr, "T")
                    self.T.append(vertNei)
                vertex.insertNeighbor(vertNei)
                edge = vertex.getEdge(vertNei)
                self.edges.append(edge)

    def __repr__(self):
        s = "S:["
        for v in self.S:
            s = s + str(v) + ","
        s = s + "]"
        t = "T:["
        for v in self.T:
            t = t + str(v) + ","
        t = t + "]"
        e = "E:["
        for edge in self.edges:
            e = e + str(edge)
        e = e + "]"
        return s + "\n" + t + "\n" + e + "\n"


def runHungarianAlgo(g):
    if len(g.S) != len(g.T):
        print(
            "Since the |S| = " + str(len(g.S)) + " and the |T| = " + str(len(g.T)) + ". There is not perfect matching)")
    initialMatching(g)
    printMatching(g)


def initialMatching(g):
    for s in g.S:
        for t in s.neighbors:
            if t.saturated == False:
                s.makeMatch(t)
                break


def printMatching(g):
    m = ""
    for s in g.S:
        if s.saturated == True:
            matchingEdge = s.getEdge(s.matchingVertex)
            m = m + str(matchingEdge)
    print(m)


graph = BipartiteGraph([["a", "b", "c"], ["a", "d", "e"]])
print(str(graph))

runHungarianAlgo(graph)
