import os
import sys
import inspect

import unittest

# CURRENTDIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# PARENTDIR = os.path.dirname(CURRENTDIR)
# sys.path.insert(0, PARENTDIR)

from LoewnerConfig import LoewnerConfig
import Constants

class LoewnerConfigTests(unittest.TestCase):

    def test_driving_function(self):

        """
        Test that driving function assignment behaves as expected
        """
        for i in range(Constants.TOTAL_DRIVING_FUNCTIONS):

            loewner_config = LoewnerConfig(driving_function=i, exact_mode=False)
            self.assertTrue(loewner_config.driving_function == i)


if __name__ == '__main__':
    unittest.main()
