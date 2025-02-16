from enum import Enum
from typing import Callable, Union

BEncodeType = Union[
    dict[Union[str, bytes], "BEncodeType"],
    str,
    list["BEncodeType"],
    int,
    bytes,
]


class EncodeType(Enum):
    DICTIONARY = dict
    STRING = str
    LIST = list
    INTEGER = int
    BYTES = bytes

    @classmethod
    def from_value(cls, value: BEncodeType) -> "EncodeType":
        return next(filter(lambda m: isinstance(value, m.value), cls))


class BEncoder:
    def __init__(self, encoding: str = "utf-8"):
        self._encoding = encoding

        self._encoders = {
            EncodeType.DICTIONARY: self._encode_dict,
            EncodeType.STRING: self._encode_str,
            EncodeType.LIST: self._encode_list,
            EncodeType.INTEGER: self._encode_int,
            EncodeType.BYTES: self._encode_bytes,
        }

    def encode(self, data: BEncodeType) -> bytes:
        return self._get_encoder(data)(data)

    def _get_encoder(self, value: BEncodeType) -> Callable[["BEncoder", BEncodeType], bytes]:
        return self._encoders[EncodeType.from_value(value)]

    def _encode_dict(self, d: dict[str, BEncodeType]) -> bytes:
        encoded_dict = b"".join(
            self._get_encoder(k)(k) + self._get_encoder(v)(v)
            for k, v in d.items()
        )

        return b"d" + encoded_dict + b"e"

    def _encode_str(self, s: str) -> bytes:
        length = str(len(s)).encode(self._encoding)
        encoded_str = s.encode(self._encoding)

        return length + b":" + encoded_str

    def _encode_list(self, l: list) -> bytes:
        encoded_values = b"".join(
            self._get_encoder(v)(v)
            for v in l
        )

        return b"l" + encoded_values + b"e"

    def _encode_int(self, i: int) -> bytes:
        return b"i" + str(i).encode(self._encoding) + b"e"

    def _encode_bytes(self, b: bytes) -> bytes:
        length = str(len(b)).encode(self._encoding)

        return length + b":" + b
