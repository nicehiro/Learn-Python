#!/usr/bin/env python
# coding: utf-8
#copyRight by heibanke

s="afAzfdfjdBHSD"

#AaBbCcDd

s_lst = list(s)

sort_lst = sorted(s_lst,cmp=lambda x,y:ord(x)-ord(y)

print ''.join(sort_lst)


介绍函数式编程
讲解函数即对象的概念
讲解函数作为参数的用法