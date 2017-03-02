#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

import time
import random

def time_cost(f):
    def _f(*arg, **kwarg):
        start = time.clock()
        a=f(*arg,**kwarg)
        end = time.clock()
        print f.__name__,"run cost time is ",end-start
        return a
    return _f
    
    
@time_cost
def list_comp(length):
    return [(x,y) for x in range(length) for y in range(length) if x*y > 25]

@time_cost    
def for_loop(xlen,ylen):
    a=[]
    for x in range(0,xlen):
        for y in range(0,ylen):
            if x*y>25:
                a.append((x,y)) 
    return a
   
if __name__ == '__main__':

    xlen,ylen=1000,100

    list_comp(1000)
    for_loop(xlen,ylen)
