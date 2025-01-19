# CipherVault

This project provides a desktop graphical application that allows users to encrypt and decrypt files using the AES-512 encryption algorithm. Users can generate public/private key pairs and use these keys to encrypt or decrypt files.

## Requirements

To run this project, you need Python 3.6 or later installed on your system. Additionally, you need to install the following dependencies:

- `cryptography` for cryptographic operations.
- `tkinter` for the graphical interface.

### Installing Dependencies

If you don't have the dependencies installed, you can install `cryptography` by running the following command:

```bash
pip install cryptography
```

The `tkinter` library is typically pre-installed with Python. If it is not installed, you can install it depending on your operating system.

## Project Description

### Features

1. **Key Generation**:
   - The user can generate a public/private key pair using a unique identifier. The public key is stored in an encrypted database, and the private key is saved as a local file on the user's machine.

2. **File Encryption**:
   - Files can be encrypted using the user's public key. The file content is encrypted using AES-512 in CBC (Cipher Block Chaining) mode, and the encrypted file is saved with a `.enc` extension.

3. **File Decryption**:
   - Encrypted files can be decrypted using the user's private key. The user must select the private key file from their machine, then they can decrypt the encrypted files. The decrypted file is saved with its original extension.

### Structure

```
/CipherVault
│
├── assets/              # Folder for storing encrypted database files (alts.db, files.db)
│
├── src/
│   ├── __init__.py
│   ├── database.py      # Functions for handling encrypted databases
│   ├── encryption.py    # Functions for encryption and decryption logic
│   ├── ui.py            # GUI components
│   └── utils.py         # Helper functions for initializing the app and loading/saving databases
│
├── README.md            # Project documentation
└── run.py               # Initialize the application logic
```

## Setup

1. **Clone the Repository**:

   You can clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/IvaanFd/CipherVault.git
   cd CipherVault
   ```

2. **Install Dependencies**:

   Install the necessary Python packages via `pip`:

   ```bash
   pip install cryptography
   ```

3. **Directory Structure**:

   When you run the application for the first time, it will automatically create in the `assets` directory the necessary files where the encrypted databases will be stored (`slts.db` and `files.db`).

4. **Run the code**

   ```bash
   python run.py
   ```

## How to Use the Application

### 1. **Generate Keys**

- When you open the application, you can generate a public/private key pair using the "Generate Keys" button.
- Enter a unique identifier and save the keys when prompted.
- The public key is stored in the encrypted database, and the private key is saved as a `.key` file on your machine.

### 2. **Encrypt Files**

- Click the "Encrypt File" button to select a file you want to encrypt.
- The application will use your public key to encrypt the file and prompt you to save the encrypted file with a `.enc` extension.
- The relationship between the encrypted file and its original extension is stored in an encrypted database.

### 3. **Decrypt Files**

- Click the "Decrypt File" button to select an encrypted file you want to decrypt.
- You will be prompted to select the file containing your private key.
- After providing the private key, the application will use it to decrypt the file and save it with its original extension.

## Security

- Public keys are stored in an encrypted database.
- Private keys are stored as `.key` files and should be protected appropriately.
- Encrypted files use AES-512 in CBC mode, with a random initialization vector (IV) to ensure data security.

## Dependencies

- `cryptography`: For cryptographic operations (key generation, encryption, decryption).
- `tkinter`: For the graphical user interface.
