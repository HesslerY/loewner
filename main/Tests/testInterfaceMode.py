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

        # Create a list of good two-argument commands
        good_args = ["starttime 0","finaltime 3","outerres 3","innerres 5","saveplots y","saveplots n","savedata y", \
                "savedata n","compile y","compile n","kappa 3.5","drivealpha 0.2"]

        # Create a list of good three-argument commands
        good_three = ["times 0 10", "res 100 2", "times 4.8 10", "times 0.5 10.5", "times 2 10.5", "res 1 1"]

        # Create a list of bad three-argument commands
        bad_three = ["times a b", "res !! -", "times 4.8 b", "times a 10.5", "res 10.2 1", "res 10.2 a", "res a 1", "res 1 a"]

        # Create a list of bad arguments
        bad_args = ["starttime x","finaltime -","outerres 3.2","innerres 0.1","outerres ???","saveplots x","saveplots 2.5","savedata 1","drivealpha bbbb","kappa aaaa"]

        # Check that InterfaceMode returns True for the correct arguments
        for arg in good_args:
            self.assertEqual(interface_mode.change_single_parameter(*arg.split()),True,arg)
            self.assertEqual(interface_mode.change_parameters(arg),True,arg)
        for arg in good_three:
            self.assertEqual(interface_mode.change_multiple_parameters(*arg.split()),True,arg)
            self.assertEqual(interface_mode.change_parameters(arg),True,arg)

        # Check that InterfaceMode returns False for the bad arguments
        for arg in bad_args:
            self.assertEqual(interface_mode.change_single_parameter(*arg.split()),False,arg)
            self.assertEqual(interface_mode.change_parameters(arg),False,arg)
        for arg in bad_three:
            self.assertEqual(interface_mode.change_multiple_parameters(*arg.split()),False,arg)
            self.assertEqual(interface_mode.change_parameters(arg),False,arg)

    def test_numerical_inverse(self):

        # Create an InterfaceMode object
        interface_mode = InverseSingle()

        # Create a list of good two-argument commands
        good_args = ["starttime 0","finaltime 3","outerres 3","innerres 5","saveplots y","saveplots n","savedata y", \
                "savedata n","compile y","compile n","kappa 3.5","drivealpha 0.2"]

        # Create a list of good three-argument commands
        good_three = ["times 0 10", "res 100 2", "times 4.8 10", "times 0.5 10.5", "times 2 10.5", "res 1 1"]

        # Create a list of bad three-argument commands
        bad_three = ["times a b", "res !! -", "times 4.8 b", "times a 10.5", "res 10.2 1", "res 10.2 a", "res a 1", "res 1 a"]

        # Create a list of bad arguments
        bad_args = ["starttime x","finaltime -","outerres 3.2","innerres 0.1","saveplots x","saveplots 2.5","savedata 1"]

        # Check that InterfaceMode returns True for the correct arguments
        for arg in good_args:
            self.assertEqual(interface_mode.change_single_parameter(*arg.split()),True,arg)
            self.assertEqual(interface_mode.change_parameters(arg),True,arg)
        for arg in good_three:
            self.assertEqual(interface_mode.change_multiple_parameters(*arg.split()),True,arg)
            self.assertEqual(interface_mode.change_parameters(arg),True,arg)

        # Check that InterfaceMode returns False for the bad arguments
        for arg in bad_args:
            self.assertEqual(interface_mode.change_single_parameter(*arg.split()),False,arg)
            self.assertEqual(interface_mode.change_parameters(arg),False,arg)
        for arg in bad_three:
            self.assertEqual(interface_mode.change_multiple_parameters(*arg.split()),False,arg)
            self.assertEqual(interface_mode.change_parameters(arg),False,arg)

    def test_exactinverse_mode(self):

        # Create an InterfaceMode object
        inverse_mode = ExactInverse()

        # Create a list of good arguments
        good_args = ["starttime 0","finaltime 3","outerres 3","saveplots y","saveplots n","savedata y", \
                "savedata n","kappa 3.5","drivealpha 0.2"]

        # Create a list of good three-argument commands
        good_three = ["times 0 10", "times 4.8 10", "times 0.5 10.5", "times 2 10.5"]

        # Create a list of bad three-argument commands - resolution pairs not used for exact inverse
        bad_three = ["times a b", "res 100 2","res !! -", "times 4.8 b", "times a 10.5", "res 10.2 1", "res 10.2 a", "res a 1", "res 1 a", "res 1 1"]

        # Create a list of bad arguments - compile and innerres are not used in exact inverse mode
        bad_args = ["starttime x","compile y","compile n","finaltime -","outerres 3.2","innerres 5","innerres 0.1","saveplots x","saveplots 2.5","savedata 1"]

        # Check that InterfaceMode returns True for the correct arguments
        for arg in good_args:
            self.assertEqual(inverse_mode.change_single_parameter(*arg.split()),True,arg)
            self.assertEqual(inverse_mode.change_parameters(arg),True,arg)
        for arg in good_three:
            self.assertEqual(inverse_mode.change_multiple_parameters(*arg.split()),True,arg)
            self.assertEqual(inverse_mode.change_parameters(arg),True,arg)

        # Check that InterfaceMode returns False for the bad arguments
        for arg in bad_args:
            self.assertEqual(inverse_mode.change_single_parameter(*arg.split()),False,arg)
            self.assertEqual(inverse_mode.change_parameters(arg),False,arg)
        for arg in bad_three:
            self.assertEqual(inverse_mode.change_multiple_parameters(*arg.split()),False,arg)
            self.assertEqual(inverse_mode.change_parameters(arg),False,arg)

    def test_kappa(self):

        # Create a Kappa InterfaceMode object
        kappa_forsin_mode = ForSinKappa()

        # Create a list of good arguments
        good_notkappa_args = ["starttime 0","finaltime 3","outerres 3","innerres 5","saveplots y","saveplots n","savedata y", \
                "savedata n","compile y","compile n"]

        # Create a list of good arguments
        good_kappa_args = ["kappalist first 0 last 5 step 0.5", "kappalist first 0 last 5 num 12"]

        # Create a list of good three-argument commands
        good_three = ["times 0 10", "res 100 2", "times 4.8 10", "times 0.5 10.5", "times 2 10.5", "res 1 1"]

        # Create a list of bad three-argument commands
        bad_three = ["times a b", "res !! -", "times 4.8 b", "times a 10.5", "res 10.2 1", "res 10.2 a", "res a 1", "res 1 a"]

        # Create a list of bad arguments
        bad_args = ["calphalist first 0 last 5 step 0.5", "kappalist last 0 last 5 num 12", "kappalist first -1 last 5 step 0.5" \
                "calphalist first 2 last 0 step 0.5", "kappalist first 1 last 1.5 step 0.6", "kappalist first 1 last 1.5 step 0.5" \
                "kappalist first 0 last 1 num 0", "kappalist first 1 last 1.5 num 1", "kappalist first 1 last 1.5 num 2"]

        # Check that InterfaceMode returns True for the correct arguments
        for arg in good_notkappa_args:
            self.assertEqual(kappa_forsin_mode.change_single_parameter(*arg.split()),True,arg)
            self.assertEqual(kappa_forsin_mode.change_parameters(arg),True,arg)
        for arg in good_three:
            self.assertEqual(kappa_forsin_mode.change_multiple_parameters(*arg.split()),True,arg)
            self.assertEqual(kappa_forsin_mode.change_parameters(arg),True,arg)
        for arg in good_kappa_args:
            self.assertEqual(kappa_forsin_mode.change_parameters(arg),True,arg)

        # Check that InterfaceMode returns True for the bad arguments
        for arg in bad_args:
            self.assertEqual(kappa_forsin_mode.change_parameters(arg),True,arg)
        for arg in good_three:
            self.assertEqual(kappa_forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
            self.assertEqual(kappa_forsin_mode.change_parameters(arg),False,arg)

