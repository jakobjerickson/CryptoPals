# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 11:23:13 2015

@author: jakoberickson
"""
import pandas as pd
import numpy as np

## Set1 Challenge 4

fh = open('Crypto Pals/Set1/4.txt')

HexStrings = []
for line in fh:
    HexStrings.append(line.strip())

fh.close()

minScores = [scoreKeys(item, type = 'hex') for item in HexStrings]

mydf = pd.DataFrame(minScores, columns = ['Integer Key', 'Score'])
mydf['Hex String'] = HexStrings


best = mydf.Score.argmin()
best = mydf.iloc[best, :].values

binKey = len(best[2]) / 2 * '{0:08b}'.format(best[0])

message = Bin2String(XORBin(binKey, Hex2Bin(best[2])))

print message

## Set1 Challenge 5

mystring = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear\
 a cymbal"
 
mykey = ''
i = 0
ice = 'ICE'
while len(mykey) < len(mystring):
    if i > 2: i = 0    
    mykey = mykey + ice[i]
    i += 1
    
test = '0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63343c2a262263242727\
65272a282b2f20430a652e2c652a3124333a653e2b2027630c692b20283165286326302e27282f'

Bin2Hex(XORString(mystring, mykey)) == test


#Set 1 Challenge 6

fh = open('Crypto Pals/Set1/6.txt')

B64text = []

for line in fh:
    B64text.append(line.strip())

fh.close()

B64text = ''.join(B64text)
myBin = Base64toBin(B64text)

HDist1 = {}
HDist2 = {}
HDist3 = {}
HDist4 = {}
HDist5 = {}
HDist6 = {}

for KEYLENGTH in np.arange(2, 41):
    bin1 = ''.join(binList[:KEYLENGTH])
    bin2 = ''.join( binList[KEYLENGTH:2*KEYLENGTH] )
    bin3 = ''.join( binList[2*KEYLENGTH:3*KEYLENGTH] )
    bin4 = ''.join( binList[3*KEYLENGTH:4*KEYLENGTH] )
    HDist1[KEYLENGTH] = float(getHDistance(bin1, bin2))/(KEYLENGTH)
    HDist2[KEYLENGTH] = float(getHDistance(bin1, bin3))/(KEYLENGTH)
    HDist3[KEYLENGTH] = float(getHDistance(bin1, bin4))/(KEYLENGTH)
    HDist4[KEYLENGTH] = float(getHDistance(bin2, bin3))/(KEYLENGTH)
    HDist5[KEYLENGTH] = float(getHDistance(bin2, bin4))/(KEYLENGTH)
    HDist6[KEYLENGTH] = float(getHDistance(bin3, bin4))/(KEYLENGTH)


#looking at the Hamming Distance for each key length I found a 
#local minimum at 29 in all the combinations from above

keylength = 29

## The length of the key is most likely 5!!

Blocks = [myBin[i:i+8*keylength] for i in range(0, len(myBin), 8*keylength)]
if len(Blocks[-1] % 8):
    newLength = len(Blocks[-1]) - len(Blocks[-1])%8
    Blocks[-1] = Blocks[-1][:newLength]
TBlocks = ['' for i in range(keylength)]
for line in Blocks:
    for i in range(len(line)/8):    
        TBlocks[i] += line[i*8:(i+1)*8]

keys = []

for line in TBlocks:
    print 'getting character'
    keys.append(scoreKeys(line, type = 'bin'))
print keys

#I found it!!!!

THEKEY = ''.join([chr(c[0]) for c in keys])
mykey = ''
i = 0
while len(mykey) < len(myBin):
    if i > len(THEKEY) - 1: i = 0    
    mykey = mykey + THEKEY[i]
    i += 1

print(applyKey(myBin, mykey))

#I'm back and I'm ringin' the bell 
#A rockin' on the mike while the fly girls yell 
#In ecstasy in the back of me 
#Well that's my DJ Deshay cuttin' all them Z's 
#Hittin' hard and the girlies goin' crazy 
#Vanilla's on the mike, man I'm not lazy. 
#
#I'm lettin' my drug kick in 
#It controls my mouth and I begin 
#To just let it flow, let my concepts go 
#My posse's to the side yellin', Go Vanilla Go! 
#
#Smooth 'cause that's the way I will be 
#And if you don't give a damn, then 
#Why you starin' at me 
#So get off 'cause I control the stage 
#There's no dissin' allowed 
#I'm in my own phase 
#The girlies sa y they love me and that is ok 
#And I can dance better than any kid n' play 
#
#Stage 2 -- Yea the one ya' wanna listen to 
#It's off my head so let the beat play through 
#So I can funk it up and make it sound good 
#1-2-3 Yo -- Knock on some wood 
#For good luck, I like my rhymes atrocious 
#Supercalafragilisticexpialidocious 
#I'm an effect and that you can bet 
#I can take a fly girl and make her wet. 
#
#I'm like Samson -- Samson to Delilah 
#There's no denyin', You can try to hang 
#But you'll keep tryin' to get my style 
#Over and over, practice makes perfect 
#But not if you're a loafer. 
#
#You'll get nowhere, no place, no time, no girls 
#Soon -- Oh my God, homebody, you probably eat 
#Spaghetti with a spoon! Come on and say it! 
#
#VIP. Vanilla Ice yep, yep, I'm comin' hard like a rhino 
#Intoxicating so you stagger like a wino 
#So punks stop trying and girl stop cryin' 
#Vanilla Ice is sellin' and you people are buyin' 
#'Cause why the freaks are jockin' like Crazy Glue 
#Movin' and groovin' trying to sing along 
#All through the ghetto groovin' this here song 
#Now you're amazed by the VIP posse. 
#
#Steppin' so hard like a German Nazi 
#Startled by the bases hittin' ground 
#There's no trippin' on mine, I'm just gettin' down 
#Sparkamatic, I'm hangin' tight like a fanatic 
#You trapped me once and I thought that 
#You might have it 
#So step down and lend me your ear 
#'89 in my time! You, '90 is my year. 
#
#You're weakenin' fast, YO! and I can tell it 
#Your body's gettin' hot, so, so I can smell it 
#So don't be mad and don't be sad 
#'Cause the lyrics belong to ICE, You can call me Dad 
#You're pitchin' a fit, so step back and endure 
#Let the witch doctor, Ice, do the dance to cure 
#So come up close and don't be square 
#You wanna battle me -- Anytime, anywhere 
#
#You thought that I was weak, Boy, you're dead wrong 
#So come on, everybody and sing this song 
#
#Say -- Play that funky music Say, go white boy, go white boy go 
#play that funky music Go white boy, go white boy, go 
#Lay down and boogie and play that funky music till you die. 
#
#Play that funky music Come on, Come on, let me hear 
#Play that funky music white boy you say it, say it 
#Play that funky music A little louder now 
#Play that funky music, white boy Come on, Come on, Come on 
#Play that funky music 

##Challenge 7

from Crypto.Cipher import AES

fh = urllib.urlopen('http://cryptopals.com/static/challenge-data/7.txt')

myB64 = []

for line in fh:
    myB64.append(line.strip())
    
fh.close()
myB64 = ''.join(myB64)
myHex = Bin2Hex(Base64toBin(MyB64))
myAES = AES.AESCipher('YELLOW SUBMARINE')

print myAES.decrypt(myB64.decode('Base64'))


## Challenge 8

import urllib

fh = urllib.urlopen('http://cryptopals.com/static/challenge-data/8.txt')
myHex = []

for line in fh:
    myHex.append(line.strip())

fh.close()
HexArray = []     
for line in myHex:
	HexArray.append([line[i: i + 32] for i in range(0, 320, 32)])
	
[len(line) != len(set(line)) for line in HexArray].index(True)




   





