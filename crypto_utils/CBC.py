# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:36:25 2015

@author: jakoberickson
"""


import ECB
import crypto_utils


def ApplyCipher(hex_input, hex_key_string, IV):
    if (len(hex_input) % 32 != 0):
        return 'Try Again: input must be even multiple of 16 bytes'
    if (len(hex_key_string) != 32):
        return 'Try Again: key must be exactly 16 bytes'
    if (len(IV) != 32):
        return 'Try Again: IV must be exactly 16 bytes'

    hex_words = ECB.KeyExpansion(hex_key_string)
    input_blocks = [hex_input[i:i+32] for i in range(0, len(hex_input), 32)]
    temp = IV
    output_blocks = []
    for block in input_blocks:
        xord = crypto_utils.hex_XOR(temp, block)
        temp = ECB.Cipher(xord, hex_words)
        output_blocks.append(temp)
    return ''.join(output_blocks)


def ApplyInvCipher(hex_input, hex_key_string, IV):
    if (len(hex_input) % 32 != 0):
        return 'Try Again: input must be even multiple of 16 bytes'
    if (len(hex_key_string) != 32):
        return 'Try Again: key must be exactly 16 bytes'
    if (len(IV) != 32):
        return 'Try Again: IV must be exactly 16 bytes'

    hex_words = ECB.KeyExpansion(hex_key_string)
    input_blocks = [hex_input[i:i+32] for i in range(0, len(hex_input), 32)]
    temp = IV
    output_blocks = []
    for block in input_blocks:
        almostdone = ECB.InvCipher(block, hex_words)
        xord = crypto_utils.hex_XOR(almostdone, temp)
        output_blocks.append(xord)
        temp = block
    return ''.join(output_blocks)
