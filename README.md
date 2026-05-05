# bcoder

### About

---

A Python package to handle bencoded values, a serialization format commonly used in `.torrent` files within
the <u>BitTorrent</u> protocol.

### Usage

---

There are __2__ types of classes:
- `BDecoder` - handle decoding of bencoded data to common Python types
- `BEncoder` - handle encoding of common Python types to `bytes` type

Example of `BDecoder` usage:
```python
from bcoder import BDecoder

decoder = BDecoder()

with open("file.torrent", "rb") as file:
    data = file.read()

decoded = decoder.decode(data)
```

Example of `BEncoder` usage:
```python
from bcoder import BEncoder

encoder = BEncoder()

data = {
    b"announce-list": [
        [b"udp:..."],
        [b"udp:..."],
    ],
    b"info": {
        b"piece": b"xfsasf",
        b"piece length": 123,
    },
}

encoded = encoder.encode(data)
```

__NOTE__: `BEncoder` is spec-strict (BEP 3). Only `bytes`, `int`, `list`, and `dict` with `bytes` keys are accepted. Pass `str` through `.encode("utf-8")` yourself if you need to encode text.
