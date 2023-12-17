# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:23:11 2023

@author: Martin
"""


''' this file implements a directed graph with the A* algorithm '''

''' implement A* algorithm, follow example from https://de.wikipedia.org/wiki/A*-Algorithmus '''

''' A* has wort-case time complexity O(V^2), V=amount of nodes '''
''' implement openlist as binary heap '''
''' optimize algorithm via openlist.decreasekey, so time complexity becomes O(log(V)*V) '''

from termcolor import colored


def assert_edge(func):
    def check_edge(self, edge):
        ''' checks if edge is the of type Edge '''
        assert isinstance(edge, Edge)
        output = func(self, edge)
        return output
    return check_edge

def assert_node(func):
    def check_node(self, node, move, weight):
        ''' checks if node is the of type Node '''
        assert isinstance(node, Node)
        output = func(self, node, move, weight)
        return output
    return check_node


class Edge:
    
    COUNTID = 0
    
    # INIT #
    @assert_node
    def __init__(self, destination_node, move, weight: int=1):
        self.id = 0
        self.destination = destination_node
        self.move = move
        self.weight = weight
    
        self.id = Edge.COUNTID
        Edge.COUNTID = Edge.COUNTID + 1

    # MAGIC METHODS #
    def __repr__(self):
         return f"Edge {self.id}: to {self.destination}"

class Node: # or Vertex
    
    COUNTID = 0

    # INIT #
    def __init__(self, board):
        self.id = 0
        self.board = board
        self.edge_list = []
        self.f = 0 # f value, guesses the length of path to target
        self.g = 0 # g value, gives the number of nodes from root node
        self.h = self.calculate_h() # h value, guessed cost from current node to target
        self.predecessor = None
        
        self.id = Node.COUNTID
        Node.COUNTID = Node.COUNTID + 1
        
    # MAGIC METHODS #
    def __repr__(self):
         return f"Node {colored(self.id, 'cyan')}"
     
    # FUNCTIONS #
    def calculate_h(self) -> int:
        ''' change the h value of the node '''
        
        ''' if card is on pile: 0 points
            if card is on fcs: 1 point
            if card is on stack: 
                unordered: 2 points
                ordered: 1 point '''
        h = 0
        #pile = self.board.pile
        fcs = self.board.fcs
        stacks = self.board.stacks
        # dont add anything for the pile
        for key in fcs.fcs:
            if fcs.fcs[key]: # if there is a card
                h += 1
        '''for stack in stacks:
            ordered = stack.takable
            unordered = len(stack.stack) - ordered
            h += ordered
            h += sum(range(2,unordered+2))
            #h += 2*unordered'''
        for stack in stacks:
            for i, card in enumerate(stack.stack):
                h += card.rank + (stack.length-i)
        return h
        
        
class Graph:
    ''' Directed graph '''
    
    # INIT #
    def __init__(self):
        self.node_list = []
        
        self.root = None # id of node to start with
        self.target = None # id of node to stop
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
                
            
    
    def add_edge(self, node1, node2, move, weight: int=1):
        edge = Edge(node2, move, weight)
        node1.edge_list.append(edge) # node2.edge_list.append(Edge(node1, weight))
        return edge
    
    def remove_edge(self, number: int) -> None:
        for node in self.node_list:
            for edge in node.edge_list:
                if edge.id == number:
                    node.edge_list.remove(edge)
                    print(f"Edge {number} removed.")
    
        
    def assemble(self) -> None:
        ''' Starting with root, explore the board and add corresponding edges on the go.
        Use A* to determine which node to explore next.
        Stop at the first time the target node is reached. '''
        
        target = self.target
        root = self.root
        
        # INITIALIZATION #
        step = 0
        solved = False
        target_found = False
        
        print(f"\n{colored('Step ' + str(step), 'white', 'on_yellow')}.\n")
        print("Initializing open list.")
        
        # put root node into open list
        self.open.append(root)
        
        step = step + 1
        
        # while there is no edge to the root node, explore
        while 1: # not target_found:
            print(f"\n{colored('Step ' + str(step), 'white', 'on_yellow')}.\n")
            
            # sort list by lowest f-Value
            self.open.sort(key=lambda x: x.f)
            prev_node = self.open[0]
            print(f"Next investigated Node with lowest f-Value is {prev_node}.")
            print(prev_node.board)
            
            # if target node is investigated, lowest f-Value is found
            if prev_node == target:
                solved = True
                print(f"{colored('Target found!', 'white', 'on_blue')} \n Reached {prev_node} with f-Value {colored(prev_node.f, 'green')}.\n\n")
                break
            
            # get all possible move from the node
            moves = prev_node.board.get_all_moves()
            
            # calculate f-Values for all successor nodes
            for move in moves:
                ## GRAPH CONSTRUCTION
                # see where the move takes you, check through all nodes in graph to detect cycles
                print(f"\nExecuting the move.")
                successor = Node(board=move())
                
                # check if the target is found!
                if successor.board == target.board:
                    print(f"{colored('Found target board!', 'white', 'on_blue')}")
                    target_found = True
                    successor = target
                
                # do not add node if the board is already in node_list
                add_it = True
                #if any([node.board == successor.board for node in self.node_list]):
                for node in reversed(self.node_list):
                    if node.board == successor.board:    
                        add_it = False
                        print(f"Successor {successor} was already in graph.node_list.")
                if add_it:
                    self.add_node(successor)
                    print(f"Successor {successor} put in graph.node_list. h={colored(successor.h, 'yellow')}.")
                   
                # do add edge to the node
                this_edge = self.add_edge(prev_node, successor, move)
                print(f"Added new Edge from {prev_node} to {successor}.")
                
                
                ## A* ALGORITHM
                # calculate g and f values for the successor
                successor.f = prev_node.g + this_edge.weight + successor.h
                successor.g = prev_node.g + this_edge.weight
                print(f"Calculation of f- and g-Value of {successor}. f={colored(successor.f, 'yellow')}, g={colored(successor.g, 'yellow')}.")
                
                if (add_it or target_found): # if the target node is found, add it to the open_list!
                    # put successor in open and mark predecessor
                    successor.predecessor = prev_node
                    self.open.append(successor)
                    print(f"Put {successor} in open. Marked predecessor of {colored(successor, 'blue')} as {colored(prev_node, 'blue')}.")
                
            
            # remove investigated node from open 
            self.open.pop(0)
            print(f"Remove {prev_node} from open.")
            
            print(self)
            
            step = step + 1
            
    def show(self):
        ''' Show how the target node is reached from root 
            compile all the nodes from target to root '''
        
        show = [self.target]
        
        # compile list from target to root
        while self.root not in show: 
            show.append(show[len(show)-1].predecessor)
        
        # reverse the list
        for node in reversed(show):
            print(node.board)
            print("")
        
        # print the path
        print(f"Solved in {len(show)} moves.")
            
            
                        
from main import Card, Stack, Pile, FC, Board, Solution_Board, Move

print(f"\n{colored('||| ----- GENERATION OF BOARDS ----- |||', 'grey', 'on_green')}\n")

sb = Solution_Board()
print(sb)
b = Board()
print(b)

target = Node(board=sb)
root = Node(board=b)

print(f"\n{colored('||| ----- GENERATION OF GRAPH ----- |||', 'grey', 'on_green')}\n")

g = Graph()

g.add_node(target)
g.add_node(root)

g.target = target # node
g.root = root # node

g.assemble()
#g.show()

''' TIME CALCULATION RESULTS -- OLD HEURISTIC''' 
''' Seed = 5, Stack size = 8, FC amount = 4, Pile size = 4 '''
'''  --> card_amount and steps to solve 
CARD_AMOUNT = 1:        16 setps    5 moves     240 nodes
CARD_AMOUNT = 2:        81 steps    9 moves     1665 nodes
CARD_AMOUNT = 3:        106 steps   14 moves    1815 nodes
CARD_AMOUNT = 4:        232 steps   20 moves    3695 nodes
CARD_AMOUNT = 5:        ? 
CARD_AMOUNT = 6:        58 steps    31 moves    1149 nodes
CARD_AMOUNT = 7:        ? >7500 nodes
CARD_AMOUNT = 8:        ? > 4000 nodes
CARD_AMOUNT = 9:        ? > 10500 nodes
'''

''' TIME CALCULATION RESULTS -- NEW HEURISTIC''' 
''' Seed = 5, Stack size = 8, FC amount = 4, Pile size = 4 '''
'''  --> card_amount and steps to solve 
CARD_AMOUNT = 1:        16 setps    5 moves     224 nodes
CARD_AMOUNT = 2:        13 steps    9 moves     248 nodes
CARD_AMOUNT = 3:        34 steps    18 moves    843 nodes --> nicht schnellster weg!
CARD_AMOUNT = 4:        48 steps    24 moves    1286 nodes --> nicht schnellster weg!
CARD_AMOUNT = 5:        30 steps    27 moves    627 nodes
CARD_AMOUNT = 6:        35 steps    32 moves    638 nodes --> nicht schnellster weg!
CARD_AMOUNT = 7:        57 steps    43 moves    889 nodes
CARD_AMOUNT = 8:        127 steps   50 moves    1656 nodes
CARD_AMOUNT = 9:        168 steps   64 moves    1742 nodes 
CARD_AMOUNT = 10:       167 steps   69 moves    1290 nodes 
CARD_AMOUNT = 11:       1499 steps  77 moves    5299 nodes 
CARD_AMOUNT = 12:       426 steps   107 moves   1709 nodes 
CARD_AMOUNT = 13:       7581 steps  104 moves   11226 nodes 
'''

