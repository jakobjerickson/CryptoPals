# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 20:15:06 2015

@author: jakoberickson
"""
import random
from crypto_utils import ECB, CBC, hex_to_char


def char_PKCS(char_input, output_length):
    padding_length = output_length - len(char_input)
    char_output = char_input + chr(padding_length) * padding_length
    return char_output


def hex_PKCS(hex_input, padding_length):
    padding = '{0:02x}'.format(padding_length) * padding_length
    return hex_input + padding


def ECB_detector(hex_ciphertext, blocksize=16):
    cipher_blocks = [hex_ciphertext[i: i+blocksize]
                     for i in range(0, len(hex_ciphertext), blocksize)]
    if len(cipher_blocks) != len(set(cipher_blocks)):
        return True
    else:
        return False


def random_hex_generator(length=1):
    random_sequence = [random.randint(0, 127) for i in range(length)]
    return ''.join('{0:02x}'.format(item) for item in random_sequence)


def encryption_oracle(plaintext_hex_input):
    padded_plaintext = random_padding(plaintext_hex_input)
    random_hex_key = random_hex_generator(16)
    if random.randint(0, 1):
        return ECB.ApplyCipher(padded_plaintext, random_hex_key)
    else:
        random_IV = random_hex_generator(16)
        return CBC.ApplyCipher(padded_plaintext, random_hex_key, random_IV)


def PKCS7_pad(hex_plaintext, blocksize=16):
    last_block_size = (len(hex_plaintext) % (2 * blocksize)) / 2
    padding_length = blocksize - last_block_size
    padding = '{0:02x}'.format(padding_length) * padding_length
    return hex_plaintext + padding


def random_padding(plain_hex):
    front_padding = random_hex_generator(length=random.randint(5, 10))
    back_padding = random_hex_generator(length=random.randint(5, 10))
    return front_padding + plain_hex + back_padding


def detect_block_size(unknown_string, hex_key_string):
    for double_block in range(2, 66, 2):
        appended_string = '41' * double_block + unknown_string
        padded_string = PKCS7_pad(appended_string, 16)
        ciphertext = ECB.ApplyCipher(padded_string, hex_key_string)
        if ECB_detector(ciphertext, double_block):
            return double_block / 2
    raise Exception('block size not detected!')


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
                random_hex_generator(random.randint(1, 16)) +
                '41' * double_block)
            padded_string = PKCS7_pad(randomly_padded, 16)
            ciphertext = ECB.ApplyCipher(padded_string, hex_key_string)
            if ECB_detector(ciphertext, double_block/2):
                return double_block / 2
            i += 1
    return None


def encryption_oracle2(unknown_hex, hex_key):
    """
    Used for questions 12 and 14
    discovers the contents of an unknown text by making multiple calls
    to the compare_text function in order to account for random padding
    added to the front of each plaintext
    """
    if ECB_detector(ECB.ApplyCipher(unknown_hex, hex_key), 16):
        print 'ECB detected!'
    blocksize = detect_block_size2(hex_key)
    if blocksize is None:
        raise Exception('block size not detected! Try again.')
    discovered_text = ''
    for i in range(0, len(unknown_hex), 2):
        oracle_text = '41' * (blocksize - 1)
        mystery_text = oracle_text + unknown_hex[i:i+2]
        next_character = compare_ciphertext(oracle_text, mystery_text, hex_key)
        while next_character is None:
            next_character = compare_ciphertext(oracle_text, mystery_text,
                                                hex_key)
        discovered_text += next_character
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
            print hex_to_char(item)
            return item
    print '??'
    return None

