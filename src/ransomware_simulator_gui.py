import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

import sys
from time import sleep

# Add the root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.file_manager import select_files, encrypt_files, decrypt_files
from encryption.key_management import generate_key, save_key, load_key
from config.settings import LOGS_DIR, TEST_FILES_DIR


class RansomwareSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ransomware Simulator")
        self.root.geometry("800x600")  # Increased window size
        self.root.configure(bg="#2C3E50")  # Dark blue-grey background

        # Initialize Variables
        self.key = None
        self.files_to_encrypt = []
        self.encrypted_files = []
        self.is_encrypted = False  # Track if the files have already been encrypted
        self.simulated_key = "decrypt"  # Simulated key obtained from attacker

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Title
        self.title_label = tk.Label(self.root, text="Ransomware Simulator", font=("Arial", 24, "bold"), fg="#ECF0F1", bg="#2C3E50")
        self.title_label.pack(pady=30)

        # Countdown Label
        self.countdown_label = tk.Label(self.root, text="Attack begins in 5 seconds...", font=("Arial", 18), bg="#2C3E50", fg="yellow")
        self.countdown_label.pack(pady=20)

        # Ransomware Dashboard
        self.dashboard_frame = tk.Frame(self.root, bg="#2C3E50")
        self.dashboard_frame.pack(pady=20)

        # Encryption Progress Bar
        self.encryption_progress_label = tk.Label(self.dashboard_frame, text="Encryption Progress", font=("Arial", 12), bg="#2C3E50", fg="white")
        self.encryption_progress_label.grid(row=0, column=0, padx=10)

        self.encryption_progress = ttk.Progressbar(self.dashboard_frame, length=350, mode='determinate', maximum=100)
        self.encryption_progress.grid(row=0, column=1, padx=10)

        # Decryption Progress Bar
        self.decryption_progress_label = tk.Label(self.dashboard_frame, text="Decryption Progress", font=("Arial", 12), bg="#2C3E50", fg="white")
        self.decryption_progress_label.grid(row=1, column=0, padx=10)

        self.decryption_progress = ttk.Progressbar(self.dashboard_frame, length=350, mode='determinate', maximum=100)
        self.decryption_progress.grid(row=1, column=1, padx=10)

        # Status Label
        self.status_label = tk.Label(self.root, text="Files' Encryption in Progress...", font=("Arial", 14), bg="#2C3E50", fg="white")
        self.status_label.pack(pady=20)

        # Key Entry Field
        self.key_entry_label = tk.Label(self.root, text="Enter decryption key:", font=("Arial", 12), bg="#2C3E50", fg="white")
        self.key_entry_label.pack(pady=10)

        self.key_entry = tk.Entry(self.root, font=("Arial", 14), width=30)
        self.key_entry.pack(pady=10)

        # Decrypt Button (after entering the correct key)
        self.decrypt_button = tk.Button(self.root, text="Decrypt Files", command=self.decrypt_files, font=("Arial", 14), bg="green", fg="white", width=20)
        self.decrypt_button.pack(pady=10)
        self.decrypt_button.config(state="disabled")

        # Start countdown
        self.countdown_time = 5
        self.start_countdown()

    def start_countdown(self):
        """Starts a 5-second countdown before encryption."""
        if self.countdown_time > 0:
            self.countdown_label.config(text=f"Attack begins in {self.countdown_time} seconds...")
            self.countdown_time -= 1
            self.root.after(1000, self.start_countdown)  # Call again after 1 second
        else:
            self.countdown_label.config(text="Attack begins now!")
            self.start_simulation()  # Start encryption after countdown ends

    def start_simulation(self):
        if not self.is_encrypted:
            # Start encryption simulation if files are not already encrypted
            self.key = generate_key()
            key_file_path = os.path.join(LOGS_DIR, 'encryption_key.key')
            save_key(self.key, key_file_path)

            # Select files to encrypt using file dialog
            self.files_to_encrypt = select_files()
            if not self.files_to_encrypt:
                messagebox.showerror("Error", "No files found to encrypt.")
                return

            self.status_label.config(text="Encrypting files...")

            # Simulate encryption
            self.encrypt_files()
        else:
            # If files are already encrypted, show decryption option
            self.decryption_prompt()

    def encrypt_files(self):
        total_files = len(self.files_to_encrypt)
        for idx, file in enumerate(self.files_to_encrypt):
            self.encryption_progress['value'] = (idx + 1) / total_files * 100
            self.root.update()

            self.status_label.config(text=f"Encrypting {os.path.basename(file)}...")
            sleep(0.5)  # Simulate time for encryption
            
            encrypted_file = encrypt_files([file], self.key)[0]
            self.encrypted_files.append(encrypted_file)

        self.status_label.config(text="Files encrypted successfully!")
        self.encryption_progress['value'] = 100
        self.root.update()

        # Update state to indicate that the files are encrypted
        self.is_encrypted = True

        # Ask the user to get the decryption key
        self.status_label.config(text="Pay the ransom and get the decryption key and paste it below.")
        self.decrypt_button.config(state="normal")

    def decryption_prompt(self):
        # Ask user if they want to decrypt
        if self.is_encrypted:
            answer = messagebox.askquestion("Decryption", "Would you like to decrypt the files now?")
            if answer == 'yes':
                self.status_label.config(text="Decrypting files...")
                self.decrypt_files()
            else:
                self.status_label.config(text="Decryption skipped. Files remain encrypted.")

    def decrypt_files(self):
        entered_key = self.key_entry.get()
        
        # Validate the key entered by the user
        if entered_key == self.simulated_key:
            total_files = len(self.encrypted_files)
            for idx, file in enumerate(self.encrypted_files):
                self.decryption_progress['value'] = (idx + 1) / total_files * 100
                self.root.update()

                self.status_label.config(text=f"Decrypting {os.path.basename(file)}...")
                sleep(0.5)  # Simulate time for decryption
               
                decrypted_file = decrypt_files([file], self.key)[0]

            self.status_label.config(text="Files decrypted successfully! See You next time.")
            self.decryption_progress['value'] = 100
            self.root.update()

            # Final message
            messagebox.showinfo("Success", "Thank you for the generocity!")

            # Close the application after decryption is successful
            self.root.quit()

        else:
            # Invalid key entered
            messagebox.showerror("Error", "Invalid key! Please enter the correct decryption key.")

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = RansomwareSimulatorApp(root)
    root.mainloop()
