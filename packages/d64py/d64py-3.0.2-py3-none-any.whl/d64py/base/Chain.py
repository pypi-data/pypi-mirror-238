#======================================================================
# Chain.py
#======================================================================
from d64py.base.TrackSector import TrackSector

class Chain:
    sectors: list[TrackSector]

    def __init__(self, sectors=[]):
        self.sectors = sectors

    def size(self):
        return len(self.sectors)
