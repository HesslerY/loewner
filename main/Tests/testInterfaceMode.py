import sys
sys.path.append('PythonTools')
import unittest
from InterfaceMode import *

class MyTest(unittest.TestCase):

    def test_initialise(self):

        # Create an InterfaceMode object
        interface_mode = SingleTrace()

        # Create a list of good arguments
        good_args = ["starttime 0","finaltime 3","outerres 3","innerres 5","saveplots y","saveplots n","savedata y", \
                "savedata n","compile y","compile n","kappa 3.5","drivealpha 0.2"]

        for arg in good_args:
            self.assertEqual(interface_mode.change_single_parameter(*arg.split()),True)
            self.assertEqual(interface_mode.change_parameters(arg),True)

    def test_kappa(self):

        kappa_forsin_mode = ForSinKappa()


