from Constants import *
from LoewnerRunFactory import LoewnerRunFactory

class InterfaceMode:

    def __init__(self):

        # Create settings of the LoewnerRunFactory
        self.time_settings =    {
                                    START_TIME : None,
                                    FINAL_TIME : None,
                                }

        self.res_settings =     {
                                    OUTER_RES : None,
                                    INNER_RES : None,
                                }


        self.save_settings =    {
                                    SAVE_PLOTS : None,
                                    SAVE_DATA : None,
                                }


        self.compile = None

        # Create a dictionary to match user-input to boolean values
        self.convert_bool = {
                                USER_TRUE : True,
                                USER_FALSE : False,
                            }

        # Create a list of driving functions that will be used during the run
        self.driving_list = set()


        # Declare extra arguments for the 'special' drving functions
        self.drivealpha = None
        self.kappa = None
        self.constant = None

        # Create a variable for the LoewnerRunFactory
        self.loewner_fact = None

        # Create a variable for storing error messages in the case of bad paramters
        self.error = None

    def show_error(self,user_input):

        # Check if the error message exists
        if self.error is None:
            return False

        # Check if the command matches the intruction to print an error message
        if user_input == DISP_ERROR:
            print(self.error)
            return True

        # Return false if the command did not match the instruction to print an error message
        return False

    def change_single_time(self,param,value):

        # Check if the time values are being changed
        if param in self.time_settings:

            try:
                # Attempt to convert the value to a float
                temp = float(value)
            except ValueError:
                # Return false if unsuccessful
                return False

            # Change the start time value
            if param == START_TIME:
                self.time_settings[START_TIME] = temp
                return True

            # Change the final time valie
            if param == FINAL_TIME:
                self.time_settings[FINAL_TIME] = temp
                return True

        # Return false if input doesn't match intruction to change time parameters
        return False

    def change_both_times(self,param,value1,value2):

        # Check if the times values are being changed
        if param == MULTIPLE_TIMES:

            try:
                # Attempt to convert the values to floats
                temp1 = float(value1)
                temp2 = float(value2)
            except ValueError:
                # Return false if unsuccessful
                return False

            # Change the start and final time values
            self.time_settings[START_TIME] = temp1
            self.time_settings[FINAL_TIME] = temp2
            return True

        # Return false if input doesn't match instruction to change time parameters
        return False

    def validate_time(self):

        # Create an array of time values
        time_values = self.time_settings.values()

        # Check that all the times values have been set
        if any([val is None for val in time_values]):
            self.error = "Validation error: Not all the time values have been set."
            return False

        # Check that the time values are non-negative
        if any([val < 0 for val in time_values]):
            self.error = "Validation error: One or both time values are negative."
            return False

        # Check that the final time is greater than the start time
        if self.time_settings[FINAL_TIME] <= self.time_settings[START_TIME]:
            self.error = "Validation error: Final time is equal to or smaller than start time."
            return False

        # Return true if all checks are passed
        return True

    def change_single_resolution(self,param,value):

        # Check if the resolution values are being changed
        if param in self.res_settings:

            try:
                # Attempt to convert the value to an int
                temp = int(value)
            except ValueError:
                return False

            # Change the outer resolution value
            if param == OUTER_RES:
                self.res_settings[OUTER_RES] = temp
                return True

            # Change the inner resolution value
            if param == INNER_RES:
                self.res_settings[INNER_RES] = temp
                return True

        # Return false if input doesn't match intruction to change resolution parameters
        return False

    def change_both_resolutions(self,param,value1,value2):

        # Check if the resolution values are being changed
        if param == MULTIPLE_RES:

            try:
                # Attempt to convert the value to an int
                temp1 = int(value1)
                temp2 = int(value2)
            except ValueError:
                return False

            # Change the resolution values
            self.res_settings[OUTER_RES] = temp1
            self.res_settings[INNER_RES] = temp2
            return True

        # Return false if input doesn't match intruction to change resolution parameters
        return False

    def change_outer_resolution(self,param,value):

        # See if the string matches the instruction to change just the outer resolution
        if param != OUTER_RES:
            return False

        # Attempt to convert the value to an integer
        try:
            self.res_settings[OUTER_RES] = int(value)
        except ValueError:
            return False

        # Return true if the conversion was successful
        return True

    def validate_resolution(self):

        # Create an array of resolution values
        res_values = self.res_settings.values()

        # Check that both the resolution values have been set
        if any([val is None for val in res_values]):
            self.error = "Validation error: Not all the resolution values have been set."
            return False

        # Check that the resolution values are greater than zero
        if any([val < 1 for val in res_values]):
            self.error = "Validation error: One or both resolution values are less than one."
            return False

        # Return true if all checks are passed
        return True

    def validate_outer_resolution(self):

        # Check that the resolution value has been set
        if self.res_settings[OUTER_RES] is None:
            self.error = "Validation error: Resolution value hasn't been set."
            return False

        # Check that the resolution value has an approrpiate value
        if self.res_settings[OUTER_RES] <= 0:
            self.error = "Validation error: Resolution value is less than one."
            return False

        # Return true if all checks are passed
        return True

    def change_saving(self,param,value):

        # See if the second argument matches a True/False response
        if value not in self.convert_bool.keys():
            return False

        # See if the first argument matches the save plots/data response
        if param in self.save_settings.keys():
            self.save_settings[param] = self.convert_bool[value]
            return True

        # Return false if input doesn't match intruction to change saving parameters
        return False

    def validate_saving(self):

        # Create an array of resolution values
        save_values = self.save_settings.values()

        # Check that both the save values have been set
        if any([val is None for val in save_values]):
            self.error = "Validation error: Not all saving values have been set."
            return False

        # Check that at least one of the save values is True
        if not any(save_values):
            self.error = "Validation error: Both save parameters are false. At least one must be set to true or the output will be lost."
            return False

        # Return true if all checks are passed
        return True

    def change_compilation(self,param,value):

        # See if the second argument matches a True/False response
        if value not in self.convert_bool.keys():
            return False

        # See if the first argument matches the compile response
        if param == COMPILE:
            self.compile = self.convert_bool[value]
            return True

        # Return false if input doesn't match instruction to compile or not compile the modules
        return False

    def validate_compilation(self):

        # Check that the compile value has been set
        if self.compile is None:
            self.error = "Validation Error: Compilation parameter hasn't been set."
            return False

        # Return true if all checks are passed
        return True

    def change_kappa(self,param,value):

        # Check if the kappa value is being changed
        if param == KAPPA:

            # Attempt to convert the value to a float
            try:
                self.kappa = float(value)
            except ValueError:
                return False

        # Return false if input doesn't match instruction to change kappa value
        return False

    def validate_kappa(self):

        # Return true if kappa-driving isn't in the driving list
        if KAPPA_IDX not in self.driving_list:
            return True

        if self.kappa is None:
            self.error = "Validation Error: Kappa value hasn't been set."
            return False

        # Check that kappa value is greater than zero
        if self.kappa <= 0:
            self.error = "Validation Error: Kappa has non-positive value."
            return False

        # Return true if all checks are passed
        return True

    def change_drive_alpha(self,param,value):

        # Check if the alpha value (for c-alpha driving) is being changed
        if param == DRIVE_ALPHA:

            # Attempt to convert the value to a float
            try:
                self.drivealpha = float(value)
            except ValueError:
                return False

        # Return false if input doesn't match instruction to change alpha value
        return False

    def validate_drive_alpha(self):

        # Return true if calpha-driving isn't in the driving list
        if CALPHA_IDX not in self.driving_list:
            return True

        if self.drivealpha is None:
            self.error = "Validation Error: Alpha value hasn't been set."
            return False

        # Check that alpha value is greater than zero
        if self.drivealpha <= 0:
            self.error = "Validation Error: Alpha has non-positive value."
            return False

        # Check that alpha value is less than one
        if self.drivealpha >= 1:
            self.error = "Validation Error: Alpha is greater than or equal to one."
            return False

        # Return true if all checks are passed
        return True

    def change_constant(self,param,value):

        # Check if the constant value is being changed
        if param == CONSTANT:

            # Attempt to convert the value to a float
            try:
                self.constant = float(value)
            except ValueError:
                return False

        # Return false if input doesn't match an instruction to change constant value
        return False

    def validate_constant(self):

        # Return true if constant-driving isn't in the driving list
        if CONST_IDX not in self.driving_list:
            return True

        # Check that the constant value has been set
        if self.constant is None:
            self.error = "Validation Error: Constant value hasn't been set."
            return False

        # Return true if all checks are passed
        return True

    def change_single_parameter(self,param,value):
        # Implemented in subclasses
        pass

    def change_multiple_parameters(self,param,value1,value2):
        # Implemented in subclasses
        pass

    def change_parameters(self,user_input):

        # Split the user input by a space
        inputs = user_input.split()

        # Check if the input array has two elements
        if len(inputs) == 2:

            # Attempt to change a single parameter
            return self.change_single_parameter(*inputs)

        # Check if the input array has three elements
        if len(inputs) == 3:

            # Attempt to change multiple parameters
            return self.change_multiple_parameters(*inputs)

        return False

    def change_driving_functions(self,user_input):
        # Implemented in subclasses
        pass

    def validate_driving_list(self):
        # Implemented in subclasses
        pass

    def validate_settings(self):
        # Implemented in subclasses
        pass

    def create_loewner_runs(self):

        # Create the LoewnerRunFactory object with the user-given parameters
        self.loewner_fact = LoewnerRunFactory(self.time_settings[START_TIME],self.time_settings[FINAL_TIME],self.res_settings[OUTER_RES],self.res_settings[INNER_RES],self.compile,self.save_settings[SAVE_DATA],self.save_settings[SAVE_PLOTS])

        # Set the 'extra' parameters of the LoewnerRunFactory
        self.loewner_fact.alpha = self.drivealpha
        self.loewner_fact.kappa = self.kappa
        self.loewner_fact.constant = self.constant

        # Create a list of LoewnerRuns with the LoewnerRunFactory
        return [self.loewner_fact.select_single_run(index=i) for i in self.driving_list]

    def execute(self):
        # Implemented in subclasses
        pass

class SingleTrace(InterfaceMode):

    def __init__(self):
        InterfaceMode.__init__(self)

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_single_resolution(param,value) or self.change_saving(param,value) or self.change_compilation(param,value) \
                or self.change_kappa(param,value) or self.change_drive_alpha(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2) or self.change_both_resolutions(param,value1,value2)

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_resolution() and self.validate_saving() and self.validate_compilation() \
                and self.validate_kappa() and self.validate_drive_alpha() and self.validate_constant()

    def change_driving_functions(self,user_input):

        # Split the user input by a space
        inputs = user_input.split()

        # Check that the first argument is the instruction for creating a driving-function list
        if inputs[0] != CREATE_DRIVING_LIST:
            return False

        # Attempt to convert the inputs to integers
        try:
            driving_functions = [int(x) for x in inputs[1:]]
        except ValueError:
            return False

        # Check that the driving functions are in the correct range
        if any([val < 0 or val > TOTAL_DRIVING_FUNCTIONS for val in driving_functions]):
            return False

        # Create a set from the list of driving functions
        self.driving_list = set(driving_functions)

        # Check that there are no repeated driving functions
        if len(self.driving_list) != len(driving_functions):
            self.driving_list = None
            return False

        # Return true if all checks are passed
        return True

class ForwardSingle(SingleTrace):

    def __init__(self):
        SingleTrace.__init__(self)

    def execute(self):

        # Create a list of LoewnerRuns
        runs = self.create_loewner_runs()

        # Carry out the single-trace forward algorithm for each of the chosen driving functions
        for run in runs:
            run.quadratic_forward_loewner()

        print("Completed all forward single-trace runs.")

class InverseSingle(SingleTrace):

    def __init__(self):
        SingleTrace.__init__(self)

    def execute(self):

        # Create a list of LoewnerRuns
        runs = self.create_loewner_runs()

        # Carry out the single-trace forward and inverse algorithms for each of the chosen driving functions
        for run in runs:
            run.quadratic_forward_loewner()
            run.quadratic_inverse_loewner()

        print("Completed all inverse single-trace runs.")

class ExactInverse(SingleTrace):

    def __init__(self):
        SingleTrace.__init__(self)

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_outer_resolution(param,value) or self.change_saving(param,value) \
                or self.change_kappa(param,value) or self.change_drive_alpha(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2)

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_outer_resolution() and self.validate_saving() \
                and self.validate_kappa() and self.validate_drive_alpha() and self.validate_constant()

    def execute(self):

        # Create a list of LoewnerRuns
        runs = self.create_loewner_runs()

        # Carry out the exact inverse algorithms for each of the chosen driving functions
        for run in runs:
            run.exact_inverse()

        print("Completed all exact inverse runs.")

