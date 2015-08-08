# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:40:37 2015

@author: jakoberickson
"""


def main():
    input_string = (
        "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a "
        'cymbal'
        )

    key_string = ''
    i = 0
    ice = 'ICE'
    while len(key_string) < len(input_string):
        if i > 2:
            i = 0
        key_string = key_string + ice[i]
        i += 1
    xord_hex_list = []
    for i in range(len(input_string)):
        temp_int1 = ord(input_string[i])
        temp_int2 = ord(key_string[i])
        xord_hex_list.append('{0:02x}'.format(temp_int1 ^ temp_int2))

    print ''.join(xord_hex_list)


main()
