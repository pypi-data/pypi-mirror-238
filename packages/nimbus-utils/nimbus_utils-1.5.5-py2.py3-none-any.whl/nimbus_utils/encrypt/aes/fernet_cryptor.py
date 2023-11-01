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
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography import exceptions
from cryptography import fernet
from .utils import bord, bchr, to_str, to_bytes, smart_str, smart_bytes
from .base import AESCryptor, AESBinCryptor, CryptorError, DecryptionError


class FernetCryptor(AESCryptor):
    mode = None

    def __init__(self, key, salt=None):
        super().__init__(key)
        self.salt = salt

    @classmethod
    def generate_salt(cls, size=16):
        return cls.generate_key(size)

    def new_aes(self, key, mode, *args, **kwargs):
        return Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=smart_bytes(self.salt),
            iterations=100000,
            backend=default_backend()
        ).derive(key)))


def generate_salt(size=16):
    return FernetCryptor.generate_salt(size=size)


generate_salt.__doc__ = FernetCryptor.generate_salt.__doc__


def decrypt(data, key, salt):
    cryptor = FernetCryptor(key=key, salt=salt)
    return cryptor.decrypt(data, key)


decrypt.__doc__ = FernetCryptor.decrypt.__doc__


def encrypt(data, key, salt):
    cryptor = FernetCryptor(key=key, salt=salt)
    return cryptor.encrypt(data, key)


encrypt.__doc__ = FernetCryptor.encrypt.__doc__
