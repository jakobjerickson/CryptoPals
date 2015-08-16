# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 10:25:13 2015

@author: jakoberickson
"""
"""
Detect AES in ECB mode
In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and
deterministic; the same 16 byte plaintext block will always produce the
same 16 byte ciphertext.
"""


def main():
    fh = open('Set1/8.txt')
    hex_array = []
    for line in fh:
        hex_array.append(line.strip())
    fh.close()

    # break each hexadecimal string into 16-byte blocks
    hex_blocks = []
    for line in hex_array:
        temp_block = [line[i: i + 32] for i in range(0, 320, 32)]
        hex_blocks.append(temp_block)

    # look for the hex string with any non-unique blocks. True for non-unique
    non_unique = [len(line) != len(set(line)) for line in hex_blocks]
    non_unique_index = non_unique.index(True)

    print 'The %ith line is ECB encrypted\n' % non_unique_index
    print hex_blocks[non_unique_index]


main()
