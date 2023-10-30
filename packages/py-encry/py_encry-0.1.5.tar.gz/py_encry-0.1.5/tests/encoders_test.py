import unittest
import pytest
from src.pyencry.utils import encode_data_to_pixel, decode_data_from_pixel

class PixelDataEncodeTests(unittest.TestCase):
    def test_can_encode_pixel(self):

        result = encode_data_to_pixel((38,120,255,0), 0b01011101)

        expected = (37, 121, 255, 1)

        self.assertEqual(result, expected)
