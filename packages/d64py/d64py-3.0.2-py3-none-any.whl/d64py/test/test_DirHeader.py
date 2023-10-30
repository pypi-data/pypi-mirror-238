#======================================================================
# test_DirHeader.py
#======================================================================
import unittest
from pathlib import Path
from d64py.base.DiskImage import DiskImage

class TestDirHeader(unittest.TestCase):
    def testDirHeader(self):
        imagePath = Path("images/geopublish-b.d64")
        diskImage = DiskImage(imagePath)
        dirHeader = diskImage.getDirHeader()
        diskName = dirHeader.getDiskName()
        print(diskName)
        self.assertEqual(diskName, "geoPublish B    ")
        diskImage.close()
        