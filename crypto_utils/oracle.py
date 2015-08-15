# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 20:15:06 2015

@author: jakoberickson
"""
import random


def char_PKCS(char_input, output_length):
    padding_length = output_length - len(char_input)
    char_output = char_input + chr(padding_length) * padding_length
    return char_output


def hex_PKCS(hex_input, padding_length):
    padding = '{0:02x}'.format(padding_length) * padding_length
    return hex_input + padding


def ECB_detector(hex_ciphertext):
    cipher_blocks = [hex_ciphertext[i: i+32]
                     for i in range(0, len(hex_ciphertext), 32)]
    if len(cipher_blocks) != len(set(cipher_blocks)):
        return True
    else:
        return False


def random_hex_generator(length=1):
    random_sequence = [random.randint(0, 127) for i in range(16)]
    return ''.join('{0:02x}'.format(item) for item in random_sequence)


def encryption_oracle(plaintext_hex_input):
    padded_plaintext = random_padder(plaintext_hex_input)
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


def random_padding(hex_plaintext):
    front_padding = random_hex_generator(length=random.randint(5, 10))
    back_padding = random_hex_generator(length=random.randint(5, 10))
    return front_padding + plaintext_hex_input + back_padding

