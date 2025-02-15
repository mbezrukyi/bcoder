from typing import Any, Callable, Dict, List

from .common import CodeType
from .errors import DecoderError


class BDecoder:
    def __init__(self, data: bytes):
        self._data = data
        self._i = 0

        self._decoders = {
            CodeType.DICTIONARY: self._decode_dict,
            CodeType.STRING: self._decode_str,
            CodeType.LIST: self._decode_list,
            CodeType.INTEGER: self._decode_int,
        }

    def decode(self) -> Any:
        return self._get_decoder()()

    def _decode_dict(self) -> Dict[bytes, Any]:
        result = {}

        self._i += 1

        while self._data[self._i] != ord("e"):
            key = self._decode_str()
            result[key] = self._get_decoder()()

        self._i += 1

        return result

    def _decode_str(self) -> bytes:
        if self._data[self._i] == ord("0") and self._data[self._i + 1] != ord(":"):
            raise DecoderError(f"Invalid leading '0' value for str in {self._i} position")

        colon = self._data.index(b":", self._i)
        length = int(self._data[self._i: colon])

        start = colon + 1
        end = start + length

        self._i = end

        return self._data[start:end]

    def _decode_list(self) -> List[Any]:
        result = []

        self._i += 1

        while self._data[self._i] != ord("e"):
            result.append(self._get_decoder()())

        self._i += 1

        return result

    def _decode_int(self) -> int:
        self._i += 1

        if self._data[self._i] == ord("-") and self._data[self._i + 1] == ord("0"):
            raise DecoderError(f"Invalid '-0' value for int in {self._i} position")
        if self._data[self._i] == ord("0") and self._data[self._i + 1] != ord("e"):
            raise DecoderError(f"Invalid leading '0' value for int in {self._i} position")

        start = self._i
        end = self._data.index(b"e", self._i)

        self._i = end + 1

        return int(self._data[start:end])

    def _get_decoder(self) -> Callable[["BDecoder"], Any]:
        return self._decoders[CodeType.from_code(self._data[self._i])]
