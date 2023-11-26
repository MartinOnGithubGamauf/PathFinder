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
        
    
b = Board()
