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


class AESECBCryptor(AESCryptor):
    mode = AES.MODE_ECB

    def __init__(self, key):
        super().__init__(key)


def decrypt(data, key):
    cryptor = AESECBCryptor(key=key)
    return cryptor.decrypt(data, key)


decrypt.__doc__ = AESECBCryptor.decrypt.__doc__


def encrypt(data, key):
    cryptor = AESECBCryptor(key=key)
    return cryptor.encrypt(data, key)


encrypt.__doc__ = AESECBCryptor.encrypt.__doc__
