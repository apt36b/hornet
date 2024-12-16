# Fully attributed to github.com/llzo3
#
# Not an official part of the ransomware, but a script to decrypt files encrypted by the ransomware as an extra. 
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from rich.console import Console
import os
import secrets

# For rich and detailed logs
console = Console()

def decrypt_file(filepath: str, key: bytes) -> None:
    """
    복호화된 파일을 복원합니다.

    :param filepath: 복호화할 파일의 경로
    :param key: AES-GCM 암호화 키
    """
    try:
        with open(filepath, "rb") as file:
            data = file.read()

        # 암호화된 파일에서 nonce(12바이트)와 ciphertext 분리
        nonce = data[:12]
        ciphertext = data[12:]

        # AES-GCM 복호화 수행
        aesgcm = AESGCM(key)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)

        # 복호화된 파일 저장 (원래 파일 이름 복원)
        decrypted_filepath = filepath.replace(".enc", "")
        with open(decrypted_filepath, "wb") as file:
            file.write(plaintext)
        console.log(f"Successfully decrypted {filepath} to {decrypted_filepath}.")

        # 원본 암호화된 파일 삭제
        os.remove(filepath)
    except Exception as e:
        console.log(f"[bold red]An error occurred while decrypting {filepath}: {e}")


def decrypt_directory_walk(directory: str, key: bytes) -> int:
    """
    디렉터리를 재귀적으로 탐색하면서 모든 암호화된 파일을 복호화

    :param directory: 탐색할 디렉터리 경로
    :param key: AES-GCM 복호화 키
    :return: 복호화된 파일의 수
    """
    number_of_files_decrypted = 0

    # 디렉터리가 존재하는지 확인
    if not os.path.exists(directory):
        console.log(f"[bold red]Directory {directory} does not exist.")
        return number_of_files_decrypted

    try:
        for root, _, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                console.log(f"Checking file: {filepath}")  # 파일 경로 출력
                if filepath.endswith(".enc"):
                    console.log(f"Decrypting: {filepath}")
                    decrypt_file(filepath, key)
                    number_of_files_decrypted += 1
    except os.error as e:
        console.log(f"[bold red]An error occurred while walking through the directory: {e}")

    return number_of_files_decrypted

if __name__ == "__main__":
    # 사용자로부터 키를 입력받음
    key_hex = input("Enter the decryption key (in hexadecimal format): ").strip()
    try:
        key = bytes.fromhex(key_hex)
        directory = input("Enter the directory to decrypt: ").strip()

        # 디렉터리 복호화 시작
        number_of_files_decrypted = decrypt_directory_walk(directory, key)
        console.log(f"[green]Decryption completed. Total files decrypted: {number_of_files_decrypted}.")
    except ValueError:
        console.log("[bold red]Invalid key format. Please ensure the key is in hexadecimal format.")
    except Exception as e:
        console.log(f"[bold red]An unexpected error occurred: {e}")
