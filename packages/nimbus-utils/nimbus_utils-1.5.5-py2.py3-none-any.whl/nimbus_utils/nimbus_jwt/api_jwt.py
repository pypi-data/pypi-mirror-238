# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import re
import os
import json
import uuid
import time
import base64
import hashlib
import logging
import gzip
from dateutil import parser
from datetime import datetime

import json
from calendar import timegm
from collections.abc import Iterable, Mapping
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Type, Union

from jwt import PyJWT as BaseJWT
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    ImmatureSignatureError,
    InvalidAudienceError,
    InvalidIssuedAtError,
    InvalidIssuerError,
    MissingRequiredClaimError,
)
from . import api_jws


__all = [
    "PyJWT",
    "encode",
    "decode",
    "decode_complete",
]


class PyJWT(BaseJWT):
    def encode(
            self,
            payload: Dict[str, Any],
            key: str,
            algorithm: Optional[str] = "HS256",
            headers: Optional[Dict] = None,
            json_encoder: Optional[Type[json.JSONEncoder]] = None,
    ) -> str:
        # Check that we get a mapping
        if not isinstance(payload, Mapping):
            raise TypeError(
                "Expecting a mapping object, as JWT only supports "
                "JSON objects as payloads."
            )

        # Payload
        payload = payload.copy()
        for time_claim in ["exp", "iat", "nbf"]:
            # Convert datetime to a intDate value in known time-format claims
            if isinstance(payload.get(time_claim), datetime):
                payload[time_claim] = timegm(payload[time_claim].utctimetuple())

        json_payload = json.dumps(
            payload, separators=(",", ":"), cls=json_encoder
        ).encode("utf-8")

        return api_jws.encode(json_payload, key, algorithm, headers, json_encoder)

    def decode(
        self,
        jwt: str,
        key: str = "",
        algorithms: List[str] = None,
        options: Dict = None,
        **kwargs,
    ) -> Dict[str, Any]:
        decoded = self.decode_complete(jwt, key, algorithms, options, **kwargs)
        return decoded["payload"]

    def decode_complete(
        self,
        jwt: str,
        key: str = "",
        algorithms: List[str] = None,
        options: Dict = None,
        **kwargs,
    ) -> Dict[str, Any]:
        if options is None:
            options = {"verify_signature": True}
        else:
            options.setdefault("verify_signature", True)

        if not options["verify_signature"]:
            options.setdefault("verify_exp", False)
            options.setdefault("verify_nbf", False)
            options.setdefault("verify_iat", False)
            options.setdefault("verify_aud", False)
            options.setdefault("verify_iss", False)

        if options["verify_signature"] and not algorithms:
            raise DecodeError(
                'It is required that you pass in a value for the "algorithms" argument when calling decode().'
            )

        decoded = api_jws.decode_complete(
            jwt,
            key=key,
            algorithms=algorithms,
            options=options,
            **kwargs,
        )

        try:
            payload = json.loads(decoded["payload"])
        except ValueError as e:
            raise DecodeError("Invalid payload string: %s" % e)
        if not isinstance(payload, dict):
            raise DecodeError("Invalid payload string: must be a json object")

        merged_options = {**self.options, **options}
        self._validate_claims(payload, merged_options, **kwargs)

        decoded["payload"] = payload
        return decoded


_jwt_global_obj = PyJWT()
encode = _jwt_global_obj.encode
decode_complete = _jwt_global_obj.decode_complete
decode = _jwt_global_obj.decode
