

import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now you should be able to import the encryption module
from encryption.key_management import generate_key, save_key, load_key
from src.file_manager import select_files, encrypt_files, decrypt_files
from config.settings import LOGS_DIR


# 1. Generate a new encryption key
key = generate_key()
key_file_path = os.path.join(LOGS_DIR, 'encryption_key.key')

# Save the key to a file for recovery
save_key(key, key_file_path)

# 2. Select the files from the test directory
files_to_encrypt = select_files()

# 3. Encrypt the files
print("Encrypting files...")
encrypted_files = encrypt_files(files_to_encrypt, key)
print(f"Encrypted files: {encrypted_files}")

# 4. Decrypt the files
print("Decrypting files...")
decrypted_files = decrypt_files(encrypted_files, key)
print(f"Decrypted files: {decrypted_files}")

# 5. Verify if the decrypted files match the originals
for original, decrypted in zip(files_to_encrypt, decrypted_files):
    with open(original, 'r') as orig_file, open(decrypted, 'r') as dec_file:
        original_content = orig_file.read()
        decrypted_content = dec_file.read()
        assert original_content == decrypted_content, f"Error: {original} and {decrypted} don't match!"
        print(f"Success: {original} matches {decrypted}")
