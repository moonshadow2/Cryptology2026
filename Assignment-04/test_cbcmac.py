import unittest

from cbcmac import mac, verify

KEY = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
MSG = bytes.fromhex(
    "6bc1bee22e409f96e93d7e117393172a ae2d8a571e03ac9c9eb76fac45af8e51 "
    "30c81c46a35ce411e5fbc1191a0a52ef f69f2445df4f9b17ad2b417be66c3710")
TAGS = {1: "3ad77bb40d7a3660a89ecaf32466ef97", 2: "b148c17f309ee692287ae57cf12add49",
        3: "c93d11bfaf08c5dc4d90b37b4dee002b", 4: "a7356e1207bb406639e5e5ceb9a9ed93"}


def flip(b: bytes) -> bytes:
    return bytes([b[0] ^ 1]) + b[1:]


class TestCBCMAC(unittest.TestCase):
    def test_known_answers(self):
        for l, t in TAGS.items():
            m, t = MSG[:16 * l], bytes.fromhex(t)
            self.assertEqual(mac(KEY, m), t)
            self.assertTrue(verify(KEY, m, t))

    def test_bad_lengths(self):
        for m in (b"", b"A" * 17):
            with self.assertRaises(ValueError):
                mac(KEY, m)
            self.assertFalse(verify(KEY, m, bytes(16)))

    def test_bad_tag_lengths(self):
        t = bytes.fromhex(TAGS[1])
        for n in (0, 15, 17):
            self.assertFalse(verify(KEY, MSG[:16], (t * 2)[:n]))

    def test_bit_flips(self):
        for l, t in TAGS.items():
            m, t = MSG[:16 * l], bytes.fromhex(t)
            self.assertFalse(verify(KEY, flip(m), t))
            self.assertFalse(verify(KEY, m, flip(t)))


if __name__ == "__main__":
    unittest.main()
