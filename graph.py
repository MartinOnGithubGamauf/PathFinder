# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 21:57:25 2023

@author: Martin
"""


''' this file implements a directed graph with the A* algorithm '''


def assert_edge(func):
    def check_edge(self, edge):
        ''' checks if edge is the of type Edge '''
        assert isinstance(edge, Edge)
        output = func(self, edge)
        return output
    return check_edge

def assert_node(func):
    def check_node(self, node):
        ''' checks if node is the of type Node '''
        assert isinstance(node, Node)
        output = func(self, node)
        return output
    return check_node


class Edge:
    
    COUNTID = 0
    
    # INIT #
    @assert_node
    def __init__(self, destination_node):
        self.id = 0
        self.destination = destination_node
        self.weigth = 1
    
        self.id = Edge.COUNTID
        Edge.COUNTID = Edge.COUNTID + 1

    # MAGIC METHODS #
    def __repr__(self):
         return f"Edge {self.id}: to {self.destination}"

class Node: # or Vertex
    
    COUNTID = 0

    # INIT #
    def __init__(self):
        self.id = 0
        self.name = "0"
        self.edge_list = []
        self.f = 0 # f value, guesses the length of path to target
        self.g = 0 # g value, gives the number of nodes from root node
        self.h = 0 # h value, guessed cost from current node to target
        
        self.id = Node.COUNTID
        Node.COUNTID = Node.COUNTID + 1
        
    # MAGIC METHODS #
    def __repr__(self):
         return f"Node {self.id}"
     
    # FUNCTIONS #
    def calculate_f(self):
        self.f = self.g + self.h
    
    def add_edge(self, edge):
        pass
    
        
class Graph:
    ''' Directed graph '''
    
    # INIT #
    def __init__(self):
        '''self.root = 0
        self.target = 0
        self.open = []
        self.closed = []'''
        self.nodes_list = []
        
    # MAGIC METHODS #
    def __repr__(self):
        return f"Graph with \n Nodes: {self.nodes_list} \n Edges: {[n.edge_list for n in self.nodes_list]}"
        
    # FUNCTIONS #
    def add_node(self, node) -> None:
        return self.nodes_list.append(node)
    
    def remove_node(self, number: int) -> None:
        pass
    
    def add_edge(self, node1, node2):
        return node1.edge_list.append(Edge(node2)) and node2.edge_list.append(Edge(node1))
    
    def remove_edge(self, number: int) -> None:
        pass


g = Graph()

n0 = Node()
n1 = Node()
n2 = Node()
n3 = Node()

g.add_node(n0)
g.add_node(n1)
g.add_node(n2)
g.add_node(n3)

g.add_edge(n0, n1)
g.add_edge(n1, n2)
g.add_edge(n2, n3)
g.add_edge(n2, n0)
g.add_edge(n3, n1)

print(g)


    