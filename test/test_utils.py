# -*- coding: utf-8 -*-

"""Test module “utils.py”."""

from mscxyz.utils import get_mscore_bin, mscore
import six
import unittest
if six.PY3:
    from unittest import mock
else:
    import mock


class TestFunctionGetMscoreBin(unittest.TestCase):

    @mock.patch('platform.system')
    @mock.patch('os.path.exists')
    @mock.patch('subprocess.check_output')
    def test_output(self, check_output, exists, system):
        system.return_value = 'Linux'
        exists.return_value = True
        path = bytes('/usr/local/bin/mscore\n'.encode('utf-8'))
        check_output.return_value = path
        output = get_mscore_bin()
        self.assertEqual(output, '/usr/local/bin/mscore')


class TestFunctionMscore(unittest.TestCase):

    @mock.patch('mscxyz.utils.get_mscore_bin')
    @mock.patch('subprocess.Popen')
    def test_function(self, popen, get_mscore_bin):
        get_mscore_bin.return_value = '/bin/mscore'
        popen.return_value = mock.MagicMock(returncode=0)
        result = mscore(['--export-to', 'troll.mscz', 'lol.mscx'])

        self.assertEqual(result.returncode, 0)


if __name__ == '__main__':
    unittest.main()
