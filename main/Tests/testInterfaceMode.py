import sys
sys.path.append('PythonTools')
import unittest
from InterfaceMode import *

class MyTest(unittest.TestCase):

    def create_int_arg(self,int_arg):
        pass

    def test_single_trace(self):

        # Create an InterfaceMode object
        interface_mode = SingleTrace()

        # Create a list of good arguments
        good_args = ["starttime 0","finaltime 3","outerres 3","innerres 5","saveplots y","saveplots n","savedata y", \
                "savedata n","compile y","compile n","kappa 3.5","drivealpha 0.2"]

        # Create a list of bad arguments
        bad_args = ["starttime x","finaltime -","outerres 3.2","innerres 0.1","saveplots x","saveplots 2.5","savedata 1"]

        # Check that InterfaceMode returns True for the correct arguments
        for arg in good_args:
            self.assertEqual(interface_mode.change_single_parameter(*arg.split()),True)
            self.assertEqual(interface_mode.change_parameters(arg),True)

        # Check that InterfaceMode returns True for the correct arguments
        for arg in bad_args:
            self.assertEqual(interface_mode.change_single_parameter(*arg.split()),False)
            self.assertEqual(interface_mode.change_parameters(arg),False)

    def test_kappa(self):

        # Create a Kappa InterfaceMode object
        kappa_forsin_mode = ForSinKappa()

        # Create a list of good arguments
        good_notkappa_args = ["starttime 0","finaltime 3","outerres 3","innerres 5","saveplots y","saveplots n","savedata y", \
                "savedata n","compile y","compile n"]

        # Create a list of good arguments
        good_kappa_args = ["kappalist first 0 last 5 step 0.5", "kappalist first 0 last 5 num 12"]

        # Create a list of bad arguments
        bad_args = ["calphalist first 0 last 5 step 0.5", "kappalist last 0 last 5 num 12", "kappalist first -1 last 5 step 0.5" \
                "calphalist first 2 last 0 step 0.5", "kappalist first 1 last 1.5 step 0.6", "kappalist first 1 last 1.5 step 0.5" \
                "kappalist first 0 last 1 num 0", "kappalist first 1 last 1.5 num 1", "kappalist first 1 last 1.5 num 2"]

        # Check that InterfaceMode returns True for the correct arguments
        for good_notkappa_arg in good_notkappa_args:
            self.assertEqual(kappa_forsin_mode.change_single_parameter(*good_notkappa_arg.split()),True)
            self.assertEqual(kappa_forsin_mode.change_parameters(good_notkappa_arg),True,good_notkappa_arg)

        for good_kappa_arg in good_kappa_args:
            self.assertEqual(kappa_forsin_mode.change_parameters(good_kappa_arg),True,good_kappa_arg)

        for bad_arg in bad_args:
            self.assertEqual(kappa_forsin_mode.change_parameters(bad_arg),True)

