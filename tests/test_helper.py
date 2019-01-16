import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from helper.helper import Helper

class Test_Helper(unittest.TestCase):

    ########################
    ## User Related Tests ##
    ########################
    def test_generate_key(self):

        helper: Helper = Helper()

        self.assertEqual(helper.generate_key('user', 42), 'user_042')
        self.assertEqual(helper.generate_key('session', 1), 'session_001')
        self.assertEqual(helper.generate_key('user', 542), 'user_542')
        self.assertEqual(helper.generate_key('session', 0), 'session_000')


if __name__ == '__main__':
    
    unittest.main(exit=False)