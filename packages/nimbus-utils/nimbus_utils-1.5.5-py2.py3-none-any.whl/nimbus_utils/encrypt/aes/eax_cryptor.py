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


class AESEAXCryptor(AESCryptor):
    mode = AES.MODE_EAX

    def __init__(self, key):
        super().__init__(key)

    def aes_encrypt(self, key, data, *args, **kwargs):
        ciphertext = super().aes_encrypt(key, data, *args, **kwargs)
        tag = self.cipher.digest()
        nonce = self.cipher.nonce
        new_data = b''.join([smart_bytes(nonce), smart_bytes(tag), ciphertext])
        return new_data

    def aes_decrypt(self, key, data, *args, **kwargs):
        n = len(data)
        nonce = data[0:16]
        tag = data[16:32]
        ciphertext = data[32:n]
        _data = super().aes_decrypt(key, ciphertext, nonce, **kwargs)
        self.cipher.verify(tag)
        return _data


def decrypt(data, key):
    cryptor = AESEAXCryptor(key=key)
    return cryptor.decrypt(data, key)


decrypt.__doc__ = AESEAXCryptor.decrypt.__doc__


def encrypt(data, key):
    cryptor = AESEAXCryptor(key=key)
    return cryptor.encrypt(data, key)


encrypt.__doc__ = AESEAXCryptor.encrypt.__doc__
