#======================================================================
# DirEntry.py
#======================================================================
from enum import Enum
from datetime import datetime
import logging
from d64py.base.Constants import (DirEntryOffsets, FileType, FileStatus,
     GeosFileType, GeosFileStructure)
from d64py.base.GeosFileHeader import GeosFileHeader
from d64py.base.TrackSector import TrackSector
from d64py.utility import D64Utility

class DirEntry:
    def __init__(self, dirBytes: bytearray):
        self.raw = bytearray(dirBytes)
        if not len(dirBytes) == DirEntryOffsets.DIR_LENGTH.value:
            msg = f"Wrong directory entry length: {len(dirBytes)}"
            raise Exception(msg)

    def __eq__(self, other):
        if not isinstance(other, DirEntry):
            raise Exception(f"Can't compare {type(other)} to DirEntry!")
        return self.raw == other.raw

    def __str__(self):
        if self.isGeosFile():
            formatString = "{:<16s} {:3d} {:s} {:<10s} {:<12s} {:s}"
            displayString = formatString.format(self.getDisplayFileName(),
                            self.getFileSize(), self.getFileTypeDescription(),
                            self.getGeosFileStructure().name,
                            self.getGeosFileType().name, self.getFormattedDateStamp())
        else:
            formatString = "{:<16s} {:3d} {:s} {:s}"
            displayString = formatString.format(self.getDisplayFileName(),
                            self.getFileSize(), self.getFileTypeDescription(),
                            self.getFormattedDateStamp())
        return displayString

    def __hash__(self):
        # self.raw is a bytearray (mutable), so we can't just use hash()
        hash = 3; i = 0
        while i < len(self.raw):
            hash = 17 * hash + self.raw[i]
            i += 1
        return hash

    def getFileType(self) -> int:
        return self.raw[0] & 0x0f

    def getFileStatus(self) -> int:
        return self.raw[0] & 0xf0

    def getFileTypeDescription(self) -> int:
        fileTypeAbbreviation = "??? "
        for fileType in FileType:
            if fileType.code == self.getFileType() & 0x0f:
                fileTypeAbbreviation = fileType.abbreviation
                if self.getFileType() & 0xf0 == FileStatus.FILE_LOCKED:
                    fileTypeAbbreviation += "<"
                else:
                    fileTypeAbbreviation += " "
                break
        return fileTypeAbbreviation

    def getFileTrackSector(self) -> TrackSector:
        return TrackSector(self.raw[1], self.raw[2])

    def getRawFileName(self) -> bytearray:
        return self.raw[3:19]

    def getDisplayFileName(self) -> str:
        unRaw = bytearray(16)
        i = 0
        while i < 16:
            unRaw[i] = self.raw[i + 3] & 0x7f
            i += 1
        return unRaw.decode("ascii").strip()

    def getAsciiFileName(self) -> str:
        fileName = bytearray(self.raw[3:19])
        if self.raw[22]: # i.e. if GEOS file
            i = 3
            while i < 19:
                if self.raw[i] == 0xa0: # shifted space
                    self.raw[i] = 0x20  # regular space
                else:
                    self.raw[i] = self.raw[i] & 0x7f
                i += 1
            return self.raw[3:19].decode("ascii")
        else:
            return D64Utility.petsciiToAsciiString(fileName)

    def isGeosFile(self) -> bool:
        return not self.getGeosFileType() == GeosFileType.NOT_GEOS

    def getGeosFileHeaderTrackSector(self) -> TrackSector:
        return TrackSector(self.raw[19], self.raw[20])

    def getGeosFileHeader(self) -> GeosFileHeader:
        return self.geosFileHeader

    def setGeosFileHeader(self, geosFileHeader):
        self.geosFileHeader = geosFileHeader

    def getGeosFileStructure(self) -> int:
        for fileStructure in GeosFileStructure:
            if fileStructure.value == self.raw[21]:
                break
        return fileStructure

    def getGeosFileType(self) -> int:
        # Do this for all files, so that NOT_GEOS will show even on a
        # non - GEOS disk image. Initialize first in case of corrupt disk.
        geosFileType = GeosFileType.NOT_GEOS
        for fileType in GeosFileType:
            if fileType.code == self.raw[22]:
                geosFileType = fileType
                break
        return geosFileType

    def getDateStamp(self) -> datetime:
        if self.raw[23] < 85:
            year = self.raw[23] + 2000
        else:
            year = self.raw[23] + 1900
        month = self.raw[24]
        day = self.raw[25]
        hour = self.raw[26]
        minute = self.raw[27]
        # datetime(year, month, day, hour, minute, second, microsecond)
        return datetime(year, month, day, hour, minute)

    def getFormattedDateStamp(self):
        dateString: str = "                "
        try :
            dateString = self.getDateStamp().strftime("%Y-%m-%d %H:%M:%S")
        except:
            pass
        return dateString

    def getFileSize(self) -> int:
        return D64Utility.makeWord(self.raw, 28)
