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
            self.takable = self.get_takable()
            print("Stack updated")
            print(self.stack)
            print(f"length: {self.length}")
            print(f"takable: {self.takable}")
            print("")
            return output
            
        return update_length
    
    # INIT #
    def __init__(self):
        self.stack = []
        self.length = len(self.stack)
        self.takable = self.get_takable()

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
        if num_to_take < num_takable: returns the list of cards that were took
        if num_to_take > num_takable: returns empty list '''
        return 

class Board:
    
    def __init__(self):
        self.stack = Stack()
        
        
    
b = Board()
s = Stack()
s.add(3)
s.add(4)
s.add(6)
s.add(7)