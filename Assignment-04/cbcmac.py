"""Basic CBC-MAC with AES-128. AES is used only to encrypt one 16-byte block
at a time; the chaining loop is written here (no CBC mode / CMAC)."""
import hmac

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK = 16


def _xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def _valid_len(msg: bytes) -> bool:
    return len(msg) > 0 and len(msg) % BLOCK == 0


def _compute(key: bytes, msg: bytes) -> bytes:
    # One cipher object per call, reused for every block (ECB, no padding,
    # so each update() of 16 bytes is exactly one F_k evaluation).
    enc = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    x = bytes(BLOCK)                                   # x_0 = 0^128
    for i in range(0, len(msg), BLOCK):
        x = enc.update(_xor(x, msg[i:i + BLOCK]))      # x_i = F_k(x_{i-1} xor m_i)
    return x                                           # t = x_l


def mac(key: bytes, msg: bytes) -> bytes:
    if not _valid_len(msg):
        raise ValueError("message must be a non-empty multiple of 16 bytes")
    return _compute(key, msg)


def verify(key: bytes, msg: bytes, tag: bytes) -> bool:
    if not _valid_len(msg) or len(tag) != BLOCK:
        return False
    return hmac.compare_digest(_compute(key, msg), tag)
