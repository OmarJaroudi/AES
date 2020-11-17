# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:37:11 2020

@author: ojaro
"""
from numpy import transpose



def HexToBin(hexStr):
    return bin(int(hexStr,16))[2:]
    
def BinToHex(binary):
    return str(hex(int(binary,2)))

def circularLeftShift(bits,n):
    bits = list(bits)
    return "".join(bits[n::] + bits[:n:])

def ciruclarRightShift(bits,n):
    bits = list(bits)
    return "".join(bits[n:len(bits):] + bits[0:n:])

def stringXOR(s1,s2):
    """
    performs and xor operation on two binary strings
    returns xor result
    """
    assert(len(s1) == len(s2))
    return "".join(["0" if s1[i] == s2[i] else "1" for i in range(len(s1))])

def getColumn(matrix,i):
        return [row[i] for row in matrix]
def xorVectors(v1,v2):
    out = []
    for i,v in enumerate(v1):
        b1 = HexToBin(v).zfill(8)
        b2 = HexToBin(v2[i]).zfill(8)
        res = BinToHex(stringXOR(b1,b2))[2:]
        res = '0'+res if len(res) == 1 else res
        out .append(res)
    return out
def transposeMatrix(matrix):
    return transpose(matrix).tolist()

def transformStreamToMatrix(stream):
        inputMatrix = [stream[i:i+2] for i in range(0,len(stream),2)]
        width = int((len(inputMatrix))/4)
        state = [[0 for j in range(width)]for i in range(4)]
        for i in range(width):
            for j in range(4):
                state[j][i] = inputMatrix[i*4 + j]
        return state
def transformMatrixToStream(matrix):
    stream = ""
    for i in range(len(matrix[0])):
        for row in matrix:
            stream+=str(row[i])
    return stream


def printmatrix(self, data):
    for i in data:
        print(i)