# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import json
import uuid
import time
import hmac
import base64
import hashlib
import logging
from dateutil import parser
from datetime import datetime
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from .utils import bord, bchr, to_str, to_bytes, smart_str, smart_bytes
from .base import AESCryptor, AESBinCryptor, CryptorError, DecryptionError


if hasattr(hmac, 'compare_digest'):
    def compare_in_constant_time(left, right):
        return hmac.compare_digest(left, right)
else:
    def compare_in_constant_time(left, right):
        length_left = len(left)
        length_right = len(right)

        result = length_left - length_right
        for i, byte in enumerate(right):
            result |= bord(left[i % length_left]) ^ bord(byte)
        return result == 0


class AESCBCCryptor(AESCryptor):
    mode = AES.MODE_CBC
    SALT_SIZE = 8

    def __init__(self, key):
        super().__init__(key)

    def aes_encrypt(self, key, data, *args, **kwargs):
        encryption_salt = self.encryption_salt
        encryption_key = self._pbkdf2(key, encryption_salt)
        hmac_salt = self.hmac_salt
        hmac_key = self._pbkdf2(key, hmac_salt)
        iv = self.iv
        cipher_text = super().aes_encrypt(encryption_key, data, iv, **kwargs)
        version = b'\x03'
        options = b'\x01'
        new_data = b''.join([version, options, encryption_salt, hmac_salt, iv, cipher_text])
        encrypted_data = new_data + self._hmac(hmac_key, new_data)
        return encrypted_data

    def aes_decrypt(self, key, data, *args, **kwargs):
        n = len(data)
        # version = data[0]  # unused now
        # options = data[1]  # unused now
        encryption_salt = data[2:10]
        hmac_salt = data[10:18]
        iv = data[18:34]
        cipher_text = data[34:n - 32]
        hmac = data[n - 32:]
        encryption_key = self._pbkdf2(key, encryption_salt)
        hmac_key = self._pbkdf2(key, hmac_salt)
        if not compare_in_constant_time(self._hmac(hmac_key, data[:n - 32]), hmac):
            raise DecryptionError("Bad data")
        return super().aes_decrypt(encryption_key, cipher_text, iv, **kwargs)


def decrypt(data, key):
    cryptor = AESCBCCryptor(key=key)
    return cryptor.decrypt(data, key)


decrypt.__doc__ = AESCBCCryptor.decrypt.__doc__


def encrypt(data, key):
    cryptor = AESCBCCryptor(key=key)
    return cryptor.encrypt(data, key)


encrypt.__doc__ = AESCBCCryptor.encrypt.__doc__
