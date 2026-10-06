"""
    python3 -m unittest test_malleability_bonus.py -v
"""

import unittest

import xor_vigenere as xv


def flip_byte(ciphertext_byte: int, known_plaintext_byte: int,
              desired_plaintext_byte: int) -> int:
    """c_i' = c_i XOR m_i XOR m_hat_i, for a single byte position."""
    return ciphertext_byte ^ known_plaintext_byte ^ desired_plaintext_byte


class MalleabilityDemo(unittest.TestCase):

    def test_attacker_flips_a_field_without_the_key(self):
        key = xv.keygen(16)
        plaintext = b"status:DENY;amt=0050"
        ciphertext = xv.xor_repeating(plaintext, key)
        known_word = b"DENY"
        desired_word = b"OKAY"
        start = plaintext.index(known_word)
        self.assertEqual(len(known_word), len(desired_word))

        tampered = bytearray(ciphertext)
        for offset in range(len(known_word)):
            i = start + offset
            tampered[i] = flip_byte(
                tampered[i], known_word[offset], desired_word[offset]
            )
        tampered = bytes(tampered)
        self.assertNotEqual(tampered, ciphertext)  # the ciphertext did change
        recovered = xv.decrypt(key.hex(), tampered.hex())
        self.assertEqual(recovered, "status:OKAY;amt=0050")

    def test_flip_byte_matches_direct_reencryption(self):
        key = b"\x9a\x3c\x77\x01"
        plaintext = bytearray(b"abcdefgh")
        ciphertext = xv.xor_repeating(bytes(plaintext), key)

        index = 3
        desired = ord("Z")
        tampered_byte = flip_byte(ciphertext[index], plaintext[index], desired)

        plaintext[index] = desired
        expected_ciphertext = xv.xor_repeating(bytes(plaintext), key)

        self.assertEqual(tampered_byte, expected_ciphertext[index])


if __name__ == "__main__":
    unittest.main()