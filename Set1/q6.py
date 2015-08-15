# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 12:24:57 2015

@author: jakoberickson
"""
"""
Break repeating-key XOR
It is officially on, now.
This challenge isn't conceptually hard, but it involves actual error-
prone coding. The other challenges in this set are there to bring you
up to speed. This one is there to qualify you. If you can do this one,
you're probably just fine up to Set 6.

There's a file here. It's been base64'd after being encrypted with
repeating-key XOR.

Decrypt it.

Here's how:

Let KEYSIZE be the guessed length of the key; try values from 2 to
(say) 40.
Write a function to compute the edit distance/Hamming distance between
two strings. The Hamming distance is just the number of differing bits.
The distance between:

this is a test

and

wokka wokka!!!

is 37. Make sure your code agrees before you proceed.
For each KEYSIZE, take the first KEYSIZE worth of bytes, and the second
KEYSIZE worth of bytes, and find the edit distance between them.
Normalize this result by dividing by KEYSIZE.
The KEYSIZE with the smallest normalized edit distance is probably the
key. You could proceed perhaps with the smallest 2-3 KEYSIZE values. Or
take 4 KEYSIZE blocks instead of 2 and average the distances.
Now that you probably know the KEYSIZE: break the ciphertext into
blocks of KEYSIZE length.
Now transpose the blocks: make a block that is the first byte of every
block, and a block that is the second byte of every block, and so on.
Solve each block as if it was single-character XOR. You already have
code to do this.
For each block, the single-byte XOR key that produces the best looking
histogram is the repeating-key XOR key byte for that block. Put them
together and you have the key.
This code is going to turn out to be surprisingly useful later on.
Breaking repeating-key XOR ("Vigenere") statistically is obviously an
academic exercise, a "Crypto 101" thing. But more people "know how" to
break it than can actually break it, and a similar technique breaks
something much more important.

No, that's not a mistake.
We get more tech support questions for this challenge than any of the
other ones. We promise, there aren't any blatant errors in this text.
In particular: the "wokka wokka!!!" edit distance really is 37.
"""


from crypto_utils import binary_XOR, get_key_scores, binary_to_char, char_to_binary


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


def get_hamming_distance(binary_string1, binary_string2):
    return binary_XOR(binary_string1, binary_string2).count('1')


def apply_repeating_key(binary_input_string, expanded_key_string):
    binary_key = ''.join(char_to_binary(letter) 
                         for letter in expanded_key_string)
    xord_binary = binary_XOR(binary_input_string, binary_key)
    return binary_to_char(xord_binary)


def main():
    fh = open('Set1/6.txt')
    temp_list = []
    for line in fh:
        temp_list.append(line.strip())
    fh.close()

    base64_input_string = ''.join(temp_list)
    binary_input_string = base64_to_binary(base64_input_string)
    hamming_distances1 = {}
    hamming_distances2 = {}
    hamming_distances3 = {}
    hamming_distances4 = {}
    hamming_distances5 = {}
    hamming_distances6 = {}

    # create 4 binary sections of 'byte_key_length' bytes and find the Hamming
    # Distance for each combination of sections
    for byte_key_length in range(2, 41):
        bit_key_length = byte_key_length * 8

        binary_section1 = ''.join(
            binary_input_string[:bit_key_length])
        binary_section2 = ''.join(
            binary_input_string[bit_key_length:2*bit_key_length])
        binary_section3 = ''.join(
            binary_input_string[2*bit_key_length:3*bit_key_length])
        binary_section4 = ''.join(
            binary_input_string[3*bit_key_length:4*bit_key_length])

        hamming_distances1[byte_key_length] = get_hamming_distance(
            binary_section1, binary_section2) / float(bit_key_length)
        hamming_distances2[byte_key_length] = get_hamming_distance(
            binary_section1, binary_section3) / float(bit_key_length)
        hamming_distances3[byte_key_length] = get_hamming_distance(
            binary_section1, binary_section4) / float(bit_key_length)
        hamming_distances4[byte_key_length] = get_hamming_distance(
            binary_section2, binary_section3) / float(bit_key_length)
        hamming_distances5[byte_key_length] = get_hamming_distance(
            binary_section2, binary_section4) / float(bit_key_length)
        hamming_distances6[byte_key_length] = get_hamming_distance(
            binary_section3, binary_section4) / float(bit_key_length)

    hamming_means = {}
    for i in hamming_distances1.keys():
        hamming_means[i] = (
            hamming_distances1[i] + hamming_distances2[i] +
            hamming_distances3[i] + hamming_distances4[i] +
            hamming_distances5[i] + hamming_distances6[i]) / 6

    print 'The mean Hamming length for each key size is:\n'
    print hamming_means
    print '\nThe minimum occurs at a key length of 29\n\n'

    # looking at the mean Hamming Distance for each key length I found
    # a minimum at 29
    byte_key_length = 29
    bit_key_length = byte_key_length * 8
    input_length = len(binary_input_string)

    # split up the binary input string into blocks of length bit_key_length
    input_blocks = [binary_input_string[i: i + bit_key_length]
                    for i in range(0, input_length, bit_key_length)]

# takes the ith byte of each input block and combines them in order to form the
# ith row of transposed_blocks
    transposed_blocks = ['' for i in range(byte_key_length)]
    for line in input_blocks:
        for i in range(0, len(line), 8):
            transposed_blocks[i/8] += line[i:i+8]

    integer_key_list = []
    for line in transposed_blocks:
        print 'getting character'
        integer_key_list.append(get_key_scores(line, encoding='bin'))
    print '\n\n\n'

    key_string = ''.join([chr(c[0]) for c in integer_key_list])
    print 'The key is:\n\n%s\n' % key_string
    expanded_key_string = ''
    i = 0
    while len(expanded_key_string) < len(binary_input_string) / 8.0:
        if i > len(key_string) - 1:
            i = 0
        expanded_key_string += key_string[i]
        i += 1

    print(
        'The message is:\n\n' +
        apply_repeating_key(binary_input_string, expanded_key_string)
        )

main()
