# -*- coding: utf-8 -*-
"""
Created on Sun Aug 9 9:49:12 2015

@author: jakoberickson
"""
"""
An ECB/CBC detection oracle
Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random
bytes.

Write a function that encrypts data under an unknown key --- that is,
a function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]
Under the hood, have the function append 5-10 bytes (count chosen
randomly) before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and
under CBC the other half (just use random IVs each time for CBC). Use
rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. You
should end up with a piece of code that, pointed at a block box that
might be encrypting ECB or CBC, tells you which one is happening.
"""
import random
from crypto_utils import CBC, ECB, oracle


def random_hex_generator(length=1):
    random_sequence = [random.randint(0, 127) for i in range(16)]
    return ''.join('{0:02x}'.format(item) for item in random_sequence)


def encryption_oracle(plaintext_hex_input):
    padded_plaintext = random_padder(plaintext_hex_input)
    padded_plaintext = PKCS7_pad(padded_plaintext)
    random_hex_key = random_hex_generator(16)
    if random.randint(0, 1):
        return ECB.ApplyCipher(padded_plaintext, random_hex_key)
    else:
        random_IV = random_hex_generator(16)
        return CBC.ApplyCipher(padded_plaintext, random_hex_key, random_IV)


def PKCS7_pad(hex_plaintext, blocksize):
    last_block_size = (len(hex_plaintext) % (2 * blocksize)) / 2
    padding_length = blocksize - last_block_size
    padding = '{0:02x}'.format(padding_length) * padding_length
    return hex_plaintext + padding

def random_padder(hex_plaintext):
    front_padding = random_hex_generator(length=random.randint(5, 10))
    back_padding = random_hex_generator(length=random.randint(5, 10))
    return front_padding + plaintext_hex_input + back_padding


def main():
    # generate some data to feed to the detection oracle
    hex_plaintext = '00' * 64
    ciphertext = encryption_oracle(hex_plaintext)
    if oracle.ECB_detector(ciphertext):
        encryption_mode = 'ECB'
    else:
        encryption_mode = 'CBC'
    print encryption_mode


main()