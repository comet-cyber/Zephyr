"""Host regression checks for the firmware's NVRAM wire format."""

import unittest

from generate_nvram import encode_nvram


class NvramFormatTests(unittest.TestCase):
    """Check the chip's format contract independently of the C-array emitter."""

    def test_text_line_endings_produce_identical_entries(self):
        """Both Windows and Unix checkouts must produce two separate variables."""
        expected = b"a=1\0b=2\0\0\0\0\0"
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                source = newline.join(("# metadata", "a=1", "", "b=2", ""))
                self.assertEqual(encode_nvram(source), expected)

    def test_terminator_and_alignment_for_all_remainders(self):
        """The final variable remains terminated for every input length modulo four."""
        for value in ("", "1", "12", "123"):
            with self.subTest(value=value):
                image = encode_nvram(f"key={value}")
                self.assertEqual(image.rstrip(b"\0"), f"key={value}".encode("ascii"))
                self.assertTrue(image.endswith(b"\0\0"))
                self.assertEqual(len(image) % 4, 0)

    def test_malformed_input_is_rejected(self):
        """Invalid records must fail the build instead of reaching the Wi-Fi chip."""
        for source in ("", "# only comments", "missing_value", "=1", "a=1\na=2",
                       "a=1\0b=2", "a =1"):
            with self.subTest(source=repr(source)):
                with self.assertRaises(ValueError):
                    encode_nvram(source)


if __name__ == "__main__":
    unittest.main()
