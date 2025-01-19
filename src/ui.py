import tkinter as tk
from tkinter import ttk
from .cipher import generate_keys, encrypt_file, decrypt_file


def create_ui():
    root = tk.Tk()
    root.title("AES-512 Encryptor")

    # Apply styles with ttk
    style = ttk.Style(root)
    style.theme_use("clam")

    frame = ttk.Frame(root, padding="20")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    # Buttons
    generate_button = ttk.Button(
        frame, text="Generate Keys", command=generate_keys)
    generate_button.grid(row=0, column=0, pady=10, sticky=(tk.W, tk.E))

    encrypt_button = ttk.Button(
        frame, text="Encrypt File", command=encrypt_file)
    encrypt_button.grid(row=1, column=0, pady=10, sticky=(tk.W, tk.E))

    decrypt_button = ttk.Button(
        frame, text="Decrypt File", command=decrypt_file)
    decrypt_button.grid(row=2, column=0, pady=10, sticky=(tk.W, tk.E))

    # Expand columns and rows
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    frame.rowconfigure(2, weight=1)

    # Run the application
    root.mainloop()
