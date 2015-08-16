# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:36:25 2015

@author: jakoberickson
"""

# declare contants
common_letters = 'etaoin shrdlu'
alphabet = 'abcdefghijklmnopqrstuvwxyz '

# the results of GetBenchmark
benchmark = {
    ' ': 0.1796022713452622,
    'a': 0.06173435834220984,
    'b': 0.01240951585907673,
    'c': 0.01886140856265773,
    'd': 0.032889347412749036,
    'e': 0.09946520677401693,
    'f': 0.01813101860371836,
    'g': 0.015095414215779635,
    'h': 0.048749342006532435,
    'i': 0.05377579254079789,
    'j': 0.0011888628266619183,
    'k': 0.004695331240910282,
    'l': 0.031049948760264585,
    'm': 0.021842629532353084,
    'n': 0.05609133293528649,
    'o': 0.06066275259032581,
    'p': 0.012257150501635403,
    'q': 0.0009499888250106817,
    'r': 0.048086415022122804,
    's': 0.04879592358418393,
    't': 0.06813530961604389,
    'u': 0.022690506031970106,
    'v': 0.008634113410308434,
    'w': 0.018455942317779982,
    'x': 0.0013616506491819771,
    'y': 0.0177803947088835,
    'z': 0.0003634739852214782
    }


def get_key_scores(input_string, encoding='hex'):

    if encoding == 'hex':
        encrypted_binary_string = hex_to_binary(input_string)
    elif encoding == 'bin':
        encrypted_binary_string = input_string
    else:
        print 'Please input a hexidecimal or binary string'
        return

    xord_binary_strings = cycle_keys(encrypted_binary_string)
    key_scores = {}

    for i in xord_binary_strings.keys():
        temp = binary_to_char(xord_binary_strings[i])
        if english_language_score(temp):
            key_scores[i] = english_language_score(temp)
    if len(key_scores) == 0:
        return None
# return the key with the smallest non-zero score
    best_score = min(key_scores, key=key_scores.get)
    return best_score, key_scores[best_score]


# returns the sum of squared deviation from the benchmark
# text's letter frequencies
def english_language_score(test_string):
    SS = 0
    letter_frequency = get_letter_frequency(test_string)
    if (sum(letter_frequency.values()) != 0):
        for char in common_letters:
            SS += (letter_frequency[char] - benchmark[char])**2
        return SS
    else:
        return None


def get_letter_frequency(input_string):
    letter_count = {}
    for char in alphabet:
        letter_count[char] = input_string.lower().count(char)
    total = float(len(input_string))
    letter_frequency = {}
    if total != 0:
        for char in alphabet:
            letter_frequency[char] = letter_count[char] / total
    return letter_frequency


def character_key_XOR(encrypted_binary, binary_key):
    length = len(encrypted_binary)
    expanded_key = binary_key * (length / 8)
    xord_binary = binary_XOR(encrypted_binary, expanded_key)
    return xord_binary


def cycle_keys(encrypted_binary):
    xord_binary_strings = {}
    for i in range(128):
        key = '{0:08b}'.format(i)
        xord_binary_strings[i] = character_key_XOR(encrypted_binary, key)
    return xord_binary_strings


def binary_XOR(binary_input1, binary_input2):
    binary_output = ''
    for m, n in zip(binary_input1, binary_input2):
        binary_output += str(int(m) ^ int(n))
    return binary_output


def hex_XOR(hex_string1, hex_string2):
    binary_string1 = hex_to_binary(hex_string1)
    binary_string2 = hex_to_binary(hex_string2)
    binary_list = []
    for i in range(len(binary_string1)):
        xord = str(int(binary_string1[i]) ^ int(binary_string2[i]))
        binary_list.append(xord)
    return binary_to_hex(''.join(binary_list))


def hex_to_binary(hex_string):
    binary_string = ['{0:08b}'.format(int(''.join(char), 16))
                     for char in zip(hex_string[::2], hex_string[1::2])]
    return ''.join(binary_string)


def hex_to_integer(input_hex_string):
    integer_output_list = [int(''.join(c), 16) for c in
                           zip(input_hex_string[::2], input_hex_string[1::2])]
    return integer_output_list


def hex_to_char(hex_input):
    char_output = ''
    for i in range(0, len(hex_input), 2):
        char_output += chr(int(hex_input[i:i+2], base=16))
    return char_output


def binary_to_base64(binary_string):
    base64chars = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        )
    i = 0
    base64_output = ''
    while i < len(binary_string):
        index = int(binary_string[i:i+6], base=2)
        base64_output += base64chars[index]
        i += 6
    return base64_output


def binary_to_char(binary_string):
    integer_list = [int(binary_string[i:i+8], base=2)
                    for i in range(0, len(binary_string), 8)]
    character_list = [chr(integer) for integer in integer_list]
    return ''. join(character_list)


def binary_to_hex(binary_string):
    hex_string = ''
    for i in range(0, len(binary_string), 8):
        temp_hex_char = '{0:02x}'.format(int(binary_string[i:i+8], base=2))
        hex_string += temp_hex_char
    return hex_string


def char_to_binary(input_char_string):
    binary_output = ''
    for letter in input_char_string:
        temp_byte = '{0:08b}'.format(ord(letter))
        binary_output += temp_byte
    return binary_output


def base64_to_binary(base64_string):
    base64chars = (
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
        )
    binary_string = ''
    base64_string = base64_string.strip('=')
    for i in base64_string:
        binary_string += '{0:06b}'.format(base64chars.find(i))
    if (len(binary_string) % 8):
        padding_length = len(binary_string) % 8
        binary_string = binary_string[:(len(binary_string) - padding_length)]
    return binary_string


def base64_to_hex(base64_string):
    return(binary_to_hex(base64_to_binary(base64_string)))


def get_hamming_distance(binary_string1, binary_string2):
    return binary_XOR(binary_string1, binary_string2).count('1')


def char_to_hex(char_input):
    return ''.join('{0:02x}'.format(ord(char)) for char in char_input)
