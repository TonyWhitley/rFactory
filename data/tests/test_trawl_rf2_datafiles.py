import os
import unittest
from data.trawl_rF2_datafiles import *
from data.rFactoryConfig import rF2root
from data.utils import executeCmd, readFile, writeFile


def vehicle(path):
    return os.path.join(
        r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles",
        path)


def location(path):
    return os.path.join(
        r"c:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Locations",
        path)


class Test_trawl_rF2_datafiles_folders(unittest.TestCase):
    """
    Tests on the folder processing
    """

    def test_find_single_mod_folders(self):
        cdf = CarDataFiles()
        sm = cdf.find_single_mod_folders()
        print(sm)
        assert len(sm)

        tdf = TrackDataFiles()
        sm = tdf.find_single_mod_folders()
        print(sm)
        assert len(sm)

    def test_find_multi_mas_folders(self):
        cdf = CarDataFiles()
        mm, multi_mfts = cdf.find_multi_mod_folders()
        print(mm)
        assert len(mm)
        assert(len(multi_mfts))

        tdf = TrackDataFiles()
        mm, multi_mfts = tdf.find_multi_mod_folders()
        print(mm)
        assert len(mm)
        assert(len(multi_mfts))

    def test_getListOfFiles(self):
        folder = location(r"Brianza_1966\2.04")
        _mas_files = getListOfFiles(folder, '*.mas')
        assert len(_mas_files)

        folder = location(r'Kyalami_Legends_[1976]\\1.01LE_dx11')
        _mas_files = getListOfFiles(folder, '*.mas')
        assert len(_mas_files)


class Test_trawl_rF2_datafiles(unittest.TestCase):
    _example_expected_car_mft_tags = {
        'Name': 'USF2000_2016',
        'Version': '2.00',
        'Type': '2',
        'Author': 'Studio 397?',
        'Origin': '0',
        'Category': '0',
        'ID': 'AAA9999',
        'URL': '',
        'Desc': '',
        'Date': '2019-12-17',
        'Flags': '270536704',
        'RefCount': '1',
        'Year': '2016',
        'Decade': '2010-',
        'strippedName': 'Usf2000_',
        'originalFolder': 'Installed\\Vehicles\\USF2000_2016\\2.00',
        'vehFile': 'USF2000_4.VEH',
        'Manufacturer': 'Usf2000',
        'Model': 'Usf2000',
        'Rating': '***'}
    # 'Signature': '9743ca82a6b4177dcffc965538f8b3200d9f5b9bfcd2324885da9ca5079cbc5d', 'MASFile': 'car.mas 703499de4dbd8bd2dccf62347cba3e1b36b18d5df0a49971a30068dfa6bfebbf',

    _example_expected_track_mft_tags = {'Name': 'BATHURST_2016_V3',
                                        'Version': '3.0',
                                        'Type': '1',
                                        'Author': '',
                                        'Origin': '3',
                                        'Category': '57',
                                        'ID': '',
                                        'URL': '',
                                        'Desc': 'Based on the 3PA Bathurst from ISI\x0fUpdated to latest technology\x0fHas 2 versions the V8 supercars 1000 and the 12h. Sponsors from 2016\x0f',
                                        'Date': '2018-08-19',
                                        'Flags': '3149824',
                                        'RefCount': '2',
                                        'strippedName': 'Bathurst__V3',
                                        'Year': '2016',
                                        'Decade': '2010-',
                                        'originalFolder': 'Installed\\Locations\\BATHURST_2016_V3\\3.0',
                                        'Scene Description': 'bathurst2016',  # 'BATHURST2016_12H',
                                        'tType': 'Temporary',
                                        'Track Name': 'Bathurst  V3',
                                        'Rating': '***'}
    # 'Signature': 'ac9cc81fada5d3cf1c2b41e8a63ce9af0c95ebf471dec94181824ebb5c6f2603',
    # 'MASFile': 'Bathurst2016_maps.mas 776d45e071fce27ad580c45f217ebb464f731e98d4e8686ab808f29db6714591',

    def test_set_new_tag(self):
        cdf = CarDataFiles()
        cdf['fred'] = '1'
        assert cdf['fred'] == '1'

    def test_no_overwrite_tag(self):
        cdf = CarDataFiles()
        cdf['fred'] = '1'
        cdf['fred'] = '2'
        assert cdf['fred'] == '1'

    def test_invalid_set_new_tag(self):
        cdf = CarDataFiles()
        with self.assertRaises(TypeError):
            cdf['fred'] = 1

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
        _newer = cdf.get_newer_mfts()
        for _mft in _newer:
            print(_mft)
        print(len(_newer))
        pass

    def test_make_datafile_name(self):
        cdf = CarDataFiles()
        _from = vehicle(r"USF2000_2016\1.94\USF2000_2016.mft")
        _to = r"datafiles\cars\USF2000_2016.rfactory.txt"
        _result = cdf.make_datafile_name(_from)
        assert _result == _to, _result

    def test_list_files_in_mas_files(self):
        cdf = CarDataFiles()
        files = cdf.dir_files_in_mas_files(
            vehicle(r"SuperCharged_Miata_Level1\1.32"))
        assert files != {}

    def test_run_ModMgr(self):
        """ Minimal test that ModMgr runs """
        ModMgr = os.path.join(rF2root, r'Bin32\ModMgr.exe')
        temporaryFile = 'temporaryFile'
        car = vehicle(r"SuperCharged_Miata_Level1\1.32\SPCL1Miata_car.mas")
        cmd = F'"{ModMgr}" -q -l"{car}"'.format() \
            + F' 2>&1 {temporaryFile} > nul 2>&1'.format()
        # Put the command in a temp batch file and it works
        bat = os.path.join(os.getcwd(), 'x.bat')
        writeFile(bat, cmd)
        retcode, rsp = executeCmd(bat)
        assert retcode == 0, retcode
        text, __error = readFile(temporaryFile)
        assert text != ''
        os.remove(bat)  # tidy up
        os.remove(temporaryFile)

        # But executing ModMgr directly doesn't work (it used to!)
        retcode, rsp = executeCmd(cmd)
        assert retcode == 0, retcode
        assert rsp == b''
        try:
            os.remove(temporaryFile)
            assert True, F"Didn't expect {temporaryFile} to have been created".format(
            )
        except BaseException:
            pass  # no file created, this confirmatory test passed.
        pass

    def test_read_track_mas_files(self):
        tdf = TrackDataFiles()
        tags = dict()
        tags = tdf.read_mas_files(tags,
                                  location(r"BATHURST_2016_V3\3.0"))
        assert tags['Scene Description'] == 'bathurst2016', tags
        assert tags['Latitude'] == '-33.26', tags
        assert tags['Longitude'] == '149.33', tags

    def test_read_car_mas_files(self):
        cdf = CarDataFiles()
        tags = dict()
        tags = cdf.read_mas_files(tags,
                                  vehicle(r"SuperCharged_Miata_Level1\1.32"))
        assert tags['Gearshift'] == 'H6', tags
        assert tags['Mass'] == '1036', tags
        assert tags['F/R/4WD'] == 'REAR', tags
    """
    Legacy
    def test_get_mas_info_track(self):
        scns, mas_tags = getMasInfo(
            location(r"BATHURST_2016_V3\3.0"))
        assert scns == ['bathurst12h2016', 'bathurst2016'], scns
        assert mas_tags == {'Latitude': '-33.26', 'Longitude': '149.33'},mas_tags

    def test_get_mas_info_car(self):
        scns, mas_tags = getMasInfo(
            vehicle(r"SuperCharged_Miata_Level1\1.32"))
        print(scns, mas_tags)
        print('Hello')
    """

    def test_get_mft_car_tags(self):
        cdf = CarDataFiles()
        _from = vehicle(
            r"BTCC_NGTC_Ford_Focus_RS\0.95\BTCC_NGTC_Ford_Focus_RS.mft")
        _tags = cdf._get_mft_tags(_from)
        assert len(_tags['Date'])
        _tags, cache_write = cdf.new_data(_from, new_cache=True)
        assert len(_tags['Date'])
        assert '-' in _tags['Date']

    def test_get_initial_track_tags(self):
        tdf = TrackDataFiles()
        _from = location(r"Dijon79\0.51\Dijon79.mft")
        _tags = tdf._get_mft_tags(_from)
        assert len(_tags['Date'])
        _tags, cache_write = tdf.new_data(_from, new_cache=True)
        assert len(_tags['Date'])
        assert '-' in _tags['Date']

    def test_new_data_car(self):
        cdf = CarDataFiles()
        _from = vehicle(r"USF2000_2016\2.00\USF2000_2016.mft")
        _tags, cache_write = cdf.new_data(_from, new_cache=True)
        if cache_write:
            cdf.cache_o.write()
        for t in self._example_expected_car_mft_tags:
            assert _tags[t].lower() == self._example_expected_car_mft_tags[t].lower(
            ), F'{t}: "{_tags[t]}", expected "{self._example_expected_car_mft_tags[t]}"'.format()

    def test_new_data_track(self):
        tdf = TrackDataFiles()
        _from = location(r"BATHURST_2016_V3\3.0\BATHURST_2016_V3.mft")
        _tags, cache_write = tdf.new_data(_from, new_cache=True)
        print(_tags)
        for t in self._example_expected_track_mft_tags:
            assert _tags[t].lower() == self._example_expected_track_mft_tags[t].lower(
            ), F'{t}: {_tags[t]} expected {self._example_expected_track_mft_tags[t]}'.format()

    """
    def test_get_data_track(self):
        tdf = TrackDataFiles()
        _from = location(r"BATHURST_2016_V3\3.0\BATHURST_2016_V3.mft"
        _tags = tdf.get_data(_from)
        for t in self._example_expected_track_mft_tags:
            assert _tags[t].lower() == self._example_expected_track_mft_tags[t].lower(), \
                F'{t}: "{_tags[t]}", expected "{self._example_expected_track_mft_tags[t]}"'.format()
    """

    def test_car_multi_mod(self):
        cdf = CarDataFiles()
        for tags in cdf.multi_mod("F1 1998"):
            print(tags)
            pass

    def test_track_multi_mod(self):
        tdf = TrackDataFiles()
        for tags in tdf.multi_mod("F1_1988_Tracks"):
            print(tags)
            pass

    def test_createDefaultDataFiles(self):
        #newFiles = NEWcreateDefaultDataFiles()
        pass

    def test_translate_date(self):
        # Windows
        datestr = translate_date('116444736000000000')
        assert datestr == '1970-01-01', datestr
        datestr = translate_date('132160618014460000')
        assert datestr == '2019-10-20', datestr
        # Unix
        datestr = translate_date('0000000000')
        assert datestr == '1970-01-01', datestr
        datestr = translate_date('1493632926')
        assert datestr == '2017-05-01', datestr


if __name__ == '__main__':
    unittest.main()
