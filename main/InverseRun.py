import Constants
from subprocess import check_output, call
from subprocess import CalledProcessError
from numpy import empty, copy
from importlib import import_module

class InverseRun:

    def __init__(self, driving_function, results, res_params):

        # Assign the driving function index
        self.driving_function = driving_function

        filename = "InverseLoewner"

        self.fortran_filename = filename + ".F90"

        self.module_name = "modules." + filename + "_"

        # Generate the command for preparing a module with f2py
        self.compile_command = None

        # Obtain the time and resolution parameters
        self.start_time = res_params[0]
        self.final_time = res_params[1]
        self.total_points = res_params[2]

        # Create a results attribute
        self.results = results

    def driving_string(self):

        # Return a string containing the name of the driving function in square
        # brackets
        return "[" + Constants.DRIVING_INFO[self.driving_function] + "] "

    def set_compile_command(self):

        self.compile_command = Constants.F2PY_FIRST \
               + [self.fortran_filename, "-m", \
                  self.module_name]

    def compile_inverse(self):

        # Compile the module with f2py
        try:
            check_output(self.compile_command)
        except CalledProcessError:
            print(self.compile_command)
            print("Error: Could not compile module.")
            exit()

    def import_inverse(self):

        # Try to import the corresponding module
        return import_module(self.module_name)

    def perform_inverse(self):

        try:

            # Check if the module can be imported successfully
            InverseLoewner = self.import_inverse()

        except ModuleNotFoundError:

            self.set_compile_command()
            self.compile_inverse()
            InverseLoewner = self.import_inverse()

        driving_arr = empty(self.total_points, dtype=float)
        time_arr = empty(self.total_points, dtype=float)
        InverseLoewner.inverse_loewner(self.results, driving_arr, time_arr, self.total_points)

        self.driving_arr = driving_arr
        self.time_arr = time_arr
