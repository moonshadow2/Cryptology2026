#!/usr/bin/env python3

from __future__ import annotations

import argparse
import secrets
import string
import sys


class InputError(Exception):
    """Raised for any expected, user-facing input-validation failure.

    The CLI catches this and turns it into a concise stderr message plus a
    nonzero exit status, rather than letting a language stack trace escape.
    """

def xor_repeating(data: bytes, key: bytes) -> bytes:
    """Repeating-key XOR core.

        c_i = m_i XOR k_{i mod len(key)},  for 0 <= i < len(data)

    `data` may be any byte string, including bytes that are not valid
    UTF-8, and may be empty. `key` must be non-empty.

    XOR is self-inverse (x ^ k ^ k == x), so this single function
    implements both encryption and decryption: it is its own inverse for a
    fixed key.
    """
    if len(key) == 0:
        raise InputError("key must not be empty")
    key_len = len(key)
    return bytes(byte ^ key[i % key_len] for i, byte in enumerate(data))


_HEX_DIGITS = set(string.hexdigits)  # '0123456789abcdefABCDEF'


def parse_hex(s: str, field_name: str, allow_empty: bool = False) -> bytes:
    """Strictly parse a hex string into bytes.

    Rejects (raising InputError):
      * leading or trailing whitespace,
      * odd length,
      * any character outside 0-9, a-f, A-F,
      * an empty string, unless allow_empty is True.
    """
    if s != s.strip():
        raise InputError(
            f"{field_name} must not have leading or trailing whitespace"
        )
    if len(s) == 0:
        if allow_empty:
            return b""
        raise InputError(f"{field_name} must not be empty")
    if len(s) % 2 != 0:
        raise InputError(
            f"{field_name} must have even length "
            f"(got {len(s)} hex characters)"
        )
    bad_chars = sorted({c for c in s if c not in _HEX_DIGITS})
    if bad_chars:
        raise InputError(
            f"{field_name} contains non-hexadecimal character(s): {bad_chars!r}"
        )
    return bytes.fromhex(s)


def to_hex(data: bytes) -> str:
    """Canonical lowercase hex encoding used for all program output."""
    return data.hex()


def keygen(length: int) -> bytes:
    """Gen(length): draw exactly `length` bytes from the OS CSPRNG."""
    if not isinstance(length, int) or isinstance(length, bool):
        raise InputError("key length must be an integer")
    if length <= 0:
        raise InputError("key length must be a positive integer")
    return secrets.token_bytes(length)


def encrypt(key_hex: str, text: str) -> str:
    """Enc_k(m): UTF-8 encode `text`, XOR against the parsed key, return hex.

    No transformation other than UTF-8 encoding is applied to `text`:
    spaces are preserved and no newline is appended.
    """
    key = parse_hex(key_hex, "key")
    plaintext = text.encode("utf-8")
    ciphertext = xor_repeating(plaintext, key)
    return to_hex(ciphertext)


def decrypt(key_hex: str, ciphertext_hex: str) -> str:
    """Dec_k(c): parse hex, XOR against the parsed key, strictly decode UTF-8."""
    key = parse_hex(key_hex, "key")
    ciphertext = parse_hex(ciphertext_hex, "ciphertext", allow_empty=True)
    plaintext_bytes = xor_repeating(ciphertext, key)
    try:
        return plaintext_bytes.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise InputError(f"decrypted bytes are not valid UTF-8 ({exc})") from exc


# CLI

def _length_type(value: str) -> int:
    """argparse type= callback for --length.

    Non-integer values are reported by argparse's own error handling. Zero and
    negative values pass this stage and are rejected later by keygen()itself, which raises InputError.
    """
    try:
        return int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"length must be an integer, got {value!r}"
        ) from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="xor_vigenere",
        description="Repeating-key XOR cipher (educational; not secure).",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_keygen = sub.add_parser("keygen", help="generate a random hex key")
    p_keygen.add_argument(
        "--length", type=_length_type, required=True,
        help="key length in bytes (positive integer)",
    )

    p_encrypt = sub.add_parser("encrypt", help="encrypt UTF-8 text")
    p_encrypt.add_argument("--key", required=True, help="key as hex")
    p_encrypt.add_argument("--text", required=True, help="plaintext as UTF-8 text")

    p_decrypt = sub.add_parser("decrypt", help="decrypt hex ciphertext")
    p_decrypt.add_argument("--key", required=True, help="key as hex")
    p_decrypt.add_argument("--ciphertext", required=True, help="ciphertext as hex")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "keygen":
            print(to_hex(keygen(args.length)))
        elif args.command == "encrypt":
            print(encrypt(args.key, args.text))
        elif args.command == "decrypt":
            print(decrypt(args.key, args.ciphertext))
    except InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())