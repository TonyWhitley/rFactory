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
    def test_list_files_in_mas_files(self):
        cdf = CarDataFiles()
        files = cdf.dir_files_in_mas_files(
            r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\SuperCharged_Miata_Level1\1.32")
        assert files != {}

    def test_read_track_mas_files(self):
        tdf = TrackDataFiles()
        tags = dict()
        tags = tdf.read_mas_files(tags,
                                 r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\BATHURST_2016_V3\3.0")
        assert tags['Scene Description'] == 'bathurst2016', tags
        assert tags['Latitude'] == '-33.26', tags
        assert tags['Longitude'] == '149.33', tags
    def test_read_car_mas_files(self):
        cdf = CarDataFiles()
        tags = dict()
        tags = cdf.read_mas_files(tags,
            r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\SuperCharged_Miata_Level1\1.32")
        assert tags['Gearshift'] == 'H6', tags
        assert tags['Mass'] == '1036', tags
        assert tags['F/R/4WD'] == 'REAR', tags
    def test_get_mas_info_track(self):
        scns, mas_tags = getMasInfo(
            r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\BATHURST_2016_V3\3.0")
        assert scns == ['bathurst12h2016', 'bathurst2016'], scns
        assert mas_tags == {'Latitude': '-33.26', 'Longitude': '149.33'},mas_tags
    def test_get_mas_info_car(self):
        scns, mas_tags = getMasInfo(
            r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\SuperCharged_Miata_Level1\1.32")
        print(scns, mas_tags)
        print('Hello')
    def test_new_data_car(self):
        cdf = CarDataFiles()
        _from = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\USF2000_2016\1.94\USF2000_2016.mft"
        cdf.new_data(_from)
    def test_new_data_track(self):
        tdf = TrackDataFiles()
        _from = r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations\BATHURST_2016_V3\3.0\BATHURST_2016_V3.mft"
        tdf.new_data(_from)
        pass


if __name__ == '__main__':
    unittest.main()
