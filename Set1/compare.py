# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 15:47:11 2015

@author: jakoberickson
"""

benchmark = {
' ': 0.18584494369869206,
 'a': 0.06409603064045284,
 'b': 0.01288415222354608,
 'c': 0.019583177579445204,
 'd': 0.034147923190163645,
 'e': 0.10327072443962551,
 'f': 0.01882483780749034,
 'g': 0.015673070027662845,
 'h': 0.050614831772697245,
 'i': 0.05583339110819815,
 'j': 0.0012341187617738623,
 'k': 0.004875007355871964,
 'l': 0.032238136318661854,
 'm': 0.022678480852218567,
 'n': 0.05823706373127469,
 'o': 0.06298389427366512,
 'p': 0.012725956305048428,
 'q': 0.0009863420219582606,
 'r': 0.04992629833224812,
 's': 0.05066248114573871,
 't': 0.07074240343914115,
 'u': 0.02355832652542916,
 'v': 0.008964514797155428,
 'w': 0.01916219536862389,
 'x': 0.0014137568981401735,
 'y': 0.018460558350588362,
 'z': 0.00037738303448837793}
             
expWordLength = 4.5833052369518485

alphabet = 'abcdefghijkl mnopqrstuvwxyz'
uppers = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' 
commons = 'etaoin shrdlu'
def normalize(myDict):
    sum = 0
    for i in myDict.keys():
        sum += myDict[i]
    for i in myDict.keys():
        myDict[i] = myDict[i]

def tryKeys(binString):
    decryptedBin = {}
    for i in range(128):
        print '.'
        key = '{0:08b}'.format(i) * (len(binString) / 8)
        decryptedBin[i] = XORBin(binString, key)
    return decryptedBin
    
    
def scoreKeys(mystring, type = 'bin'):    
    keyScores = {}
    if type == 'hex':
        mystring = Hex2Bin(mystring)
    decryptedBin = tryKeys(mystring)
    for i in decryptedBin.keys():
        lengths = getWordLength(Bin2String(decryptedBin[i]))
        if scoreString(Bin2String(decryptedBin[i])): 
            keyScores[i] = scoreString(Bin2String(decryptedBin[i]))
    if len(keyScores) == 0: return None
#    return keyScores
    return min(keyScores, key = keyScores.get),\
               keyScores[min(keyScores, key = keyScores.get)]

def getWordLength(mystr):
    total = 0.0
    for letter in alphabet:
        total += float(mystr.lower().count(letter))
    wordcount = float(len(mystr.split(' ')))
    return total, wordcount

    
def getLetterFreq(mystr):
    charFreq = {}
    for letter in alphabet:
        charFreq[letter] = mystr.lower().count(letter)
    total = len(mystr)
    if total != 0:
        for letter in alphabet:
           charFreq[letter] = float(charFreq[letter]) / total
    return charFreq 
    
        
def scoreString(mystring):
    SS = 0
    charFreq = getLetterFreq(mystring)
    if sum(charFreq.values()) != 0:
        for letter in commons:
            SS += (charFreq[letter] - benchmark[letter])**2
        return SS
    else: return None
    
    
def getHDistance(str1, str2):
    return XORString(str1, str2).count('1')
    
def applyKey(binstring, keystring):
    length = len(binstring)
    binkey = [String2Bin(letter) for letter in keystring]
    fullkey = ''
    i = 0
    while len(fullkey) < len(binstring):
        if i > len(binkey)-1: i = 0    
        fullkey += binkey[i]
        i += 1
    result = Bin2String(XORBin(binstring, fullkey))
    return result
    
    
    