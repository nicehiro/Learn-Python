#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

import time
import random

"""
def time_cost(f):
    def _f(*arg, **kwarg):
        start = time.clock()
        a=f(*arg,**kwarg)
        end = time.clock()
        print f.__name__,"run cost time is ",end-start
        return a
    return _f
"""

def time_cost(timef):
    def decorator(f):
        def _f(*arg, **kwarg):
            start = timef()
            a=f(*arg,**kwarg)
            end = timef()
            print f.__name__,"run cost time is ",end-start
            return a
        return _f
    return decorator


@time_cost(time.time)
def list_comp(length):
    return [(x,y) for x in range(length) for y in range(length) if x*y > 25]


@time_cost(time.time)
def for_loop(length):
    a=[]
    for x in range(0,length):
        for y in range(0,length):
            if x*y>25:
                a.append((x,y)) 
    return a
   
if __name__ == '__main__':
    

    a=list_comp(1000)
    print len(a)
    b=for_loop(1000)
    print len(b)
