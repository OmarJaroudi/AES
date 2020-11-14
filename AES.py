# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:23:41 2020

@author: ojaro
"""

from utils import BinToHex,HexToBin,stringXOR,getColumn,xorVectors,transformMatrixToStream,transformStreamToMatrix,transposeMatrix
from galois import multiply
import numpy as np
from pickle import load
from copy import deepcopy

class AES():
    def __init__(self):
        
        file = open(r"pickles/SBox.pkl","rb")
        self.sbox = load(file)
        file.close()
        
        file = open(r"pickles/InvSBox.pkl","rb")
        self.invsbox = load(file)
        file.close()
        
        file = open(r"pickles/MixColumns.pkl","rb")
        self.mCols = load(file)
        file.close()
        
        file = open(r"pickles/InvMixColumns.pkl","rb")
        self.invMCols = load(file)
        file.close()

        
        file = open(r"pickles/RConVectors.pkl","rb")
        self.rconVectors = load(file)
        file.close()
        
        
        self.keyOutput = ""
        self.plainTextOutput = ""
        

    def printmatrix(self, data):
        for i in data:
            print(i)
    
    
    
    def addToOutput(self, name, data):
        self.plainTextOutput += str(name) + ": \n" + "\n" + "************" + "\n"
            
        for i in data:
            self.plainTextOutput += str(" ".join(i)) + "\n"
        self.plainTextOutput += "\n" + "************" + "\n\n"
            
    def addRoundKey(self,state,key):
        newState = [[0 for j in range(len(state))]for i in range(len(state))]
        for i in range(len(state)):
            for j in range(len(state)):
                elem_1 = int(state[i][j],16)
                elem_2 = int(key[i][j],16)
                newState[i][j] = str(hex(elem_1 ^ elem_2))[2:]
                newState[i][j] = '0' + newState[i][j] if len(newState[i][j]) == 1 else newState[i][j]
        return newState
    
    def substituteBytes(self,state,inv=False):
        newState = [[0 for j in range(len(state))]for i in range(len(state))]
        for i in range(len(state)):
            for j in range(len(state)):
                rowIdx = int(state[i][j][0],16)
                columnIdx = int(state[i][j][1],16)
                if(inv):
                    newState[i][j] = self.invsbox[rowIdx][columnIdx]
                else:
                    newState[i][j] = self.sbox[rowIdx][columnIdx]
        return newState
   
    def shiftRows(self,state,inv=False):
        newState = []
        for i,row in enumerate(state):
            
            if(inv):
              
               newRow = np.roll(row,i)                   
               #newRow = row[1:len(row):] +row[0:1:] 
            else:
                newRow = row[i::] + row[:i:]           
            newState.append(newRow)
        return newState
    def mixColumns(self,state,inv=False):
        newState = [['00000000' for j in range(len(state))]for i in range(len(state))]
        mCols = self.mCols if inv == False else self.invMCols
        for i in range(len(state)):
            for j in range(len(state)):
                for k in range(len(state)):
                    x = HexToBin(mCols[i][k]).zfill(8)
                    y = HexToBin(state[k][j]).zfill(8)
                    product = multiply(x,y).zfill(8)
                    newState[i][j] = stringXOR(newState[i][j],product)
        for i in range(len(state)):
            for j in range(len(state)):
                newState[i][j] = BinToHex(newState[i][j])[2:]
                newState[i][j] = '0' + newState[i][j] if len(newState[i][j]) == 1 else newState[i][j]
        return newState
    
    def keyExpansion(self,keyMatrix):
        N = len(keyMatrix[0])
        if N==4:
            length = 44
        elif N==6:
            length = 52
        elif N == 8:
            length = 60
        
        w = [getColumn(keyMatrix,i) for i in range(N)]
        print(w)
        for i in range(N,length):
            
            temp = deepcopy(w[i-1]) 
            if i % N == 0:
                
                temp = temp[1::] + temp[:1:]
                for j,elem in enumerate(temp):
                    row = int(elem[0],16)
                    col = int(elem[1],16)
                    temp[j] = self.sbox[row][col]
                temp = xorVectors(temp,self.rconVectors[int((i-1)/N)])
            elif N==8 and i%N==4:
                
                for j,elem in enumerate(temp):
                    row = int(elem[0],16)
                    col = int(elem[1],16)
                    temp[j] = self.sbox[row][col]
                    
            
            
            w.append(xorVectors(temp,w[i-N]))
            
        
        
        
       
        
        print(w)
        keys = [w[i:i+4] for i in range(0, len(w), 4)]
        
        self.printmatrix(keys)
        
        self.keyOutput += "Key Expansion: \n"+  "\n" + "************" + "\n"
        for i in keys:
            for j in i:
                self.keyOutput += str(" ".join(j)) + "\n"
            self.keyOutput += "\n" + "************" + "\n"
        
        
        
        for i,k in enumerate(keys):
            keys[i] = transposeMatrix(k)
        return keys
        
    
    
    def multiplyVectorByMcols(self,vector):
       keyState = [[vector[0],'00','00','00'],
                   [vector[1],'00','00','00'],
                   [vector[2],'00','00','00'],
                   [vector[3],'00','00','00']]
       return [row[0] for row in self.mixColumns(keyState)]
   
    def SingleRoundEncrypt(self,plainText,expandedKey,round,MaxRound):
        
        plainText = transformStreamToMatrix(plainText)
        if round==1:
            pxorK = self.addRoundKey(plainText,expandedKey[0]) 
            self.addToOutput("First Round XOR", pxorK)
        
        else:
            pxorK = plainText
            
        sub = self.substituteBytes(pxorK)
        self.addToOutput("Substitute", sub)
        
        shift = self.shiftRows(sub)
        self.addToOutput("Shifting", shift)
        
        if round!= MaxRound:
            mix = self.mixColumns(shift)
            self.addToOutput("Mixing", mix)
        else: 
            mix =shift
            self.addToOutput("Last Mix", mix)
        
        roundResult= self.addRoundKey(mix, expandedKey[round])
        self.addToOutput("Adding round key", roundResult)

        return transformMatrixToStream(roundResult)
    
    def Encrypt(self,plainText,key):
        if len(key)==32:
            MaxRound =10
        elif len(key)==48:
            MaxRound = 12
        elif len(key)==64:
            MaxRound = 14
        else:
            print("Key length not valid")
            return
        
        key = transformStreamToMatrix(key)
        
        keys = self.keyExpansion(key)
        
        self.plainTextOutput += "PlainText: \n" + "\n" + "************" + "\n"
        for i in range(0, len(plainText), 2):
            if(i%8 == 0 and i != 0):
                self.plainTextOutput += "\n"
            self.plainTextOutput += plainText[i] + plainText[i+1] + " "
            
        self.plainTextOutput += "\n" + "************" + "\n\n"
        
        for i in range(1,MaxRound+1):
            plainText = self.SingleRoundEncrypt(plainText, keys, i,MaxRound)
            print(transformMatrixToStream(plainText))


    def SingleRoundDecrypt(self,cipherText,expandedKey,round):
    
         cipherText = transformStreamToMatrix(cipherText)
         
         if round==1:
             pxorK = self.addRoundKey(cipherText,expandedKey[0])
        
         else:
             pxorK = cipherText
         self.printmatrix(pxorK)
         print("*******")
         shift = self.shiftRows(pxorK,True)
         self.printmatrix(shift)
         sub = self.substituteBytes(shift,True)
         
         roundResult = self.addRoundKey(sub, expandedKey[round])
        
     
         if round!= 10:
             mix = self.mixColumns(roundResult,True)
         else: 
             mix = roundResult
        
    
         return transformMatrixToStream(mix)
        
 

    def Decrypt(self,cipherText,key):
         key = transformStreamToMatrix(key)
         keys = self.keyExpansion(key)
         keys = keys[::-1]

         for i in range(1,11):
             cipherText = self.SingleRoundDecrypt(cipherText, keys, i)
             print(transformMatrixToStream(cipherText))
                

aes = AES()
cipherText = '3a0352540ea9ec5626fa83c03d3b8403'
plainText = '000102030405060708090a0b0c0d0e0f'
key =       '603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4'

aes.Encrypt(plainText,key)


# aes.Decrypt(cipherText, key)


#print(aes.plainTextOutput)
#
#with open("AES_Encrypt.txt","w") as f:
#    f.write(aes.plainTextOutput)
#f.close()
#
#with open("KeyExpansion.txt", "w") as f:
#    f.write(aes.keyOutput)
#f.close()



    
        