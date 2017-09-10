import os
import sys
import inspect
import unittest
from LoewnerConfig import LoewnerConfig
import Constants

class LoewnerRunTests(unittest.TestCase):

    def test_driving_function(self):

        """
        Test that driving function assignment behaves as expected
        """
        for i in range(Constants.TOTAL_DRIVING_FUNCTIONS):

            loewner_config = LoewnerConfig(driving_function=i)
            self.assertTrue(loewner_config.driving_function == i)

if __name__ == '__main__':
    unittest.main()
