# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:19:44 2023

@author: Martin
"""

### SETUP SMALL SCALE FREECELL BOARD
#-> traceback, falls ein error ist, dass sich das board nicht verändert! (take from stack, but cant put on pile!, take from freecell but cant put on stack...)

## Definition ungerichteten Graphs

''' -> implement moving more cards at once '''

from termcolor import colored

PRINT_UPDATES = False
PRINT_ATOMICS = False
PRINT_MOVES = True

# PRINTS # 
def print_update(obj):
    if PRINT_UPDATES:
        print(obj)
    return
        
def print_atomic(obj):
    if PRINT_ATOMICS:
        print(obj)
    return

def print_moves(obj):
    if PRINT_MOVES:
        print(obj)
    return


# WRAPPERS #
def assert_list(func):
    def check_list(self, cards):
        ''' checks input to be list of cards '''
        assert type(cards) == list, "cards must be of type list"
        assert len(cards) > 0, "cards must not be empty"
        assert all([isinstance(card, Card) for card in cards]), "content of list must be a Card"
        output = func(self, cards)
        return output
    return check_list

def assert_list_length_1(func):
    def check_and_transform(self, item):
        ''' checks input to be list and transforms list into singular card '''
        assert type(item) == list, "card must be of type list"
        assert len(item) == 1, "card must be a list of length 1"
        item = item[0]
        assert isinstance(item, Card), "content of list must be a Card"
        output = func(self, item)
        return output
    return check_and_transform

def assert_other(func):
    def check_other(self, other):
        ''' checks if other is the same class as self '''
        assert isinstance(self, type(other)), f"{type(self)} and {type(other)}"
        output = func(self, other)
        return output
    return check_other



class Card:
    ''' french playing cards 
    value of Card is a tuple of two ints, 
        the first corresponding to the suit, 
        the second correponding to the rank of the card '''
    
    # CONFIGURATION VARIABLES #
    #SUITS = {0:'Hearts', 1:'Clubs', 2:'Diamonds', 3:'Spades'} 
    #RANKS = {0:'Ace', 1:'2', 2:'3', 3:'4', 4:'5', 5:'6', 6:'7', 7:'8', 8:'9', 9:'10', 10:'Jack', 11:'Dame', 12:'King'}
    SUITS = {0:'H', 1:'C', 2:'D', 3:'S'} 
    RANKS = {0:'1', 1:'2', 2:'3', 3:'4', 4:'5', 5:'6', 6:'7', 7:'8', 8:'9', 9:'T', 10:'J', 11:'Q', 12:'K'}
    RED = {0,2}
    BLACK = {1,3}
    COLOR = {0:'red', 1:'black', 2:'red', 3:'black'}
    
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
        #return f"Card {self.RANKS[self.rank]} of {self.SUITS[self.suit]}"
        return f"{colored(self.RANKS[self.rank] + self.SUITS[self.suit], self.COLOR[self.suit], 'on_light_green', ['bold'])}"
        
    @assert_other
    def __eq__(self, other):
        if self.suit == other.suit:
            if self.value == other.value:
                return True
        return False
    
    @assert_other
    def __lt__(self, other):
        if self.suit < other.suit:
            # ?
            return False#True
        elif self.suit == other.suit:
            if self.rank < other.rank:
                return True
        else:
            return False
        
    @assert_other
    def __gt__(self, other):
        if self.suit > other.suit:
            # ?
            return False#True
        elif self.suit == other.suit:
            if self.rank > other.rank:
                return True
        else:
            return False
    
    # FUNCTIONS #
    @assert_other
    def card_fits_on_stack(self, other) -> bool:
        ''' returns True if the Card 'other' fits on 'self', otherwise False '''
        RED = self.RED
        BLACK = self.BLACK
        if (self.suit in RED and other.suit in BLACK) or (self.suit in BLACK and other.suit in RED):
            if self.rank == other.rank + 1:
                print_atomic(f"{other} fits on {self} in the stack.")
                return True
        print_atomic(f"{other} does not fit on {self} in the stack.")
        return False
            
    
    @assert_other
    def card_fits_on_pile(self, other) -> bool:
        ''' returns True if the Card 'other' fits on 'self', otherwise False '''
        if self.suit == other.suit:
            if self.rank == other.rank - 1:
                print_atomic(f"{other} fits on {self} in the pile.")
                return True
        print_atomic(f"{other} does not fit on {self} in the pile.")
        return False
    

class Stack_Base:
    
    # DECORATORS #
    def update(func):
        def update_stack(self, *args):
            print_update("")
            print_update(colored("Stack:", "red") + " Executing function " + colored(func.__name__, 'cyan') + " with args " + colored(args, "cyan"))
            output = func(self, *args)
            self.length = len(self.stack)
            self.takable = self.get_takable()
            self.last_card = self.get_last_card()
            print_update("Stack updated")
            print_update(self.stack)
            print_update(f"length: {self.length}")
            print_update(f"takable: {self.takable}")
            print_update(f"last_card: {self.last_card}")
            print_update("")
            return output
            
        return update_stack
    
    # INIT #
    def __init__(self):
        self.stack = []
        self.length = len(self.stack)
        self.takable = self.get_takable()
        self.last_card = None #! watch what happens

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
        takable = 1
        for i in range(length-1): # from i=0 to i=length-2
            top_card = stack[-1-i]
            bottom_card = stack[-2-i]
            if not bottom_card.card_fits_on_stack(top_card):
                return takable
            takable += 1
        return takable
    
    def get_last_card(self):
        ''' returns the last card on the stack
        returns None, if there are no cards '''
        if self.length == 0:
            return None
        else:
            return self.stack[self.length-1]
        
    
    @assert_list
    @update
    def populate(self, cards: list) -> None:
        for card in cards:
            self.stack.append(card)
    
    @assert_list_length_1
    def can_add(self, card: list) -> bool:
        ''' returns if card can be put on the stack '''
        bottom_card_stack = self.last_card
        if not self.last_card: # if last_card is None
            print_atomic("Card fits on Stack.")
            return True
        if bottom_card_stack.card_fits_on_stack(card):
            print_atomic("Card fits on Stack.")
            return True
        else:
            print_atomic("Card does not fit on Stack.")
            return False
        
    
    @assert_list
    @update
    def add(self, cards: list) -> None:
        if self.length == 0:
            for card in cards:
                self.stack.append(card)
            return
        bottom_card_stack = self.stack[-1]
        top_card_to_add = cards[0]
        if bottom_card_stack.card_fits_on_stack(top_card_to_add):
            for card in cards:
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
    ''' DEPRECATED: defines a Stack with cards from 1 to STACK_SIZE '''
    
    # CONFIGURATION VARIABLES #

    
    # INIT #
    def __init__(self):
        # init the Stack without any cards
        super().__init__()
        
        
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
            print_update("")
            print_update(colored("Pile:", "magenta") + " Executing function " + colored(func.__name__, 'cyan') + " with args " + colored(args, "cyan"))
            output = func(self, *args)
            self.highest = self.get_highest()
            print_update("Pile updated")
            print_update(self.pile)
            print_update(f"highest: {self.highest}")
            print_update("")
            return output
        
        return update_pile
    
    # INIT #
    def __init__(self):
        self.pile = {0:[], 1:[], 2:[], 3:[]}
        self.highest = {i:None for i in range(4)}
        
    # MAGIC METHODS #
    def __repr__(self):
        return f"Pile with {self.pile}"
    
    @assert_other
    def __eq__(self, other):
        # check if .highest is same type for self and other for each card
        tf = []
        for i in range(4):
            if isinstance(self.highest[i], type(other.highest[i])):
                if self.highest[i] == other.highest[i]:
                    tf.append(True)
            else:
                tf.append(False)
        return all(tf)
        
    # FUNCTIONS #
    def get_highest(self) -> dict: #??? wie highest, list of highest card on each pile 
        ''' returns the highest card on the pile
        returns None, if there are no cards '''
        ret = dict()
        for suit in self.pile:
            cards = self.pile[suit]
            l = len(cards)
            if l == 0:
                ret[suit] = None
            else:
                ret[suit] = cards[len(cards)-1]
        return ret
    
    @assert_list_length_1
    def can_discard(self, card: list) -> bool:
        ''' returns if the card can be put on the pile '''
        suit = card.suit
        if not self.highest[suit]: # highest == None 
            if card.rank == 0:
                print_atomic("Card fits on Pile.")
                return True
        elif self.highest[suit].card_fits_on_pile(card):
            print_atomic("Card fits on Pile.")
            return True
        else:
            print_atomic("Card does not fit on Pile.")
            return False
        
    @assert_list_length_1
    @update
    def discard(self, card: list) -> None:
        ''' puts a card on the discard pile if the card fits on the other 
        card has to be a list of length 1 '''
        suit = card.suit
        pile = self.pile
        highest = self.highest
        if not highest[suit]: # highest == None 
            if card.rank == 0:
                pile[suit].append(card)
        elif highest[suit].card_fits_on_pile(card):
            pile[suit].append(card)
        return
    

class FC:
    ''' Free Cells as a dictionary
    0 represents an empty cell'''
    
    # CONFIGURATION VARIABLES #
    AMOUNT = 4
    
    # DECORATORS #
    def update(func):
        def update_fcs(self, *args):
            print_update("")
            print_update(colored("Free Cells:", "green") + " Executing function " + colored(func.__name__, 'cyan') + " with args " + colored(args, "cyan"))
            output = func(self, *args)
            print_update("Free Cells updated")
            print_update(self.fcs)
            print_update("")
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
            self_list = sorted([self.fcs[i] for i in range(len(self.fcs)) if isinstance(self.fcs[i], Card)])
            other_list = sorted([other.fcs[i] for i in range(len(other.fcs)) if isinstance(other.fcs[i], Card)])
            if self_list == other_list: # compare the sorted contents of the dicts 
                return True
        return False
    
    # FUCNTIONS #
    def generate_fcs(self) -> dict:
        fcs = {}
        for i in range(self.AMOUNT):
            fcs[i] = 0
        return fcs
    
    def can_put(self) -> bool:
        ''' returns if I can put a card on any of the fcs '''
        fcs = self.fcs
        for i in range(self.AMOUNT):
            if not isinstance(fcs[i], Card): #slot is 0
                print_atomic("Freecells are available.")
                return True
        print_atomic("Freecells are not available.")
        return False
    
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
        returns the card in a list if successful
        returns empty list if the card could not be found '''
        fcs = self.fcs
        for i in range(self.AMOUNT):
            if isinstance(fcs[i], Card):
                if fcs[i] == card:
                    fcs[i] = 0
                    return [card]
        return []
    

class Board:
    ''' acts as Node/Vertex or Knoten '''
    
    CARD_AMOUNT = 13
    STACK_SIZE = 8
    FC_SIZE = FC.AMOUNT
    
    # INIT # 
    def __init__(self, seed: int=5):
        self.stacks = [Stack() for i in range(Board.STACK_SIZE)]
        self.pile = Pile()
        self.fcs = FC()
        self.seed = seed
        
        self.movable = 0 # how many cards can be moved at once
        self.movable_into_empty = 0 # how many cards can be moved at once into empty stack
        # --> how do I update this for every move taken
        
        self.deal_cards()
    
    # MAGIC METHODS #
    def __repr__(self):
        nl = '\n '
        return f"Board containing: \n {self.pile} \n {self.fcs} \n {nl.join([str(stack) for stack in self.stacks])}"
        
    @assert_other
    def __eq__(self, other):
        if len(self.stacks) == len(other.stacks):
            if all([self.stacks[i] == other.stacks[i] for i in range(len(self.stacks))]):
                if self.pile == other.pile:
                    if self.fcs == other.fcs:
                        return True
        return False
        
    # FUNCTIONS #
    def update_movable(self) -> None:
        # depending on FC space and empty Stacks calculate movable items
        # == Türme von Hanoi
        # n_stacks = 0, n_fcs = n, movable = (2 ** n_stacks) + (n_fcs * (2 ** n_stacks)) = 1 + (n * 1) == 1 + n
        # n_stacks = 1, n_fcs = 0, movable = (2 ** n_stacks) + (n_fcs * (2 ** n_stacks)) = 2 + (0 * 2) == 2
        # n_stacks = 1, n_fcs = 2, movable = (2 ** n_stacks) + (n_fcs * (2 ** n_stacks)) = 2 + (2 * 2) == 6
        # n_stacks = 2, n_fcs = 0, movable = (2 ** n_stacks) + (n_fcs * (2 ** n_stacks)) = 4 + (0 * 3) == 4
        # n_stacks = 2, n_fcs = 1, movable = (2 ** n_stacks) + (n_fcs * (2 ** n_stacks)) = 4 + (1 * 4) == 8
        # n_stacks = 3, n_fcs = 0, movable = (2 ** n_stacks) + (n_fcs * (2 ** n_stacks)) = 8 + (0 * 4) == 8
        # 
        # -> Weltformel: n_stacks = m, n_fcs = n, movable = 2 ** m * (1 + n)
        #
        # -> Weltformel 2: n_stacks = m, n_fcs = n, movable_into_empty = 2 ** (m-1) * (1 + n)
        n_fcs = 0
        n_stacks = 0
        for key in self.fcs.fcs:
            if not self.fcs.fcs[key]: # if it is None
                n_fcs += 1
        for stack in self.stacks:
            if len(stack.stack) == 0: # no Card on Stack
                n_stacks += 1
        # update self.movable
        self.movable = 2**n_stacks * (1 + n_fcs)
        self.movable_into_empty = 2**(n_stacks - 1) * (1 + n_fcs)
        return
        
    def deal_cards(self) -> None:
        # generate cards
        cards_to_deal = [Card((j,i)) for i in range(Board.CARD_AMOUNT) for j in range(len(Card.SUITS))]
        
        # shuffle the cards and deal to the stacks
        #from random import shuffle
        import random
        random.Random(self.seed).shuffle(cards_to_deal)
        
        # deal cards uniformly to stacks
        stack_number = len(self.stacks)
        i = 0
        for card in cards_to_deal:
            self.stacks[i].populate([card])
            i = i + 1
            i = i % stack_number
            
        self.update_movable()
        return
    
    def get_all_moves(self) -> list:
        print_moves("\nGetting all moves:")
        
        from functools import partial
        output = []
        
        # iterate through every possible card on the stack
        for i, take_stack in enumerate(self.stacks):
            card = take_stack.last_card
            
            # only check this if there is a card on the stack
            if isinstance(card, Card):
                
                # check the pile
                if self.pile.can_discard([card]):
                    
                    copy = self.copy()
                    
                    output.append( Move( board = copy, source = partial(copy.stacks[i].take, 1),
                                          sink = partial(copy.pile.discard, [card]),
                                          name = f"Move {card} from Stack {i} to Pile.") ) 
                
                # check the freecells
                if self.fcs.can_put():
                    
                    copy = self.copy()
                    
                    output.append( Move( board = copy, source = partial(copy.stacks[i].take, 1),
                                          sink = partial(copy.fcs.put, [card]),
                                          name = f"Move {card} from Stack {i} to Freecells.") )
            
            # check the other stacks
            for j in range(Board.STACK_SIZE):
                if i != j:
                    put_stack = self.stacks[j]
                    
                    # check for the last card and for the takable sub-stack
                    takable = take_stack.takable # guarenteed greater than 0
                    for k in range(1,takable+1): # iterate from 1 up to takable
                        
                        # stop if too many cards are moved at once
                        if k > self.movable:
                            break
                        if len(put_stack.stack) == 0:
                            if k > self.movable_into_empty:
                                break
                    
                        l = len(take_stack.stack)
                        cards = take_stack.stack[l-k:l] # take list of k cards which are takable
                        
                        if put_stack.can_add([cards[0]]): # check if the bottom card of the cards fits on the put_stack
                            
                            copy = self.copy() # copy the board for every move appended
                            
                            output.append( Move( board = copy, source = partial(copy.stacks[i].take, k), # take_stack
                                                  sink = partial(copy.stacks[j].add, cards), # put_stack
                                                  name = f"Move {cards} from Stack {i} to Stack {j}.") ) 
                
        # iterate through every card on the freecells
        fcs_dict = self.fcs.fcs
        for key in fcs_dict:
            card = fcs_dict[key]
            
            # check that card is not None
            if isinstance(card, Card):
                # check the pile
                if self.pile.can_discard([card]):
                    
                    copy = self.copy()
                    
                    output.append( Move ( board = copy, source = partial(copy.fcs.get, [card]),
                                          sink = partial(copy.pile.discard, [card]),
                                          name = f"Move {card} from Freecells to Pile.") )
                    
                # check the stacks
                for j, put_stack in enumerate(self.stacks):
                    if put_stack.can_add([card]):
                        
                        copy = self.copy()
                        
                        output.append( Move( board = copy, source = partial(copy.fcs.get, [card]),
                                              sink = partial(copy.stacks[j].add, [card]),
                                              name = f"Move {card} from Freecells to Stack {j}.") )
                
                
                
        print_moves(f"Found {colored(str(len(output)), 'magenta')} moves.")
        return output
        
    def copy(self):
        ''' return deepcopy of self '''
        from copy import deepcopy
        return deepcopy(self)
        

class Solution_Board(Board):
    
    # INIT # 
    def __init__(self):
        self.stacks = [Stack() for i in range(Board.STACK_SIZE)]
        self.pile = Pile()
        self.fcs = FC()
        
        cards_to_deal = [Card((j,i)) for i in range(Board.CARD_AMOUNT) for j in range(len(Card.SUITS))]
        for card in cards_to_deal:
            self.pile.discard([card])

class Move:
    ''' acts as Edge or Kante '''
    
    # INIT #
    def __init__(self, board, source, sink, name):
        self.board = board
        self.source = source # functool.partial to fetch card
        self.sink = sink # functool.partial to allocate card
        self.name = name # description
    
    # MAGIC METHODS #
    def __repr__(self):
        return self.name
    
    def __call__(self):    
        self.source()
        self.sink()
        self.board.update_movable()
        return self.board
        
    # FUNCTIONS #
    def move(self):
        self()
        
if __name__=="__main__":
    b = Board()
    s = Solution_Board()
    d = Board(seed = 1)
    d.pile.discard( d.stacks[1].take(1) )
    print(d)
    print(b.pile == b.pile)
    print(b.pile == d.pile)
    
