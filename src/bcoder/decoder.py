from enum import Enum
from typing import Union

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
        self._decoders = {
            DecodeType.DICTIONARY: self._decode_dict,
            DecodeType.STRING: self._decode_str,
            DecodeType.LIST: self._decode_list,
            DecodeType.INTEGER: self._decode_int,
        }

    def decode(self, data: bytes) -> BDecodeType:
        value, _ = self._decode(data, 0)

        return value

    def _decode(self, data: bytes, i: int) -> tuple[BDecodeType, int]:
        return self._decoders[DecodeType.from_code(data[i])](data, i)

    def _decode_dict(self, data: bytes, i: int) -> tuple[dict[bytes, BDecodeType], int]:
        result = {}

        i += 1

        while data[i] != ord("e"):
            key, i = self._decode_str(data, i)
            result[key], i = self._decode(data, i)

        return result, i + 1

    def _decode_str(self, data: bytes, i: int) -> tuple[bytes, int]:
        if data[i] == ord("0") and data[i + 1] != ord(":"):
            raise DecodeError(f"Invalid leading '0' value for str in {i} position")

        colon = data.index(b":", i)
        length = int(data[i:colon])

        start = colon + 1
        end = start + length

        return data[start:end], end

    def _decode_list(self, data: bytes, i: int) -> tuple[list[BDecodeType], int]:
        result = []

        i += 1

        while data[i] != ord("e"):
            value, i = self._decode(data, i)
            result.append(value)

        return result, i + 1

    def _decode_int(self, data: bytes, i: int) -> tuple[int, int]:
        i += 1

        if data[i] == ord("-") and data[i + 1] == ord("0"):
            raise DecodeError(f"Invalid '-0' value for int in {i} position")
        if data[i] == ord("0") and data[i + 1] != ord("e"):
            raise DecodeError(f"Invalid leading '0' value for int in {i} position")

        end = data.index(b"e", i)

        return int(data[i:end]), end + 1
