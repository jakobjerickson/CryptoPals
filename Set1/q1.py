# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:24:43 2015

@author: jakoberickson
"""
"""
Convert hex to base64
The string:

49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6
e6f7573206d757368726f6f6d
Should produce:

SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
So go ahead and make that happen. You'll need to use this code for the
rest of the exercises.

Cryptopals Rule
Always operate on raw bytes, never on encoded strings. Only use hex and
base64 for pretty-printing.
"""


# converts a hexidecimal encoded string to a 8-bit per character binary string
def hex_to_binary(hex_string):
    binary_string = ['{0:08b}'.format(int(''.join(char), 16))
                     for char in zip(hex_string[::2], hex_string[1::2])]
    return ''.join(binary_string)


# encodes a binary string to Base64
def binary_to_base64(binary_string):
    base64chars = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        )
    i = 0
    base64_output = ''
    while i < len(binary_string):
        index = int(binary_string[i:i+6], base=2)
        base64_output += base64chars[index]
        i += 6
    return base64_output


def main():
    hex_string = (
        '49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736'
        'f6e6f7573206d757368726f6f6d'
        )
    temp_binary_string = hex_to_binary(hex_string)
    base64_string = binary_to_base64(temp_binary_string)
    print base64_string


main()
