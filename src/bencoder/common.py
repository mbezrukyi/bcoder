from enum import Enum


class CodeType(Enum):
    DICTIONARY = b"d"
    STRING = b"1234567890"
    LIST = b"l"
    INTEGER = b"i"

    @classmethod
    def from_code(cls, code: int) -> "CodeType":
        return next(filter(lambda m: code in m.value, cls))
