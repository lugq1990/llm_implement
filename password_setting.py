## based on AES cipher to encrypt and decrypt
import base64
import os
from Crypto.Cipher import AES 


PASSWORD_PATH = os.getcwd()


def get_default_key(key):
    if not key or len(key) != 16:
        # will use current folder path as key
        key = PASSWORD_PATH.split('/')[-1]
        if len(key) < 16:
            # key should be length 16
            key = key + '@' * (16 - len(key))
        else:
            key = key[:16]
    return key.encode()
    

def encrypt(data, key=None, password_path=PASSWORD_PATH):
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    key = get_default_key(key)
    
    cipher = AES.new(key, AES.MODE_EAX)
    # do encrpt
    ciphertext, tag = cipher.encrypt_and_digest(data)
    
    # write res into folder
    with open('encrpyed.bin', 'wb') as f:
        [f.write(x) for x in [cipher.nonce, tag, ciphertext]]
    
    return True


def decrpt(key=None):
    with open('encrpyed.bin', 'rb') as f:
        nonce, tag, ciphertext = [f.read(x) for x in [16, 16, -1]]
    
    key = get_default_key(key)
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    data = data.decode()
    
    return data
        

              
if __name__ == "__main__":
    print(PASSWORD_PATH)  
    data = 'this is '
    encrypt(data)
    print(decrpt())
    
