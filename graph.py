# -*- coding: utf-8 -*-
"""
Created on Fri Dec  1 21:57:25 2023

@author: Martin
"""


''' this file implements a directed graph with the A* algorithm '''

''' implement A* algorithm, follow example from https://de.wikipedia.org/wiki/A*-Algorithmus '''


from termcolor import colored


def assert_edge(func):
    def check_edge(self, edge):
        ''' checks if edge is the of type Edge '''
        assert isinstance(edge, Edge)
        output = func(self, edge)
        return output
    return check_edge

def assert_node(func):
    def check_node(self, node, weight):
        ''' checks if node is the of type Node '''
        assert isinstance(node, Node)
        output = func(self, node, weight)
        return output
    return check_node


class Edge:
    
    COUNTID = 0
    
    # INIT #
    @assert_node
    def __init__(self, destination_node, weight: int):
        self.id = 0
        self.destination = destination_node
        self.weight = weight
    
        self.id = Edge.COUNTID
        Edge.COUNTID = Edge.COUNTID + 1

    # MAGIC METHODS #
    def __repr__(self):
         return f"Edge {self.id}: to {self.destination}"

class Node: # or Vertex
    
    COUNTID = 0

    # INIT #
    def __init__(self, name: str, h: int):
        self.id = 0
        self.name = name
        self.edge_list = []
        self.f = 0 # f value, guesses the length of path to target
        self.g = 0 # g value, gives the number of nodes from root node
        self.h = h # h value, guessed cost from current node to target
        self.predecessor = 0
        
        self.id = Node.COUNTID
        Node.COUNTID = Node.COUNTID + 1
        
    # MAGIC METHODS #
    def __repr__(self):
         return f"Node {self.id} - {colored(self.name, 'cyan')}"
     
    # FUNCTIONS #
    def calculate_f(self):
        self.f = self.g + self.h
    
    def add_edge(self, edge):
        pass
    
        
class Graph:
    ''' Directed graph '''
    
    # INIT #
    def __init__(self):
        self.node_list = []
        
        self.root = 0 # id of node to start with
        self.target = 0 # id of node to stop
        self.open = []
        self.closed = []
        
    # MAGIC METHODS #
    def __repr__(self):
        return f"Graph with \n Nodes: {self.node_list} \n Edges: {[n.edge_list for n in self.node_list]}"
        
    # FUNCTIONS #
    def add_node(self, node) -> None:
        return self.node_list.append(node)
    
    def remove_node(self, number: int) -> None:
        for node in self.node_list:
            if node.id == number:
                edges = node.edge_list
                for edge in edges:
                    self.remove_edge(edge.id)
                
                self.node_list.remove(node)
                print(f"Node {number} removed.")
                
            
    
    def add_edge(self, node1, node2, weight: int):
        return node1.edge_list.append(Edge(node2, weight)) # node2.edge_list.append(Edge(node1, weight))
    
    def remove_edge(self, number: int) -> None:
        for node in self.node_list:
            for edge in node.edge_list:
                if edge.id == number:
                    node.edge_list.remove(edge)
                    print(f"Edge {number} removed.")
                    
    def solve(self):
        
        step = 0
        solved = False
        
        print(f"\nStep {step}.\n")
        print("Initializing open list.")
        
        # put root node into open list
        for node in self.node_list:
            if node.id == self.root:
                self.open.append(node)
        # put all successor nodes into loop
        #prev_node = self.closed[len(self.closed)-1] # last edge in closed
        
        
        step = step + 1
        
        while not solved:
            
            print(f"\nStep {step}.\n")
            
            # sort list by lowest f-Value
            self.open.sort(key=lambda x: x.f)
            prev_node = self.open[0]
            print(f"Next investigated Node with lowest f-Value is {prev_node}.")
            
            # if target node is investigated, lowest f-Value is found
            if prev_node.id == self.target:
                solved = True
                print(f"Target found! \n Reached {prev_node.name} with f-Value {colored(prev_node.f, 'green')}.")
                break
            
            # calculate f-Values for successor nodes
            for edge in prev_node.edge_list:
                
                successor = edge.destination
                # check if successor has already been investigated
                if successor in self.closed:
                    break
                
                # calculate g and f values for the successor
                successor.f = prev_node.g + edge.weight + successor.h
                successor.g = prev_node.g + edge.weight
                print(f"Calculation of f- and g-Value of {successor.name}. f={colored(successor.f, 'yellow')}, g={colored(successor.g, 'yellow')}.")
                
                # put successor in open and mark predecessor
                successor.predecessor = prev_node
                self.open.append(successor)
                print(f"Put {successor.name} in open. Marked predecessor of {colored(successor.name, 'blue')} as {colored(prev_node.name, 'blue')}.")
                
            
            # put investigated node from open to closed
            self.closed.append(self.open.pop(0))
            print(f"Put {prev_node.name} from open to closed.")
            
            
            step = step + 1
                
            
                        
from main import Card, Stack, Pile, FC, Board, Solution_Board, Move



b = Board()

            


g = Graph()

n0 = Node(name="Saarbrücken", h=222)
n1 = Node(name="Kaiserslautern", h=158)
n2 = Node(name="Frankfurt", h=96)
n3 = Node(name="Ludwigshafen", h=108)
n4 = Node(name="Karlsruhe", h=140)
n5 = Node(name="Würzburg", h=0)
n6 = Node(name="Heilbronn", h=87)

g.add_node(n0)
g.add_node(n1)
g.add_node(n2)
g.add_node(n3)
g.add_node(n4)
g.add_node(n5)
g.add_node(n6)

g.add_edge(n0, n1, 70)
g.add_edge(n0, n4, 145)
g.add_edge(n1, n2, 103)
g.add_edge(n1, n3, 53)
g.add_edge(n2, n5, 116)
g.add_edge(n3, n5, 183)
g.add_edge(n4, n6, 84)
g.add_edge(n5, n5, 102)

print(g)

g.root = 0 # Saarbrücken
g.target = 5 # Würzburg

g.solve()

    