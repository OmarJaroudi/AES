# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 18:00:30 2020

@author: WarPeace101
"""
from utils import getColumn,xorVectors, transposeMatrix
from copy import deepcopy
import re

def addToOutput(self, name, data, out):
    out += str(name) + ": \n" + "\n"       
    for i in data:
        out += str(" ".join(i)) + "\n"
    out += "\n" + "\n"
    
    return out

def keyExpansion(keyMatrix, rconVectors, sbox):
    
    keySteps = []
    step = ""
    output = []
    N = len(keyMatrix[0])
    if N==4:
        length = 44
    elif N==6:
        length = 52
    elif N == 8:
        length = 60
    
    w = [getColumn(keyMatrix,i) for i in range(N)]
    
    for i in range(len(w)):
        output.append(re.sub("[\]\[\,\']+","",str(w[i])))
        keySteps.append("Doesn't Change")
    
    for i in range(N,length):
        step += "Word[i-1]: " + re.sub("[\]\[\,\']+","",str(w[i-1])) + "\n"
        temp = deepcopy(w[i-1]) 
        if i % N == 0:
            temp = temp[1::] + temp[:1:]
            step += "Circular Left Shift: " + re.sub("[\]\[\,\']+","",str(temp)) + "\n"
            for j, elem in enumerate(temp):
                row = int(elem[0],16)
                col = int(elem[1],16)
                temp[j] = sbox[row][col]
            step += "Substituion: " + re.sub("[\]\[\,\']+","",str(temp)) + "\n"
            temp = xorVectors(temp, rconVectors[int((i-1)/N)])
            step += "XOR with Rcon: " + re.sub("[\]\[\,\']+","",str(temp)) + "\n"
        elif N==8 and i%N==4:
            
            for j, elem in enumerate(temp):
                row = int(elem[0],16)
                col = int(elem[1],16)
                temp[j] = sbox[row][col]
            step += "Substitute: " + re.sub("[\]\[\,\']+","",str(temp)) + "\n"
        
        
        w.append(xorVectors(temp,w[i-N]))
        step += "XOR with w[i - "+str(N)+"]: " + re.sub("[\]\[\,\']+","",str(w[i])) + "\n"
        keySteps.append(step)
        step = ""
        output.append(re.sub("[\]\[\,\']+","",str(w[i])))
        
    
    keys = [w[i:i+4] for i in range(0, len(w), 4)]
    
    
       

    
    for i,k in enumerate(keys):
        keys[i] = transposeMatrix(k)
        
    return keys, keySteps, output