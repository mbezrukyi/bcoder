import re

_INTEGER = re.compile(rb"i(0|-?[1-9][0-9]*)e")
_STRING_LENGTH = re.compile(rb"(0|[1-9][0-9]*):")

type Value = int | bytes | list[Value] | dict[bytes, Value]


class DecodeError(ValueError):
    pass


def encode(value: Value) -> bytes:
    match value:
        case bytes():
            return b"%d:%b" % (len(value), value)
        case list():
            return b"l" + b"".join(map(encode, value)) + b"e"
        case dict():
            pairs = (encode(key) + encode(item) for key, item in sorted(value.items()))

            return b"d" + b"".join(pairs) + b"e"
        case int():
            return b"i%de" % value


def decode(data: bytes) -> Value:
    value, end = _decode_value(data, 0)

    if end != len(data):
        raise DecodeError(f"trailing data at position {end}")

    return value


def _decode_value(data: bytes, position: int) -> tuple[Value, int]:
    match data[position : position + 1]:
        case b"i":
            integer = _INTEGER.match(data, position)

            if not integer:
                raise DecodeError(f"invalid integer at position {position}")

            return int(integer[1]), integer.end()
        case b"l":
            items = []
            position += 1

            while data[position : position + 1] != b"e":
                item, position = _decode_value(data, position)
                items.append(item)

            return items, position + 1
        case b"d":
            entries = {}
            position += 1

            while data[position : position + 1] != b"e":
                key, position = _decode_string(data, position)
                entries[key], position = _decode_value(data, position)

            return entries, position + 1
        case digit if digit.isdigit():
            return _decode_string(data, position)
        case _:
            raise DecodeError(f"invalid value at position {position}")


def _decode_string(data: bytes, position: int) -> tuple[bytes, int]:
    length = _STRING_LENGTH.match(data, position)

    if not length:
        raise DecodeError(f"invalid string at position {position}")

    end = length.end() + int(length[1])

    if end > len(data):
        raise DecodeError(f"truncated string at position {position}")

    return data[length.end() : end], end
