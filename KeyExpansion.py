# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:00:30 2020

@author: WarPeace101
"""
from utils import getColumn,xorVectors, transposeMatrix
from copy import deepcopy


def addToOutput(self, name, data, out):
    out += str(name) + ": \n" + "\n"       
    for i in data:
        out += str(" ".join(i)) + "\n"
    out += "\n" + "\n"
    
    return out

def keyExpansion(keyMatrix, rconVectors, sbox):
    
    keySteps = []
    step = ""
    
    N = len(keyMatrix[0])
    if N==4:
        length = 44
    elif N==6:
        length = 52
    elif N == 8:
        length = 60
    
    w = [getColumn(keyMatrix,i) for i in range(N)]
    
    for i in range(N,length):
        
        temp = deepcopy(w[i-1]) 
        if i % N == 0:
            
            temp = temp[1::] + temp[:1:]
            for j, elem in enumerate(temp):
                row = int(elem[0],16)
                col = int(elem[1],16)
                temp[j] = sbox[row][col]
            temp = xorVectors(temp, rconVectors[int((i-1)/N)])
        elif N==8 and i%N==4:
            
            for j, elem in enumerate(temp):
                row = int(elem[0],16)
                col = int(elem[1],16)
                temp[j] = sbox[row][col]
                
        
        
        w.append(xorVectors(temp,w[i-N]))
 
    keys = [w[i:i+4] for i in range(0, len(w), 4)]
    
       
#    self.keyOutput += "Key Expansion: \n"+  "\n" + "************" + "\n"
#    for i in keys:
#        for j in i:
#            self.keyOutput += str(" ".join(j)) + "\n"
#        self.keyOutput += "\n" + "************" + "\n"
    
    for i,k in enumerate(keys):
        keys[i] = transposeMatrix(k)
        
    return keys