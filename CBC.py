##Encryption tools

#  pad key with extra bytes

# 
import ECB


def PKCS(myKey, newLength):
    myKey = myKey + chr(4) * (newLength - len(myKey))
    return myKey
PKCS('YELLOW SUBMARINE', 20)    

def CBCCipher(inp, key, IV):
    if (len(inp)%32 != 0):
        return 'Try Again: input must be even multiple of 16 bytes'
    if (len(key) != 32):
        return 'Try Again: key must be exactly 16 bytes'
    if (len(IV) != 32):
        return 'Try Again: IV must be exactly 16 bytes'    
    w = KeyExpansion(key)
    blocks = [inp[i:i+32] for i in range(0, len(inp), 32)]
    temp = IV
    ciphertext = []
    for block in blocks:
        temp = ECB.Cipher(XORHex(temp, block), w)
        ciphertext.append(temp)
    return ''.join(ciphertext)
    

def CBCInvCipher(inp, key, IV):
    if (len(inp)%32 != 0):
        return 'Try Again: input must be even multiple of 16 bytes'
    if (len(key) != 32):
        return 'Try Again: key must be exactly 16 bytes'
    if (len(IV) != 32):
        return 'Try Again: IV must be exactly 16 bytes'    
    w = KeyExpansion(key)
    blocks = [inp[i:i+32] for i in range(0, len(inp), 32)]
    temp = IV
    plaintext = []
    for block in blocks:
        plaintext.append(XORHex(temp, ECB.InvCipher(block, w)))
        temp = block
    return ''.join(plaintext)