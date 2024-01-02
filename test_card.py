# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:30:03 2024

@author: marti
"""

import unittest
from card import Card, Stack, Pile, FC, Board, Move

class TestCard(unittest.TestCase):
    target = 'card.py'
    
    def test_equal_greater_lesser(self):
        c1 = Card((0,1))
        c2 = Card((0,2))
        c3 = Card((0,3))
        c4 = Card((2,4))
        c5 = Card((2,6))
        self.assertTrue(c1==c1, 'cards should be the same')
        self.assertFalse(c1==c2, 'cards should not be the same')
        
        self.assertTrue(c1 < c2, 'card1 should be smaller than card2')
        self.assertTrue(c4 < c5, 'card1 should be smaller than card2')
        self.assertFalse(c2 < c1, 'card1 should not be smaller than card2')
        self.assertFalse(c2 < c4, 'card1 should not be smaller than card2')
        
        self.assertTrue(c2 > c1, 'card1 should be bigger than card2')
        self.assertTrue(c5 > c4, 'card1 should be bigger than card2')
        self.assertFalse(c1 > c2, 'card1 should not be bigger than card2')
        self.assertFalse(c4 > c2, 'card1 should not be bigger than card2')
        
    def test_card_fits(self):
        c1 = Card((0,1))
        c2 = Card((0,2))
        c3 = Card((0,3))
        c4 = Card((2,4))
        c5 = Card((2,6))
        c6 = Card((1,5))
        self.assertTrue(c6.card_fits_on_stack(c4), 'card1 should fit in stack')
        self.assertFalse(c2.card_fits_on_stack(c3), 'card1 should not fit in stack')
        self.assertTrue(c5.card_fits_on_stack(c6), 'card1 should fit in stack')
        self.assertFalse(c2.card_fits_on_stack(c1), 'card1 should not fit in stack')
        self.assertFalse(c6.card_fits_on_stack(c5), 'card1 should not fit in stack')
        
        self.assertTrue(c1.card_fits_on_pile(c2), 'card1 should fit in pile')
        self.assertFalse(c3.card_fits_on_pile(c2), 'card1 should not fit in pile')
        self.assertFalse(c3.card_fits_on_pile(c4), 'card1 should not fit in pile')
        self.assertFalse(c6.card_fits_on_pile(c5), 'card1 should not fit in pile')
        

class TestStack(unittest.TestCase):
    pass

if __name__ == '__main__':
    tests = (TestCard, TestStack)#, TestPile, TestFC, TestBoard)
    
    for test in tests:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(test)
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        
    