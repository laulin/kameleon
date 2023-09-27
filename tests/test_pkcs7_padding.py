import unittest
import kameleon.crypto.pkcs7_padding as pkcs

class TestPKCS7(unittest.TestCase):
    def test_pad_1(self):
        data=b"aaaaaaaaaa"

        result = pkcs.pad(data, 16)
        expected = b"aaaaaaaaaa\x06\x06\x06\x06\x06\x06"

        self.assertEqual(result, expected)

    def test_pad_2(self):
        data=b"aaaaaaaaaaaaaaaa"

        result = pkcs.pad(data, 16)
        expected = b"aaaaaaaaaaaaaaaa"

        self.assertEqual(result, expected)

    def test_unpad_1(self):
        data=b"aaaaaaaaaa\x06\x06\x06\x06\x06\x06"

        result = pkcs.unpad(data, 16)
        expected = b"aaaaaaaaaa"

        self.assertEqual(result, expected)

    def test_unpad_2(self):
        data=b"aaaaaaaaaaaaaaaa"

        result = pkcs.unpad(data, 16)
        expected = b"aaaaaaaaaaaaaaaa"

        self.assertEqual(result, expected)

    def test_unpad_invalid_block_size(self):
        data=b"aaaaaaaaaa\x06\x06\x06\x06\x06"

        with self.assertRaises(Exception) as exc:
            pkcs.unpad(data, 16)

        self.assertEqual(str(exc.exception), "Block size is incorrect")

    def test_unpad_invalid_padding(self):
        data=b"aaaaaaaaaa\x06\x06\x06\x06\x01\x06"

        with self.assertRaises(Exception) as exc:
            pkcs.unpad(data, 16)

        self.assertEqual(str(exc.exception), "Invalid padding")
