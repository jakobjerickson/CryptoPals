# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 20:32:54 2015

@author: jakoberickson
"""
from crypto_utils import binary_to_hex, base64_to_binary, hex_to_char, ECB


"""
AES in ECB mode
The Base64-encoded content in this file has been encrypted via AES-128
in ECB mode under the key

"YELLOW SUBMARINE".
(case-sensitive, without the quotes; exactly 16 characters; I like
"YELLOW SUBMARINE" because it's exactly 16 bytes long, and now you do
too).

Decrypt it. You know the key, after all.

Easiest way: use OpenSSL::Cipher and give it AES-128-ECB as the cipher.

Do this with code.
You can obviously decrypt this using the OpenSSL command-line tool,
but we're having you get ECB working in code for a reason. You'll
need it a lot later on, and not just for attacking ECB.
"""


def main():
    fh = open('Set1/7.txt')
    base64_list = []
    for line in fh:
        base64_list.append(line.strip())
    fh.close()

    base64_input = ''.join(base64_list)
    hex_input = binary_to_hex(base64_to_binary(base64_input))

    key_string = 'YELLOW SUBMARINE'
    hex_key_string = ''.join(['{0:02x}'.format(ord(c)) for c in key_string])

    hex_output = ECB.ApplyInvCipher(hex_input, hex_key_string)
    print hex_to_char(hex_output)

main()
