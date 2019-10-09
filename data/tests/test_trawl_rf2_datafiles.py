import unittest
from data.trawl_rF2_datafiles import *

class Test_trawl_rF2_datafiles(unittest.TestCase):
    def test_get_folders_and_timestamps(self):
        cdf = CarDataFiles()
        folders_and_timestamps = cdf.get_mfts_and_timestamps()
        assert folders_and_timestamps
    def test_get_data_files_and_timestamps(self):
        cdf = CarDataFiles()
        data_files_and_timestamps = cdf.get_data_files_and_timestamps()
        assert data_files_and_timestamps
    def test_newer_mfts(self):
        cdf = CarDataFiles()
        cdf.get_mfts_and_timestamps()
        cdf.get_data_files_and_timestamps()
        _newer = cdf.newer_mfts()
        for _mft in _newer:
            print(_mft)
        print(len(_newer))
        pass
    def test_make_datafile_name(self):
        cdf = CarDataFiles()
        _from = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.94\USF2000_2016.mft"
        _to = r"datafiles\cars\USF2000_2016.rfactory.txt"
        _result = cdf.make_datafile_name(_from)
        assert _result == _to, _result
    def test_get_mas_info(self):
        scns, mas_tags = getMasInfo(
            r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\BATHURST_2016_V3\3.0" )
        pass
    def test_new_data(self):
        cdf = CarDataFiles()
        _from = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.94\USF2000_2016.mft"
        cdf.new_data(_from)
        pass


if __name__ == '__main__':
    unittest.main()
