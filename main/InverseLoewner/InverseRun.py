import Constants
from subprocess import check_output, call
from subprocess import CalledProcessError
from numpy import empty, copy, column_stack, savetxt
from importlib import import_module

class InverseRun:

    def __init__(self, forward_run):

        filename = "InverseLoewner"

        self.fortran_filename = "../" + filename + "/" + filename + ".F90"

        self.module_name = "modules." + filename + "_"

        # Generate the command for preparing a module with f2py
        self.compile_command = None

        self.output_dir = "../Output/Data/Quadratic/Inverse/"

        self.forward_run = forward_run

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

        driving_arr = empty(self.forward_run.outer_points, dtype=float)
        time_arr = empty(self.forward_run.outer_points, dtype=float)
        InverseLoewner.inverseloewner(self.forward_run.results, driving_arr, time_arr, self.forward_run.outer_points)

        self.driving_arr = driving_arr
        self.time_arr = time_arr

    def save_to_dat(self):

        filename = self.output_dir + self.forward_run.generate_properties_string() + Constants.DATA_EXT
        combined = column_stack((self.time_arr,self.driving_arr))
        savetxt(filename, combined, fmt="%.18f")

