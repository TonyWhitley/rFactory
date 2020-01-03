import os
import unittest
from data.utils import executeCmd, writeFile


class Test_test_utils(unittest.TestCase):
    def test_executeCmd(self):
        test_text = 'Hello world\n'
        bat = os.path.join(os.getcwd(), 'x.bat')
        writeFile(bat, '@echo ' + test_text)
        cmd = bat
        retcode, rpt = executeCmd(cmd)
        os.remove(bat)
        assert retcode == 0, retcode
        assert rpt.strip() == bytearray(test_text, 'utf8').strip(), rpt
        pass


if __name__ == '__main__':
    unittest.main()
