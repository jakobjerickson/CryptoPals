# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 22:47:09 2015

@author: jakoberickson
"""
"""
PKCS#7 padding validation
Write a function that takes a plaintext, determines if it has valid
PKCS#7 padding, and strips the padding off.

The string:

"ICE ICE BABY\x04\x04\x04\x04"
... has valid padding, and produces the result "ICE ICE BABY".

The string:

"ICE ICE BABY\x05\x05\x05\x05"
... does not have valid padding, nor does:

"ICE ICE BABY\x01\x02\x03\x04"
If you are writing in a language with exceptions, like Python or Ruby,
make your function throw an exception on bad padding.

Crypto nerds know where we're going with this. Bear with us.
"""


def check_PKCS7_size(char_plaintext, blocksize=16):
    last_block = char_plaintext[len(char_plaintext)-blocksize:]
    if last_block[-1:] == chr(1):
        return 1
    for i in range(2, blocksize):
        if (last_block[-i:] == i * chr(i)):
            return i
    raise Exception('The string is not PKCS7 padded!')


def remove_padding(char_plaintext, blocksize=16):
    try:
        padding_length = check_PKCS7_size(char_plaintext, 16)
        print 'padding removed'
        return char_plaintext[:-padding_length]
    except:
        print 'PKCS7 was not detected; no padding was removed!'
        return char_plaintext


def main():
    examples = ['ICE ICE BABY\x04\x04\x04\x04',
                'ICE ICE BABY\x05\x05\x05\x05',
                'ICE ICE BABY\x01\x02\x03\x04']
    for item in examples:
        print repr(remove_padding(item))


main()
