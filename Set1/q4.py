# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:43:25 2015

@author: jakoberickson
"""
"""
Detect single-character XOR
One of the 60-character strings in this file has been encrypted by
single-character XOR.

Find it.

(Your code from #3 should help.)
"""
import crypto_utils


def main():
    fh = open('Set1/4.txt')
    hex_list = []
    for line in fh:
        hex_list.append(line.strip())
    fh.close()

    temp = [crypto_utils.get_key_scores(item) for item in hex_list]
    best_scores = [item[1] for item in temp]
    best_keys = [item[0] for item in temp]
    minimum_score = min(best_scores)
    minimum_score_index = best_scores.index(minimum_score)

    short_binary_key = '{0:08b}'.format(best_keys[minimum_score_index])
    expanded_key = len(hex_list[minimum_score_index]) / 2 * short_binary_key

    binary_input = crypto_utils.hex_to_binary(hex_list[minimum_score_index])
    binary_message = crypto_utils.binary_XOR(expanded_key, binary_input)
    english_message = crypto_utils.binary_to_char(binary_message)
    key_character = chr(best_keys[minimum_score_index])

    print (
        'The %dth hex string is English and it has been encrypted with %s.'
        % (minimum_score_index + 1, key_character)
        )
    print 'The message is:\n' + english_message


main()
