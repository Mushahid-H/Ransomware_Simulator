from Crypto.Cipher import AES
import os

# Decrypt a file
def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        nonce, tag, ciphertext = [file.read(x) for x in (16, 16, -1)]
    
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    # Save the decrypted file
    decrypted_file_path = file_path.replace('.encrypted', '')
    with open(decrypted_file_path, 'wb') as dec_file:
        dec_file.write(decrypted_data)
    
    return decrypted_file_path
