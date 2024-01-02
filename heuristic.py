# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 20:51:58 2024

@author: marti
"""

# find best way to find out if there is a greater number before smaller one

# find repeated patterns of ordered lists

import unittest
from card import Card

def ordered(a,b):
    return a > b

def fits(a,b):
    return a-1 == b

def ans(l: list):
    s = len(l)
    ans = 0
    curr_min = 10000
    for i in range(s-1):
        # see how far the ordered part goes
        # for every unordered part, add 1
        
        if l[i] < curr_min:
            curr_min = l[i]
        
        # determine, how long the ordered list goes
        a = l[i]
        b = l[i+1]
        if fits(a,b): # cards can be taken as two -> continue
            continue
        elif ordered(a,b): # b is smaller than a, nothing to worry about
            if b > curr_min: # but if b is a card that is bigger than the minimum we already had -> count
                ans +=1 
                continue
        else: # if b is bigger than before -> count
            ans += 1
            continue
    
    return ans


def ans_card(stack: list):
    ''' we now have 4 different suits of cards '''
    l = len(stack)
    ans = 0
    curr_min = {0: 10000, 1: 10000, 2: 10000, 3: 10000}
    for i in range(l-1):
        a = stack[i]
        
        if a.rank < curr_min[a.suit]: # if new minimum on stack is found, set new minimum
            curr_min[a.suit] = a.rank 
        
        b = stack[i+1]
        
        if a.card_fits_on_stack(b): # if the stack can be taken away in one move, continue (penalty has already been applied beforehand)
            continue
        elif b.rank > curr_min[b.suit]: # if the next card is bigger than the limit before, apply penalty
            ans += 1
                
    return ans

class TestHeuristic(unittest.TestCase):

    def test_ints(self):
        l = ([6,5,4,3,2,1], 0) # -> 0
        k = ([6,4,3,5,2,1], 1) # -> 1
        j = ([6,3,4,5,2,1], 2) # -> 2 
        h = ([4,3,5,6,1,2], 3) # -> 3
        g = ([1,2,3,4,5,6], 5) # -> 5
        f = ([1,6,5,4,3,2], 1) # -> 5? --> mit multiple card move theoretisch 1
        d = ([1,6,5,3,4,2], 4) # -> 5? --> mit multiple card move theoretisch 4!
        
        prod = [l,k,j,h,g,f,d]
        
        for p in prod:
            self.assertEqual(ans(p[0]), p[1], 'not correct answer')
        
    def test_numbers(self):
        H1 = Card((0,0))
        H2 = Card((0,1))
        H3 = Card((0,2))
        H4 = Card((0,3))
        C1 = Card((1,0))
        C2 = Card((1,1))
        C3 = Card((1,2))
        C4 = Card((1,3))
        D1 = Card((2,0))
        D2 = Card((2,1))
        D4 = Card((2,3))
        S1 = Card((3,0))
        S2 = Card((3,1))
        S4 = Card((3,3))
        
        l = ([H4,H2,H1,C4,C2,C1], 0)
        k = ([H1,H2,H4,C1,C2,C4], 4)
        j = ([H1,S2,D1,H2,C4], 1)
        h = ([H1,H4,C3,H2,D1], 1)
        g = ([H1,H4,C3,H2,D1,C2,S1], 2)
        f = ([H1,H4,C3,H2,D1,C2,S1,C4], 2)
        g = ([H1,C1,H4,C3,H2,D1,C2,S1,C4], 3)
        h = ([H1,C1,H4,C3,H2], 1)
        i = ([H1,C1,H4,C3,H2,D1,C4,H3], 2)
        
        prod = [l,k,j,h,g,f,g,h,i]
        
        for p in prod:
            self.assertEqual(ans_card(p[0]), p[1], f'not correct answer, should get {p[1]} for stack {p[0]}.')
    
# DRIVER CODE
if __name__ == '__main__':
    test = TestHeuristic
    
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(test)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    
    