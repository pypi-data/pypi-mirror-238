import base64
import json
import os
from typing import Optional

from jwt import jwk_from_dict


def validate(
    signature: Optional[str],
    sub: Optional[str],
    timestamp: Optional[str],
    public_key: Optional[str] = None,
) -> bool:
    """Validate a Ship It request signature

    Args:
        signature (str): The signature from the `X-Proxy-Signature` header
        sub (str): The sub from the `X-User-Sub` header
        timestamp (str): The timestamp from the `X-Proxy-Timestamp` header
        public_key (str, optional): The public key to use for validation.
            If unset, will use the `SHIP_IT_PUBLIC_KEY` environment variable.
    """
    if public_key is None:
        public_key = os.environ["SHIP_IT_PUBLIC_KEY"]

    if signature is None:
        raise ValueError("signature is required")
    if sub is None:
        raise ValueError("sub is required")
    if timestamp is None:
        raise ValueError("timestamp is required")

    key_data = base64.b64decode(public_key)

    key = jwk_from_dict(json.loads(key_data))

    return key.verify(
        signature.encode("utf-8"), f"{sub}@{timestamp}".encode("utf-8")
    )
