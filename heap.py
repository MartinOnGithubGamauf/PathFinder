# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 20:56:33 2023

@author: marti
"""

import heapq
from heapq import heapify, heappush, heappop

from graph import Node
from main import Board

h = []
l = []

n1 = Node(board=Board())
n2 = Node(board=Board())
n3 = Node(board=Board())
n4 = Node(board=Board())

n1.f = 10
n2.f = 20
n3.f = 30
n4.f = 40

heappush(h, n1)
heappush(h, n2)
heappush(h, n3)
heappush(h, n4)

l.append(n1)
l.append(n2)
l.append(n3)
l.append(n4)

heapify(l)

print(h)
print(l)

print(heappop(h))
print(heappop(h))

print(h)

