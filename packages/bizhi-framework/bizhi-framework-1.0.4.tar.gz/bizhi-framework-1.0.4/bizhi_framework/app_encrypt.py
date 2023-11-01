# -*- coding: utf-8 -*-
"""
@Author: HuangWenBin
@Date: 2023-02-24 11:30:45
@LastEditTime: 2023-05-11 15:53:57
@LastEditors: HuangWenBin
@Description: 
"""

from Crypto.Cipher import DES
from seven_framework import config
import base64

class app_des_encrypt():
    def __init__(self):
        self.des_secret_key=config.get_value("des_encrypt_key")

    def des_encrypt(self,content):
        content=content.encode()
        padding_len = DES.block_size - (len(content) % DES.block_size)
        padded_plaintext = content + bytes([padding_len] * padding_len)

        des_obj = DES.new(self.des_secret_key.encode(), DES.MODE_CBC, self.des_secret_key.encode())
        secret_bytes = des_obj.encrypt(padded_plaintext)    
        return base64.b64encode(secret_bytes)

    def des_decrypt(self, content):
        secret_bytes = base64.b64decode(content)
        des_obj = DES.new(self.des_secret_key.encode(), DES.MODE_CBC, self.des_secret_key.encode())
        decrypted_padded_plaintext = des_obj.decrypt(secret_bytes)

        # 移除填充
        if len(decrypted_padded_plaintext) > 0:
            padding_len = decrypted_padded_plaintext[-1]
            decrypted_plaintext = decrypted_padded_plaintext[:-padding_len]
        else:
            decrypted_plaintext = decrypted_padded_plaintext

        return decrypted_plaintext