import pickle
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from assets.constants import APP_KEY

# Function to load and decrypt the database


def load_database(db_path):

    with open(db_path, "rb") as f:
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(APP_KEY), modes.ECB(),
                    backend=default_backend())
    decryptor = cipher.decryptor()

    try:
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return pickle.loads(data)
    except Exception:
        return {}

# Function to save and encrypt the database


def save_database(db_path, data):

    serialized_data = pickle.dumps(data)

    padder = PKCS7(128).padder()
    padded_data = padder.update(serialized_data) + padder.finalize()

    cipher = Cipher(algorithms.AES(APP_KEY), modes.ECB(),
                    backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    with open(db_path, "wb") as f:
        f.write(encrypted_data)
