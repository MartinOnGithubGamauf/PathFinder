# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:19:44 2023

@author: Martin
"""

# implement PathFinder Algorithm for use in FreeCell Solver

### SETUP SMALL SCALE FREECELL BOARD

## Definition ungerichteten Graphs

from termcolor import colored

class Stack_Base:
    
    # DECORATORS #
    def update(func):
        def update_stack(self, *args):
            print("")
            print(colored("Stack:", "red") + " Executing function " + colored(func.__name__, 'cyan') + " with args " + colored(args, "cyan"))
            output = func(self, *args)
            self.length = len(self.stack)
            self.takable = self.get_takable()
            print("Stack updated")
            print(self.stack)
            print(f"length: {self.length}")
            print(f"takable: {self.takable}")
            print("")
            return output
            
        return update_stack
    
    # INIT #
    def __init__(self):
        self.stack = []
        self.length = len(self.stack)
        self.takable = self.get_takable()

    # MAGIC METHODS #
    def __repr__(self):
        return f"Stack with {self.stack}"
    
    def __eq__(self, other):
        if self.stack == other.stack:
            return True
        return False
    
    # FUNCTIONS #
    def get_takable(self) -> int:
        ''' iterates backwards through stack to determine amount of cards that can be taken away'''
        length = self.length
        if length == 0:
            return 0
        if length == 1:
            return 1
        stack = self.stack
        card = stack[length-1] # get last card
        takable = 1
        for i in range(length-2, -1, -1): # loop from i=length-2 to i=0
            if stack[i] != card - 1:
                return takable
            takable += 1
        return takable
    
    @update        
    def add(self, number: int) -> None:
        self.stack.append(number)
    
    @update
    def take(self, num_to_take: int) -> list:
        ''' take the amount of num_to_take cards from the stack
        if num_to_take > num_takable: returns empty list 
        if num_to_take < num_takable: returns the list of cards that were took '''
        assert num_to_take > 0, "input must be greater than 1"
        takable = self.takable
        if num_to_take > takable: 
            return []
        stack = self.stack
        length = self.length
        ret = []
        for i in range(num_to_take):
            ret.append(stack.pop( (length-1) - (num_to_take-1) )) # pop highest takable card and add to return
        return ret
        
    
class Stack(Stack_Base):
    ''' defines a Stack with cards from 1 to STACK_SIZE '''
    
    # CONFIGURATION VARIABLES #
    STACK_SIZE = 10
    
    # INIT #
    def __init__(self):
        # fills stack and shuffles it
        super().__init__()
        for i in range(self.STACK_SIZE):
            self.add(i+1)
        self.shuffle()
        
    # FUNCTIONS #
    @Stack_Base.update
    def shuffle(self):
        import random
        random.shuffle(self.stack)


class Pile:
    ''' Discard Pile '''
    
    # DECORATORS #
    def update(func):
        def update_pile(self, *args):
            print("")
            print(colored("Pile:", "magenta") + " Executing function " + colored(func.__name__, 'cyan') + " with args " + colored(args, "cyan"))
            output = func(self, *args)
            self.highest = len(self.pile)
            print("Pile updated")
            print(self.pile)
            print(f"highest: {self.highest}")
            print("")
            return output
        
        return update_pile
    
    # INIT #
    def __init__(self):
        self.pile = []
        self.highest = len(self.pile)
        
    # MAGIC METHODS #
    def __repr__(self):
        return f"Pile with {self.pile}"
    
    def __eq__(self, other):
        if self.highest == other.highest:
            return True
        return False
        
    # FUNCTIONS #
    @update
    def discard(self, card: int) -> None:
        ''' puts a card on the discard pile if the card fits on the other '''
        pile = self.pile
        highest = self.highest
        if card == highest + 1:
            pile.append(card)
        return


class FC:
    ''' Free Cells as a dictionary
    0 represents an empty cell'''
    
    # CONFIGURATION VARIABLES #
    AMOUNT = 5
    
    # DECORATORS #
    def update(func):
        def update_fcs(self, *args):
            print("")
            print(colored("Free Cells:", "red") + " Executing function " + colored(func.__name__, 'cyan') + " with args " + colored(args, "cyan"))
            output = func(self, *args)
            print("Free Cells updated")
            print(self.fcs)
            print("")
            return output
            
        return update_fcs
    
    # INIT #
    def __init__(self):
        self.fcs = self.generate_fcs()
        
    # MAGIC METHODS #
    def __repr__(self):
        return f"Free Cells with {self.fcs}"
    
    def __eq__(self, other):
        if len(self.fcs) == len(other.fcs):
            if sorted([self.fcs[i] for i in range(len(self.fcs))]) == sorted([other.fcs[i] for i in range(len(other.fcs))]): # compare the sorted contents of the dicts 
                return True
        return False
    
    # FUCNTIONS #
    def generate_fcs(self) -> dict:
        fcs = {}
        for i in range(self.AMOUNT):
            fcs[i] = 0
        return fcs
    
    @update
    def put(self, item: list) -> None:
        ''' put a card into the Free Cell if there is space
        puts the card into the first free space 
        if there is no space, 
        item has to be a list of length 1 '''
        assert type(item) == list, "card must be of type list"
        assert len(item) == 1, "card must be a list of length 1"
        item = item[0]
        assert type(item) == int, "content of list must be an int"
        assert item > 0, "number in list must be greater than 1"
        fcs = self.fcs
        for i in range(self.AMOUNT):
            if fcs[i] == 0:
                fcs[i] = item
                return
        raise IndexError("Free Cells are full!")
        
    @update 
    def get(self, card: int) -> list:
        ''' takes the desired card from the Free Cells
        returns the card number if successful
        returns empty list if the card could not be found '''
        fcs = self.fcs
        for i in range(self.AMOUNT):
            if fcs[i] == card:
                fcs[i] = 0
                return [card]
        return []
    

class Board:
    
    # INIT # 
    def __init__(self):
        self.stack = Stack()
        self.pile = Pile()
    
    # MAGIC METHODS #
    def __eq__(self, other):
        if self.stack == other.stack:
            if self.pile == other.pile:
                return True
        return False
        
    
f = FC()
f.put([10])
f.put([3])
f.put([3])
f.put([4])
f.put([5])
print(f.get(10))
print(f.get(3))
print(f.get(5))
f.put([20])
print(f.get(10))
print(f.get(3))
