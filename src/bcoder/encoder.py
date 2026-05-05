from enum import Enum
from typing import Callable, Union

BEncodeType = Union[
    dict[bytes, "BEncodeType"],
    list["BEncodeType"],
    int,
    bytes,
]


class EncodeType(Enum):
    DICTIONARY = dict
    LIST = list
    INTEGER = int
    BYTES = bytes

    @classmethod
    def from_value(cls, value: BEncodeType) -> "EncodeType":
        return next(filter(lambda m: isinstance(value, m.value), cls))


class BEncoder:
    def __init__(self):
        self._encoders = {
            EncodeType.DICTIONARY: self._encode_dict,
            EncodeType.LIST: self._encode_list,
            EncodeType.INTEGER: self._encode_int,
            EncodeType.BYTES: self._encode_bytes,
        }

    def encode(self, data: BEncodeType) -> bytes:
        return self._get_encoder(data)(data)

    def _get_encoder(self, value: BEncodeType) -> Callable[["BEncoder", BEncodeType], bytes]:
        return self._encoders[EncodeType.from_value(value)]

    def _encode_dict(self, d: dict[bytes, BEncodeType]) -> bytes:
        encoded_dict = b"".join(
            self._encode_bytes(k) + self._get_encoder(v)(v)
            for k, v in sorted(d.items())
        )

        return b"d" + encoded_dict + b"e"

    def _encode_list(self, l: list) -> bytes:
        encoded_values = b"".join(
            self._get_encoder(v)(v)
            for v in l
        )
        return b"l" + encoded_values + b"e"

    def _encode_int(self, i: int) -> bytes:
        return b"i" + str(i).encode() + b"e"

    def _encode_bytes(self, b: bytes) -> bytes:
        return str(len(b)).encode() + b":" + b
