# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import json
import uuid
import time
import string
import base64
import hashlib
import logging
import abc
import six
import hashlib
import hmac
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Protocol import KDF
from nimbus_utils.crypto import get_random_string
from .utils import bord, bchr, to_str, to_bytes, smart_str, smart_bytes


__all__ = ["CryptorError", "DecryptionError", "AESBinCryptor", "AESCryptor", "AES"]

logger = logging.getLogger("encrypt")


class CryptorError(Exception):
    """Base error for when anything goes wrong with AESBaseCryptor."""


class DecryptionError(CryptorError):
    """Raised when bad data is inputted."""


@six.add_metaclass(abc.ABCMeta)
class AESBaseCryptor(object):
    SALT_SIZE = 8
    random_strings = string.ascii_letters + string.digits

    @abc.abstractmethod
    def encrypt(self, data, key):
        pass

    @abc.abstractmethod
    def decrypt(self, data, key):
        pass

    @abc.abstractmethod
    def aes_encrypt(self, key, data, *args, **kwargs):
        pass

    @abc.abstractmethod
    def aes_decrypt(self, key, data, *args, **kwargs):
        pass

    def new_aes(self, key, mode, *args, **kwargs):
        return AES.new(key, mode, *args, **kwargs)

    @classmethod
    def generate_key(cls, size=16):
        return get_random_string(size, cls.random_strings)

    @property
    def encryption_salt(self):
        return Random.new().read(self.SALT_SIZE)

    @property
    def hmac_salt(self):
        return Random.new().read(self.SALT_SIZE)

    @property
    def iv(self):
        return Random.new().read(AES.block_size)

    def _hmac(self, key, data):
        return hmac.new(key, data, hashlib.sha256).digest()

    def _prf(self, secret, salt):
        return hmac.new(secret, salt, hashlib.sha1).digest()

    def _pbkdf2(self, key, salt, iterations=10000, key_length=32):
        return KDF.PBKDF2(key, salt, dkLen=key_length, count=iterations, prf=self._prf)

    def _base64_decode(self, value=""):
        value = smart_bytes(value)
        _de_data = base64.urlsafe_b64decode(value)
        return smart_bytes(_de_data)

    def _base64_encode(self, value=""):
        value = smart_bytes(value)
        _en_data = base64.urlsafe_b64encode(value)
        return smart_str(_en_data)


class AESBinCryptor(AESBaseCryptor):
    mode = AES.MODE_ECB
    cipher = None

    def __init__(self, key, mode=None, **kwargs):
        self.key = key
        self.kwargs = kwargs
        self.mode = mode or self.mode

    def encrypt(self, data, key=None):
        try:
            _key = self._encrypt_key(key)
            _data = self.pre_encrypt_data(data)
            cipher_text = self.aes_encrypt(key=_key, data=_data, **self.kwargs)
            return self.post_encrypt_data(cipher_text)
        except Exception as e:
            logger.error(e)
            return ""

    def decrypt(self, data, key=None):
        try:
            _key = self._decrypt_key(key)
            _data = self.pre_decrypt_data(data)
            decrypted_data = self.aes_decrypt(key=_key, data=_data, **self.kwargs)
            return self.post_decrypt_data(decrypted_data)
        except Exception as e:
            logger.error(e)
            return ""

    def aes_encrypt(self, key, data, *args, **kwargs):
        self.cipher = self.new_aes(key, self.mode, *args, **kwargs)
        _data = self.cipher.encrypt(data)
        return _data

    def aes_decrypt(self, key, data, *args, **kwargs):
        self.cipher = self.new_aes(key, self.mode, *args, **kwargs)
        _data = self.cipher.decrypt(data)
        return _data

    def pre_encrypt_data(self, data):
        data = smart_bytes(data)
        aes_block_size = AES.block_size
        rem = aes_block_size - len(data) % aes_block_size
        return data + bchr(rem) * rem

    def post_encrypt_data(self, data):
        return data

    def pre_decrypt_data(self, data):
        return smart_bytes(data)

    def post_decrypt_data(self, data):
        data = data[:-bord(data[-1])]
        return smart_str(data)

    def _encrypt_key(self, key):
        key = key or self.key
        return smart_bytes(key)

    def _decrypt_key(self, key):
        key = key or self.key
        return smart_bytes(key)


class AESCryptor(AESBinCryptor):
    mode = AES.MODE_ECB

    def pre_encrypt_data(self, data):
        _data = smart_bytes(data)
        return super().pre_encrypt_data(_data)

    def post_encrypt_data(self, data):
        _endata = super().post_encrypt_data(data)
        _endata = smart_bytes(_endata)
        return smart_str(base64.urlsafe_b64encode(_endata))

    def pre_decrypt_data(self, data):
        _data = base64.urlsafe_b64decode(smart_bytes(data))
        _data = smart_bytes(_data)
        return super().pre_decrypt_data(_data)

    def post_decrypt_data(self, data):
        _dedata = super().post_decrypt_data(data)
        return smart_str(_dedata)

