from typing import NamedTuple

from nacl.signing import SigningKey as NaClSigningKey

from .types import AccountNumber, SigningKey, hexstr


class KeyPair(NamedTuple):
    private: SigningKey
    public: AccountNumber


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
