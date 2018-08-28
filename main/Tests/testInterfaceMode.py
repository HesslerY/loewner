import sys
sys.path.append('PythonTools')
import unittest
from InterfaceMode import *
from random import randint, uniform
from Constants import *

test_runs = 20

min_rand = 0
max_rand = 150

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!£$%^&*()-+=@?/\.,#~;:][{}<>|"

rand_str_length = 10

# Create a list of single commands that can be matched with integer arguments
int_args = [START_TIME, FINAL_TIME, OUTER_RES, INNER_RES, KAPPA, DRIVE_ALPHA]

# Create a list of single commands that can ONLY be matched with integer arguments (not converted to float)
only_int_args = [OUTER_RES, INNER_RES]

# Create a list of single commands that can be matched with float arguments
float_args = [START_TIME, FINAL_TIME, KAPPA, DRIVE_ALPHA]

# Create a list of single commands that can be matched with 'boolean' (y/n) arguments
bool_args = [SAVE_PLOTS, SAVE_DATA, COMPILE]

# Create a list 'multiple' commands (i.e. take the form PARAM VAL1 VAL2) that accept int values
mult_int_args = [MULTIPLE_RES,MULTIPLE_TIMES]

# Create a list 'multiple' commands (i.e. take the form PARAM VAL1 VAL2) that accept float values
mult_float_args = [MULTIPLE_TIMES]

# Create a list 'multiple' commands (i.e. take the form PARAM VAL1 VAL2) that only accept int values
mult_only_int_args = [MULTIPLE_RES]

class InterfaceModeTests(unittest.TestCase):

    def valid_int_single(self,first_arg):
        return first_arg + " " + str(randint(min_rand,max_rand))

    def valid_int_multiple(self,first_arg):
        return " ".join([first_arg, str(randint(min_rand,max_rand)), str(randint(min_rand,max_rand))])

    def random_string(self,first_arg):
        return first_arg + " " + "".join([chars[randint(min_rand,max_rand) % len(chars)] for _ in range(rand_str_length)])

    def valid_float_single(self,first_arg):
        return first_arg + " " + str(uniform(min_rand,max_rand))

    def valid_float_multiple(self,first_arg):
        return " ".join([first_arg, str(uniform(min_rand,max_rand)), str(uniform(min_rand,max_rand))])

    def test_change_multiple_parameters(self):

        # Create InterfaceMode objects
        single_mode = SingleTrace()
        forsin_mode = ForwardSingle()
        invsin_mode = InverseSingle()

        # Repeat the tests a set number of times:
        for _ in range(test_runs):

            for command in mult_int_args:

                # Check that the int commands accept ints
                arg = self.valid_int_multiple(command)
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),True,arg)

                # Check that the int commands reject strings
                arg = self.random_string(command) + " " + self.random_string("")
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),False,arg)

            for command in mult_float_args:

                # Check that the float commands accept floats
                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),True,arg)

                # Check that the float commands reject strings
                arg = self.random_string(command) + " " + self.random_string("")
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),False,arg)

            for command in mult_only_int_args:

                # Check that the int only commands reject floats
                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),False,arg)

    def test_change_single_parameter(self):

        # Create InterfaceMode objects
        single_mode = SingleTrace()
        forsin_mode = ForwardSingle()
        invsin_mode = InverseSingle()

        # Repeat the tests a set number of times:
        for _ in range(test_runs):

            for command in int_args:

                # Check that the int commands accept ints
                arg = self.valid_int_single(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),True,arg)

                # Check that the int commands reject strings
                arg = self.random_string(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

            for command in float_args:

                # Check that the float commands accept floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),True,arg)

                # Check that the float commands reject strings
                arg = self.random_string(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

            for command in only_int_args:

                # Check that the int only commands reject floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

    def test_change_parameters(self):

        # Create an InterfaceMode object
        single_mode = SingleTrace()
        forsin_mode = ForwardSingle()
        invsin_mode = InverseSingle()

        # Repeat the tests a set number of times:
        for _ in range(test_runs):

            # Check that the int commands accept ints and reject strings
            for command in int_args:

                arg = self.valid_int_single(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                arg = self.random_string(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            # Check that the float commands accept floats and reject strings
            for command in float_args:

                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                arg = self.random_string(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            # Check that the int only commands reject floats
            for command in only_int_args:

                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            # Check that the int commands accept ints and reject strings
            for command in mult_int_args:

                arg = self.valid_int_multiple(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                arg = self.random_string(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            # Check that the float commands accept floats and reject strings
            for command in mult_float_args:

                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                arg = self.random_string(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            # Check that the int only commands reject floats
            for command in mult_only_int_args:

                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

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
                "calphalist first 2 last 0 step 0.5", "kappalist first 1 last 1.5 step 0.6", "kappalist first 1 last 1 step 0.5" \
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

        # Check that InterfaceMode returns False for the bad arguments
        for arg in bad_args:
            self.assertEqual(kappa_forsin_mode.change_parameters(arg),False,arg)
        for arg in bad_three:
            self.assertEqual(kappa_forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
            self.assertEqual(kappa_forsin_mode.change_parameters(arg),False,arg)

