import os
import unittest

from data.cached_data import Cached_data
from data.rFactoryConfig import carTags, trackTags


class Test_test_cached_data(unittest.TestCase):
    def setUp(self):
        self.cache_o = Cached_data('test.csv', carTags)
        self.cache_o.load()

    def test_get_values_empty(self):
        row = self.cache_o.get_values('New ID')
        assert row == dict()

    def test_set_value(self):
        self.cache_o.set_value('New ID', 'Type', '1')
        row = self.cache_o.get_values('New ID')
        assert row['DB file ID'] == 'New ID'
        assert row['Type'] == '1'

    def test_set_value_new(self):
        self.cache_o.set_value('New ID 2', 'Aero', '1')
        row = self.cache_o.get_values('New ID 2')
        assert row['DB file ID'] == 'New ID 2'
        assert row['Type'] == ''
        assert row['Aero'] == '1'

    def test_write(self):
        if os.path.isfile('test.csv'):
            os.remove('test.csv')
        self.test_set_value()
        self.cache_o.write()
        assert os.path.isfile('test.csv')
        self.cache2_o = Cached_data('test.csv', carTags)
        self.cache2_o.load()
        row = self.cache2_o.get_values('New ID')
        assert row['DB file ID'] == 'New ID'
        assert row['Type'] == '1'
        os.remove('test.csv')


if __name__ == '__main__':
    unittest.main()
