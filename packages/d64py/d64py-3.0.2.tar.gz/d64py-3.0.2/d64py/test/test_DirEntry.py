#======================================================================
# test_DirEntry.py
#======================================================================
import logging
from pathlib import Path
import unittest
from d64py.base.DiskImage import DiskImage
from d64py.utility import D64Utility

class TestDirEntry(unittest.TestCase):
    # def testPetsciiToAscii(self):
    #     # "BROWSERDOCS.ASCI" in PETSCII
    #     testName = bytearray.fromhex("42 52 4f 57 53 45 52 44 4f 43 53 2e 43 42 4d")
    #     index = 0
    #     while index < len(testName):
    #         inChar = testName[index]
    #         outChar = D64Utility.petsciiToAsciiChar(inChar)
    #         logging.debug(f"in: {hex(testName[index])}, out: {hex(D64Utility.petsciiToAsciiChar(inChar))}")
    #         testName[index] = outChar
    #         index += 1
    #     print(f"converted name: {str(testName)}")

    def testGetAsciiFileName(self):
        imagePath = Path("images/BOGEOS2.D64")
        diskImage = DiskImage(imagePath)
        dirEntries = diskImage.getDirectory()
        diskImage.close()
        dirEntry = dirEntries[1]
        asciiFileName = dirEntry.getAsciiFileName()
        print(f"ascii filename: \"{asciiFileName}\"")
        self.assertEqual(asciiFileName, "geoBrowserDocs  ")

    def testDirListing(self):
        try:
            image = DiskImage(Path("images/BOGEOS2.D64"))
            dirEntries = image.getDirectory()
            image.close()
            for dirEntry in dirEntries:
                print(dirEntry)
            print("")

            image = DiskImage(Path("images/BOGEOS2.D64"))
            dirEntries = image.getDirectory()
            image.close()
            for dirEntry in dirEntries:
                print(dirEntry)

            self.assertEqual(dirEntries[0], dirEntries[0])
            self.assertNotEqual(dirEntries[0], dirEntries[1])
        except Exception as exc:
            logging.exception(exc)
            image.close()

if __name__ == '__main__':
    unittest.main()
