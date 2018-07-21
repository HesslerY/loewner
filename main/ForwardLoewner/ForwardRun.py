import Constants
from subprocess import check_output, call
from subprocess import CalledProcessError
from numpy import empty, column_stack, savetxt, complex128
from importlib import import_module

class ForwardRun:

    def __init__(self, driving_function, filename = "ForwardLoewner", constant = 0):

        # Assign the driving function index
        self.driving_function = driving_function

        # Assign the module code
        self.module_code = str(driving_function)

        # Determine the filename of the relevant Fortran file
        self.fortran_filename = "../" + filename + "/" + filename + ".F90"

        # Set a filename for the compiled module
        self.module_name = "modules." + filename + "_"  + self.module_code

        # Generate the command for preparing a module with f2py
        self.compile_command = None

        # Set a value for the case of xi(t) = constant
        self.constantParam = constant

        self.output_dir = "../Output/Data/Quadratic/Forward/"

    def set_compile_command(self):

        # Create a string that is used to compile for fortran file with f2py
        self.compile_command = Constants.F2PY_FIRST + ["-DCASE=" + self.module_code] \
               + [self.fortran_filename, "-m", \
                  self.module_name]

    def compile_loewner(self):

        # Compile the module with f2py
        try:
            check_output(self.compile_command)

        except CalledProcessError:
            
            print(self.compile_command)
            call(["ls","-l"])
            print("Error: Could not compile module.")
            exit()

    def import_loewner(self):

        # Try to import the corresponding module
        return import_module(self.module_name)

    def perform_loewner(self):

        try:

            # Check if the module can be imported successfully
            ForwardLoewner = self.import_loewner()

        except ModuleNotFoundError:

            # Compile and import the module if it does not already exist
            self.set_compile_command()
            self.compile_loewner()
            ForwardLoewner = self.import_loewner()

        # Declare an empty complex array for the results
        self.results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        if self.driving_function == 0:
            ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.results, constantdrivingarg=self.constantParam)
        else:
            ForwardLoewner.quadraticloewner(self.start_time, self.final_time, self.inner_points, self.results)

    def generate_properties_string(self):

        # Place the parameters of the run into a list
        properties = [self.driving_function, self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename
        return "-".join(desc)

    def save_to_csv(self):

        # Create a filename for the CSV file
        filename = self.output_dir + self.generate_properties_string() + Constants.DATA_EXT

        # Create a 2D array from the real and imaginary values of the results
        combined = column_stack((self.results.real,self.results.imag))

        # Convert the 2D array to a file
        savetxt(filename, combined, fmt="%.18f")

class SqrtForwardRun(ForwardRun):

    def __init__(self, driving_function):

        ForwardRun.__init__(self, driving_function)
        self.sqrt_param = None

    def sqrt_param_string(self, param_name, param_val):

        # Generate a string for the kappa or c_alpha conditional compilation option
        return [param_name + str(param_val)]

    def perform_loewner(self):

        try:

            # Check if the module can be imported successfully
            ForwardLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.set_compile_command()
            self.compile_loewner()
            ForwardLoewner = self.import_loewner()

        # Compile and import the module if it does not already exist
        self.results = empty(self.outer_points, dtype=complex128)
        ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.results, sqrtdrivingarg=self.sqrt_param)

    def sqrt_filename_string(self):

        return str(self.sqrt_param)[:3].replace(".","dot")

    def shift(self):

        offset = self.results[0].real

        for i in range(self.outer_points): 
            self.results[i] -= offset

    def generate_properties_string(self):

        properties = [self.driving_function, self.sqrt_filename_string(), self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename
        return "-".join(desc)

    def save_to_csv(self):

        filename = self.output_dir + self.generate_properties_string() + Constants.DATA_EXT

        if self.driving_function == 10:
            self.shift()

        real_vals = self.results.real
        imag_vals = self.results.imag

        combined = column_stack((real_vals,imag_vals))
        savetxt(filename, combined, fmt="%.18f")

class ExactForwardRun(ForwardRun):

    def __init__(self, driving_function):

        ForwardRun.__init__(self, driving_function, "ExactLoewner")
        self.module_name = "modules.ExactLoewner"

    def set_compile_command(self):

        self.compile_command = Constants.F2PY_FIRST \
               + [self.fortran_filename, "-m", \
               self.module_name]

    def perform_loewner(self):

        try:

            # Check that the module can be imported successfully
            ExactLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.set_compile_command()
            self.compile_loewner()
            ExactLoewner = self.import_loewner()

        self.results = empty(self.outer_points, dtype=complex128)

        if self.driving_function == 1:
            ExactLoewner.asymptotic_linear_driving(final_time=self.final_time,outer_n=self.outer_points,g_arr=self.results)
        else:
            # Not yet implemented
            pass

