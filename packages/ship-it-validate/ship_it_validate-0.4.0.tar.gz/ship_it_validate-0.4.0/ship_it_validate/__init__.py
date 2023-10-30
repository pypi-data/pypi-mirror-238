import base64
import json
import os
import time
from typing import Optional

from jose import jwk


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

    if time.time() - int(timestamp) / 1000 > 60:
        raise ValueError("signature is expired")

    key_data = json.loads(base64.b64decode(public_key))

    key = jwk.construct(key_data, "ES256")

    # Verify the signature using the key
    payload = f"{sub}@{timestamp}"

    sig = base64.b64decode(signature)

    return key.verify(payload.encode("utf-8"), sig)
