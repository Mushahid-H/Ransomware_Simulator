from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
from config.settings import TEST_FILES_DIR, KEY_SIZE, ENC_MODE

# Encrypt a file
def encrypt_file(file_path, key):
    cipher = AES.new(key, AES.MODE_EAX)
    
    with open(file_path, 'rb') as file:
        file_data = file.read()
    
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    
    # Save encrypted file with ".encrypted" extension
    encrypted_file_path = file_path + '.encrypted'
    with open(encrypted_file_path, 'wb') as enc_file:
        [enc_file.write(x) for x in (cipher.nonce, tag, ciphertext)]
    
    return encrypted_file_path
