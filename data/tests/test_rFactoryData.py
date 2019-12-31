import unittest
from data.rFactoryData import *
from data.rFactoryConfig import config_tabCar, config_tabTrack

class Test_test_rFactoryData(unittest.TestCase):
    def test_getAllCarData(self):
        tags = getAllCarData(tags=config_tabCar['carColumns'])
        assert len(tags)

    def test_getAllTrackData(self):
        tags = getAllTrackData(tags=config_tabTrack['trackColumns'])
        assert len(tags)

if __name__ == '__main__':
    unittest.main()
