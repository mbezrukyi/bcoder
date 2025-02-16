from enum import Enum
from typing import Callable, Union

BEncodeType = Union[
    dict[str, "BEncodeType"],
    str,
    list["BEncodeType"],
    int,
]


class EncodeType(Enum):
    DICTIONARY = dict
    STRING = str
    LIST = list
    INTEGER = int

    @classmethod
    def from_value(cls, value: BEncodeType) -> "EncodeType":
        return next(filter(lambda m: isinstance(value, m.value), cls))


class BEncoder:
    def __init__(self, data: BEncodeType, encoding: str = "utf-8"):
        self._data = data
        self._encoding = encoding

        self._encoders = {
            EncodeType.DICTIONARY: self._encode_dict,
            EncodeType.STRING: self._encode_str,
            EncodeType.LIST: self._encode_list,
            EncodeType.INTEGER: self._encode_int,
        }

    def encode(self) -> bytes:
        return self._get_encoder(self._data)(self._data)

    def _get_encoder(self, value: BEncodeType) -> Callable[["BEncoder", BEncodeType], bytes]:
        return self._encoders[EncodeType.from_value(value)]

    def _encode_dict(self, d: dict[str, BEncodeType]) -> bytes:
        encoded_dict = b"".join(
            self._encode_str(k) + self._get_encoder(v)(v)
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
