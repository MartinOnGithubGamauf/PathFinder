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

''' implement Heuristic class '''
# Manhatten Heuristic for 15-tile puzzle: 
'''the Manhattan distance heuristic: for each movable tile, the number of grid units
between the current position of the tile and its goal position are computed, and
these values are summed for all tiles.'''
# edge branching factor, node branching factor -> for 15-tile: ebf slighly grater than nbf -> good for IDA*

from termcolor import colored
from heapq import heappush, heappop
from main import assert_other

PRINT_BOARD_AND_GRAPH = True
PRINT_INFOS = True

# PRINTS #
def print_board_and_graph(obj):
    if PRINT_BOARD_AND_GRAPH:
        print(obj)
    return

def print_info(obj):
    if PRINT_INFOS:
        print(obj)
    return

# WRAPPERS #

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
    H_VERSION = "exp"

    # INIT #
    def __init__(self, board):
        self.id = 0
        self.board = board
        self.edge_list = []
        self.f = 0 # f value, guesses the length of path to target
        self.g = 0 # g value, gives the number of nodes from root node
        self.h = self.calculate_h() # h value, guessed cost from current node to target
        self.predecessor = None
        self.predecessor_move = None
        
        self.id = Node.COUNTID
        Node.COUNTID = Node.COUNTID + 1
        
    # MAGIC METHODS #
    def __repr__(self):
         return f"Node {colored(self.id, 'cyan')}"
    
    @assert_other
    def __lt__(self, other):
        return self.f < other.f
        
    # FUNCTIONS #
    def calculate_h(self) -> int:
        ''' change the h value of the node '''
        # idea: charge 1 point for cards that are takable AND are only 1 higher than the card on the pile!
        # so 2 of hearts is noly 1 move away of going onto ace of hearts on the pile,
        # while 3 of hearts is 2 moves away (if it is also takable)
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
        if Node.H_VERSION == "exp":
            ''' add 1 point for each card on the board which is not in the pile '''
            ''' if on the stack there the cards are ordered, do not add anything to h '''
            ''' from the bottom of the stack (index [0]) to the top (index [-1]), add 
                1 to h if the card beneath is greater than the one on top '''
            # Card in Freecells
            for key in fcs.fcs:
                if fcs.fcs[key]: # if there is a card
                    h += 1
            # Card in Stacks
            for stack in stacks:
                l = len(stack.stack)
                h += l 
                # if card on top is greater, add 1 --> THIS HAS TO CHECK EACH AND 
                #                                      EVERY CARD, NOT JUST 2 CARD 
                #                                      RIGHT ON TOP OF EACH OTHER
                #                                      --> use 2 Pointers Method
                if l >= 0:
                    for i in range(l-1):
                        bottom = stack.stack[i]
                        top = stack.stack[i+1]
                        if (top.rank > bottom.rank and top.suit == bottom.suit):
                            h += 1
        else:
            raise ValueError("Version of heuristic is not set correctly.")
        return h
    
            
class Graph:
    ''' Directed graph '''
    
    # INIT #
    def __init__(self):
        self.node_list = []
        
        self.root = None # id of node to start with
        self.target = None # id of node to stop
        
        self.open = []
        
        self.stack = []
        
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
                print_info(f"Node {number} removed.")
                
            
    
    def add_edge(self, node1, node2, move, weight: int=1):
        edge = Edge(node2, move, weight)
        node1.edge_list.append(edge) # node2.edge_list.append(Edge(node1, weight))
        return edge
    
    def remove_edge(self, number: int) -> None:
        for node in self.node_list:
            for edge in node.edge_list:
                if edge.id == number:
                    node.edge_list.remove(edge)
                    print_info(f"Edge {number} removed.")
    
    def assemble_A(self) -> None:
        ''' Starting with root, explore the board and add corresponding edges on the go.
        Use A* to determine which node to explore next.
        Stop at the first time the target node is reached. '''
        
        target = self.target
        root = self.root
        
        # INITIALIZATION #
        step = 0
        solved = False
        target_found = False
        
        print_info(f"\n{colored('Step ' + str(step), 'white', 'on_yellow')}.\n")
        print_info("Initializing open list.")
        
        # put root node into open list
        heappush(self.open, root)
        
        step = step + 1
        
        # while there is no edge to the root node, explore
        while 1: # not target_found:
            print(f"\n{colored('Step ' + str(step), 'white', 'on_yellow')}.\n")
            
            ## sort list by lowest f-Value
            #self.open.sort(key=lambda x: x.f)
            prev_node = heappop(self.open)
            print_info(f"Next investigated Node with lowest f-Value is {prev_node}.")
            print_board_and_graph(prev_node.board)
            
            # if target node is investigated, lowest f-Value is found
            if prev_node == target:
                solved = True
                print_info(f"{colored('Target found!', 'white', 'on_blue')} \n Reached {prev_node} with f-Value {colored(prev_node.f, 'green')}.\n\n")
                break
            
            # get all possible move from the node
            moves = prev_node.board.get_all_moves()
            
            # calculate f-Values for all successor nodes
            for move in moves:
                ## GRAPH CONSTRUCTION
                # see where the move takes you, check through all nodes in graph to detect cycles
                print_info(f"\nExecuting the move.")
                successor = Node(board=move())
                
                # check if the target is found!
                if successor.board == target.board:
                    print_info(f"{colored('Found target board!', 'white', 'on_blue')}")
                    target_found = True
                    successor = target
                
                # do not add node if the board is already in node_list
                add_it = True
                #if any([node.board == successor.board for node in self.node_list]):
                for node in reversed(self.node_list):
                    if node.board == successor.board:    
                        add_it = False
                        print_info(f"Successor {successor} was already in graph.node_list.")
                if add_it:
                    self.add_node(successor)
                    print_info(f"Successor {successor} put in graph.node_list. h={colored(successor.h, 'yellow')}.")
                   
                # do add edge to the node
                this_edge = self.add_edge(prev_node, successor, move)
                print_info(f"Added new Edge from {prev_node} to {successor}.")
                
                
                ## A* ALGORITHM
                # calculate g and f values for the successor
                successor.f = prev_node.g + this_edge.weight + successor.h
                successor.g = prev_node.g + this_edge.weight
                print_info(f"Calculation of f- and g-Value of {successor}. f={colored(successor.f, 'yellow')}, g={colored(successor.g, 'yellow')}.")
                
                if (add_it or target_found): # if the target node is found, add it to the open_list!
                    # put successor in open and mark predecessor
                    successor.predecessor = prev_node
                    successor.predecessor_move = move
                    heappush(self.open, successor)
                    print_info(f"Put {successor} in open. Marked predecessor of {colored(successor, 'blue')} as {colored(prev_node, 'blue')}.")
                
            
            # remove investigated node from open - done by heap
            print_info(f"Removed {prev_node} from open.")
            
            print_board_and_graph(self)
            
            step = step + 1
            
        
    def assemble_IDA(self) -> None:
        ''' Starting with root, explore the board and add corresponding edges on the go.
        Use IDA* to determine which node to explore next.'''
        
        target = self.target
        root = self.root
        
        # INITIALIZATION #
        def track(func):
            level = 0
            def wrapper(*args, **kwargs):
                nonlocal level
                print(f"\nIn: {colored(level, 'magenta')}")
                level += 1
                ret = func(*args, **kwargs)
                level -= 1
                print(f"Out: {colored(level, 'magenta')}\n")
                return ret
            return wrapper
        
        step = 0
        found = False
        INF = 10000
        FOUND = -999999
        
        print(f"\nStep {step}.\n")
        print("Setting bound to h(root) and putting root in the stack.")
        bound = root.h
        self.stack.append(root)
        
        @track
        def search(stack, g, bound):
            nonlocal found, target, INF, FOUND
            print(f"{colored('Entering search:', 'yellow')} current g={g}, current bound={bound}.")
            
            node = stack[-1] # last node in stack
            print(f"{colored('Node points to ' + str(node) + '.', 'red', 'on_white')}")
            node.g = g
            node.f = g + node.h
            print(f"Investigating {node}, it has f-value of {node.f}.")
            if node.f > bound: 
                print("The Node has a higher f-value then bound -> returning.")
                return node.f
            if node.board == target.board: 
                print("We found the Target Node.")
                return FOUND
            print("The Node has a lower f-value then bound -> setting minn to INF")
            minn = INF
            
            ## expand the node and add edges to the graph ##
            moves = node.board.get_all_moves()
            for move in moves:
                successor = Node(board=move())
                # check if the target is found!
                is_target = False
                if successor.board == target.board:
                    print_info(f"{colored('Found target board!', 'white', 'on_blue')}")
                    is_target = True
                    successor = target
                    
                # update g and f value for the successor
                successor.g = g+1
                successor.f = g+1 + successor.h
                
                '''# do not add node if the board is already in node_list
                add_it = True
                #if any([node.board == successor.board for node in self.node_list]):
                #for node_obj in reversed(self.node_list):
                    if node_obj.board == successor.board:    
                        add_it = False
                        #print_info(f"Successor {successor} was already in graph.node_list.")
                        # set the sucessor as the found node!
                        successor = node_obj
                        break
                if add_it:
                    self.add_node(successor)
                    #print_info(f"Successor {successor} put in graph.node_list. h={colored(successor.h, 'yellow')}.")
                '''# do add edge to the node
                self.add_node(successor)
                self.add_edge(node, successor, move)
                #print_info(f"Added new Edge from {node} to {successor}.")
                # mark predecessor
                if True:#(add_it or is_target): # if the node comes up the 2nd time, do not set its predecessor
                    successor.predecessor = node
                    successor.predecessor_move = move
                    #print(f"{colored('Setting predecessor of ' + str(successor) + ' as ' + str(node) + '.', 'red', 'on_white')}")
                
            
            ### IDA* ###
            # order the edge_list based on the lowest destination f-values
            node.edge_list.sort(key=lambda e: e.destination.f)
            
            print(colored("Entering edge iteration.", 'green'))
            print(f"{node} has {len(node.edge_list)} successors: {node.edge_list}")
            
            # choose next successor with lowest f-value
            for edge in node.edge_list:
                
                successor = edge.destination
                print(f"Looking for the next successor with lowest f-value, it is {successor} with f={successor.f}.")
                
                if successor not in stack:
                    print("The successor was not in the stack, adding it now.")
                    stack.append(successor)
                    print("Setting the next t-value to the result of this successor:")
                    t = search(stack, g + edge.weight, bound)
                    print(f"Now we compare the returned t={t} with minn={minn}.")
                    if t == FOUND:
                        print("We found the Target Node (with t).")
                        return FOUND
                    if t < minn:
                        print(f"t-value is smaller than minn -> setting minn to t=minn={t}.")
                        minn = t
                    print(f"Removing the last item from the stack: {stack[-1]}.")
                    stack.pop(-1)
                else:
                    print("The successor was already in the stack, going to next edge and successor.")
                print(f"{colored('After edge iteration', 'green')}, minn={minn}, the stack looks like this: {stack}")
                
            
            print(f"{colored('Iteration of search is done', 'yellow')}, returning minn={minn}.")
            print(f"The stack looks like this: {stack}")
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
            print(f"{colored('Starting search from anew!', 'cyan', 'on_yellow')}, setting bound to t=bound={t}.")
            bound = t
            
            
    def show(self):
        ''' Show how the target node is reached from root 
            compile all the nodes from target to root '''
        
        show = [self.target]
        
        # compile list from target to root
        while self.root not in show: 
            show.append(show[-1].predecessor_move)
            show.append(show[-2].predecessor)
        
        # reverse the list
        for item in reversed(show):
            if isinstance(item, Node):
                node = item
                print(f"{colored('F_VALUE: '+str(node.f)+', G_VALUE: '+str(node.g)+', H_VALUE: '+str(node.h), 'red', 'on_light_blue')}")
                print(node)
                print(node.board)
            if isinstance(item, Move):
                move = item
                print(move)
            print("")
        
        # print the path
        print(f"Solved in {len(show)-1} moves.")
            
            
if __name__ == "__main__":
    from main import Card, Stack, Pile, FC, Board, Solution_Board, Move
    
    print(f"\n{colored('||| ----- GENERATION OF BOARDS ----- |||', 'grey', 'on_green')}\n")
    
    sb = Solution_Board()
    print(sb)
    b = Board(seed=4)
    print(b)
    
    target = Node(board=sb)
    root = Node(board=b)
    
    print(f"\n{colored('||| ----- GENERATION OF GRAPH ----- |||', 'grey', 'on_green')}\n")
    
    g = Graph()
    
    g.add_node(target)
    g.add_node(root)
    
    g.target = target # node
    g.root = root # node
    root.g = 0 # for first iteration of IDA
    root.f = root.g + root.h # for first iteration of IDA
    
    g.assemble_IDA()
    g.show()
    
    ''' TIME CALCULATION RESULTS -- medium HEURISTIC''' 
    ''' Seed = 5, Stack size = 8, FC amount = 4, Pile size = 4 '''
    '''  --> card_amount and steps to solve 
    CARD_AMOUNT = 1:        16 setps    5 moves     240 nodes, 2x: 16 setps    5 moves     202 nodes
    CARD_AMOUNT = 2:        81 steps    9 moves     1665 nodes, 2x: 52 steps    9 moves     922 nodes
    CARD_AMOUNT = 3:        106 steps   14 moves    1815 nodes, 2x: 100 steps   14 moves    1674 nodes
    CARD_AMOUNT = 4:        232 steps   20 moves    3695 nodes
    CARD_AMOUNT = 5:        483 steps   26 moves    9865 nodes
    CARD_AMOUNT = 6:        58 steps    31 moves    1149 nodes
    CARD_AMOUNT = 7:        ? >7500 nodes
    CARD_AMOUNT = 8:        ? > 4000 nodes
    CARD_AMOUNT = 9:        ? > 10500 nodes
    CARD_AMOUNT = 13:       1705 steps  124 moves   6858 nodes, seed = 5
    CARD_AMOUNT = 13:       2408 steps  113 moves   7238 nodes, seed = 4
    CARD_AMOUNT = 13:       3542 steps  112 moves   15248 nodes, seed = 3
    '''
    
    ''' TIME CALCULATION RESULTS -- non-admissable HEURISTIC''' 
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
    
