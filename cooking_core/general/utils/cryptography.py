import json
from typing import NamedTuple
from uuid import UUID

from nacl.exceptions import CryptoError
from nacl.signing import SigningKey as NaClSigningKey
from nacl.signing import VerifyKey

from .types import AccountNumber, SigningKey, hexstr


class KeyPair(NamedTuple):
    private: str
    public: str


class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)

        return super().default(obj)


def bytes_to_hex(bytes_: bytes) -> hexstr:
    return hexstr(bytes(bytes_).hex())


def derive_public_key(signing_key: SigningKey) -> AccountNumber:
    return AccountNumber(bytes_to_hex(NaClSigningKey(hex_to_bytes(signing_key)).verify_key))


def generate_key_pair() -> KeyPair:
    signing_key = NaClSigningKey.generate()
    return KeyPair(
        private=bytes_to_hex(bytes(signing_key)),
        public=bytes_to_hex(signing_key.verify_key),
    )


def hex_to_bytes(hex_string: hexstr) -> bytes:
    return bytes.fromhex(hex_string)


def is_dict_signature_valid(dict_: dict, verify_key: str, signature: str) -> bool:
    if 'signature' in dict_:
        dict_ = dict_.copy()
        del dict_['signature']

    return is_signature_valid(normalize_dict(dict_), verify_key, signature)


def is_signature_valid(message: bytes, verify_key: str, signature: str) -> bool:
    try:
        verify_key_bytes = hex_to_bytes(verify_key)
        signature_bytes = hex_to_bytes(signature)
    except ValueError:
        return False

    try:
        VerifyKey(verify_key_bytes).verify(message, signature_bytes)
    except CryptoError:
        return False

    return True


def normalize_dict(dict_: dict) -> bytes:
    return json.dumps(dict_, separators=(',', ':'), sort_keys=True, cls=CustomEncoder).encode('utf-8')
