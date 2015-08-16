# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 08:42:26 2015

@author: jakoberickson
"""
from crypto_utils import oracle, CBC, hex_to_char, char_to_hex, hex_XOR
import random


"""
CBC bitflipping attacks
Generate a random AES key.

Combine your padding code and CBC code to write two functions.

The first function should take an arbitrary input string, prepend the
string:

"comment1=cooking%20MCs;userdata="
.
.. and append the string:

";comment2=%20like%20a%20pound%20of%20bacon"
The function should quote out the ";" and "=" characters.

The function should then pad out the input to the 16-byte AES block
length and encrypt it under the random AES key.

The second function should decrypt the string and look for the
characters ";admin=true;" (or, equivalently, decrypt, split the string
on ";", convert each resulting string into 2-tuples, and look for the
"admin" tuple).

Return true or false based on whether the string exists.

If you've written the first function properly, it should not be
possible to provide user input to it that will generate the string the
second function is looking for. We'll have to break the crypto to do
that.

Instead, modify the ciphertext (without knowledge of the AES key) to
accomplish this.

You're relying on the fact that in CBC mode, a 1-bit error in a
ciphertext block:

Completely scrambles the block the error occurs in
Produces the identical 1-bit error(/edit) in the next ciphertext block.
Stop and think for a second.
Before you implement this attack, answer this question: why does CBC
mode have this property?
"""


def prepare_string(char_input):
    head = 'comment1=cooking%20MCs;userdata='
    tail = ';comment2=%20like%20a%20pound%20of%20bacon'
    head = prep_helper(head)
    tail = prep_helper(tail)
    return head + char_input + tail


def prep_helper(raw_string):
    temp = '"="'.join(raw_string.split('='))
    return '";"'.join(temp.split(';'))


def pad_and_encrypt(char_input, hex_key, IV):
    plain_hex = char_to_hex(prepare_string(char_input))
    padded_plain = oracle.PKCS7_pad(plain_hex, 16)
    return CBC.ApplyCipher(padded_plain, hex_key, IV)


def admin_checker(cipher, hex_key, IV):
    plain_hex = CBC.ApplyInvCipher(cipher, hex_key, IV)
    depadded = oracle.remove_padding(hex_to_char(plain_hex))
    print [depadded[i:i+16] for i in range(0, len(depadded), 16)]
    return ';admin=true;' in depadded


def bit_flipper(desired_text, existing_text, hex_cipher_block):
    """
    desired and existing are both readable texts. The cipher block must
    immediately precede the block that is being changed. The function
    returns a block of ciphertext that will replace the passed cipher
    block
    """
    desired_text = desired_text + existing_text[len(desired_text):]
    hex1 = char_to_hex(desired_text)
    hex2 = char_to_hex(existing_text)
    flipper = hex_XOR(hex1, hex2)
    return hex_XOR(hex_cipher_block, flipper)


def main():
    hex_key = oracle.random_hex_generator(16)
    random_integers = [random.randint(65, 122) for i in range(35)]
    arbitrary_input = ''.join(chr(i) for i in random_integers)
    IV = oracle.random_hex_generator(16)
    cipher_hex = pad_and_encrypt(arbitrary_input, hex_key, IV)
    if admin_checker(cipher_hex, hex_key, IV):
        print 'admin privileges exist!'
    else:
        print 'you are not the admin!'
    admin = ';admin=true;'
    replacement_block = bit_flipper(admin, 'ng%20MCs";"userd', cipher_hex[:32])
    cipher_hex = replacement_block + cipher_hex[32:]
    if admin_checker(cipher_hex, hex_key, IV):
        print 'admin privileges exist!'
    else:
        print 'you are not the admin!'


main()
