# pyleb128
Powerful little-endian base-128 encoding/decoding library for Python 3.
</br>
</br>
Supports the following types:
* Unsigned LEB128
* Signed LEB128
* Unsigned LEB128 +1 ([ULEB128P1](https://source.android.com/docs/core/runtime/dex-format#leb128))

# Example Usage
```python
from pyleb128 import (
    uleb128,
    uleb128p1, 
    sleb128
)

# decode
print(uleb128.decode(b'\x80\x80\x80\x00'))

```