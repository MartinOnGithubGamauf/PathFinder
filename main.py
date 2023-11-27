# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:19:44 2023

@author: Martin
"""

# implement PathFinder Algorithm for use in FreeCell Solver

### SETUP SMALL SCALE FREECELL BOARD
#-> traceback, falls ein error ist, dass sich das board nicht verändert! (take from stack, but cant put on pile!, take from freecell but cant put on stack...)

#-> implement + and - with Card - int, so one card higher or lower is possible

## Definition ungerichteten Graphs

from termcolor import colored

# WRAPPERS #
def assert_list_length_1(func):
    def check_and_transform(self, item):
        ''' checks for input and transforms list into singular card '''
        assert type(item) == list, "card must be of type list"
        assert len(item) == 1, "card must be a list of length 1"
        item = item[0]
        assert isinstance(item, Card), "content of list must be an int"
        output = func(self, item)
        return output
    return check_and_transform

def assert_other(func):
    def check_other(self, other):
        ''' checks if other is the same class as self '''
        assert isinstance(self, type(other))
        output = func(self, other)
        return output
    return check_other



class Card:
    ''' french playing cards 
    value of Card is a tuple of two ints, 
        the first corresponding to the suit, 
        the second correponding to the rank of the card '''
    
    # CONFIGURATION VARIABLES #
    SUITS = {0:'Hearts', 1:'Clubs', 2:'Diamonds', 3:'Spades'} 
    RANKS = {0:'Ace', 1:'2', 2:'3', 3:'4', 4:'5', 5:'6', 6:'7', 7:'8', 8:'9', 9:'10', 10:'Jack', 11:'Dame', 12:'King'}
    RED = {0,2}
    BLACK = {1,3}
    
    # DECORATORS #
    def assert_tuple(func):
        def check_tuple(self, value):
            ''' checks for value being a tuple of length two, 
            values are ints, and must be part of keyword args of SUITS and RANKS '''
            assert type(value) == tuple, "value must be a tuple"
            assert len(value) == 2, "value must be of length 2"
            assert (type(value[0]) == int and type(value[1]) == int), "items in value must be ints"
            assert ((value[0] in [*self.SUITS]) and (value[1] in [*self.RANKS])), "items in value are not in SUITS or RANKS"
            output = func(self, value)
            return output
        return check_tuple
            
    # INIT #
    @assert_tuple
    def __init__(self, value: tuple):
        self.value = value
        self.suit = self.value[0]
        self.rank = self.value[1]
    
    # MAGIC METHODS #
    def __repr__(self):
        return f"Card {self.RANKS[self.rank]} of {self.SUITS[self.suit]}"
    
    @assert_other
    def __eq__(self, other):
        if self.value == other.value:
            return True
        return False
    
    # FUNCTIONS #
    @assert_other
    def card_fits_on_stack(self, other):
        ''' returns True if the Card 'other' fits on 'self', otherwise False '''
        RED = self.RED
        BLACK = self.BLACK
        if (self.suit in RED and other.suit in RED) or (self.suit in BLACK and other.suit in BLACK):
            if self.rank == other.rank + 1:
                print(f"{other} fits on {self} in the stack.")
                return True
        print(f"{other} does not fit on {self} in the stack.")
        return False
            
    
    @assert_other
    def card_fits_on_pile(self, other):
        ''' returns True if the Card 'other' fits on 'self', otherwise False '''
        if self.suit == other.suit:
            if self.rank == other.rank - 1:
                print(f"{other} fits on {self} in the pile.")
                return True
        print(f"{other} does not fit on {self} in the pile.")
        return False
    

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
    
    @assert_other
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
            if not stack[i].card_fits_on_stack(card):
                return takable
            takable += 1
        return takable
    
    @update
    def add(self, card) -> None:
        assert isinstance(card, Card), "input must be of type Card"
        self.stack.append(card)
    
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
            c = Card((0,i+1))
            self.add(c)
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
    
    @assert_other
    def __eq__(self, other):
        if self.highest == other.highest:
            return True
        return False
        
    # FUNCTIONS #
    @assert_list_length_1
    @update
    def discard(self, card: list) -> None:
        ''' puts a card on the discard pile if the card fits on the other 
        card has to be a list of length 1 '''
        pile = self.pile
        highest = self.highest        
        top_card = pile[highest-1]
        if top_card.card_fits_on_pile(card):
            pile.append(card)
        return
    

class FC:
    ''' Free Cells as a dictionary
    0 represents an empty cell'''
    
    # CONFIGURATION VARIABLES #
    AMOUNT = 10
    
    # DECORATORS #
    def update(func):
        def update_fcs(self, *args):
            print("")
            print(colored("Free Cells:", "green") + " Executing function " + colored(func.__name__, 'cyan') + " with args " + colored(args, "cyan"))
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
    
    @assert_other
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
    
    @assert_list_length_1
    @update
    def put(self, card: list) -> None:
        ''' put a card into the Free Cell if there is space
        puts the card into the first free space 
        if there is no space, 
        card has to be a list of length 1 '''
        fcs = self.fcs
        for i in range(self.AMOUNT):
            if not isinstance(fcs[i], Card): # slot is 0
                fcs[i] = card
                return
        raise IndexError("Free Cells are full!")
    
    @assert_list_length_1
    @update 
    def get(self, card: list) -> list:
        ''' takes the desired card from the Free Cells
        returns the card number if successful
        returns empty list if the card could not be found '''
        fcs = self.fcs
        for i in range(self.AMOUNT):
            if isinstance(fcs[i], Card):
                if fcs[i] == card:
                    fcs[i] = 0
                    return [card]
        return []
    

class Board:
    ''' acts as Node or Knoten '''
    
    # INIT # 
    def __init__(self):
        self.stack = Stack()
        self.pile = Pile()
        self.fcs = FC()
    
    # MAGIC METHODS #
    def __repr__(self):
        return f"Board containing: \n {self.pile} \n {self.fcs} \n {self.stack}"
        
    @assert_other
    def __eq__(self, other):
        if self.stack == other.stack:
            if self.pile == other.pile:
                if self.fcs == other.fcs:
                    return True
        return False
        
    # FUNCTIONS #
    def move(self):
        pass


class Move:
    ''' acts as Edge or Kante '''
    
    # INIT #
    def __init__(self):
        pass

b = Board()
d = Board()

print(b)
print(d)






