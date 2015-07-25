# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 11:20:32 2015

@author: jakoberickson
"""
# declare contants
common_letters = 'etaoin shrdlu'
alphabet = 'abcdefghijklmnopqrstuvwxyz '


from crypto_utils import hex_to_binary

def get_key_scores(input_string, type = 'hex'):    

    if type == 'hex':
        encrypted_binary_string = hex_to_binary(input_string)
    elif type == 'bin':
        encrypted_binary_string = input_string
    else:
        print 'Please input a hexidecimal or binary string'
        return

    xord_binary_strings = cycle_keys(encrypted_binary_string)
    key_scores = {}

    for i in xord_binary_strings.keys():
        temp = binary_to_string(xord_binary_strings[i])
        if english_language_score(temp): 
            key_scores[i] = english_language_score(temp)
    if len(key_scores) == 0: return None
    # return the key with the smallest non-zero score 
    best_score = min(key_scores, key = key_scores.get)
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
    else: return None               
               
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

def binary_XOR(str1, str2):    
    mylist = []
    for i in range(len(str1)):
        mylist.append(str(int(str1[i]) ^ int(str2[i])))
    return ''.join(mylist)



def get_benchmark_frequencies():
        #loads the complete works of Jane Austen found at www.gutenberg.org
    # and removes any extra whitespace
    fh = open('Set1/JaneAusten.txt')

    temp = []
    for line in fh:
        if (len(line.strip()) != 0): temp.append(line.strip())
    #skip the first 31 lines, which is the BOM and a description of the file
    jane_austen_text = ' '.join(temp[31:])
    fh.close()

    # get the frequency of each of the common letters in Jane Austen's texts
    return get_letter_frequency(jane_austen_text)

def binary_to_string(binary_string):
    integer_list = [int(binary_string[i:i+8], base = 2)
        for i in range(0, len(binary_string), 8)]
    character_list = [chr(integer) for integer in integer_list]
    return ''. join(character_list)    

def main():
    global benchmark
    benchmark = get_benchmark_frequencies()
    print "the benchmark letter frequencies from Jane Austen's novels are"
    print benchmark
    
    encrypted_hex = \
    '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'

    integer_key = get_key_scores(encrypted_hex, type = 'hex')[0]
    binary_key = '{0:08b}'.format(integer_key)
    encrypted_binary = hex_to_binary(encrypted_hex)
    xord_binary_string = character_key_XOR(encrypted_binary, binary_key)
    print 'The key is %s and the decrpyted message is:\n' %chr(integer_key) +\
          binary_to_string(xord_binary_string)


main()