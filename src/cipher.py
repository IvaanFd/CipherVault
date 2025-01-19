import os
import base64
import secrets
from tkinter import filedialog, messagebox, simpledialog
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.backends import default_backend
from .database import load_database, save_database
from assets.constants import SALT_DB, FILE_DB

# Function to generate cipher keys


def generate_keys():

    user_identifier = simpledialog.askstring(
        "Identificador", "Ingrese su identificador:")
    if not user_identifier:
        return

    db = load_database(SALT_DB)

    if user_identifier in db:
        messagebox.showerror("Error", "El identificador ya existe.")
        return

    # Generar un salt y claves
    salt = secrets.token_bytes(16)
    private_key = secrets.token_bytes(64)  # AES-512 (64 bytes)
    public_key = base64.urlsafe_b64encode(private_key[:32])  # Primera mitad

    # Guardar en la base de datos cifrada
    db[user_identifier] = {
        "salt": salt,
        "public_key": public_key
    }

    save_database(SALT_DB, db)

    # Guardar la clave privada en el PC del usuario
    private_key_path = filedialog.asksaveasfilename(
        title="Guardar clave privada",
        filetypes=[("Archivos clave", "*.key")],
        defaultextension=".key"
    )
    if private_key_path:
        with open(private_key_path, "wb") as f:
            f.write(private_key)
        messagebox.showinfo(
            "Éxito", "Claves generadas y guardadas correctamente.")
    else:
        messagebox.showerror("Error", "No se guardó la clave privada.")

# Function to encrypt a file


def encrypt_file():

    user_identifier = simpledialog.askstring(
        "Identificador", "Ingrese su identificador:")
    if not user_identifier:
        return

    db = load_database(SALT_DB)

    if user_identifier not in db:
        messagebox.showerror("Error", "Identificador no encontrado.")
        return

    public_key = base64.urlsafe_b64decode(db[user_identifier]["public_key"])

    # Seleccionar archivo para cifrar
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo para cifrar")
    if not file_path:
        return

    # Leer el contenido del archivo
    with open(file_path, "rb") as f:
        plaintext = f.read()

    # Cifrar el contenido
    iv = secrets.token_bytes(16)
    cipher = Cipher(algorithms.AES(public_key),
                    modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Guardar archivo cifrado
    encrypted_file_path = filedialog.asksaveasfilename(
        title="Guardar archivo cifrado",
        filetypes=[("Archivos cifrados", "*.enc")],
        defaultextension=".enc"
    )

    if encrypted_file_path:
        with open(encrypted_file_path, "wb") as f:
            f.write(iv + ciphertext)

        # Guardar la relación en la base de datos de archivos
        file_db = load_database(FILE_DB)
        file_db[os.path.basename(encrypted_file_path)
                ] = os.path.splitext(file_path)[1]
        save_database(FILE_DB, file_db)

        messagebox.showinfo("Éxito", "Archivo cifrado correctamente.")

# Function to decrypt a file


def decrypt_file():

    user_identifier = simpledialog.askstring(
        "Identificador", "Ingrese su identificador:")
    if not user_identifier:
        return

    db = load_database(SALT_DB)

    if user_identifier not in db:
        messagebox.showerror("Error", "Identificador no encontrado.")
        return

    # Seleccionar archivo de clave privada
    private_key_path = filedialog.askopenfilename(
        title="Seleccionar archivo de clave privada",
        filetypes=[("Archivos clave", "*.key")]
    )
    if not private_key_path:
        return

    # Leer la clave privada desde el archivo
    try:
        with open(private_key_path, "rb") as f:
            private_key = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Error al leer la clave privada: {e}")
        return

    # Verificar que la clave privada tenga el tamaño correcto (64 bytes para AES-512)
    if len(private_key) != 64:
        messagebox.showerror("Error", "La clave privada no es válida.")
        return

    # Seleccionar archivo cifrado
    file_path = filedialog.askopenfilename(title="Seleccionar archivo cifrado")
    if not file_path:
        return

    # Leer el contenido del archivo cifrado
    with open(file_path, "rb") as f:
        file_data = f.read()

    iv = file_data[:16]  # Primeros 16 bytes son el IV
    ciphertext = file_data[16:]

    # Descifrar el contenido usando la clave privada (la primera mitad de la clave privada se usa como clave)
    cipher = Cipher(algorithms.AES(private_key[:32]), modes.CBC(
        iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = PKCS7(128).unpadder()
    try:
        plaintext = unpadder.update(padded_data) + unpadder.finalize()
    except ValueError:
        messagebox.showerror(
            "Error", "La clave o el archivo no son correctos.")
        return

    # Recuperar la extensión original del archivo
    file_db = load_database(FILE_DB)
    original_extension = file_db.get(os.path.basename(file_path), "")

    # Guardar archivo descifrado
    decrypted_file_path = filedialog.asksaveasfilename(
        title="Guardar archivo descifrado",
        filetypes=[("Todos los archivos", f"*{original_extension}")],
        defaultextension=original_extension
    )
    if decrypted_file_path:
        with open(decrypted_file_path, "wb") as f:
            f.write(plaintext)
        messagebox.showinfo("Éxito", "Archivo descifrado correctamente.")
