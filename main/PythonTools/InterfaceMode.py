from Constants import *
from LoewnerRunFactory import LoewnerRunFactory
from numpy import arange, linspace

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
        if param not in self.time_settings:
            return False

        try:
            # Attempt to convert the value to a float
            self.time_settings[param] = float(value)
        except ValueError:
            # Return false if unsuccessful
            return False

        # Return true if input matches intruction to change time parameters
        return True

    def change_both_times(self,param,value1,value2):

        # Check if the times values are being changed
        if param not in MULTIPLE_TIMES:
            return False

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

        # Return true if input matches instruction to change time parameters
        return True

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
        if param not in self.res_settings:
            return False

        try:
            # Attempt to convert the value to an int
            self.res_settings[param]  = int(value)
        except ValueError:
            return False

        # Return true if input matches intruction to change resolution parameters
        return True

    def change_both_resolutions(self,param,value1,value2):

        # Check if the resolution values are being changed
        if param != MULTIPLE_RES:
            return False

        try:
            # Attempt to convert the value to an int
            self.res_settings[OUTER_RES] = int(value1)
            self.res_settings[INNER_RES] = int(value2)
        except ValueError:
            return False

        # Return true if input matches intruction to change resolution parameters
        return True

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
        if param != KAPPA:
            return False

        # Attempt to convert the value to a float
        try:
            self.kappa = float(value)
        except ValueError:
            return False

        # Return true if input matches instruction to change kappa value
        return True

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
        if param != DRIVE_ALPHA:
            return False

        # Attempt to convert the value to a float
        try:
            self.drivealpha = float(value)
        except ValueError:
            return False

        # Return true if input matches instruction to change alpha value
        return True

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
        if param != CONSTANT:
            return False

        # Attempt to convert the value to a float
        try:
            self.constant = float(value)
        except ValueError:
            return False

        # Return true if input matches an instruction to change constant value
        return True

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

        # Return false if input doesn't have correct number of arguments
        return False

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

        # Initialise superclass
        InterfaceMode.__init__(self)

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_single_resolution(param,value) or self.change_saving(param,value) or self.change_compilation(param,value) \
                or self.change_kappa(param,value) or self.change_drive_alpha(param,value) or self.change_constant(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2) or self.change_both_resolutions(param,value1,value2)

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_resolution() and self.validate_saving() and self.validate_compilation() \
                and self.validate_kappa() and self.validate_drive_alpha() and self.validate_constant()

class ForwardSingle(SingleTrace):

    def __init__(self):

        # Initialise superclass
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

        # Initialise superclass
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

        # Initialise superclass
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

class TwoTrace(InterfaceMode):

    def __init__(self):

        # Initialise superclass
        InterfaceMode.__init__(self)

        # Set the constant to one by default for two-trace mode
        self.constant = 1

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
                and self.validate_kappa() and self.validate_drive_alpha()

    def execute(self):

        # Create a list of LoewnerRuns
        runs = self.create_loewner_runs()

        # Carry out the two-trace forward algorithm for each of the chosen driving functions
        for run in runs:
            run.cubic_forward_loewner()

        print("Completed all forward two-trace runs.")

class WedgeAlpha(InterfaceMode):

    def __init__(self):

        # Initialise superclass
        InterfaceMode.__init__(self)

        # Set the constant to one by default for two-trace mode
        self.constant = 1

        # Create a variable for storing the wedge angle
        self.wedgealpha = None

    def change_wedge_alpha(self,param,value):

        # Check if the wedge alpha value is being changed
        if param != WEDGE_ALPHA:
            return False

        try:
            # Attempt to convert the value to a float
            self.wedgealpha = float(value)
        except ValueError:
            # Return false if unsuccessful
            return False

        # Return true if the command matches an instruction to change the wedgealpha value
        return True

    def validate_wedge_alpha(self):

        # Check that the wedge alpha value has been set
        if self.wedgealpha is None:
            self.error = "Validation Error: Wedge angle hasn't been set."
            return False

        # Check that the wedge alpha value is greather than zero
        if self.wedgealpha <= 0:
            self.error = "Validation Error: Wedge angle is less than or equal to zero."
            return False

        # Return true if all checks are passed
        return True

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
        if not all([val in NOTORIGIN_IDXS for val in driving_functions]):
            return False

        # Create a set from the list of driving functions
        self.driving_list = set(driving_functions)

        # Check that there are no repeated driving functions
        if len(self.driving_list) != len(driving_functions):
            self.driving_list = None
            return False

        # Return true if all checks are passed
        return True

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_single_resolution(param,value) or self.change_saving(param,value) \
                or self.change_wedge_alpha(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2) or self.change_both_resolutions(param,value1,value2)

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_resolution() and self.validate_saving() \
                and self.validate_wedge_alpha()

    def execute(self):

        # Create a list of LoewnerRuns
        runs = self.create_loewner_runs()

        # Carry out the wedge algorithm for each of the chosen driving functions
        for run in runs:
            run.wedge_growth(self.wedgealpha)

class ExactLinear(InterfaceMode):

    def __init__(self):

        # Initialise superclass
        InterfaceMode.__init__(self)

        # Create variables to control if the implicit or explicit algorithm is used
        self.equation_type = {
                                LINR_EX : None,
                                LINR_IM : None,
                              }

        # Create variables to control phi values
        self.phi = {
                     START_PHI : None,
                     FINAL_PHI : None,
                    }

        # Create a driving list containing only the index for linear driving
        self.driving_list = [LINR_IDX]

    def change_phi(self,param,value):

        # Check that the parameter matches an intruction to change the phi values
        if param not in self.phi.keys():
            return False

        # Attempt to to convert the value to a float
        try:
            self.phi[param] = float(value)
        except ValueError:
            return False

        # Return true if the float conversion was successful
        return True

    def validate_phi(self):

        # Check if the explicit equation is being used
        if not self.equation_type[LINR_EX]:
            return True

        # Check that the phi values have been set
        if any([val is None for val in self.phi.values()]):
            self.error = "Validation Error: Phi valies haven't been set."
            return False

        # Check that start phi is greater than or equal to zero
        if self.phi[START_PHI] < 0:
            self.error = "Validation Error: Start phi is less than zero."
            return False

        # Check that final phi is less than pi
        if self.phi[FINAL_PHI] > pi:
            self.error = "Validation Error: Final phi is greater than pi."
            return False

        # Return True if all checks are passed
        return True

    def change_equation_type(self,param,value):

        # See if the second argument matches a True/False response
        if value not in self.convert_bool.keys():
            return False

        # Check that the parameter matches an instruction to change the equation settings
        if param not in self.equation_type.keys():
            return False

        # Set the corresponding equation type to true
        self.equation_type[param] = self.convert_bool[value]

        # Return true when parameter change is successful
        return True

    def validate_equation_type(self):

        # Create a list from the equation type values
        eq_type_values = self.equation_type.values()

        # Check that the equation types have been set
        if any([val is None for val in eq_type_values]):
            self.error = "Validation Error: Function type hasn't been set. Need to chose implicit and/or explicit exact solution."
            return False

        # Check that one or both of the equation type parameters has been set to True
        if not any(eq_type_values):
            self.error = "Validation Error: Both equation types have been set to False. At least one must be True."
            return False

        # Return True if all checks have been passed
        return True

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_outer_resolution(param,value) or self.change_saving(param,value) \
                or self.change_phi(param,value) or self.change_equation_type(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2)

    def validate_time(self):

        # Check if only the explicit equation is being used
        if not self.equation_type[LINR_IM]:
            return True

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

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_outer_resolution() and self.validate_saving() \
                and self.validate_phi() and self.validate_equation_type()

    def execute(self):

        # Set the time values to integers if only the explicit solution is used (prevents initialisation problem for LoewnerRun)
        if self.time_settings[START_TIME] is None:
            self.time_settings[START_TIME] = 0
        if self.time_settings[FINAL_TIME] is None:
            self.time_settings[FINAL_TIME] = 0

        # Create a single LoewnerRun
        run = self.create_loewner_runs()[0]

        # Find the explicit and/or implicit solutions
        if self.equation_type[LINR_IM]:
            run.exact_quadratic_forward_loewner()

        if self.equation_type[LINR_EX]:
            run.phi_quadratic_exact(self.phi[START_PHI],self.phi[FINAL_PHI])

        print("Completed linear single-trace exact solution runs.")

class ExactConstant(InterfaceMode):

    def __init__(self):

        # Initailise superclass
        InterfaceMode.__init__(self)

        # Create a driving list containing only the index for constant driving
        self.driving_list = [CONST_IDX]

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_outer_resolution(param,value) or self.change_saving(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2)

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_outer_resolution() and self.validate_saving()

    def execute(self):

        # Obtain a single LoewnerRun object for constant driving
        run = self.create_loewner_runs()[0]

        # Carry out the exact solution
        run.exact_cubic_forward_loewner()

        print("Completed constant two-trace exact solution run.")

class ExactSquareRoot(InterfaceMode):

    def __init__(self):

        # Initailise superclass
        InterfaceMode.__init__(self)

        # Create a driving list containing only the index for xi(t) = sqrt(1 + t) driving
        self.driving_list = [SQRTPLUS_IDX]

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_outer_resolution(param,value) or self.change_saving(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2)

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_outer_resolution() and self.validate_saving()

    def execute(self):

        # Obtain a single LoewnerRun object for constant driving
        run = self.create_loewner_runs()[0]

        # Carry out the exact solution
        run.exact_cubic_forward_loewner()

        print("Completed sqrt(1 + t) two-trace exact solution run.")

class KappaAlpha(InterfaceMode):

    def __init__(self,varname):

        # Initialise superclass
        InterfaceMode.__init__(self)

        # Set variable name
        self.varname = varname

        # Create a dictionary of argument-function pairs for creating kappa/calpha array
        self.input_type = {
                            NUM_SQRT_RUNS : linspace,
                            SQRT_STEP : arange,
                          }

        # Create a variable for storing the array of kappa/calpha values
        self.sqrt_arr = None

    def sqrt_param_interval(self,param,values):

        # Check that a list of kappa/calpha values is being entered
        if param != self.varname + LIST_ENTRY:
            return False

        # Check that the next argument indicated that the start kappa/calpha value is being given
        if values[0] != FIRST_VALUE:
            return False

        try:
            # Attempt to convert the value to a float
            start_val = float(values[1])
        except ValueError:
            # Return false if unsuccessful
            return False

        # Check that the next argument indicated that the start kappa/calpha value is being given
        if values[2] != LAST_VALUE:
            return False

        try:
            # Attempt to convert the value to a float
            final_val = float(values[3])
        except ValueError:
            # Return false if unsuccessful
            return False

        # See if the next argument matches an instruction to create an array of kappa/calpha values
        if values[4] not in self.input_type.keys():
            return False

        if values[4] == NUM_SQRT_RUNS:

            try:
                # Attempt to convert the value to an int
                third_arg = int(values[5])
            except ValueError:
                # Return False if unsuccessful
                return False

            if third_arg <= 2:
                return False

        if values[4] == SQRT_STEP:

            try:
                # Attempt to convert the value to an int
                third_arg = float(values[5])
            except ValueError:
                # Return False if unsuccessful
                return False

            if third_arg >= final_val - start_val:
                return False

        if not self.validate_range(start_val,final_val):
            return False

        # Use the inputs to create a list of kappa/calpha values
        self.sqrt_arr = self.input_type[values[4]](start_val,final_val,third_arg)

        # Return true if input matches intruction to change kappa/calpha parameters
        return True

    def validate_range(self,start_val,final_val):
        pass

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_resolution() and self.validate_saving() and self.validate_compilation() and self.validate_sqrt_array()

    def change_single_parameter(self,param,value):

        # See if the inputs match with an instruction to change a single parameters
        return self.change_single_time(param,value) or self.change_single_resolution(param,value) or self.change_saving(param,value) or self.change_compilation(param,value)

    def change_multiple_parameters(self,param,value1,value2):

        # See if the inputs match with an instruction to change multiple parameters
        return self.change_both_times(param,value1,value2) or self.change_both_resolutions(param,value1,value2)

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

        # Check if the input array has seven elements
        if len(inputs) == 7:

            # Attempt to create an araay of kappa/calpha values
            return self.sqrt_param_interval(inputs[0],inputs[1:])

        # Return false if input doesn't have correct number of arguments
        return False

    def create_kappa_runs(self):

        # Create the LoewnerRunFactory object with the user-given parameters
        self.loewner_fact = LoewnerRunFactory(self.time_settings[START_TIME],self.time_settings[FINAL_TIME],self.res_settings[OUTER_RES],self.res_settings[INNER_RES],self.compile,self.save_settings[SAVE_DATA],self.save_settings[SAVE_PLOTS])

        # Create a list of LoewnerRuns with the LoewnerRunFactory
        return self.loewner_fact.vary_kappa(self.sqrt_arr)

    def create_calpha_runs(self):

        # Create the LoewnerRunFactory object with the user-given parameters
        self.loewner_fact = LoewnerRunFactory(self.time_settings[START_TIME],self.time_settings[FINAL_TIME],self.res_settings[OUTER_RES],self.res_settings[INNER_RES],self.compile,self.save_settings[SAVE_DATA],self.save_settings[SAVE_PLOTS])

        # Create a list of LoewnerRuns with the LoewnerRunFactory
        return self.loewner_fact.vary_alpha(self.sqrt_arr)

    def validate_kappa_range(self,start_val,final_val):

        # Check that the range of kappa values starts with a value >= 0
        if start_val < 0:
            return False

        # Check that the final value is greater than the starting value
        if final_val <= start_val:
            return False

        # Return True when all conditions are satisifed
        return True

    def validate_sqrt_array(self):

        # Check that the array has been set
        if self.sqrt_arr is None:
            self.error = "Validation Error: Array of kappa/alpha values hasn't been set."
            return False

        # Return True if the array is valid
        return True

    def validate_calpha_range(self,start_val,final_val):

        # Check that the range of kappa values starts with a value greater than zero
        if start_val <= 0:
            return False

        # Check that the final value is greater than the starting value
        if final_val <= start_val:
            return False

        # Check that the final value is less than one
        if final_val >= 1:
            return False

        # Return True when all conditions are satisifed
        return True

class ForSinKappa(KappaAlpha):

    def __init__(self):

        # Initialise superclass
        KappaAlpha.__init__(self,KAPPA)

        # Set the validate_range function to check for appropriate kappa values
        self.validate_range = self.validate_kappa_range

    def execute(self):

        # Create a list of kappa runs for the different kappa values
        kappa_runs = self.create_kappa_runs()

        # Execute the forward single-trace algorithm for the different kappa valiues
        for run in kappa_runs:
            run.quadratic_forward_loewner()
