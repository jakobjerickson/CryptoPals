# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 10:25:13 2015

@author: jakoberickson
"""

def main():
    fh = open('Set1/8.txt')
    hex_array = []
    for line in fh:
        hex_array.append(line.strip())
    fh.close()
    
    # break each hexadecimal string into 16-byte blocks
    
    hex_blocks = []
    for line in hex_array:
        temp_block = [line[i: i + 32] for i in range(0, 320, 32)]
        hex_blocks.append(temp_block)
    
    # look for the hex string with any non-unique blocks. True for non-unique
    non_unique = [len(line) != len(set(line)) for line in hex_blocks]
    non_unique_index = non_unique.index(True)

    print 'The %ith line is ECB encrypted\n' %non_unique_index  
    print  hex_blocks[non_unique_index]
    
main()

