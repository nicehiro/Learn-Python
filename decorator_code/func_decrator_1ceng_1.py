#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

def decorator(f):  
    print "before "+f.__name__+" called."  
    return f

def myfunc1():  
    print " myfunc1() called."  



@decorator
def myfunc2():  
    print " myfunc2() called."  


if __name__=="__main__":
    #pass
    decorator(myfunc1)()
    myfunc2()