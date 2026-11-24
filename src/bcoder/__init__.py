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
    value, _ = _decode_value(data, 0)

    return value


def _decode_value(data: bytes, position: int) -> tuple[Value, int]:
    match data[position : position + 1]:
        case b"i":
            end = data.index(b"e", position)
            digits = data[position + 1 : end]

            if digits.startswith((b"-0", b"0")) and digits != b"0":
                raise DecodeError(f"invalid integer at position {position}")

            return int(digits), end + 1
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
        case _:
            return _decode_string(data, position)


def _decode_string(data: bytes, position: int) -> tuple[bytes, int]:
    colon = data.index(b":", position)
    digits = data[position:colon]

    if digits.startswith(b"0") and digits != b"0":
        raise DecodeError(f"invalid string at position {position}")

    end = colon + 1 + int(digits)

    return data[colon + 1 : end], end
