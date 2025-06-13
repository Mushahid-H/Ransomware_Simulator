from Crypto.Random import get_random_bytes
import os

# Generate a new encryption key
def generate_key():
    key = get_random_bytes(16)  # 128-bit key for AES
    return key

# Save the key to a file for later recovery
import os

# Save the key to a file for later recovery
def save_key(key, file_path):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    # Save the key to the file
    with open(file_path, 'wb') as key_file:
        key_file.write(key)


# Load the key from a file
def load_key(file_path):
    with open(file_path, 'rb') as key_file:
        key = key_file.read()
    return key
