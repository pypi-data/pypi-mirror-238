#======================================================================
# test_TrackSector.py
#======================================================================
import unittest
from d64py.base.TrackSector import TrackSector

class TestTrackSector(unittest.TestCase):
    def test_values(self):
        print("testValues()")
        ts = TrackSector(18, 1)
        self.assertEqual(ts.track, 18)
        self.assertEqual(ts.sector, 1)
        print(ts)

    def test_hash(self):
        print("testHash()")
        ts1 = TrackSector(18, 1)
        ts2 = TrackSector(18, 1)
        ts3 = TrackSector(40, 3)
        self.assertEqual(hash(ts1), hash(ts2))
        self.assertNotEqual(hash(ts2), hash(ts3))

if __name__ == '__main__':
    unittest.main()
