# coding: utf-8

import time

def f1(x, y):
    return x+y

def f2(x, y):
    return x-y

def f(a, b, c):
    time.sleep((5.6-(3.1*a+1.9*b+.5*c))*0.1)
    if a==0:
        x = 1
    elif a==1:
        x = 7

    if b==0:
        y = x
    elif b==1:
        y = 9

    if c==0:
        z = f1(x,y)
    elif c==1:
        z = f2(x,y)

    return z
