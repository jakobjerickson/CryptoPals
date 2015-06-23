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

a = np.matrix(([2,3,1,1],[1,2,3,1],[1,1,2,3],[3,1,1,2]))


def SubBytes(state):
    temp = np.array((['','','',''],['','','',''],['','','',''],['','','','']),\
                     dtype = '|S2')
    for i in range(Nb):
        for j in range(Nk):
            x = int(state[i][j][0], base = 16)
            y = int(state[i][j][1], base = 16)
            temp[i][j] = sBox[x][y]
    return temp

def ShiftRows(state):
    temp = np.array((['','','',''],['','','',''],['','','',''],['','','','']),\
                     dtype = '|S2')
    for i, row in enumerate(state):
        temp[i][0] = row[i%4]
        temp[i][1] = row[(i+1)%4]
        temp[i][2] = row[(i+2)%4]
        temp[i][3] = row[(i+3)%4]
    return temp
    
def MixColumns(state):
    temp = np.array((['','','',''],['','','',''],['','','',''],['','','','']), dtype = '|S2')
    for j in range(Nk):
        column = [[int(state[i][j], base = 16)] for i in range(4)]
        Mixed = a * column
        print column, Mixed
        for i in range(Nb):
            temp[i][j] = '{0:02x}'.format(Mixed[i][0])
    return temp


def xtime(hexString):
    myInt = int(hexString, base = 16)
    shifted = (myInt<<1)^((myInt>>7&1) * 0x11b)
    return shifted
    return '{0:02x}'.format(shifted)