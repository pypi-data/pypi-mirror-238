# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
"""
1.电码本模式（Electronic Codebook Book (ECB)）
2.密码分组链接模式（Cipher Block Chaining (CBC)）
3.计算器模式（Counter (CTR)）
4.密码反馈模式（Cipher FeedBack (CFB)）
5.输出反馈模式（Output FeedBack (OFB)）
四种模式除了 ECB 相对不安全外，其它模式没有太大的差别
"""
# AES/ECB/PKCS#7 对称加密解密
# AES/CBC/PKCS#7/SALT 对称加密解密
# Fernet/SALT 对称加密解密
# RSA/PKCS#1 非对称加密解密

from .aes import *
from .rsa import encryptor, RSAEncryption
