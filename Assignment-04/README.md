# Assignment 4: Forging Basic CBC-MAC

Name: Savar Shrestha

- Language: Python 3.12.3
- AES library: `cryptography` 46.0.6 (AES-128 in ECB mode, used only to encrypt one 16-byte block per call; the chaining loop is in `cbcmac.py`)

## Files
- `cbcmac.py` – `mac`, `verify`
- `forgery.py` – oracle, `forge`, demo, 100-run trial, fixed-length check
- `test_cbcmac.py` – known-answer, length, tag-length and bit-flip tests

## Commands
```text
pip install cryptography
python3 -m unittest -v      # tests
python3 forgery.py          # 3(b) demo, 100 trials, 3(c) check
```
