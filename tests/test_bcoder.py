import pytest

from bcoder import DecodeError, decode, encode

ENCODED_VALUES = [
    (0, b"i0e"),
    (42, b"i42e"),
    (-42, b"i-42e"),
    (b"", b"0:"),
    (b"spam", b"4:spam"),
    ([], b"le"),
    ([b"spam", 42], b"l4:spami42ee"),
    ({}, b"de"),
    ({b"spam": [b"eggs", {b"ham": -1}]}, b"d4:spaml4:eggsd3:hami-1eeee"),
]

MALFORMED = [
    b"i-0e",
    b"i01e",
    b"01:a",
]


@pytest.mark.parametrize(("value", "encoded"), ENCODED_VALUES)
def test_encode(value, encoded):
    assert encode(value) == encoded


@pytest.mark.parametrize(("value", "encoded"), ENCODED_VALUES)
def test_decode(value, encoded):
    assert decode(encoded) == value


def test_encode_sorts_dict_keys():
    assert encode({b"b": 1, b"a": 2}) == b"d1:ai2e1:bi1ee"


def test_decode_accepts_unsorted_dict_keys():
    assert decode(b"d1:bi1e1:ai2ee") == {b"a": 2, b"b": 1}


def test_decode_keeps_last_duplicate_dict_key():
    assert decode(b"d1:ai1e1:ai2ee") == {b"a": 2}


@pytest.mark.parametrize("data", MALFORMED)
def test_decode_rejects_malformed_data(data):
    with pytest.raises(DecodeError):
        decode(data)
