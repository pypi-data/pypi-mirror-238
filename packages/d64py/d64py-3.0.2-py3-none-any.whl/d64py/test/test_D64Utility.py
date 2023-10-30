#======================================================================
# test_D64Utility.py
#======================================================================
import unittest
from pathlib import Path
from d64py.utility import D64Utility
from d64py.base.Constants import ImageType

class TestD64Utility(unittest.TestCase):
    def test_FindImageType(self):
        imagePath = Path("images/geopublish-b.d64")
        self.assertEqual(D64Utility.findImageType(imagePath), ImageType.D64)

    def test_getMegaRecordNo(self):
        char = "x"
        print(f"char '{char}' is {ord(char)}")
        recordNo = D64Utility.getMegaRecordNo(char)
        print(f"'{char}' is found in mega record {recordNo}")
        self.assertEqual(recordNo,53)

        char = "Q"
        print(f"char '{char}' is {ord(char)}")
        recordNo = D64Utility.getMegaRecordNo(char)
        print(f"'{char}' is found in mega record {recordNo}")
        self.assertEqual(recordNo, 51)

    def test_asciiToPetsciiString(self):
        testString = "Cenbe loves Wizard"
        hex = ":".join("{:02x}".format(ord(c)) for c in testString)
        print(f"\"{testString}\": {hex}")

        translatedString = D64Utility.asciiToPetsciiString(testString)
        hex = ":".join("{:02x}".format(ord(c)) for c in translatedString)
        print("after translating to PETSCII:")
        print(f"\"{testString}\": {hex}")
        self.assertEqual(hex, "c3:45:4e:42:45:20:4c:4f:56:45:53:20:d7:49:5a:41:52:44")

if __name__ == '__main__':
    unittest.main()
