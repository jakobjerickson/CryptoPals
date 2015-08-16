# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 14:12:49 2015

@author: jakoberickson
"""
import crypto_utils


"""
AES Electronic Code Book encryption-decryption for 128-bit key
A detailed description of the algorithm and its implementation can be
found at:
http://csrc.nist.gov/publications/fips/fips197/fips-197.pdf
"""


# Declare Constants:
# The length of the imput block
Nb = 4
# the number of words in a key
Nk = 4
# number of rounds of encryption/decryption
Nr = 10
# the irreducible polynomials for AES
Rcon = [
    '01000000',
    '02000000',
    '04000000',
    '08000000',
    '10000000',
    '20000000',
    '40000000',
    '80000000',
    '1b000000',
    '36000000']

sBox = [
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
]

sBoxinv = [
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
]


def SubWord(word):
    temp = ['', '', '', '']
    for i in range(Nb):
        x = word[2*i]
        y = word[2*i+1]
        temp[i] = sBox[int(x, base=16)][int(y, base=16)]
    return ''.join(temp)


def RotWord(word):
    return ''.join(word[i:i+2] for i in [2, 4, 6, 0])


# Expands the hex key from 4 4-byte words to 44 4-byte words
# and stores them in the array w
# Each block of 4 words is derived from the previous 4-word block according
# to the algorithm from the above link.
def KeyExpansion(hex_key_string):
    w = [hex_key_string[i:i+8] for i in range(0, 32, 8)]

    i = Nk
    while i < (Nb * (Nr + 1)):
        temp = w[i-1]
        if (i % Nk == 0):
            temp = crypto_utils.hex_XOR(SubWord(RotWord(temp)), Rcon[(i/Nk)-1])
        elif ((Nk > 6) & (i % Nk == 0)):
            temp = SubWord(temp)
        w.append(crypto_utils.hex_XOR(w[i-Nk], temp))
        i += 1
    return w


def SubBytes(input_state):
    output_state = [[0 for i in range(4)] for j in range(4)]
    for i in range(Nb):
        for j in range(Nk):
            x = input_state[i][j] / 16
            y = input_state[i][j] % 16
            output_state[i][j] = int(sBox[x][y], base=16)
    return output_state


def ShiftRows(state):
    return [[state[(i+j) % 4][i]
             for i in range(Nb)]
            for j in range(Nk)]


def MixColumns(state):
    temp = [[0 for i in range(4)] for j in range(4)]
    for i, col in enumerate(state):
        temp[i][0] = (xtime(col[0]) ^ col[1] ^ xtime(col[1]) ^
                      col[2] ^ col[3] % 283)
        temp[i][1] = (col[0] ^ xtime(col[1]) ^ xtime(col[2]) ^
                      col[2] ^ col[3] % 283)
        temp[i][2] = (col[0] ^ col[1] ^ xtime(col[2]) ^
                      xtime(col[3]) ^ col[3] % 283)
        temp[i][3] = (xtime(col[0]) ^ col[0] ^ col[1] ^
                      col[2] ^ xtime(col[3]) % 283)
    return temp


# the algorithm will implement n times
def xtime(int_x, n=1):
    for i in range(n):
        int_x = (int_x << 1) ^ ((int_x >> 7 & 1) * 283)
    return int_x


def AddRoundKey(state, int_words):
    return [[state[j][i] ^ int_words[j][i]
             for i in range(Nb)]
            for j in range(Nk)]


def InvShiftRows(state):
    return [[state[(Nb-i+j) % Nb][i]
             for i in range(Nb)]
            for j in range(Nk)]


def InvSubBytes(input_state):
    output_state = [[0 for i in range(4)] for j in range(4)]
    for i in range(Nb):
        for j in range(Nk):
            x = input_state[i][j] / 16
            y = input_state[i][j] % 16
            output_state[i][j] = int(sBoxinv[x][y], base=16)
    return output_state


def InvMixColumns(state):
    temp = [[0 for i in range(4)] for j in range(4)]
    for i, col in enumerate(state):
        temp[i][0] = (
            xtime(col[0], 3) ^ xtime(col[0], 2) ^ xtime(col[0]) ^
            xtime(col[1], 3) ^ xtime(col[1], 1) ^ col[1] ^
            xtime(col[2], 3) ^ xtime(col[2], 2) ^ col[2] ^
            xtime(col[3], 3) ^ col[3] % 283
            )
        temp[i][1] = (
            xtime(col[1], 3) ^ xtime(col[1], 2) ^ xtime(col[1]) ^
            xtime(col[2], 3) ^ xtime(col[2], 1) ^ col[2] ^
            xtime(col[3], 3) ^ xtime(col[3], 2) ^ col[3] ^
            xtime(col[0], 3) ^ col[0] % 283
            )
        temp[i][2] = (
            xtime(col[2], 3) ^ xtime(col[2], 2) ^ xtime(col[2]) ^
            xtime(col[3], 3) ^ xtime(col[3], 1) ^ col[3] ^
            xtime(col[0], 3) ^ xtime(col[0], 2) ^ col[0] ^
            xtime(col[1], 3) ^ col[1] % 283
            )
        temp[i][3] = (
            xtime(col[3], 3) ^ xtime(col[3], 2) ^ xtime(col[3]) ^
            xtime(col[0], 3) ^ xtime(col[0], 1) ^ col[0] ^
            xtime(col[1], 3) ^ xtime(col[1], 2) ^ col[1] ^
            xtime(col[2], 3) ^ col[2] % 283
            )
    return temp


# state is the 16-byte block arranged in a 4x4 matrix, moving across rows for
# ease of indexing in Python.This is different than the fips document which
# moves down columns.
def Cipher(hex_input, hex_words):
    state = [[int(hex_input[j+i:j+i+2], base=16)
              for i in range(0, 8, 2)]
             for j in range(0, 32, 8)]

    int_words = [crypto_utils.hex_to_integer(word) for word in hex_words]

    state = AddRoundKey(state, int_words[0:Nk])
    for r in range(1, Nr):
        state = SubBytes(state)
        state = ShiftRows(state)
        state = MixColumns(state)
        state = AddRoundKey(state, int_words[r*Nk:(r+1)*Nk])
    state = SubBytes(state)
    state = ShiftRows(state)
    state = AddRoundKey(state, int_words[Nr*Nk:(Nr+1)*Nk])

    hex_output = ''.join('{0:02x}'.format(integer)
                         for row in state
                         for integer in row)
    return hex_output


def ApplyCipher(hex_input, hex_key_string):
    if (len(hex_input) % 32 != 0):
        return 'input must be even multiple of 16 bytes'
    if (len(hex_key_string) != 32):
        return 'hex key must be 16 bytes!'

    hex_words = KeyExpansion(hex_key_string)
    input_blocks = [hex_input[i:i+32] for i in range(0, len(hex_input), 32)]
    output_blocks = [Cipher(block, hex_words) for block in input_blocks]
    return ''.join(output_blocks)


# See note for Cipher
def InvCipher(hex_input, hex_words):
    state = [[int(hex_input[j+i:j+i+2], base=16)
              for i in range(0, 8, 2)]
             for j in range(0, 32, 8)]

    int_words = [crypto_utils.hex_to_integer(word) for word in hex_words]

    state = AddRoundKey(state, int_words[Nr*Nb:])
    for r in range(Nr - 1, 0, -1):
        state = InvShiftRows(state)
        state = InvSubBytes(state)
        state = AddRoundKey(state, int_words[r*Nk:(r+1)*Nk])
        state = InvMixColumns(state)
    state = InvSubBytes(state)
    state = InvShiftRows(state)
    state = AddRoundKey(state, int_words[0:Nb])

    hex_output = ''.join('{0:02x}'.format(integer)
                         for row in state
                         for integer in row)
    return hex_output


def ApplyInvCipher(hex_input, hex_key_string):
    if (len(hex_input) % 32 != 0):
        return 'input must be even multiple of 16 bytes'
    if (len(hex_key_string) != 32):
        return 'hex key must be 16 bytes!'

    hex_words = KeyExpansion(hex_key_string)
    input_blocks = [hex_input[i:i+32] for i in range(0, len(hex_input), 32)]
    output_blocks = [InvCipher(block, hex_words) for block in input_blocks]
    return ''.join(output_blocks)
