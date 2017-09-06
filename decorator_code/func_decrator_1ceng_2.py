#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

import time
import random

# 
def time_cost(f):    
    start = time.clock()
    a=f()
    end = time.clock()
    print f.__name__,"run cost time is ",end-start
    return a

@time_cost
def list_comp():
    return [(x,y) for x in range(1000) for y in range(1000) if x*y > 25]

@time_cost    
def for_loop():
    a=[]
    for x in range(0,1000):
        for y in range(0,1000):
            if x*y>25:
                a.append((x,y)) 
    return a
   
   
if __name__ == '__main__':
    pass    
    a=list_comp
    print len(a)
    #a=for_loop
    #print len(a)
