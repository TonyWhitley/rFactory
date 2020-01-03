import os
import unittest

import data.rFactoryConfig as rFactoryConfig


class Test_test_rFactoryConfig(unittest.TestCase):
    def test_validate(self):
        rFactoryConfig.new_config_file()
        paths = rFactoryConfig.validate()
        assert paths['rF2root'], rFactoryConfig.rF2root
        assert paths['SteamExe'], rFactoryConfig.SteamExe
        assert paths['DiscordExe'], rFactoryConfig.DiscordExe
        assert paths['CrewChiefExe'], rFactoryConfig.CrewChiefExe
        assert paths['playerPath'], rFactoryConfig.playerPath
        assert paths['vehicles'], rFactoryConfig.vehicles


if __name__ == '__main__':
    unittest.main()
