# bencoder

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
from bencoder import BDecoder

decoder = BDecoder()

with open("file.torrent", "rb") as file:
    data = file.read()

decoded = decoder.decode(data)
```

Example of `BEncoder` usage:
```python
from bencoder import BEncoder

encoder = BEncoder()

data = {
    b"announce-list": [
        ["udp:..."],
        ["udp:..."],
    ],
    "info": {
        "piece": b"xfsasf",
        "piece length": 123,
    },
}

encoded = encoder.encode(data)
```

__NOTE__: `BEncoder` can handle mixed types of Python strings - `bytes` and `str`.
