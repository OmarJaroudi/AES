# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:38:30 2020

@author: ojaro
"""

from utils import circularLeftShift,stringXOR
import functools
from sympy.abc import x
from sympy import Poly
def multiplyByX(p1):
    if p1[0] == '0':
        return circularLeftShift(p1,1)
    elif p1[0] == '1':
        p2 = p1
        p2 = '0' + p2[1:]
        p2 = circularLeftShift(p2,1)
        return stringXOR(p2,'00011011')

def multiplyByXPowerN(p1,n):
    answer = p1
    for i in range(n):
        answer = multiplyByX(answer)
    return answer

def multiply(p1,p2):
    """
    multiplies two  polynomials in galois field 2^8
    """
    if(p2 == '00000000'):
        return '00000000'
    out = []
    i = len(p1)-1 
    for b in p2:
        if(b == '1'):
            out.append(multiplyByXPowerN(p1,i))
        i-=1
    answer = functools.reduce(lambda a,b:stringXOR(a,b),out)
    return answer
def extended_euclid(m,b):
   a1,a2,a3 = (Poly(1,x,domain='GF(2)'),Poly(0,x,domain='GF(2)'),Poly(m,x,domain='GF(2)')) 
   b1,b2,b3 = (Poly(0,x,domain='GF(2)'),Poly(1,x,domain = 'GF(2)'),Poly(b,domain='GF(2)'))
   q = '-'
   while(True):
      q,r = a3.div(b3)
      t1,t2,t3 = (a1.sub(q.mul(b1)),a2.sub(q.mul(b2)),a3.sub(q.mul(b3)))
      a1,a2,a3 = (b1,b2,b3)
      b1,b2,b3 = (t1,t2, t3)
      if(b3 == Poly(1,x,domain='GF(2)')):
            return b2
      elif(b3 == Poly(0,x,domain='GF(2)')):
          return None