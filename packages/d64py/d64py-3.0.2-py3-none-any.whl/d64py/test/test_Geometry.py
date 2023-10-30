#======================================================================
# test_Geometry.py
#======================================================================
import logging
import unittest
from d64py.base.TrackSector import TrackSector
from d64py.base.Constants import ImageType
from d64py.base import Geometry
from d64py.base.Constants import ImageType

class TestGeometry(unittest.TestCase):
    def testImageTypeLength(self):
        self.assertEqual(Geometry.imageLength(ImageType.D64), 174848)
        self.assertEqual(Geometry.getErrorOffset(ImageType.D64_ERROR), 174848)
        self.assertEqual(Geometry.getSectorSize(ImageType.D81), 256)
        self.assertEqual(Geometry.getZone(ImageType.D64, 1), 0)
        self.assertEqual(Geometry.getZone(ImageType.D64, 18), 1)
        self.assertEqual(Geometry.isValidTrackSector(TrackSector(39, 0), ImageType.D64), False)
        self.assertEqual(Geometry.isValidTrackSector(TrackSector(39, 0), ImageType.D81), True)
        self.assertEqual(Geometry.getMaxTrack(ImageType.D64), 35)
        self.assertEqual(Geometry.getMaxTrack(ImageType.D81), 80)
        self.assertEqual(Geometry.getMaxSector(ImageType.D64, 1), 20)
        self.assertEqual(Geometry.getMaxSector(ImageType.D64, 18), 18)
        self.assertEqual(Geometry.getMaxSector(ImageType.D64, 25), 17)
        self.assertEqual(Geometry.getMaxSector(ImageType.D64, 31), 16)
        self.assertEqual(Geometry.getZone(ImageType.D64, 1), 0)
        self.assertEqual(Geometry.getZone(ImageType.D64, 18), 1)
        self.assertEqual(Geometry.getZone(ImageType.D64, 25), 2)
        self.assertEqual(Geometry.getZone(ImageType.D64, 31), 3)
        self.assertEqual(Geometry.getDirectoryTrack(ImageType.D64), 18)
        self.assertEqual(Geometry.getDirectoryTrack(ImageType.D81), 40)
        self.assertEqual(Geometry.getDirHeaderTrackSector(ImageType.D64), TrackSector(18, 0))
        self.assertEqual(Geometry.getDirHeaderTrackSector(ImageType.D81), TrackSector(40, 0))

    def testOffsetConversion(self):
        #zone 1
        logging.debug("D64, zone 1");
        self.showOffsetConversion(1, 0, ImageType.D64)
        self.showOffsetConversion(1, 20, ImageType.D64)
        self.showOffsetConversion(2, 0, ImageType.D64)
        self.showOffsetConversion(2, 20, ImageType.D64)

        #zone 2
        logging.debug("D64, zone 2")
        self.showOffsetConversion(18, 0, ImageType.D64)
        self.showOffsetConversion(18, 18, ImageType.D64)
        self.showOffsetConversion(24, 0, ImageType.D64)
        self.showOffsetConversion(24, 18, ImageType.D64)

        #zone 3
        logging.debug("D64, zone 3")
        self.showOffsetConversion(25, 0, ImageType.D64)
        self.showOffsetConversion(25, 17, ImageType.D64)
        self.showOffsetConversion(30, 0, ImageType.D64)
        self.showOffsetConversion(30, 17, ImageType.D64)

        #zone 4
        logging.debug("D64, zone 4")
        self.showOffsetConversion(31, 0, ImageType.D64)
        self.showOffsetConversion(31, 16, ImageType.D64)
        self.showOffsetConversion(35, 0, ImageType.D64)
        self.showOffsetConversion(35, 16, ImageType.D64)

    def showOffsetConversion(self, track: int, sector: int, imageType: ImageType):
        ts = TrackSector(track, sector)
        if not Geometry.isValidTrackSector(ts, imageType):
            raise Exception(f"Not a valid track/sector: {ts}")
        offset = Geometry.getSectorOffset(ts, imageType)
        self.assertEqual(TrackSector(track, sector), Geometry.getOffsetSector(offset, imageType))
        logging.debug(f"{ts} offset is {offset}, converts back to {Geometry.getOffsetSector(offset, imageType)}")

if __name__ == '__main__':
    unittest.main()
