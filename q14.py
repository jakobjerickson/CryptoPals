# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 15:41:20 2015

@author: jakoberickson
"""
from crypto_utils import oracle
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


def main():
    hex_key = oracle.random_hex_generator(16)
    unknown_hex = oracle.random_hex_generator(random.randint(30, 50))
    mystery_hex = oracle.encryption_oracle2(unknown_hex, hex_key)
    print unknown_hex + '\n' + ''.join(mystery_hex)

main()
