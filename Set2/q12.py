# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 14:45:28 2015

@author: jakoberickson
"""
from crypto_utils import oracle, base64_to_hex, ECB


"""
Byte-at-a-time ECB decryption (Simple)
Copy your oracle function to a new function that encrypts buffers under
ECB mode using a consistent but unknown key (for instance, assign a
single random key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE
ENCRYPTING, the following string:

Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
Spoiler alert.
Do not decode this string now. Don't do it.

Base64 decode the string before appending it. Do not base64 decode the
string by hand; make your code do it. The point is that you don't know
its contents.

What you have now is a function that produces:

AES-128-ECB(your-string || unknown-string, random-key)
It turns out: you can decrypt "unknown-string" with repeated calls to
the oracle function!

Here's roughly how:

Feed identical bytes of your-string to the function 1 at a time ---
start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the
block size of the cipher. You know it, but do this step anyway.
Detect that the function is using ECB. You already know, but do this
step anyways.
Knowing the block size, craft an input block that is exactly 1 byte
short (for instance, if the block size is 8 bytes, make "AAAAAAA").
Think about what the oracle function is going to put in that last byte
position.
Make a dictionary of every possible last byte by feeding different
strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB",
"AAAAAAAC", remembering the first block of each invocation.
Match the output of the one-byte-short input to one of the entries in
your dictionary. You've now discovered the first byte of unknown-
string.
Repeat for the next byte.
Congratulations.
This is the first challenge we've given you whose solution will break
real crypto. Lots of people know that when you encrypt something in ECB
mode, you can see penguins through it. Not so many of them can decrypt
the contents of those ciphertexts, and now you can. If our experience
is any guideline, this attack will get you code execution in security
tests about once a year.
"""


def detect_block_size(unknown_string, hex_key_string):
    for double_block in range(2, 66, 2):
        appended_string = '41' * double_block + unknown_string
        padded_string = oracle.PKCS7_pad(appended_string, 16)
        ciphertext = ECB.ApplyCipher(padded_string, hex_key_string)
        if oracle.ECB_detector(ciphertext, double_block):
            return double_block / 2
    raise Exception('block size not detected!')


def encryption_oracle2(unknown_hex, hex_key):
    if oracle.ECB_detector(ECB.ApplyCipher(unknown_hex, hex_key)):
        print 'ECB detected!'
    blocksize = detect_block_size(unknown_hex, hex_key)
    discovered_text = []
    for i in range(0, len(unknown_hex), 2):
        oracle_text = '41' * (blocksize - 1)
        mystery_text = oracle_text + unknown_hex[i:i+2]
        discovered_text.append(compare_ciphertext(oracle_text, mystery_text,
                                                  hex_key))
    return discovered_text


def compare_ciphertext(oracle_text, mystery_text, hex_key):
    mystery_cipher = ECB.ApplyCipher(mystery_text, hex_key)
    hex_dictionary = ['{0:02x}'.format(i) for i in range(256)]
    for item in hex_dictionary:
        oracle_cipher = ECB.ApplyCipher(oracle_text + item, hex_key)
        if oracle_cipher == mystery_cipher:
            print item
            return item
    print '??'
    return '??'


def main():
    unknown_encoded = (
        'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24g'
        'c28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFu'
        'ZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/'
        'IE5vLCBJIGp1c3QgZHJvdmUgYnkK'
        )
    unknown_hex = base64_to_hex(unknown_encoded)
    persistent_key = oracle.random_hex_generator(16)
    print encryption_oracle2(unknown_hex, persistent_key)
main()
