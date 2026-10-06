# Assignment 1: Repeating-Key XOR

- **Name:** Savar Shrestha
- **Language / version:** Python 3.10+ 
  `argparse`, `secrets`, `string`, `sys`, `unittest`, `subprocess`).

## Running from a clean environment

No third-party dependencies are required.

```bash
# Generate a key 
python3 xor_vigenere.py keygen --length 16

# Encrypt UTF-8 text with a hex key
python3 xor_vigenere.py encrypt --key <hex-key> --text "Attack!"

# Decrypt hex ciphertext with the same hex key
python3 xor_vigenere.py decrypt --key <hex-key> --ciphertext <hex-ciphertext>
```

```bash
$ python3 xor_vigenere.py encrypt --key 494345 --text "Attack!"
08373128202e6922316927243e2d64
```

## Running the tests

```bash
python3 -m unittest test_xor_vigenere.py -v          
python3 -m unittest test_malleability_bonus.py -v    # for the bonus question


```
All  tests in the required suite pass, plus 2 tests in the bonus
module. The CLI integration tests `xor_vigenere.py` as a subprocess
using `sys.executable`, so they run correctly regardless of which
`python3` is on `PATH`, as long as tests are run from this directory.

## Design notes

- The `xor_repeating(data: bytes, key: bytes) ->
  bytes`, contains no argument parsing, hex handling, or text encoding. It
  is the single implementation used for both encryption and decryption,
  since XOR is self-inverse.
- Hex parsing (`parse_hex`) is intentionally stricter than
  `bytes.fromhex`, which by default tolerates embedded whitespace between
  byte pairs. `parse_hex` explicitly rejects leading/trailing whitespace,
  odd length, and any non-`[0-9a-fA-F]` character before ever calling
  `bytes.fromhex`.
- All expected input errors are raised as a single
  `InputError` type, which prints a message to stderr and returns exit status `1`. Argparse's own
  usage error path that uses argparse's built-in exit status `2`; both are nonzero and neither
  produces a Python traceback.
- `keygen` uses `secrets.token_bytes`, which reads from the OS CSPRNG.
  

## Assumptions and known limitations

- "Positive integer" for `--length` is interpreted as a base-10 integer
  literal accepted by Python's `int()`.
- The CLI takes `--text` and `--ciphertext`/`--key` as literal
  command line arguments.
- This cipher must never be used to protect real
  credentials, personal data, files, or network traffic.

## Disclosure of assistance

This analysis, and  README was gramatically corrected and structured with the help
of Claude. No other generative-AI tool was used.
