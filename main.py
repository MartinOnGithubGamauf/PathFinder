# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:19:44 2023

@author: Martin
"""

# implement PathFinder Algorithm for use in FreeCell Solver

### SETUP SMALL SCALE FREECELL BOARD

## Definition ungerichteten Graphs

class Stack:
    
    def update(func):
        def update_length(self, *args):
            self.length = len(self.stack)
            print("Length updated")
            return func(self, *args)
            
        return update_length
    

    def __init__(self):
        self.stack = []
        self.length = len(self.stack)

    @update        
    def add(self, number: int):
        self.stack.append(number)

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
