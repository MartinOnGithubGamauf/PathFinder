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
        self.weight = weight # acts as g value for the successor node
    
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
        # DFS
        self.node_list = []
        self.root = 0 # id of node to start with
        
        # IDA
        self.target = 0 # id of node to end with
        self.stack = [] # represents the search path
        self.path = []
        
        
        
        
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
        ''' solve with pseudocode from https://en.wikipedia.org/wiki/Iterative_deepening_A* '''
        
        step = 0
        found = False
        INF = 10000
        FOUND = -999999
        
        root = self.node_list[self.root]
        target = self.node_list[self.target]
        
        print(f"\nStep {step}.\n")
        print("Setting bound to h(root) and putting root in the stack.")
        bound = root.h
        self.stack.append(root)
        
        def search(stack, g, bound):
            nonlocal found, target, INF, FOUND
            print(f"Current: g={g}, bound={bound}.")
            
            node = stack[len(stack)-1] # last node in stack
            node.f = g + node.h
            print(f"Investigating {node}, it has f-value of {node.f}.")
            if node.f > bound: 
                print("The Node has a higher f-value then bound -> returning.")
                return node.f
            if node == target: 
                print("We found the Target Node.")
                return FOUND
            print("The Node has a lower f-value then bound -> setting minn to INF")
            minn = INF
            
            # order the edge_list based on the lowest destination f-values
            node.edge_list.sort(key=lambda e: e.destination.f)
            
            # choose next successor with lowest f-value
            for edge in node.edge_list:
                
                successor = edge.destination
                print(f"Looking for the next successor with lowest f-value, it is {successor} with {successor.f}.")
                
                if successor not in stack:
                    print("The successor was not in the stack, adding it now.\n")
                    stack.append(successor)
                    print("Setting the next t-value to the result of this successor:")
                    t = search(stack, g + edge.weight, bound)
                    if t == FOUND:
                        print("We found the Target Node (with t).")
                        return FOUND
                    if t < minn:
                        print(f"t-value is smaller than minn -> setting minn to t={t}.")
                        minn = t
                    print(f"Removing {stack[len(stack)-1]} the fist item from the stack.")
                    stack.pop()
                
            return minn
    
        
        print("Entering loop")
        while not found:
            
            t = search(self.stack, 0, bound)
            if t == FOUND:
                found = True
                break
            if t == INF:
                print("t NOT FOUND")
                break
            bound = t
            
            
        
        
        
        
        
                
def example_dfs():
    ''' search through a graph with recursive DFS, from https://en.wikipedia.org/wiki/Depth-first_search'''
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
    
    return g

def example_ida():
    ''' IDA '''
    
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
    
    g.solve_ida()
    
    return g

if __name__=='__main__':
    
    g = example_ida()
    
    