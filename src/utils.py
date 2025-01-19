# Auxliary functions
import os
import pickle
from assets.constants import SALT_DB, FILE_DB

# Function to initialize the databases


def initialize_databases():
    if not os.path.exists(SALT_DB):
        with open(SALT_DB, "wb") as f:
            pickle.dump({}, f)

    if not os.path.exists(FILE_DB):
        with open(FILE_DB, "wb") as f:
            pickle.dump({}, f)

# Function to check if the file exists before opening


def file_exists(file_path):
    return os.path.exists(file_path)
