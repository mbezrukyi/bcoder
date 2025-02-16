from enum import Enum
from typing import Callable, Union

from .errors import DecodeError

BDecodeType = Union[
    dict[bytes, "BDecodeType"],
    bytes,
    list["BDecodeType"],
    int,
]


class DecodeType(Enum):
    DICTIONARY = b"d"
    STRING = b"1234567890"
    LIST = b"l"
    INTEGER = b"i"

    @classmethod
    def from_code(cls, code: int) -> "DecodeType":
        return next(filter(lambda m: code in m.value, cls))


class BDecoder:
    def __init__(self):
        self._data = None
        self._i = None

        self._decoders = {
            DecodeType.DICTIONARY: self._decode_dict,
            DecodeType.STRING: self._decode_str,
            DecodeType.LIST: self._decode_list,
            DecodeType.INTEGER: self._decode_int,
        }

    def decode(self, data: bytes) -> BDecodeType:
        self._data = data
        self._i = 0

        return self._get_decoder()()

    def _get_decoder(self) -> Callable[["BDecoder"], BDecodeType]:
        return self._decoders[DecodeType.from_code(self._data[self._i])]

    def _decode_dict(self) -> dict[bytes, BDecodeType]:
        result = {}

        self._i += 1

        while self._data[self._i] != ord("e"):
            key = self._decode_str()
            result[key] = self._get_decoder()()

        self._i += 1

        return result

    def _decode_str(self) -> bytes:
        if self._data[self._i] == ord("0") and self._data[self._i + 1] != ord(":"):
            raise DecodeError(f"Invalid leading '0' value for str in {self._i} position")

        colon = self._data.index(b":", self._i)
        length = int(self._data[self._i: colon])

        start = colon + 1
        end = start + length

        self._i = end

        return self._data[start:end]

    def _decode_list(self) -> list[BDecodeType]:
        result = []

        self._i += 1

        while self._data[self._i] != ord("e"):
            result.append(self._get_decoder()())

        self._i += 1

        return result

    def _decode_int(self) -> int:
        self._i += 1

        if self._data[self._i] == ord("-") and self._data[self._i + 1] == ord("0"):
            raise DecodeError(f"Invalid '-0' value for int in {self._i} position")
        if self._data[self._i] == ord("0") and self._data[self._i + 1] != ord("e"):
            raise DecodeError(f"Invalid leading '0' value for int in {self._i} position")

        start = self._i
        end = self._data.index(b"e", self._i)

        self._i = end + 1

        return int(self._data[start:end])
