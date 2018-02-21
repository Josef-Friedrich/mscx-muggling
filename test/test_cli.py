# -*- coding: utf-8 -*-

"""Test module “cli.py”."""


import helper
import unittest
import mscxyz
import six
import re


class TestCommandlineInterface(unittest.TestCase):

    def test_help_short(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing():
                mscxyz.execute(['-h'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_help_long(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing():
                mscxyz.execute(['--help'])
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '0')

    def test_without_arguments(self):
        with self.assertRaises(SystemExit) as cm:
            with helper.Capturing('err'):
                mscxyz.execute()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), '2')

    def test_help_text(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                mscxyz.execute(['-h'])
        self.assertTrue('[-h]' in output[0])


class TestHelp(unittest.TestCase):

    def test_all(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                mscxyz.execute(['help', 'all'])
        self.assertTrue(len(output) > 150)

    def test_restructuredtext(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                mscxyz.execute(['help', '--rst', 'all'])
        self.assertTrue('.. code-block:: text' in output)

    def test_markdown(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                mscxyz.execute(['help', '--markdown', 'all'])
        self.assertTrue('```' in output)

    def test_functions_in_all(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                mscxyz.execute(['help', 'all'])
        self.assertTrue('%asciify{text}' in '\n'.join(output))

    def test_functions_in_rename(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                mscxyz.execute(['rename', '--help'])
        self.assertTrue('%asciify{text}' in '\n'.join(output))


class TestVersion(unittest.TestCase):

    def test_version(self):
        with self.assertRaises(SystemExit):
            if six.PY2:
                with helper.Capturing('err') as output:
                    mscxyz.execute(['--version'])
            else:
                with helper.Capturing() as output:
                    mscxyz.execute(['--version'])

        result = re.search('[^ ]* [^ ]*', output[0])
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
