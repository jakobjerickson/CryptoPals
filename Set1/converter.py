# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 10:30:46 2015

@author: jakoberickson
"""
#Decodes a Hexidecimal string and converts to Binary
def Hex2Bin(mystr):
    mybytes = ['{0:08b}'.format(int(''.join(c), 16)) for c in zip(mystr[::2], \
                                                                mystr[1::2])]
    return ''.join(mybytes)


def String2Bin(mystr):
    mybytes = ['{0:08b}'.format(ord(c)) for c in mystr]
    return ''.join(mybytes)


def Bin2Hex(mybin):
    myHex = ['{0:02x}'.format(int(''.join(c), base = 2)) for c in zip(mybin[::8],
                                                                   mybin[1::8],
                                                                   mybin[2::8],
                                                                   mybin[3::8],
                                                                   mybin[4::8],
                                                                   mybin[5::8],
                                                                   mybin[6::8],
                                                                   mybin[7::8])]
    return ''.join(myHex)

def Bin2String(mybin):
    myString = [chr(int(''.join(c), base=2)) for c in zip(mybin[::8],
                                                          mybin[1::8], 
                                                          mybin[2::8],
                                                          mybin[3::8],
                                                          mybin[4::8],
                                                          mybin[5::8],
                                                          mybin[6::8],
                                                          mybin[7::8])]
    return ''. join(myString)

def Bin2Base64(mybin):
    base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    i = 0
    mylist = []
    while i < len(mybin):
        index = int(mybin[i:i+6], base= 2)
        mylist.append(base64chars[index])
        i += 6
    return ''.join(mylist)
  

def XORHex(str1, str2):
    Bin1 = Hex2Bin(str1)
    Bin2 = Hex2Bin(str2)
    mylist = []
    for i in range(len(Bin1)):
        mylist.append(str(int(Bin1[i]) ^ int(Bin2[i])))
    return ''.join(mylist)
    
def XORBin(str1, str2):    
    mylist = []
    for i in range(len(str1)):
        mylist.append(str(int(str1[i]) ^ int(str2[i])))
    return ''.join(mylist)

def XORString(str1, str2):    
    Bin1 = String2Bin(str1)
    Bin2 = String2Bin(str2)
    mylist = []
    for i in range(len(Bin1)):
        mylist.append(str(int(Bin1[i]) ^ int(Bin2[i])))
    return ''.join(mylist)

def Base64toBin(myB64):
    base64chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    binstring = ''
    myB64 = myB64.strip('=')
    for i in myB64:
        binstring += '{0:06b}'.format(base64chars.find(i))
    if (len(binstring)%8):
        binstring = binstring[:len(binstring)-len(binstring)%8]
    return binstring