# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:19:44 2023

@author: Martin
"""

# implement PathFinder Algorithm for use in FreeCell Solver

### SETUP SMALL SCALE FREECELL BOARD

## Definition ungerichteten Graphs

class Stack:
    
    # DECORATORS #
    def update(func):
        def update_length(self, *args):
            output = func(self, *args)
            self.length = len(self.stack)
            print("Length updated")
            return output
            
        return update_length
    
    # INIT #
    def __init__(self):
        self.stack = []
        self.length = len(self.stack)

    # FUNCTIONS #
    @update        
    def add(self, number: int):
        
        self.stack.append(number)
    
    @update
    def take(self, num_to_take: int):
        ''' take the amount of num_to_take cards from the stack
        if num_to_take < num_takable: returns the list of cards that were took
        if num_to_take > num_takable: returns empty list '''
        return 

class Board:
    
    def __init__(self):
        self.stack = Stack()
        
        
    
b = Board()
s = Stack()
s.add(3)
print(s.length)
print(s.stack)
s.add(4)
print(s.length)
