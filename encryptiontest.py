from Crypto.Cipher import AES
import requests
# Function is to check the length of the utf-8
def utf8len(s):
    return len(s.encode('utf-8'))
key = ''
#to get the random number so that I can start traversing through that point
r = requests.get(url="http://quest.phy.stevens.edu:5050/main?lower=1&higher=194&amount=1")
startPosition = r.json()['finalrandomarray'][0]
offsetAmount = 0
print(startPosition)
#To calculate the start position from where we are going to start traversing in a file
#if the startposition is greater than 194, i.e., minimum line number to be taken from a file then subtract it a bit
if startPosition > 194:
    offsetAmount = startPosition-194
    startPosition= startPosition-offsetAmount
#Read the quantum_keys file and then read 16 lines to generate a key of length 32 bytes, because each character is a byte
with open('Quantum_Keys.txt','r') as f:
    keys = f.readlines()
    for i in range(startPosition-1,startPosition-1+16):
        key = key + keys[i].replace("\n","")
content = key
print("Key size is ",utf8len(content),"\n\n")



#start the encryption with the 32 bytes ecryption, and, Initialization Vector 16 bytes
encryption_suite = AES.new(content, AES.MODE_CBC, 'EncryptionOf16By')
cipher_text = encryption_suite.encrypt("hello world 1234hello world ")
print("cipher text's length is ", len(cipher_text),'and the text')


# Decryption
decryption_suite = AES.new(content, AES.MODE_CBC, 'EncryptionOf16By')
plain_text = decryption_suite.decrypt(cipher_text)
print("decrypted text is ", plain_text)