#======================================================================
# test_ImageType.py
#======================================================================
import unittest
from d64py.base.Constants import ImageType

class TestImamgeType(unittest.TestCase):
    def testImageTypeValues(self):
        self.assertEqual(ImageType.D64.description, "D64 image")
        self.assertEqual(ImageType.D64.extensions, (".d64", ".d41"))
        self.assertEqual(ImageType.D81.description, "D81 image")
        self.assertEqual(ImageType.D81.extensions, (".d81",))
        self.assertEqual(ImageType.D81.description, "D81 image")
        self.assertEqual(ImageType.D81.extensions, (".d81",))

if __name__ == '__main__':
    unittest.main()
