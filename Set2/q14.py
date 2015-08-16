# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:41:20 2015

@author: jakoberickson
"""
from crypto_utils import oracle, ECB
import random


"""
Take your oracle function from #12. Now generate a random count of
random bytes and prepend this string to every plaintext. You are
now doing:

AES-128-ECB(random-prefix || attacker-controlled || target-bytes,
random-key)

Same goal: decrypt the target-bytes.

Stop and think for a second.
What's harder than challenge #12 about doing this? How would you
overcome that obstacle? The hint is: you're using all the tools you
already have; no crazy math is required.

Think "STIMULUS" and "RESPONSE".
"""


def detect_block_size2(hex_key_string, max_blocksize=32, max_attempts=30):
    """
    determines the block size used in ECB encrytion, with multiple
    passes at each block size to account for the random padding added
    to the front of each plaintext.
    """
    for double_block in range(8, 2*max_blocksize, 2):
        i = 0
        while i < max_attempts:
            randomly_padded = (
                oracle.random_hex_generator(random.randint(1, 16)) +
                '41' * double_block)
            padded_string = oracle.PKCS7_pad(randomly_padded, 16)
            ciphertext = ECB.ApplyCipher(padded_string, hex_key_string)
            if oracle.ECB_detector(ciphertext, double_block/2):
                return double_block / 2
            i += 1
    return None


def encryption_oracle2(unknown_hex, hex_key):
    """
    discovers the contents of an unknown text by making multiple calls
    to the compare_text function in order to account for random padding
    added to the front of each plaintext
    """
    if oracle.ECB_detector(ECB.ApplyCipher(unknown_hex, hex_key), 16):
        print 'ECB detected!'
    blocksize = detect_block_size2(hex_key)
    if blocksize is None:
        raise Exception('block size not detected! Try again.')
    discovered_text = []
    for i in range(0, len(unknown_hex), 2):
        oracle_text = '41' * (blocksize - 1)
        mystery_text = oracle_text + unknown_hex[i:i+2]
        next_character = compare_ciphertext(oracle_text, mystery_text, hex_key)
        while next_character is None:
            next_character = compare_ciphertext(oracle_text, mystery_text,
                                                hex_key)
        discovered_text.append(next_character)
    return discovered_text


def compare_ciphertext(oracle_text, mystery_text, hex_key):
    """
    the heavy-lifting of the oracle. encrypts and checks until a match
    is found for each character
    """
    mystery_cipher = ECB.ApplyCipher(mystery_text, hex_key)
    hex_dictionary = ['{0:02x}'.format(i) for i in range(256)]
    for item in hex_dictionary:
        oracle_cipher = ECB.ApplyCipher(oracle_text + item, hex_key)
        if oracle_cipher == mystery_cipher:
            print item
            return item
    print '??'
    return None


def main():
    hex_key = oracle.random_hex_generator(16)
    unknown_hex = oracle.random_hex_generator(random.randint(30, 50))
    mystery_hex = encryption_oracle2(unknown_hex, hex_key)
    print unknown_hex + '\n' + ''.join(mystery_hex)

main()
