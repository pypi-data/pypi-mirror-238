#======================================================================
# test_DiskImage.py
#======================================================================
import logging
import os
from pathlib import Path
import sys
import unittest
from d64py.base.Chain import Chain
from d64py.base.Constants import CharSet, ImageType, SectorErrors
from d64py.base.DiskImage import DiskImage
from d64py.base import Geometry
from d64py.base.TrackSector import TrackSector

class TestDiskImage(unittest.TestCase):
    # def test_DirAndHeaders(self):
    #     print("testDirAndHeaders()")
    #     imagePath = Path("images/BOGEOS2.D64")
    #     diskImage = DiskImage(imagePath)
    #     dirEntries = diskImage.getDirectory()
    #     self.assertIsNotNone(dirEntries)
    #     dirEntry = dirEntries[0]
    #     self.assertIsNotNone(dirEntry)
    #     dirHeader = diskImage.getDirHeader()
    #     raw = dirHeader.getRaw()
    #     self.assertIsNotNone(dirHeader)
    #     geosFileHeader = dirEntry.getGeosFileHeader()
    #     self.assertIsNotNone(geosFileHeader)
    #     diskImage.close()

    # def test_ErrorMessages(self):
    #     print("test_ErrorMessage()")
    #     for sectorError in SectorErrors:
    #         print(f"{sectorError.code} / {sectorError.description}")

    # def test_VlirChains(self):
    #     print("test_VlirChains()")
    #     try:
    #         diskImage = DiskImage(Path("images/BOGEOS2.D64"))
    #         dirEntry = diskImage.findDirEntry("geoBrowserDocs", CharSet.ASCII)
    #         chains = diskImage.getVlirChains(dirEntry)
    #         diskImage.close()
    #         self.assertEqual(len(chains), 3)
    #         print(f"there are {len(chains)} records")
    #         self.assertEqual(len(chains[0].sectors), 13)
    #         self.assertEqual(len(chains[1].sectors), 14)
    #         self.assertEqual(len(chains[2].sectors), 11)
    #         for record in chains.keys():
    #             print(f"record {record} has {len(chains[record].sectors)} sectors")
    #     except Exception as exc:
    #         print(exc)
    #         logging.error(exc)
    #         diskImage.close()
    #     print("\ntest_VlirChains() complete")

    # def test_Chain(self):
    #     print("testChain()")
    #     sectors = [TrackSector(18,1), \
    #                TrackSector(18, 4), \
    #                TrackSector(18, 7), \
    #                TrackSector(18, 10)]
    #     chain = Chain(sectors)
    #     self.assertIsInstance(chain, Chain)
    #     self.assertEqual(chain.size(), 4)
    #
    #     imagePath = Path("images/geopublish-b.d64")
    #     diskImage = DiskImage(imagePath)
    #     dirChain = diskImage.followChain(Geometry.getFirstDirTrackSector(diskImage.imageType))
    #     diskImage.close()
    #     self.assertIsInstance(dirChain, Chain)
    #     self.assertEqual(len(dirChain.sectors), 3)

    # def test_ErrorMap(self):
    #     print("test_ErrorMap()")
    #     errorMap = {}
    #     try:
    #         diskImage = DiskImage(Path("images/COMAL0.14.D64"))
    #         errorMap = diskImage.getSectorErrorMap()
    #         diskImage.close()
    #     except Exception as exc:
    #         print(exc)
    #         logging.error(exc)
    #         diskImage.close()
    #     print(f"error map size: {len(errorMap)}")
    #     self.assertEqual(len(errorMap), 683)

    # def test_GeoWriteFileAsLines(self):
    #     print("test_GeoWriteFileAsLines()")
    #     p = Path("images/BOGEOS2.D64")
    #     image = DiskImage(p)
    #     try:
    #         dirEntry = image.findDirEntry("geoBrowserDocs", CharSet.ASCII)
    #         pages = image.getGeoWriteFileAsLines(dirEntry)
    #         for page in pages:
    #             print("*** NEW PAGE ***")
    #             for line in page:
    #                 print(line.text)
    #     except Exception as exc:
    #         logging.exception(exc)
    #     image.close()

    # def test_FileAsText(self):
    #     print("test_FileAsText()")
    #     p = Path("/mnt/common/download/c64/os/geos/BOGEOS2.D64")
    #     image = DiskImage(p)
    #     try:
    #         dirEntry = image.findDirEntry("BROWSERDOCS.CBM", CharSet.ASCII)
    #         print(dirEntry)
    #     except Exception as exc:
    #         print(exc)
    #         logging.error(exc)
    #         image.close()
    #         return
    #     lines = image.getFileAsText(dirEntry, CharSet.PETSCII, False)
    #     image.close()
    #     for line in lines:
    #         print(line.text)
    #     image.close()

    # def test_FileAsAscii(self):
    #     print("test_FileAsAscii()")
    #     p = Path("images/BOGEOS2.D64")
    #     image = DiskImage(p)
    #     try:
    #         dirEntry = image.findDirEntry("BROWSERDOCS.ASCI", CharSet.ASCII)
    #         print(dirEntry)
    #     except Exception as exc:
    #         print(exc)
    #         logging.error(exc)
    #         image.close()
    #         return
    #
    #     lines = image.getFileAsText(dirEntry, CharSet.ASCII)
    #     image.close()
    #     for line in lines:
    #         print(line.text)
    #     image.close()

    def test_fileAsPetscii(self):
        print("test_fileAsPetscii()")
        p = Path("images/BOGEOS2.D64")
        image = DiskImage(p)
        try:
            dirEntry = image.findDirEntry("browserdocs.cbm", CharSet.PETSCII)
            print(dirEntry)
        except Exception as exc:
            print(exc)
            logging.error(exc)
            image.close()
            return
        # request translation
        lines = image.getFileAsText(dirEntry, CharSet.PETSCII, False, True)
        image.close()
        self.assertEqual(lines[0].text.strip(), "geoBrowser v1.6")
        for line in lines:
            print(line.text)

    def test_MegaFont(self):
        print("test_MegaFont()")
        p = Path("images/geopublish-b.d64")
        image = DiskImage(p)
        filename = "Mega Cal"
        try:
            dirEntry = image.findDirEntry(filename, CharSet.ASCII)
            print(dirEntry)
            geosFileHeader = dirEntry.getGeosFileHeader()
            isMega = image.isMegaFont(dirEntry, geosFileHeader)
            print(f"{filename} is mega font? {isMega}")
            self.assertTrue(isMega)

            megaFontData = image.readMegaFontData(dirEntry)
            self.assertIsInstance(megaFontData, dict)
            self.assertEqual(len(megaFontData.keys()), 7)
        except Exception as exc:
            print(exc)
            logging.error(exc)
            image.close()
            return
        image.close()

if __name__ == '__main__':
    if __name__ == '__main__':
        logging.basicConfig(level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S',
                            filename='../../d64.log', encoding='utf-8', style='{',
                            format='{asctime} {levelname} {filename}:{lineno}: {message}')
        console = logging.StreamHandler()
        logging.getLogger().addHandler(console)

        logging.info(f"sys.prefix: {sys.prefix}")
        logging.info(f"sys.base_prefix: {sys.base_prefix}")
        if not sys.prefix == sys.base_prefix:
            logging.info("running in a venv")
        else:
            logging.info("not running in a venv")
    unittest.main()
