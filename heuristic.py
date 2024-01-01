# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 20:51:58 2024

@author: marti
"""

# find best way to find out if there is a greater number before smaller one

# find repeated patterns of ordered lists

l = [6,5,4,3,2,1] # -> 0
k = [6,4,3,5,2,1] # -> 1
j = [6,3,4,5,2,1] # -> 2 
h = [4,3,5,6,1,2] # -> 3
g = [1,2,3,4,5,6] # -> 5
f = [1,6,5,4,3,2] # -> 5? --> mit multiple card move theoretisch 1
d = [1,6,5,3,4,2] # -> 5? --> mit multiple card move theoretisch 4!

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
        if fits(a,b):
            continue
        elif ordered(a,b):
            if b > curr_min:
                ans +=1 
                continue
        else:
            ans += 1
            continue
    
    return ans


prod = [l,k,j,h,g,f,d]

for item in prod:
    print(ans(item))