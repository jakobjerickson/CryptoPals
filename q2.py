# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 10:42:43 2015

@author: jakoberickson
"""
"""
Fixed XOR
Write a function that takes two equal-length buffers and produces their
XOR combination.

If your function works properly, then when you feed it the string:

1c0111001f010100061a024b53535009181c
... after hex decoding, and when XOR'd against:

686974207468652062756c6c277320657965
... should produce:

746865206b696420646f6e277420706c6179
"""


def hex_to_integer(input_hex_string):
    integer_output_list = [int(''.join(c), 16) for c in
                           zip(input_hex_string[::2], input_hex_string[1::2])]
    return integer_output_list


def hex_XOR(hex_input1, hex_input2):
    integer_input1 = hex_to_integer(hex_input1)
    integer_input2 = hex_to_integer(hex_input2)
    hex_output = ''
    for i, j in zip(integer_input1, integer_input2):
        hex_output += '{0:02x}'.format(i ^ j)
    return hex_output


def main():
    hex_string1 = '1c0111001f010100061a024b53535009181c'
    hex_string2 = '686974207468652062756c6c277320657965'
    xord_hex_string = hex_XOR(hex_string1, hex_string2)
    print xord_hex_string


main()
