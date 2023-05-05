from typing import NamedTuple

from nacl.signing import SigningKey as NaClSigningKey

from .types import AccountNumber, SigningKey, hexstr


class KeyPair(NamedTuple):
    private: SigningKey
    public: AccountNumber


def bytes_to_hex(bytes_: bytes) -> hexstr:
    return hexstr(bytes(bytes_).hex())


def generate_key_pair() -> KeyPair:
    signing_key = NaClSigningKey.generate()
    return KeyPair(
        private=bytes_to_hex(bytes(signing_key)),
        public=bytes_to_hex(signing_key.verify_key),
    )
