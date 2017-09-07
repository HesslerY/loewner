import Constants
from subprocess import call
from numpy import empty
from importlib import import_module

class LoewnerRun:

    def __init__(self, driving_function):

        # Assign the driving function index
        self.driving_function = driving_function

        # Assign the module code
        self.module_code = str(driving_function)

        # Generate the command for preparing a module with f2py
        self.compile_command = self.set_compile_command() 

        # Obtain the time and resolution parameters
        self.resolution_parameters = None

        # Create a results attribute
        self.results = None

    def driving_string(self):

        # Return a string containing the name of the driving function in square 
        # brackets
        return "[" + Constants.DRIVING_INFO[self.driving_function][0] + "] "

    def case_string(self):

        # Generate a string for the CASE conditional compilation option
        return ["-DCASE=" + self.module_code]

    def generate_f2p_last(self):

        # Create the string that defines the module name
        return ["modules.NumericalLoewner_" + self.module_code]

    def set_compile_command(self):
    
        return Constants.F2PY_FIRST + self.case_string() \
               + ["NumericalLoewner.F90", "-m", "modules.NumericalLoewner_" \
               + self.module_code] 

    def compile_loewner(self):

        # Compile the module with f2py
        call(self.compile_command)
        
    def import_loewner(self):

        # Try to import the corresponding module
        return import_module("modules.NumericalLoewner_" + self.module_code)

    def perform_loewner(self):

        try:

            # Check if the module can be imported successfully
            NumericalLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.set_compile_command()
            self.compile_loewner()
            NumericalLoewner = self.import_loewner()
      
        g_arr = empty(self.resolution_parameters[2], dtype=complex)
        NumericalLoewner.loewners_equation(self.resolution_parameters[0], self.resolution_parameters[1], g_arr)

        self.results = g_arr

class SqrtLoewnerRun(LoewnerRun):

    def __init__(self, driving_function):

        LoewnerRun.__init__(self, driving_function)
        self.sqrt_param = None
        
    def sqrt_param_string(self, param_name, param_val):

        # Generate a string for the kappa or c_alpha conditional compilation option
        return [param_name + str(param_val)]
 
    def perform_loewner(self):

        try:

            # Check if the module can be imported successfully
            NumericalLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.set_compile_command()
            self.compile_loewner()
            NumericalLoewner = self.import_loewner()
      
        g_arr = empty(self.resolution_parameters[2], dtype=complex)
        NumericalLoewner.loewners_equation(self.resolution_parameters[0], self.resolution_parameters[1], g_arr, sqrt_driving=self.sqrt_param)

        self.results = g_arr

