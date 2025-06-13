import os

# Define the base directory for the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Corrected path for test files directory
TEST_FILES_DIR = os.path.join(BASE_DIR, '..', 'assets', 'test_files')

# Directory paths for logs
LOGS_DIR = os.path.join(BASE_DIR, '..', 'logs')

# Encryption parameters
KEY_SIZE = 16  # AES key size (128 bits)
ENC_MODE = 'EAX'  # AES mode of operation
