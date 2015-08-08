# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 20:32:54 2015

@author: jakoberickson
"""

from crypto_utils import binary_to_hex, base64_to_binary, hex_to_char, ECB


def main():
    fh = open('Set1/7.txt')
    base64_list = []
    for line in fh:
        base64_list.append(line.strip())
    fh.close()

    base64_input = ''.join(base64_list)
    hex_input = binary_to_hex(base64_to_binary(base64_input))

    key_string = 'YELLOW SUBMARINE'
    hex_key_string = ''.join(['{0:02x}'.format(ord(c)) for c in key_string])

    hex_output = ECB.ApplyInvCipher(hex_input, hex_key_string)
    print hex_to_char(hex_output)

main()
