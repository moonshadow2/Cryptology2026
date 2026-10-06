import subprocess
import sys
import unittest

import xor_vigenere as xv


PYTHON = sys.executable
SCRIPT = "xor_vigenere.py"


def run_cli(*args):
    """Run the CLI as a subprocess; return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [PYTHON, SCRIPT, *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout, result.stderr



class KnownAnswerTests(unittest.TestCase):

    def test_kat_1_attack_at_dawn(self):
        pt = bytes.fromhex("41747461636b206174206461776e21")
        key = bytes.fromhex("494345")
        self.assertEqual(
            xv.xor_repeating(pt, key).hex(),
            "08373128202e6922316927243e2d64",
        )

    def test_kat_2_hello(self):
        pt = bytes.fromhex("68656c6c6f")
        key = bytes.fromhex("6b6579")
        self.assertEqual(xv.xor_repeating(pt, key).hex(), "030015070a")

    def test_kat_3_binary_plaintext(self):
        pt = bytes.fromhex("00010203feff")
        key = bytes.fromhex("a55a")
        self.assertEqual(xv.xor_repeating(pt, key).hex(), "a55ba7595ba5")


class RoundTripTests(unittest.TestCase):

    def _assert_round_trip(self, key: bytes, message: bytes):
        ciphertext = xv.xor_repeating(message, key)
        self.assertEqual(xv.xor_repeating(ciphertext, key), message)

    def test_round_trip_ordinary_message(self):
        self._assert_round_trip(b"key", b"a fairly ordinary ASCII sentence.")

    def test_round_trip_empty_message(self): 
        self._assert_round_trip(b"anykey", b"")

    def test_round_trip_message_longer_than_key(self):  
        key = b"IC"  
        message = b"x" * 97  
        self._assert_round_trip(key, message)

    def test_round_trip_key_longer_than_message(self):
        key = b"a much longer key than the message that follows"
        message = b"hi"
        self._assert_round_trip(key, message)

    def test_round_trip_single_byte_key(self):
        self._assert_round_trip(b"\x00", b"anything at all")


class Utf8HandlingTests(unittest.TestCase):

    def test_multibyte_utf8_round_trip_high_level_api(self):
        key_hex = "abcd12"
        text = "héllo wörld — 日本語 🎉"  # multi-byte UTF-8 characters
        ciphertext_hex = xv.encrypt(key_hex, text)
        self.assertEqual(xv.decrypt(key_hex, ciphertext_hex), text)

    def test_multibyte_utf8_at_core_level(self):
        message = "日本語".encode("utf-8")
        key = b"\x01\x02\x03\x04"
        ciphertext = xv.xor_repeating(message, key)
        self.assertEqual(xv.xor_repeating(ciphertext, key), message)


class SpacePreservationTests(unittest.TestCase):
    """Requirement 3.1.6: no operation may silently change its input."""

    def test_spaces_preserved_no_newline_appended(self):
        key_hex = "42"
        text = "  leading and trailing spaces  "
        ciphertext_hex = xv.encrypt(key_hex, text)
        recovered = xv.decrypt(key_hex, ciphertext_hex)
        self.assertEqual(recovered, text)
        self.assertNotIn("\n", recovered)


class ArbitraryByteCoreTests(unittest.TestCase):

    def test_core_accepts_invalid_utf8_bytes(self):
        not_utf8 = bytes([0xff, 0xfe, 0x80, 0x81, 0x00, 0xc0, 0xc1])
        key = b"\x10\x20\x30"
        ciphertext = xv.xor_repeating(not_utf8, key)
        self.assertEqual(xv.xor_repeating(ciphertext, key), not_utf8)

    def test_core_round_trips_every_byte_value(self):
        message = bytes(range(256))
        key = bytes([7, 42, 200, 1])
        ciphertext = xv.xor_repeating(message, key)
        self.assertEqual(xv.xor_repeating(ciphertext, key), message)


class KeygenTests(unittest.TestCase):

    def test_keygen_length_and_hex_format(self):
        for length in (1, 2, 16, 32):
            key = xv.keygen(length)
            self.assertEqual(len(key), length)
            hex_str = xv.to_hex(key)
            self.assertEqual(len(hex_str), 2 * length)
            self.assertRegex(hex_str, r"^[0-9a-f]*$")

    def test_keygen_not_constant_across_calls(self):
        keys = {xv.keygen(16) for _ in range(5)}
        self.assertGreater(len(keys), 1)

    def test_keygen_rejects_zero_length(self):
        with self.assertRaises(xv.InputError):
            xv.keygen(0)

    def test_keygen_rejects_negative_length(self):
        with self.assertRaises(xv.InputError):
            xv.keygen(-3)

class ValidationRejectionTests(unittest.TestCase):

    def test_rejects_empty_key(self):
        with self.assertRaises(xv.InputError):
            xv.encrypt("", "hello")

    def test_rejects_odd_length_key(self):
        with self.assertRaises(xv.InputError):
            xv.encrypt("abc", "hello")

    def test_rejects_odd_length_ciphertext(self):
        with self.assertRaises(xv.InputError):
            xv.decrypt("ab", "abc")

    def test_rejects_non_hex_character_in_key(self):
        with self.assertRaises(xv.InputError):
            xv.encrypt("zz", "hello")

    def test_rejects_non_hex_character_in_ciphertext(self):
        with self.assertRaises(xv.InputError):
            xv.decrypt("ab", "zzzz")

    def test_rejects_leading_or_trailing_whitespace_in_key(self):
        with self.assertRaises(xv.InputError):
            xv.encrypt(" ab", "hello")
        with self.assertRaises(xv.InputError):
            xv.encrypt("ab ", "hello")

    def test_rejects_leading_or_trailing_whitespace_in_ciphertext(self):
        with self.assertRaises(xv.InputError):
            xv.decrypt("ab", " 1234")

    def test_rejects_zero_key_length(self):
        with self.assertRaises(xv.InputError):
            xv.keygen(0)

    def test_rejects_negative_key_length(self):
        with self.assertRaises(xv.InputError):
            xv.keygen(-1)

    def test_rejects_non_utf8_decryption_result(self):
        key = bytes([0x01])
        bad_ciphertext = xv.xor_repeating(bytes([0xff]), key).hex()
        with self.assertRaises(xv.InputError):
            xv.decrypt(key.hex(), bad_ciphertext)


class CliIntegrationTests(unittest.TestCase):

    def test_cli_keygen_prints_hex_and_newline(self):
        code, out, err = run_cli("keygen", "--length", "8")
        self.assertEqual(code, 0)
        self.assertEqual(err, "")
        self.assertTrue(out.endswith("\n"))
        stripped = out.strip()
        self.assertEqual(len(stripped), 16)
        int(stripped, 16)  

    def test_cli_encrypt_decrypt_round_trip(self):
        _, out, _ = run_cli("keygen", "--length", "4")
        key_hex = out.strip()

        code, out, err = run_cli(
            "encrypt", "--key", key_hex, "--text", "Attack at dawn!"
        )
        self.assertEqual(code, 0)
        ciphertext_hex = out.strip()

        code, out, err = run_cli(
            "decrypt", "--key", key_hex, "--ciphertext", ciphertext_hex
        )
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "Attack at dawn!")

    def test_cli_known_answer_via_encrypt_subcommand(self):
        code, out, err = run_cli(
            "encrypt", "--key", "494345", "--text", "Attack at dawn!"
        )
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "08373128202e6922316927243e2d64")

    def test_cli_encrypt_accepts_empty_text(self):  
        code, out, err = run_cli("encrypt", "--key", "ab", "--text", "")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "")

    def test_cli_decrypt_accepts_empty_ciphertext(self):
        code, out, err = run_cli("decrypt", "--key", "ab", "--ciphertext", "")
        self.assertEqual(code, 0)
        self.assertEqual(out.strip(), "")

    def test_cli_rejects_missing_length(self):
        code, out, err = run_cli("keygen")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)

    def test_cli_rejects_non_integer_length(self):
        code, out, err = run_cli("keygen", "--length", "abc")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)

    def test_cli_rejects_zero_length(self):
        code, out, err = run_cli("keygen", "--length", "0")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)

    def test_cli_rejects_empty_key(self):
        code, out, err = run_cli("encrypt", "--key", "", "--text", "hi")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)

    def test_cli_rejects_invalid_hex_key(self):
        code, out, err = run_cli("encrypt", "--key", "zz", "--text", "hi")
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)

    def test_cli_rejects_bad_utf8_after_decrypt(self):
        key = bytes([0x01]).hex()
        bad_ciphertext = "fe"  # 0xfe ^ 0x01 = 0xff, never valid UTF-8
        code, out, err = run_cli(
            "decrypt", "--key", key, "--ciphertext", bad_ciphertext
        )
        self.assertNotEqual(code, 0)
        self.assertEqual(out, "")
        self.assertNotIn("Traceback", err)


if __name__ == "__main__":
    unittest.main()