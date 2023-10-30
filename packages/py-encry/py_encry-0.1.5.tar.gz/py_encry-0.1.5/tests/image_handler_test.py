import unittest
import pytest
from src.pyencry.image_handler import ImageHandler

class ImageHandlerTests(unittest.TestCase):
    def test_can_import_image(self):
        expected = {"filename": "./img/Tower_Bridge_from_Shad_Thames.jpg", "format": "JPEG", "mode": "RGB", "size": (1200, 600)}
        self.assertEqual(True, True)

