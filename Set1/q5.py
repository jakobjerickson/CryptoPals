# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 11:40:37 2015

@author: jakoberickson
"""
"""
Here is the opening stanza of an important work of the English
language:

Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal
Encrypt it, under the key "ICE", using repeating-key XOR.

In repeating-key XOR, you'll sequentially apply each byte of the key;
the first byte of plaintext will be XOR'd against I, the next C, the
next E, then I again for the 4th byte, and so on.

It should come out to:

0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a2622632427276
5272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e
27282f

Encrypt a bunch of stuff using your repeating-key XOR function. Encrypt
your mail. Encrypt your password file. Your .sig file. Get a feel for
it. I promise, we aren't wasting your time with this.
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
