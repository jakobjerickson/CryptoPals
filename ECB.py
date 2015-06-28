# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 14:12:49 2015

@author: jakoberickson
"""
## AES Electronic Code Book encryption-decryption for 128-bit key
import numpy as np
#Declare Constants:
#The length of the imput block
Nb = 4
#the number of words in a key 
Nk = 4
#number of rounds of encryption/decryption
Nr = 10
# the irreducible polynomials for AES
m8 = '100011011'
m4 = '10001'
Rcon = ['01000000',
 '02000000',
 '04000000',
 '08000000',
 '10000000',
 '20000000',
 '40000000',
 '80000000',
 '1b000000',
 '36000000']

sBox = np.array((
#  0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f
['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],# 0
['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],# 1
['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],# 2
['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],# 3
['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],# 4
['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],# 5
['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],# 6
['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],# 7
['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],# 8
['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],# 9
['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],# a
['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],# b
['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],# c
['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],# d
['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],# e
['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']#  f
))

sBoxinv = np.array((
#  0     1     2     3     4     5     6     7     8     9     a     b     c     d     e     f   
['52', '09', '6a', 'd5', '30', '36', 'a5', '38', 'bf', '40', 'a3', '9e', '81', 'f3', 'd7', 'fb'],# 0
['7c', 'e3', '39', '82', '9b', '2f', 'ff', '87', '34', '8e', '43', '44', 'c4', 'de', 'e9', 'cb'],# 1
['54', '7b', '94', '32', 'a6', 'c2', '23', '3d', 'ee', '4c', '95', '0b', '42', 'fa', 'c3', '4e'],# 2
['08', '2e', 'a1', '66', '28', 'd9', '24', 'b2', '76', '5b', 'a2', '49', '6d', '8b', 'd1', '25'],# 3
['72', 'f8', 'f6', '64', '86', '68', '98', '16', 'd4', 'a4', '5c', 'cc', '5d', '65', 'b6', '92'],# 4
['6c', '70', '48', '50', 'fd', 'ed', 'b9', 'da', '5e', '15', '46', '57', 'a7', '8d', '9d', '84'],# 5
['90', 'd8', 'ab', '00', '8c', 'bc', 'd3', '0a', 'f7', 'e4', '58', '05', 'b8', 'b3', '45', '06'],# 6
['d0', '2c', '1e', '8f', 'ca', '3f', '0f', '02', 'c1', 'af', 'bd', '03', '01', '13', '8a', '6b'],# 7
['3a', '91', '11', '41', '4f', '67', 'dc', 'ea', '97', 'f2', 'cf', 'ce', 'f0', 'b4', 'e6', '73'],# 8
['96', 'ac', '74', '22', 'e7', 'ad', '35', '85', 'e2', 'f9', '37', 'e8', '1c', '75', 'df', '6e'],# 9
['47', 'f1', '1a', '71', '1d', '29', 'c5', '89', '6f', 'b7', '62', '0e', 'aa', '18', 'be', '1b'],# a
['fc', '56', '3e', '4b', 'c6', 'd2', '79', '20', '9a', 'db', 'c0', 'fe', '78', 'cd', '5a', 'f4'],# b
['1f', 'dd', 'a8', '33', '88', '07', 'c7', '31', 'b1', '12', '10', '59', '27', '80', 'ec', '5f'],# c
['60', '51', '7f', 'a9', '19', 'b5', '4a', '0d', '2d', 'e5', '7a', '9f', '93', 'c9', '9c', 'ef'],# d
['a0', 'e0', '3b', '4d', 'ae', '2a', 'f5', 'b0', 'c8', 'eb', 'bb', '3c', '83', '53', '99', '61'],# e
['17', '2b', '04', '7e', 'ba', '77', 'd6', '26', 'e1', '69', '14', '63', '55', '21', '0c', '7d']#  f
))



def SubBytes(state):
    temp = []
    for i in range(Nb):
        for j in range(Nk):
            x = int('{0:02x}'.format(state[i][j])[0], base = 16)
            y = int('{0:02x}'.format(state[i][j])[1], base = 16)
            temp.append(int(sBox[x][y], base = 16))
    out = [temp[i:i+4] for i in range(0, Nk*Nb, Nk)]
    return out

def ShiftRows(state):
    temp = [[state[(i+j)%4][i]for i in range(Nb)] for j in range(Nk)]
    return temp

def MixColumns(state):
    temp = [[0]*4,[0]*4,[0]*4,[0]*4]
    for i, col in enumerate(state):
        temp[i][0] = xtime(col[0])^col[1]^xtime(col[1])^col[2]^col[3]%283
        temp[i][1] = col[0]^xtime(col[1])^xtime(col[2])^col[2]^col[3]%283
        temp[i][2] = col[0]^col[1]^xtime(col[2])^xtime(col[3])^col[3]%283
        temp[i][3] = xtime(col[0])^col[0]^col[1]^col[2]^xtime(col[3])%283
    return temp
# n is an integer representing which power of 2 to use
def xtime(myInt, n = 1):
    for i in range(n):
        myInt = (myInt<<1)^((myInt>>7&1) * 0x11b)
    return myInt

def AddRoundKey(state, w):
    temp = [[state[j][i] ^ Hex2Int(w[j])[i] for i in range(4)] for j in range(4)]
    return temp
    

def SubWord(word):
    temp = ['','','','']
    for i in range(Nb):
        x = word[2*i]
        y = word[2*i+1]
        temp[i] = sBox[int(x, base = 16)][int(y, base = 16)]
    return ''.join(temp)

def RotWord(word):
    temp = [word[i:i+2] for i in range(0, 8, 2)]
    return ''.join([temp[(i+1)%4] for i in range(4)])

def KeyExpansion(key):
    w = [key[i:i+8] for i in range(0, 32, 8)]
    i = Nk
    while i < (Nb * (Nr + 1)):
        temp = w[i-1]
        if (i % Nk == 0):
            temp = XORHex(SubWord(RotWord(temp)), Rcon[(i/Nk)-1])
        elif ((Nk > 6) & (i % Nk == 0)):
            temp = SubWord(temp)
        w.append(XORHex(w[i-Nk],temp))
        i += 1
    return w

def InvShiftRows(state):
    temp = [[state[(4-i+j)%4][i]for i in range(Nb)] for j in range(Nk)]

    return temp

def InvSubBytes(state):
    temp = []
    for i in range(Nb):
        for j in range(Nk):
            x = int('{0:02x}'.format(state[i][j])[0], base = 16)
            y = int('{0:02x}'.format(state[i][j])[1], base = 16)
            temp.append(int(sBoxinv[x][y], base = 16))
    out = [temp[i:i+4] for i in range(0, Nk*Nb, Nk)]
    return out



def InvMixColumns(state):
    temp = [[0]*4,[0]*4,[0]*4,[0]*4]
    for i, col in enumerate(state):
        temp[i][0] = xtime(col[0], 3)^xtime(col[0], 2)^xtime(col[0])^\
                     xtime(col[1], 3)^xtime(col[1], 1)^col[1]^\
                     xtime(col[2], 3)^xtime(col[2], 2)^col[2]^\
                     xtime(col[3], 3)^col[3]%283
        temp[i][1] = xtime(col[1], 3)^xtime(col[1], 2)^xtime(col[1])^\
                     xtime(col[2], 3)^xtime(col[2], 1)^col[2]^\
                     xtime(col[3], 3)^xtime(col[3], 2)^col[3]^\
                     xtime(col[0], 3)^col[0]%283
        temp[i][2] = xtime(col[2], 3)^xtime(col[2], 2)^xtime(col[2])^\
                     xtime(col[3], 3)^xtime(col[3], 1)^col[3]^\
                     xtime(col[0], 3)^xtime(col[0], 2)^col[0]^\
                     xtime(col[1], 3)^col[1]%283
        temp[i][3] = xtime(col[3], 3)^xtime(col[3], 2)^xtime(col[3])^\
                     xtime(col[0], 3)^xtime(col[0], 1)^col[0]^\
                     xtime(col[1], 3)^xtime(col[1], 2)^col[1]^\
                     xtime(col[2], 3)^col[2]%283
    return temp
    
    
def Cipher(inp, w):
    state = [[int(inp[j+i:j+i+2], base = 16) for j in range(0, 8, 2)] for i in range(0, 32, 8)]
    state = AddRoundKey(state, w[0:Nk])
    for r in range(1, Nr):
        state = AddRoundKey(MixColumns(ShiftRows(SubBytes(state))), w[r*Nk:(r+1)*Nk])
    state = AddRoundKey(ShiftRows(SubBytes(state)), w[Nr*Nk:(Nr+1)*Nk])
    outp = ''.join([''.join(['{0:02x}'.format(c) for c in row]) for row in state])

    return outp    
    
def ApplyCipher(inp, key):
    if (len(inp)%32 != 0):
        return 'input must be even multiple of 16 bytes'
    w = KeyExpansion(key)
    blocks = [inp[i:i+32] for i in range(0, len(inp), 32)]
    temp = [Cipher(block, w) for block in blocks]
    return ''.join(temp)


def InvCipher(inp, w):
    state = [[int(inp[j+i:j+i+2], base = 16) for j in range(0, 8, 2)] for i in range(0, 32, 8)]
    state = AddRoundKey(state, w[Nr*Nb:])
    for r in range(Nr - 1, 0, -1):
        state = InvMixColumns(AddRoundKey((InvSubBytes(InvShiftRows(state))), w[r*Nk:(r+1)*Nk]))

    state = AddRoundKey(InvShiftRows(InvSubBytes(state)), w[0:Nb])
    outp = ''.join([''.join(['{0:02x}'.format(c) for c in row]) for row in state])
    return outp   
    
def ApplyInvCipher(inp, key):
    if (len(inp)%32 != 0):
        return 'input must be even multiple of 16 bytes'
    w = KeyExpansion(key)
    blocks = [inp[i:i+32] for i in range(0, len(inp), 32)]
    temp = [InvCipher(block, w) for block in blocks]
    return ''.join(temp)
