#======================================================================
# PartialDirectoryException.py
#======================================================================
from d64py.base import DirEntry

class PartialDirectoryException(BaseException):
    partialDir: list[DirEntry]

    def __init__(self, message, partialDir: list[DirEntry]):
        super().__init__(message)
        self.partialDir = partialDir

    def getPartialDir(self) -> list[DirEntry]:
        return self.partialDir
