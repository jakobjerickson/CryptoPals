# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:42:43 2015

@author: jakoberickson
"""

from crypto_utils import hex_to_binary

def binary_to_hex(binary_string):
    binary_list = \
        [binary_string[i:i+8] for i in range(0, len(binary_string), 8)] 
    hex_string = ['{0:02x}'.format(int(item)) for item in binary_list]
    return ''.join(hex_string)

def hex_XOR(hex_string1, hex_string2):
    binary_string1 = hex_to_binary(hex_string1)
    binary_string2 = hex_to_binary(hex_string2)
    binary_list = []
    for i in range(len(binary_string1)):
        xord = str(int(binary_string1[i]) ^ int(binary_string2[i]))
        binary_list.append(xord)
    return binary_to_hex(''.join(binary_list))



def main():
    hex_string1 = '1c0111001f010100061a024b53535009181c'
    hex_string2 = '686974207468652062756c6c277320657965'
    
    xord_hex_string = hex_XOR(hex_string1, hex_string2)
    
    print xord_hex_string

main()