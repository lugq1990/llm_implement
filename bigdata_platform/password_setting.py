## based on AES cipher to encrypt and decrypt
import base64
import os
from Crypto.Cipher import AES 




PASSWORD_PATH = os.getcwd()


def get_default_key(key=None):
    if not key or len(key) != 16:
        # will use current folder path as key
        key = PASSWORD_PATH.split('/')[-1]
        if len(key) < 16:
            # key should be length 16
            key = key + '@' * (16 - len(key))
        else:
            key = key[:16]
    return key.encode()


def bytes_to_str(x):
    if isinstance(x, bytes):
        return x.decode('utf-8')
    return x
    

def encrypt(data, key=None, save_to_local=False, file_name='encrpyted.bin', spe=b' '):
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if not key:
        key = get_default_key()
        
    cipher = AES.new(key, AES.MODE_EAX)
    # do encrpt
    ciphertext, tag = cipher.encrypt_and_digest(data)

    # write res into folder
    if save_to_local:
        with open(file_name, 'wb') as f:
            [f.write(x) for x in [cipher.nonce, tag, ciphertext]]
        return ''
    else:
        res_data = cipher.nonce + spe + tag + spe + ciphertext
        return res_data
    

def decrpt(data=None, key=None, from_local=False, file_name='encrpyted.bin', spe=b'|'):
    if from_local:
        with open(file_name, 'rb') as f:
            nonce, tag, ciphertext = [f.read(x) for x in [16, 16, -1]]
    else:
        if not isinstance(data, bytes):
            raise ValueError("couldn't extract data")
        nonce, tag, ciphertext = data.split(spe)
    
    key = get_default_key(key)
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    
    data = data.decode()
    
    return data
        

# register with pyspark udf function
from pyspark.sql.types import BinaryType, StringType
from pyspark.sql.functions import udf 
from pyspark.sql import SparkSession

spark = SparkSession.builder.getOrCreate()

spark.udf.register('encrypt', encrypt, returnType=BinaryType())
spark.udf.register('decrpt', decrpt, returnType=StringType())


              
if __name__ == "__main__":
    print(PASSWORD_PATH)  
    data = 'this is '
    print(encrypt(data))
    print(decrpt())
    
