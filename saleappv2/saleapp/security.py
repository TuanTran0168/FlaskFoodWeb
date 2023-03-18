from builtins import print


def caesar_encrypt(plaintext, shift):
    """
    Mã hóa một chuỗi văn bản bằng thuật toán Caesar
    với số đơn vị shift cho trước.
    """
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():
            # Mã hóa chữ cái
            shifted_char = chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            # Không mã hóa ký tự đặc biệt hoặc số
            shifted_char = char
        ciphertext += shifted_char
    return ciphertext


def caesar_decrypt(ciphertext, shift):
    """
    Giải mã một chuỗi mã hóa bằng thuật toán Caesar
    với số đơn vị shift cho trước.
    """
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            # Giải mã chữ cái
            shifted_char = chr((ord(char) - 65 - shift) % 26 + 65)
        else:
            # Không giải mã ký tự đặc biệt hoặc số
            shifted_char = char
        plaintext += shifted_char
    return plaintext


# from Crypto.Cipher import AES
# import base64

# Khóa mã hóa
# key = b'sixteen byte key'
#
#
# # Hàm mã hóa số điện thoại
# def encrypt_phone_number(phone_number):
#     # Điều chỉnh độ dài chuỗi để phù hợp với khối 16 byte
#     padded_phone_number = phone_number + ' ' * (16 - len(phone_number) % 16)
#
#     # Tạo đối tượng mã hóa AES
#     cipher = AES.new(key, AES.MODE_ECB)
#
#     # Mã hóa chuỗi số điện thoại
#     encrypted_phone_number = cipher.encrypt(padded_phone_number.encode('utf-8'))
#
#     # Chuyển đổi kết quả mã hóa sang dạng Base64 để dễ dàng lưu trữ và truyền tải
#     encoded_encrypted_phone_number = base64.b64encode(encrypted_phone_number)
#
#     return encoded_encrypted_phone_number.decode('utf-8')
#
#
# # Hàm giải mã số điện thoại
# def decrypt_phone_number(encoded_encrypted_phone_number):
#     # Giải mã chuỗi mã hóa từ Base64
#     encrypted_phone_number = base64.b64decode(encoded_encrypted_phone_number)
#
#     # Tạo đối tượng giải mã AES
#     cipher = AES.new(key, AES.MODE_ECB)
#
#     # Giải mã chuỗi số điện thoại
#     decrypted_phone_number = cipher.decrypt(encrypted_phone_number).decode('utf-8').strip()
#
#     return decrypted_phone_number
#
#
# # Mã hóa số điện thoại
# encrypted_phone_number = encrypt_phone_number('0123456789')
# print('Mã hóa số điện thoại:', encrypted_phone_number)
#
# # Giải mã số điện thoại
# decrypted_phone_number = decrypt_phone_number(encrypted_phone_number)
# print('Giải mã số điện thoại:', decrypted_phone_number)


#
# # Tạo khóa bí mật ngẫu nhiên
# # key = Fernet.generate_key()
# # print(key)
#

# print(MY_KEY)
#
# # Tạo đối tượng Fernet từ khóa bí mật
# fernet = Fernet(MY_KEY)
#
# # Tin nhắn cần được mã hóa
# message = b"Hello, World!"
# message = b"123"
#
# # Mã hóa tin nhắn
# encrypted_message = fernet.encrypt(message)
#
# # Giải mã tin nhắn
# decrypted_message = fernet.decrypt(encrypted_message)
#
# print("Tin nhắn gốc:", message)
# print("Tin nhắn đã được mã hóa:", encrypted_message)
# print("Tin nhắn đã được giải mã:", decrypted_message)
# print(MY_KEY)

from cryptography.fernet import Fernet

MY_KEY = b'ykWaetYMhda53pQkaSOjsDHLzousmpH0SUUH6ul-TJM='


def ma_hoa_AES(text, key):
    fernet = Fernet(key)
    b_text = str(text).encode()
    text_encrypt = fernet.encrypt(b_text)
    return text_encrypt


def giai_ma_AES(text, key):
    fernet = Fernet(key)
    text_decrypt = fernet.decrypt(text).decode()
    return text_decrypt


import random
from twilio.rest import Client


def send_OTP(account_sid, auth_token, messaging_service_sid, otp, phone_number, message):
    client = Client(account_sid, auth_token)

    client.messages.create(
        messaging_service_sid=messaging_service_sid,
        body=message + str(otp),
        to=phone_number
    )
