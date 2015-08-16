# -*- coding: utf-8 -*-
"""
Created on Sat Aug 8 17:50:12 2015

@author: jakoberickson
"""
from crypto_utils import CBC, base64_to_binary, binary_to_hex, hex_to_char


"""
Implement CBC mode
CBC mode is a block cipher mode that allows us to encrypt irregularly-
sizedmessages, despite the fact that a block cipher natively only
transforms individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block
before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext
block, is added to a "fake 0th ciphertext block" called the
initialization vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote
earlier, making it encrypt instead of decrypt (verify this by
decrypting whatever you encrypt to test), and using your XOR function
from the previous exercise to combine them.

The file here is intelligible (somewhat) when CBC decrypted against
"YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

Don't cheat.
Do not use OpenSSL's CBC code to do CBC mode, even to verify your
results. What's the point of even doing this stuff if you aren't going
to learn from it?
"""


def main():
    fh = open('Set2/10.txt')
    base64_list = []
    for line in fh:
        base64_list.append(line.strip())
    fh.close()

    base64_cipher = ''.join(base64_list)
    hex_ciphertext = binary_to_hex(base64_to_binary(base64_cipher))

    key_string = 'YELLOW SUBMARINE'
    hex_key_string = ''.join(['{0:02x}'.format(ord(c)) for c in key_string])
    initialization_vector = '0' * 32

    hex_plaintext = CBC.ApplyInvCipher(
        hex_ciphertext, hex_key_string, initialization_vector)
    print hex_to_char(hex_plaintext)


main()
