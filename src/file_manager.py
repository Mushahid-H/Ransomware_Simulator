import os
from encryption.encrypt import encrypt_file
from encryption.decrypt import decrypt_file
from encryption.key_management import generate_key, save_key, load_key
from config.settings import TEST_FILES_DIR, LOGS_DIR

# Select all files from the test directory
def select_files():
    return [os.path.join(TEST_FILES_DIR, f) for f in os.listdir(TEST_FILES_DIR) if os.path.isfile(os.path.join(TEST_FILES_DIR, f))]

# Encrypt selected files
def encrypt_files(files, key):
    encrypted_files = []
    for file in files:
        encrypted_file = encrypt_file(file, key)
        encrypted_files.append(encrypted_file)
        
        # Delete the original file after encryption
        os.remove(file)
        print(f"Original file {file} deleted after encryption.")
    
    return encrypted_files

# Decrypt selected files
def decrypt_files(files, key):
    decrypted_files = []
    for file in files:
        decrypted_file = decrypt_file(file, key)
        decrypted_files.append(decrypted_file)
        
        # Delete the encrypted file after decryption
        os.remove(file)
        print(f"Encrypted file {file} deleted after decryption.")
    
    return decrypted_files

# Save encryption key for later use
def save_encryption_key(key):
    key_file_path = os.path.join(LOGS_DIR, 'encryption_key.key')
    save_key(key, key_file_path)
