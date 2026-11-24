# bcoder

Encode and decode [bencode](https://www.bittorrent.org/beps/bep_0003.html#bencoding), the format of `.torrent` files.

```
pip install bcoder
```

```python
import bcoder

bcoder.encode({b"spam": [b"eggs", 42]})  # b"d4:spaml4:eggsi42eee"
bcoder.decode(b"d4:spaml4:eggsi42eee")  # {b"spam": [b"eggs", 42]}
```

Values are `int`, `bytes`, `list` and `dict` with `bytes` keys. `encode` raises `TypeError` for anything else. `decode` raises `bcoder.DecodeError` for malformed data.
