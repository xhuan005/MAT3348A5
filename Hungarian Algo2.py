# -*- coding: utf-8 -*-
"""
@author: Xiaopei Huang, Xuankai Chen
"""
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button

"""
Let g be a graph
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


class HungarianAlgorithm:
    def __init__(self, g):
        self.g = g
        self.V = g.nodes
        self.X = g.graph['X']
        self.Y = g.graph['Y']
        self.visited = dict.fromkeys(self.V, False)  # record visited status in constructing M-alternating tree
        self.mAlternatingTree = nx.Graph()
        self.next = 1

    def doesMSaturateX(self):
        '''
        Check if M saturates X in g
        :return: True if M saturates X and False otherwise
        '''
        return all(self.V[x]['saturated'] for x in self.X)

    def initialMatching(self):
        for x in self.X:  # loop through all element of x. x is only the key
            # g.graph['X'] = {0, 1, 2, 3, 4}
            for y in self.g[x]:  # loop through all neighbor of x. y is a key
                if self.V[y]['saturated'] == False:  # find a neighbor that is not saturated
                    # match x and y
                    self.V[x]['saturated'] = True
                    self.V[y]['saturated'] = True
                    self.V[y]['matchingVertex'] = x
                    self.V[x]['matchingVertex'] = y
                    self.g[x][y]['match'] = True
                    self.g[x][y]['color'] = setEdgeColor(self.g[x][y]['match'],
                                                         self.g[x][y]['path'])  # set color for visual
                    self.drawGraph()
                    break

    def getFirstUnsaturatedX(self):
        '''
        Get the first M-unsaturated vertex in X. Return None if there is no such vertex.
        :return: The first M-unsaturated vertex in X and None if no such vertex exists.
        '''
        return next((x for x in self.X if not self.V[x]['saturated']), None)

    def getMAlternatingTree(self, u, needEdgeInM):
        '''
        Use DFS to construct an M-alternating tree.
        :param u: The current vertex
        :param needEdgeInM: True if the child vertex needs to be M-saturated and False otherwise
        '''
        self.visited[u] = True
        for v in sorted(self.g[u]):
            if not self.visited[v] and (needEdgeInM == (self.V[u]['matchingVertex'] == v)):
                self.mAlternatingTree.add_edge(u, v)
                self.getMAlternatingTree(v, not needEdgeInM)

    def enlargeM(self, u):
        '''
        Enlarge M with a (u, y)-path if there is one.
        :param u: The root of the M-alternating tree
        '''
        # T = intersection of V(mAlternatingTree) and Y
        # T contains an M-unsaturated vertex y different from u.
        T = sorted(set(self.mAlternatingTree.nodes.keys()) & self.Y)
        mUnsaturatedY = next((y for y in T if not self.V[y]['saturated']), None)
        if mUnsaturatedY:  # An M-unsaturated y exists. Enlarge M.
            uyPath = next(nx.all_simple_paths(self.mAlternatingTree, u, mUnsaturatedY), None)
            if uyPath:
                print('The ({}, {}) path is {}'.format(u, mUnsaturatedY, uyPath))
                # For every two vertices, update the matching properties (saturated, matchingVertex)
                # of it and the next vertex in the (u, y)-path.
                for i in range(0, len(uyPath), 2):
                    # Clear current matching
                    if i != 0:
                        prevEdge = self.g[uyPath[i]][self.V[uyPath[i]]['matchingVertex']]
                        prevEdge['match'] = False
                        prevEdge['path'] = True
                        prevEdge['color'] = setEdgeColor(False, True)
                        print(uyPath[i], uyPath[i + 1], prevEdge['color'])
                        self.drawGraph()

                    vProps = self.V[uyPath[i]]
                    vProps['saturated'] = True
                    vProps['matchingVertex'] = uyPath[i + 1]

                    nextVProps = self.V[uyPath[i + 1]]
                    nextVProps['saturated'] = True
                    nextVProps['matchingVertex'] = uyPath[i]

                    edge = self.g[uyPath[i]][uyPath[i + 1]]
                    edge['match'] = True
                    edge['path'] = True
                    edge['color'] = setEdgeColor(True, True)
                    print(uyPath[i], uyPath[i + 1], edge['color'])
                    self.drawGraph()

                    print('{{{}, {}}} is marked M-saturated'.format(uyPath[i], uyPath[i + 1]))

                # Cleanup the path
                for i in range(len(uyPath)):
                    edge = self.g[uyPath[i]][uyPath[i + 1]]
                    edge['path'] = False
                    edge['color'] = setEdgeColor(edge['match'], False)
                    print(uyPath[i], uyPath[i + 1], edge['color'])
                    self.drawGraph()

    def getMatching(self):
        '''
        Get the current matching in G in pairs of vertices.
        :return: A list of pairs of vertices representing edges in the current matching
        '''
        return [{x, self.V[x]['matchingVertex']} for x in sorted(self.X)]

    def start(self):
        if len(self.X) != len(self.Y):
            print("|X| != |Y| ==> impossible to have a perfect matching")

        self.drawGraph()
        self.initialMatching()  # initial matching.
        print('The initial matching is:', self.getMatching())

        while not self.doesMSaturateX():
            # Choose the first M-unsaturated vertex u in X and start searching for M-augmenting paths from u
            u = self.getFirstUnsaturatedX()
            self.visited = dict.fromkeys(self.V, False)
            self.getMAlternatingTree(u, False)
            print(self.mAlternatingTree.edges)

            if len(self.mAlternatingTree):
                self.enlargeM(u)
                self.mAlternatingTree.clear()
            else:
                print('Impossible to have a perfect matching')
                break

        print('The final matching is:', self.getMatching())

    def drawGraph(self):
        self.next = 1
        colors = [self.g[u][v]['color'] for u, v in self.g.edges()]

        # Specify positions of vertices in bipartitions X and Y in the drawing
        pos = dict(list({v: (i, 1) for i, v in enumerate(sorted(self.X))}.items()) +
                   list({v: (i, 2) for i, v in enumerate(sorted(self.Y))}.items()))

        nx.draw(self.g, pos=pos, with_labels=True, edge_color=colors, width=5)

        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(self.nextButton)

        plt.show()

    def nextButton(self, event):
        self.next = 0
        plt.close()


def createBipartiteGraph(adjacencyList):
    """
    @purpose:  created a bipartite graph using adjacencyList
               index number is set X and element in each array is set Y
    @param: adjacencyList
    """
    g = nx.Graph()  # create nx graph
    for i in range(len(adjacencyList)):
        g.add_node(i, bipartite=0, saturated=False, matchingVertex=None)
        # i is the key for node with param(bipartite:integer, saturated:bool, matchingVertex:node)
        for e in adjacencyList[i]:
            g.add_node(e, bipartite=1, saturated=False, matchingVertex=None)
            g.add_edge(i, e, match=False, path=False, color='black')  # path may or may not need
            # (i,e) are endpoints of edge with param (match:bool, path:bool, color:string)
    g.graph.update(X=nx.bipartite.sets(g)[0], Y=nx.bipartite.sets(g)[1])
    # set param(x: all node with bipartite = 0, y:all nodes with bipartite = 1)
    return g


def nsEqualT(g, s, t):
    """
    @purpose test N(S) = T condition
    @return ?N(S) = T :bool
    @sNeighbor - t : set of N(S) which not in T
    """
    sNeighbor = set()  # init s neighbor
    for x in s:
        for y in g[x]:
            sNeighbor.add(y)
    return (sNeighbor == t, sNeighbor - t)


def setEdgeColor(match, path):
    if (match == True and path == True):
        return 'orange'
    elif (match == True and path == False):
        return 'red'
    elif (match == False and path == True):
        return 'yellow'
    elif (match == False and path == False):
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
    for x in g.graph['X']:  # find all unSaturatedX
        if g.nodes[x]['saturated'] == False:
            unSaturatedX.append(x)
    for y in g.graph['Y']:  # find all unSaturatedY
        if g.nodes[y]['saturated'] == False:
            unSaturatedY.append(y)
    if (len(unSaturatedX) == len(unSaturatedY) == 0):  # if both list is empty return true
        perfect = True
    return (perfect, unSaturatedX, unSaturatedY)


if __name__ == '__main__':
    # input List - needs to find way to input.
    inputAdjacencyList = [["a", "b", "c"], ["a", "b"], ["a", "d", "e"], ["d"], ["a", "d"]]
    g = createBipartiteGraph(inputAdjacencyList)
    for item in g.adj.items():
        print(item)
    # print(g.graph['y'])
    # top = nx.bipartite.sets(g)[0]
    # pos = nx.bipartite_layout(g,top)
    # colors = [g[u][v]['color'] for u,v in g.edges()]
    # print(colors)
    # nx.draw(g,pos,with_labels = True,edge_color = colors )
    # nx.draw_networkx_edges(g,pos)

    # print(g.edges())
    # print(list(g.nodes(data=True)))
    HungarianAlgorithm(g).start()  # start algorithm
