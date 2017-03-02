#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

import time
import random

def time_cost(runloops):
    def decorator(f):
        def _f(*arg, **kwarg):
            min_time = 1000
            avg_time = 0
            for i in range(runloops):
                start = time.clock()
                a=f(*arg,**kwarg)
                end = time.clock()
                if min_time>end-start:
                    min_time = end-start
                avg_time+=(end-start)
            print f.__name__,"best run cost time is ",min_time
            print f.__name__,"avg run cost time is ",float(avg_time)/runloops
            
            return a
        return _f
    return decorator


@time_cost(100)
def list_comp(length):
    return [(x,y) for x in range(length) for y in range(length) if x*y > 25]


@time_cost(100)
def for_loop(length):
    a=[]
    for x in range(0,length):
        for y in range(0,length):
            if x*y>25:
                a.append((x,y)) 
    return a
   
if __name__ == '__main__':
        
    a=list_comp(100)
    print len(a)
    b=for_loop(100)
    print len(b)
