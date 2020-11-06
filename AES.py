# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 13:23:41 2020

@author: ojaro
"""

from utils import BinToHex,HexToBin,stringXOR,getColumn,xorVectors,transformMatrixToStream,transformStreamToMatrix,transposeMatrix
from galois import multiply
class AES():
    def __init__(self):
        self.sbox = [
        ["63", "7C", "77", "7B", "F2", "6B", "6F", "C5", "30", "01", "67", "2B", "FE", "D7", "AB", "76"],
        ["CA", "82", "C9", "7D", "FA", "59", "47", "F0", "AD", "D4", "A2", "AF", "9C", "A4", "72", "C0"],
        ["B7", "FD", "93", "26", "36", "3F", "F7", "CC", "34", "A5", "E5", "F1", "71", "D8", "31", "15"],
        ["04", "C7", "23", "C3", "18", "96", "05", "9A", "07", "12", "80", "E2", "EB", "27", "B2", "75"],
        ["09", "83", "2C", "1A", "1B", "6E", "5A", "A0", "52", "3B", "D6", "B3", "29", "E3", "2F", "84"],
        ["53", "D1", "00", "ED", "20", "FC", "B1", "5B", "6A", "CB", "BE", "39", "4A", "4C", "58", "CF"],
        ["D0", "EF", "AA", "FB", "43", "4D", "33", "85", "45", "F9", "02", "7F", "50", "3C", "9F", "A8"],
        ["51", "A3", "40", "8F", "92", "9D", "38", "F5", "BC", "B6", "DA", "21", "10", "FF", "F3", "D2"],
        ["CD", "0C", "13", "EC", "5F", "97", "44", "17", "C4", "A7", "7E", "3D", "64", "5D", "19", "73"],
        ["60", "81", "4F", "DC", "22", "2A", "90", "88", "46", "EE", "B8", "14", "DE", "5E", "0B", "DB"],
        ["E0", "32", "3A", "0A", "49", "06", "24", "5C", "C2", "D3", "AC", "62", "91", "95", "E4", "79"],
        ["E7", "C8", "37", "6D", "8D", "D5", "4E", "A9", "6C", "56", "F4", "EA", "65", "7A", "AE", "08"],
        ["BA", "78", "25", "2E", "1C", "A6", "B4", "C6", "E8", "DD", "74", "1F", "4B", "BD", "8B", "8A"],
        ["70", "3E", "B5", "66", "48", "03", "F6", "0E", "61", "35", "57", "B9", "86", "C1", "1D", "9E"],
        ["E1", "F8", "98", "11", "69", "D9", "8E", "94", "9B", "1E", "87", "E9", "CE", "55", "28", "DF"],
        ["8C", "A1", "89", "0D", "BF", "E6", "42", "68", "41", "99", "2D", "0F", "B0", "54", "BB", "16"]]
        self.invsbox = [
        ["52", "09", "6A", "D5", "30", "36", "A5", "38", "BF", "40", "A3", "9E", "81", "F3", "D7", "FB"],
        ["7C", "E3", "39", "82", "9B", "2F", "FF", "87", "34", "8E", "43", "44", "C4", "DE", "E9", "CB"],
        ["54", "7B", "94", "32", "A6", "C2", "23", "3D", "EE", "4C", "95", "0B", "42", "FA", "C3", "4E"],
        ["08", "2E", "A1", "66", "28", "D9", "24", "B2", "76", "5B", "A2", "49", "6D", "8B", "D1", "25"],
        ["72", "F8", "F6", "64", "86", "68", "98", "16", "D4", "A4", "5C", "CC", "5D", "65", "B6", "92"],
        ["6C", "70", "48", "50", "FD", "ED", "B9", "DA", "5E", "15", "46", "57", "A7", "8D", "9D", "84"],
        ["90", "D8", "AB", "00", "8C", "BC", "D3", "0A", "F7", "E4", "58", "05", "B8", "B3", "45", "06"],
        ["D0", "2C", "1E", "8F", "CA", "3F", "0F", "02", "C1", "AF", "BD", "03", "01", "13", "8A", "6B"],
        ["3A", "91", "11", "41", "4F", "67", "DC", "EA", "97", "F2", "CF", "CE", "F0", "B4", "E6", "73"],
        ["96", "AC", "74", "22", "E7", "AD", "35", "85", "E2", "F9", "37", "E8", "1C", "75", "DF", "6E"],
        ["47", "F1", "1A", "71", "1D", "29", "C5", "89", "6F", "B7", "62", "0E", "AA", "18", "BE", "1B"],
        ["FC", "56", "3E", "4B", "C6", "D2", "79", "20", "9A", "DB", "C0", "FE", "78", "CD", "5A", "F4"],
        ["1F", "DD", "A8", "33", "88", "07", "C7", "31", "B1", "12", "10", "59", "27", "80", "EC", "5F"],
        ["60", "51", "7F", "A9", "19", "B5", "4A", "0D", "2D", "E5", "7A", "9F", "93", "C9", "9C", "EF"],
        ["A0", "E0", "3B", "4D", "AE", "2A", "F5", "B0", "C8", "EB", "BB", "3C", "83", "53", "99", "61"],
        ["17", "2B", "04", "7E", "BA", "77", "D6", "26", "E1", "69", "14", "63", "55", "21", "0C", "7D"],
            ]
        self.mCols = [['02','03','01','01'],
                      ['01','02','03','01'],
                      ['01','01','02','03'],
                      ['03','01','01','02']]
        self.invMCols = [['0e','0b','0d','09'],
                         ['09','0e','0b','0d'],
                         ['0d','09','0e','0b'],
                         ['0b','0d','09','0e']
                         ]

        self.rcon = ['01','02','04','08','10','20','40','80','1b','36']
        self.rconVectors = [[r,'00','00','00'] for r in self.rcon ]

            
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
               newRow = row[1:len(row):] +row[0:1:] 
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
        w = [getColumn(keyMatrix,i) for i in range(len(keyMatrix))]
        for i in range(4,44):
            temp = w[i-1]
            if i % 4 == 0:
                temp = temp[1::] + temp[:1:]#circular left shift of bytes
                for j,elem in enumerate(temp):
                    row = int(elem[0],16)
                    col = int(elem[1],16)
                    temp[j] = self.sbox[row][col]
                temp = xorVectors(temp,self.rconVectors[int((i-1)/4)])
            w.append(xorVectors(temp,w[i-4]))
        keys = [w[i:i+4] for i in range(0, len(w), 4)]
        for i,k in enumerate(keys):
            keys[i] = transposeMatrix(k)
        return keys
    def multiplyVectorByMcols(self,vector):
       keyState = [[vector[0],'00','00','00'],
                   [vector[1],'00','00','00'],
                   [vector[2],'00','00','00'],
                   [vector[3],'00','00','00']]
       return [row[0] for row in self.mixColumns(keyState)]
   
    def SingleRoundEncrypt(self,plainText,expandedKey,round):
        
        plainText = transformStreamToMatrix(plainText)
        if round==1:
            pxorK = self.addRoundKey(plainText,expandedKey[0])

        else:
            pxorK = plainText
        sub = self.substituteBytes(pxorK)

        shift = self.shiftRows(sub)
        if round!= 10:
            mix = self.mixColumns(shift)
        else: 
            mix =shift
        
        roundResult= self.addRoundKey(mix, expandedKey[round])

        return transformMatrixToStream(roundResult)
    def Encrypt(self,plainText,key):
        key = transformStreamToMatrix(key)
        keys = aes.keyExpansion(key)
        for i in range(1,11):
            plainText = aes.SingleRoundEncrypt(plainText, keys, i)
            print(transformMatrixToStream(plainText))

    # def SingleRoundDecrypt(self,cipherText,expandedKey,round):
            
    #         cipherText = transformStreamToMatrix(cipherText)
    #         if round==1:
    #             pxorK = self.addRoundKey(cipherText,expandedKey[0])
    
    #         else:
    #             pxorK = cipherText
    #         shift = self.shiftRows(pxorK,True)
    
    #         sub = self.substituteBytes(shift,True)
    #         roundResult= self.addRoundKey(sub, expandedKey[round])
    
    #         if round!= 10:
    #             mix = self.mixColumns(roundResult,True)
    #         else: 
    #             mix =roundResult
                
    #         return transformMatrixToStream(mix)
        
 

    # def Decrypt(self,cipherText,key):
    #     key = transformStreamToMatrix(key)
    #     keys = aes.keyExpansion(key)
    #     keys = keys[::-1]
    #     for i in range(1,11):
    #         cipherText = aes.SingleRoundDecrypt(cipherText, keys, i)
    #         print(transformMatrixToStream(cipherText))
                

aes = AES()
key = '0f1571c947d9e8590cb7add6af7f6798'
plainText = '0123456789abcdeffedcba9876543210'
cipherText = 'ff0b844a0853bf7c6934ab4364148fb9'

aes.Encrypt(plainText,key)
print("\n")
# aes.Decrypt(cipherText, key)

    
        