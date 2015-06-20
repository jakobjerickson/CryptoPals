##Encryption tools

#  pad key with extra bytes
def PKCS(myKey, newLength):
    myKey = myKey + chr(4) * (length - len(myKey))
	return myKey
PKCS('YELLOW SUBMARINE', 20)	

