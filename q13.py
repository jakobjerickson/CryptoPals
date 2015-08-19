# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 08:23:06 2015

@author: jakoberickson
"""
from crypto_utils import char_to_hex, ECB, hex_to_char
from crypto_utils.oracle import PKCS7_pad, random_hex_generator


"""
ECB cut-and-paste
Write a k=v parsing routine, as if for a structured cookie. The routine
should take:

foo=bar&baz=qux&zap=zazzle
... and produce:

{
  foo: 'bar',
  baz: 'qux',
  zap: 'zazzle'
}
(you know, the object; I don't care if you convert it to JSON).

Now write a function that encodes a user profile in that format, given
an email address. You should have something like:

profile_for("foo@bar.com")
... and it should produce:

{
  email: 'foo@bar.com',
  uid: 10,
  role: 'user'
}
... encoded as:

email=foo@bar.com&uid=10&role=user
Your "profile_for" function should not allow encoding metacharacters
(& and =). Eat them, quote them, whatever you want to do, but don't let
people set their email address to "foo@bar.com&role=admin".

Now, two more easy functions. Generate a random AES key, then:

Encrypt the encoded user profile under the key; "provide" that to the
"attacker".
Decrypt the encoded user profile and parse it.
Using only the user input to profile_for() (as an oracle to generate
"valid" ciphertexts) and the ciphertexts themselves, make a role=admin
profile.
"""


def parser(input):
    """
    The routine takes a string input in the form 'foo=bar&baz=qux&zap=zazzle'
    """
    split_input = input.split('&')
    split_entries = [item.split('=') for item in split_input]
    profile = {i[0]: i[1] for i in split_entries if len(i) == 2}
    return profile


def profile_for(email):
    if '=' in email or '&' in email:
        raise Exception('Invalid email address! Cannot contain "=" or "&"')
    return {
        'email': email,
        'uid': 10,
        'role': 'user'
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
    print parse_encrypted_profile(cut_n_paste, hex_key)


main()
