# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import sys
import json
import uuid
import time
import base64
import hashlib
import hmac
import logging
import six
from dateutil import parser
from datetime import datetime
from nimbus_utils.encoding import smart_str, smart_bytes

if six.PY2:
    def to_bytes(s):
        if isinstance(s, str):
            return s
        if isinstance(s, unicode):
            return s.encode('utf-8')

    to_str = to_bytes

    def bchr(s):
        return chr(s)

    def bord(s):
        return ord(s)
else:
    unicode = str  # hack for pyflakes (https://bugs.launchpad.net/pyflakes/+bug/1585991)

    def to_bytes(s):
        if isinstance(s, bytes):
            return s
        if isinstance(s, str):
            return s.encode('utf-8')

    def to_str(s):
        if isinstance(s, bytes):
            return s.decode('utf-8')
        if isinstance(s, str):
            return s

    def bchr(s):
        return bytes([s])


    def bord(s):
        return s

