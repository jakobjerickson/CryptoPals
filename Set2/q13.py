# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 08:23:06 2015

@author: jakoberickson
"""
from crypto_utils import char_to_hex, ECB, hex_to_char
from crypto_utils.oracle import PKCS7_pad, random_hex_generator

def parser(input):
    """
    The routine takes a string input in the form 'foo=bar&baz=qux&zap=zazzle'
    """
    split_input = input.split('&')
    split_entries = [item.split('=') for item in split_input]
    profile = {i[0]:i[1] for i in split_entries if len(i) == 2}
    return profile


def profile_for(email):
    assert '=' not in email and '&' not in email
    return {
        'email' : email,
        'uid' : 10,
        'role' : 'user'
        }


def encode_profile(p):
    """
    takes a profile dictionary and returns an profile encoded as a string
    """
    return '&'.join([
        'email=%s' % p['email'],
        'uid=%d' % p['uid'],
        'role=%s' % p['role']])


def encrypt_profile(profile, hex_key):
    encoded_profile = char_to_hex(profile)
    padded = PKCS7_pad(encoded_profile, 16)
    return ECB.ApplyCipher(padded, hex_key)


def parse_encrypted_profile(encrypted_profile, hex_key):
    encoded_profile = ECB.ApplyInvCipher(encrypted_profile, hex_key)
    parsable = hex_to_char(encoded_profile)
    return parser(parsable)


def main():
    hex_key = random_hex_generator(16)
    admin = profile_for('XXXXXXXXXXadmin')
    honesty = profile_for('honest@mail.c')
    admin_encr = encrypt_profile(encode_profile(admin), hex_key)
    honesty_encr = encrypt_profile(encode_profile(honesty), hex_key)
    cut_n_paste = honesty_encr[:64] + admin_encr[32:64]
    #hex_to_char(ECB.ApplyInvCipher(cut_n_paste, hex_key))

    print parse_encrypted_profile(cut_n_paste, hex_key)


main()