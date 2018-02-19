"""File for various tests"""


import helper
import unittest
import mscxyz


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

    @unittest.skip('No working in tox')
    def test_help_text(self):
        with self.assertRaises(SystemExit):
            with helper.Capturing() as output:
                mscxyz.execute(['-h'])
        self.assertEqual(
            output[0],
            'usage: test.py [-h] [-b] [-g GLOB] [-p PICK] \
[-c CYCLE_LENGTH] [-v]')


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


if __name__ == '__main__':
    unittest.main()