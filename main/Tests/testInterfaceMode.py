import sys
sys.path.append('PythonTools')
import unittest
from InterfaceMode import *

class MyTest(unittest.TestCase):

    def test_initialise(self):

        interface_mode = SingleTrace()

        good_args = [("starttime","0"),("finaltime","3"),("outerres","3"),("innerres","5"),("saveplots","y"),("saveplots","n"),("savedata","y"), \
                ("savedata","n"),("compile","y"),("compile","n"),("kappa","3.5"),("drivealpha","0.2")]

        for arg in good_args:
            self.assertEqual(interface_mode.change_single_parameter(arg[0],arg[1]),True)

