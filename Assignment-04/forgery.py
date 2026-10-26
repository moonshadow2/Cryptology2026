"""Oracle, the Problem 2(b) forgery, the demo, and the fixed-length check."""
import os

from cbcmac import BLOCK, mac, verify, _xor

TARGET = b"from=alice&to=mallory&amount=1000000&note=rent!!"


class Oracle:
    """MAC oracle with a hidden random key; records every queried message.
    If fixed_blocks is set, it accepts only messages of that many blocks."""

    def __init__(self, fixed_blocks=None):
        self._key = os.urandom(16)
        self.fixed_blocks = fixed_blocks
        self.queried = []

    def _ok_len(self, msg):
        return self.fixed_blocks is None or len(msg) == BLOCK * self.fixed_blocks

    def query(self, msg: bytes) -> bytes:
        if not self._ok_len(msg):
            raise ValueError(f"oracle accepts only {self.fixed_blocks}-block "
                             f"messages; got {len(msg)} bytes")
        self.queried.append(msg)
        return mac(self._key, msg)

    def verify(self, msg: bytes, tag: bytes) -> bool:
        return self._ok_len(msg) and verify(self._key, msg, tag)


def forge(query, target: bytes) -> bytes:
    """Two queries; returns a valid tag for target (needs >= 2 blocks)."""
    if len(target) % BLOCK or len(target) < 2 * BLOCK:
        raise ValueError("target needs at least 2 whole blocks")
    blocks = [target[i:i + BLOCK] for i in range(0, len(target), BLOCK)]
    t = query(blocks[0])                                   # query 1: M_1
    m_prime = _xor(blocks[1], t) + b"".join(blocks[2:])    # query 2: (M_2 xor t)||M_3..M_L
    return query(m_prime)                                  # t' is the tag on M


def demo():
    o = Oracle()
    sent = []

    def spy(msg):
        tag = o.query(msg)
        sent.append((msg, tag))
        return tag

    forged = forge(spy, TARGET)
    for n, (m, t) in enumerate(sent, 1):
        print(f"query {n}: msg={m.hex()}\n         tag={t.hex()}")
    print("forged tag:        ", forged.hex())
    print("oracle saw target: ", TARGET in o.queried)
    print("verify(target,tag):", o.verify(TARGET, forged))


def run_trials(n=100):
    ok = 0
    for _ in range(n):
        o = Oracle()
        tag = forge(o.query, TARGET)
        ok += (TARGET not in o.queried) and o.verify(TARGET, tag)
    return ok


def fixed_length_check():
    o = Oracle(fixed_blocks=3)
    try:
        forge(o.query, TARGET)
        print("attack unexpectedly succeeded")
    except ValueError as e:
        print("attack failed at query 1:", e)
    print("queries accepted by oracle:", len(o.queried))
    # Even a hand-built 2-block second query is rejected:
    print("2-block query would be rejected:", not o._ok_len(bytes(32)))


if __name__ == "__main__":
    assert len(TARGET) == 48
    print("=== 3(b) demo ===")
    demo()
    print(f"\nsuccessful forgeries in 100 runs: {run_trials(100)}/100")
    print("\n=== 3(c) fixed 3-block oracle ===")
    fixed_length_check()
