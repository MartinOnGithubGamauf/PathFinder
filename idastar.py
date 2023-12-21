# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 21:49:12 2023

@author: marti
"""

# IMPLEMENTATION OF IDA* (iterative deepening A*) ALGORITHM

# better memory usage than A*



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
        self.discovered = False
        
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
                    
    def solve_dfs(self):
        ''' solve graph with recursive depth first search '''
        
        step = 0
        
        def dfs(self, node):
            
            nonlocal step
            step = step + 1
            
            print(f"\nStep {step}.\n")
            
            print(f"Label {node} as discovered.")
            node.discovered = True
            
            # iterate through all following edges
            for edge in node.edge_list:
                print(f"Checking {edge} with destination {edge.destination}.")
                
                # check if destination has already be visited
                if not edge.destination.discovered:
                    
                    print(f"{edge.destination} has not been visited.")
                    dfs(self, edge.destination)
        
        print("\nStarting recursive DFS with root node.")
        dfs(self, self.node_list[self.root])
        
                    
    def solve_ida(self):
        pass
                
        
if __name__=='__main__':
    
    g = Graph()
    
    n0 = Node(name="A", h=0)
    n1 = Node(name="B", h=0)
    n2 = Node(name="C", h=0)
    n3 = Node(name="D", h=0)
    n4 = Node(name="E", h=0)
    n5 = Node(name="F", h=0)
    n6 = Node(name="G", h=0)
    
    g.add_node(n0)
    g.add_node(n1)
    g.add_node(n2)
    g.add_node(n3)
    g.add_node(n4)
    g.add_node(n5)
    g.add_node(n6)
    
    g.add_edge(n0, n1, 0)
    g.add_edge(n0, n2, 0)
    g.add_edge(n0, n4, 0)
    g.add_edge(n1, n3, 0)
    g.add_edge(n1, n5, 0)
    g.add_edge(n2, n6, 0)
    g.add_edge(n5, n4, 0)
    
    print(g)
    
    g.root = 0 # A
    
    g.solve_dfs()
    
    
    
    