# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 20:43:25 2015

@author: jakoberickson
"""

## Set1 Challenge 4
from crypto_utils import get_key_scores, binary_XOR, binary_to_string


def main():

    fh = open('Set1/4.txt')
    hex_list = []
    for line in fh:
        hex_list.append(line.strip())
    fh.close()
   
   
    # 
    temp =  [get_key_scores(item) for item in hex_list]
    best_scores = [item[1] for item in temp]
    best_keys = [item[0] for item in temp]

    minimum_score_index = best_scores.index(min(best_scores))
    
    
    binKey = len(hex_list[minimum_score_index]) / 2 *\
             '{0:08b}'.format(best_keys[minimum_score_index])
    
    binary_message = binary_XOR(binKey, Hex2Bin(hex_list[minimum_score_index]))
    english_message = binary_to_string(binary_message)
    print (
        'The %dth hex string is English and it has been encrypted with "%s."'
        %(minimum_score_index + 1, 
        '{0:02x}'.format(best_keys[minimum_score_index]))
        )
    print 'The message is:\n' + english_message

main()