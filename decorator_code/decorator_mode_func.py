#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

def printInfo(info):  
    print unicode(info, 'utf-8')
    
    
def wearTrouser(f):
    def _f(*arg, **kwarg):
        printInfo("裤子")    
        return f(*arg, **kwarg)
    return _f
    
def wearSuit(f):
    def _f(*arg, **kwarg):
        printInfo("西服")    
        return f(*arg, **kwarg)
    return _f
    
def wearTShirt(f):
    def _f(*arg, **kwarg):
        printInfo("T恤")    
        return f(*arg, **kwarg)
    return _f

def wearCap(f):
    def _f(*arg, **kwarg):
        printInfo("帽子")    
        return f(*arg, **kwarg)
    return _f

def wearSportShoes(f):
    def _f(*arg, **kwarg):
        printInfo("运动鞋")    
        return f(*arg, **kwarg)
    return _f    

def wearLeatherShoes(f):
    def _f(*arg, **kwarg):
        printInfo("皮鞋")    
        return f(*arg, **kwarg)
    return _f    
    
def wearedPerson(person,cloths):
    w = person
    for f in cloths:
        w=f(w)
    return w
    
    
    
#@wearTrouser    
#@wearTShirt    
def person(name):
    printInfo("装扮好的%s" % name)
    
if __name__ == '__main__':
            
    person("晓明")
    print "-----------------------"
    
    business_wear=[wearLeatherShoes,wearSuit,wearTrouser]
    sports_wear = [wearSportShoes,wearCap,wearTShirt,wearTrouser]

    weared_business_person = wearedPerson(person,business_wear)
    weared_sports_person = wearedPerson(person,sports_wear)

    weared_business_person("晓明")
    print "-----------------------"
    weared_sports_person("晓红")
    

 