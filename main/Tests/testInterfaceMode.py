import sys
sys.path.append('PythonTools')
import unittest
from InterfaceMode import *
from random import randint, uniform
from Constants import *

test_runs = 20

min_rand = 0
max_rand = 150

# List of characters used to constuct a random word
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!£$%^&*()-+=@?/\.,#~;:][{}<>|"

# List of characters with y and n ommitted to test yes/no functions
bad_chars = "abcdefghijklmopqrstuvwxzABCDEFGHIJKLMNOPQRSTUVWXYZ!£$%^&*()-+=@?/\.,#~;:][{}<>|"

rand_str_length = 10

# Create a list of time-related commands for the InterfaceMode object
time_args = [START_TIME, FINAL_TIME]

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

# Create a list of all InterfaceMode objects
interface_modes = [InterfaceMode(),SingleTrace(),ForwardSingle(),InverseSingle(),ExactInverse(),TwoTrace(),WedgeAlpha(),ExactLinear(),ExactConstant(),ExactSquareRoot(),KappaAlpha(""), \
        ForSinKappa()]

class InterfaceModeTests(unittest.TestCase):

    # Create an valid y boolean argument
    def valid_yes(self,first_arg):
        return first_arg + " y"

    # Create an valid n boolean argument
    def valid_no(self,first_arg):
        return first_arg + " n"

    # Create an valid int argument
    def valid_int_single(self,first_arg):
        return first_arg + " " + str(randint(min_rand,max_rand))

    # Create an valid multiple int argument
    def valid_int_multiple(self,first_arg):
        return " ".join([first_arg, str(randint(min_rand,max_rand)), str(randint(min_rand,max_rand))])

    # Create a random string of length rand_str_length
    def random_string(self):
        return "".join([chars[randint(min_rand,max_rand) % len(chars)] for _ in range(rand_str_length)])

    # Create an invalid argument in the form of a random string
    def random_string_command(self,first_arg):
        return first_arg + " " + self.random_string()

    # Create a valid float argument
    def valid_float_single(self,first_arg):
        return first_arg + " " + str(uniform(min_rand,max_rand))

    # Create a valid multiple float argument
    def valid_float_multiple(self,first_arg):
        return " ".join([first_arg, str(uniform(min_rand,max_rand)), str(uniform(min_rand,max_rand))])

    # Create a command string from a parameter and a value
    def two_command_string(self,param,value):
        return param + " " + str(value)

    # Create a command string from a parameter and a value
    def three_command_string(self,param,value1,value2):
        return param + " " + str(value1) + " " + str(value2)

    # Create an invalid boolean argument - parameter plus a single character that is neither y nor n (e.g. compile z)
    def invalid_single_char(self,param):
        return param + " " + bad_chars[randint(min_rand,max_rand) % len(bad_chars)]

    def test_change_single_time(self):

        for _ in range(test_runs):
            for command in time_args:
                for mode in interface_modes:

                    ## CORRECT ASSIGNMENT TESTS - See that object member variables change as expected and that valid input returns True

                    # Create a command for setting to the time to a random int
                    rand_int = randint(min_rand,max_rand)
                    arg = self.two_command_string(command,rand_int)
                    # Check that the time-change function returns True when this command is passed to the InterfaceMode obejct
                    self.assertTrue(mode.change_single_time(*arg.split()))
                    # Check that the member variable has changed to the expected value
                    self.assertEqual(mode.time_settings[command],rand_int,mode.time_settings[command])

                    # Create a command for setting to the time to a random float (risky due to conversion to and from string but this seems to work anyway)
                    rand_float = uniform(min_rand,max_rand)
                    arg = self.two_command_string(command,rand_float)
                    # Check that the time-change function returns True when this command is passed to the InterfaceMode obejct
                    self.assertTrue(mode.change_single_time(*arg.split()))
                    # Check that the assignment worked
                    self.assertEqual(mode.time_settings[command],rand_float,mode.time_settings[command])

                    ## BAD INPUT TESTS - See that input function rejects unusual input (e.g. "starttime aaaa", "starttime starttime" rather than "starttime 2")

                    # Create a command for 'setting' time to a string - bad input
                    arg = self.random_string_command(command)
                    # Check that the time-change function returns False when this command is passed to the InterfaceMode obejct
                    self.assertFalse(mode.change_single_time(*arg.split()))
                    # Check that the time-change function returns False when only one argument is given
                    self.assertFalse(mode.change_single_time(command,""))
                    # Check that the time-change function returns False when the 'param' is given twice
                    self.assertFalse(mode.change_single_time(command,command))
                    # Check that the time-change function returns False when the time commands aren't given
                    self.assertFalse(mode.change_single_time(command,command))

    def test_change_both_times(self):

        for _ in range(test_runs):
            for mode in interface_modes:

                ## CORRECT ASSIGNMENT TESTS - See that object member variables change as expected and that valid input returns True

                # Create a command for setting both times to random ints
                start_time = randint(min_rand,max_rand)
                final_time = randint(min_rand,max_rand)
                arg = self.three_command_string(MULTIPLE_TIMES,start_time,final_time)
                # Check that the time-change function returns True when this command is passed to the InterfaceMode obejct
                self.assertTrue(mode.change_both_times(*arg.split()))
                # Check that the member variable has changed to the expected value
                self.assertEqual(mode.time_settings[START_TIME],start_time,mode.time_settings[START_TIME])
                self.assertEqual(mode.time_settings[FINAL_TIME],final_time,mode.time_settings[FINAL_TIME])

                # Create a command for setting both times to random floats
                start_time = uniform(min_rand,max_rand)
                final_time = uniform(min_rand,max_rand)
                arg = self.three_command_string(MULTIPLE_TIMES,start_time,final_time)
                # Check that the time-change function returns True when this command is passed to the InterfaceMode obejct
                self.assertTrue(mode.change_both_times(*arg.split()))
                # Check that the member variable has changed to the expected value
                self.assertEqual(mode.time_settings[START_TIME],start_time,mode.time_settings[START_TIME])
                self.assertEqual(mode.time_settings[FINAL_TIME],final_time,mode.time_settings[FINAL_TIME])

                ## BAD INPUT TESTS - See that input function rejects unusual input (e.g. "times 0 aaaa", "times times times" rather than "times 0 2")

                '''

                # Create a command for 'setting' time to a string - bad input
                arg = self.random_string_command(command)
                # Check that the time-change function returns False when this command is passed to the InterfaceMode obejct
                self.assertFalse(mode.change_single_time(*arg.split()))
                # Check that the time-change function returns False when only one argument is given
                self.assertFalse(mode.change_single_time(command,""))
                # Check that the time-change function returns False when the 'param' is given twice
                self.assertFalse(mode.change_single_time(command,command))
                # Check that the time-change function returns False when the time commands aren't given
                self.assertFalse(mode.change_single_time(command,command))

                '''

    def test_single_trace(self):

        # Create an InterfaceMode object
        single_mode = SingleTrace()
        forsin_mode = ForwardSingle()
        invsin_mode = InverseSingle()

        for _ in range(test_runs):

            for command in float_args:

                # Check that the float commands accept floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),True,arg)

                # Check that the float commands reject strings
                arg = self.random_string_command(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

                # Check that the float commands accept floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                # Check that the float commands reject strings
                arg = self.random_string_command(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            for command in only_int_args:

                # Check that the int only commands reject floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

                # Check that the int only commands reject floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            for command in bool_args:

                # Check that the bool commands accept a 'true' response
                arg = self.valid_yes(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),True,arg)

                # Check that the bool commands accept a 'false' response
                arg = self.valid_no(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),True,arg)

                # Check that the bool commands reject random strings
                arg = self.random_string_command(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

                # Check that the bool commands reject ints
                arg = self.valid_int_single(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

                # Check that the bool commands reject floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

                # Check that the bool commands reject single-letter arguments that aren't y/n
                arg = self.invalid_single_char(command)
                self.assertEqual(single_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_single_parameter(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_single_parameter(*arg.split()),False,arg)

                # Check that the bool commands accept a 'true' response
                arg = self.valid_yes(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                # Check that the bool commands accept a 'false' response
                arg = self.valid_no(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                # Check that the bool commands reject random strings
                arg = self.random_string_command(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

                # Check that the bool commands reject ints
                arg = self.valid_int_single(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

                # Check that the bool commands reject floats
                arg = self.valid_float_single(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

                # Check that the bool commands reject single-letter arguments that aren't y/n
                arg = self.invalid_single_char(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            for command in mult_int_args:

                # Check that the int commands accept ints
                arg = self.valid_int_multiple(command)
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),True,arg)

                # Check that the int commands reject strings
                arg = self.random_string_command(command) + " " + self.random_string_command("")
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),False,arg)

                # Check that the int commands accept ints
                arg = self.valid_int_multiple(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                # Check that the int commands reject strings
                arg = self.random_string_command(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            for command in mult_float_args:

                # Check that the float commands accept floats
                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),True,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),True,arg)

                # Check that the float commands reject strings
                arg = self.random_string_command(command) + " " + self.random_string_command("")
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),False,arg)

                # Check that the float commands accept floats
                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_parameters(arg),True,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),True,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),True,arg)

                # Check that the float commands reject strings
                arg = self.random_string_command(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            for command in mult_only_int_args:

                # Check that the int only commands reject floats
                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(forsin_mode.change_multiple_parameters(*arg.split()),False,arg)
                self.assertEqual(invsin_mode.change_multiple_parameters(*arg.split()),False,arg)

                # Check that the int only commands reject floats
                arg = self.valid_float_multiple(command)
                self.assertEqual(single_mode.change_parameters(arg),False,arg)
                self.assertEqual(forsin_mode.change_parameters(arg),False,arg)
                self.assertEqual(invsin_mode.change_parameters(arg),False,arg)

            for command in time_args:

                # Set the time to a random int with change_single_parameter
                rand_int = randint(min_rand,max_rand)
                arg = self.two_command_string(command,rand_int)
                single_mode.change_single_parameter(*arg.split())
                forsin_mode.change_single_parameter(*arg.split())
                invsin_mode.change_single_parameter(*arg.split())

                # Check that the assignment worked
                self.assertEqual(single_mode.time_settings[command],rand_int,single_mode.time_settings[command])
                self.assertEqual(forsin_mode.time_settings[command],rand_int,forsin_mode.time_settings[command])
                self.assertEqual(invsin_mode.time_settings[command],rand_int,invsin_mode.time_settings[command])

                # Set the time to a random int with change_parameters
                rand_int = randint(min_rand,max_rand)
                arg = self.two_command_string(command,rand_int)
                single_mode.change_parameters(arg)
                forsin_mode.change_parameters(arg)
                invsin_mode.change_parameters(arg)

                # Check that the assignment worked
                self.assertEqual(single_mode.time_settings[command],rand_int,single_mode.time_settings[command])
                self.assertEqual(forsin_mode.time_settings[command],rand_int,forsin_mode.time_settings[command])
                self.assertEqual(invsin_mode.time_settings[command],rand_int,invsin_mode.time_settings[command])

                # Set the time to a random float with change_single_parameter
                rand_float = uniform(min_rand,max_rand)
                arg = self.two_command_string(command,rand_float)
                single_mode.change_single_parameter(*arg.split())
                forsin_mode.change_single_parameter(*arg.split())
                invsin_mode.change_single_parameter(*arg.split())

                # Check that the assignment worked
                self.assertEqual(single_mode.time_settings[command],rand_float,single_mode.time_settings[command])
                self.assertEqual(forsin_mode.time_settings[command],rand_float,forsin_mode.time_settings[command])
                self.assertEqual(invsin_mode.time_settings[command],rand_float,invsin_mode.time_settings[command])

                # Set the time to a random int with change_parameters
                rand_float = uniform(min_rand,max_rand)
                arg = self.two_command_string(command,rand_float)
                single_mode.change_parameters(arg)
                forsin_mode.change_parameters(arg)
                invsin_mode.change_parameters(arg)

                # Check that the assignment worked
                self.assertEqual(single_mode.time_settings[command],rand_float,single_mode.time_settings[command])
                self.assertEqual(forsin_mode.time_settings[command],rand_float,forsin_mode.time_settings[command])
                self.assertEqual(invsin_mode.time_settings[command],rand_float,invsin_mode.time_settings[command])

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

