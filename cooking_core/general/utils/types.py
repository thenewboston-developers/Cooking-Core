from pydantic import constr
from pydantic.types import _registered

hexstr = constr(regex=r'^[0-9a-f]+$', strict=True)


class hexstr64(hexstr):  # type: ignore
    min_length = 64
    max_length = 64


class hexstr128(hexstr):  # type: ignore
    min_length = 128
    max_length = 128


@_registered
class AccountNumber(hexstr64):
    pass


@_registered
class SigningKey(hexstr64):
    pass


@_registered
class Signature(hexstr128):
    pass
