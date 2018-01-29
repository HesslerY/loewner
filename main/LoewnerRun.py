import Constants
from subprocess import check_output, call
from subprocess import CalledProcessError
from numpy import empty, delete
from importlib import import_module

class LoewnerRun:

    def __init__(self, driving_function, filename = "NumericalLoewner"):

        # Assign the driving function index
        self.driving_function = driving_function

        # Assign the module code
        self.module_code = str(driving_function)

        self.fortran_filename = filename + ".F90"

        self.module_name = "modules." + filename + "_"  + self.module_code

        # Generate the command for preparing a module with f2py
        self.compile_command = None

        # Obtain the time and resolution parameters
        self.start_time = None
        self.final_time = None
        self.total_points = None

        # Create a results attribute
        self.results = None

    def driving_string(self):

        # Return a string containing the name of the driving function in square
        # brackets
        return "[" + Constants.DRIVING_INFO[self.driving_function] + "] "

    def set_compile_command(self):

        self.compile_command = Constants.F2PY_FIRST + ["-DCASE=" + self.module_code] \
               + [self.fortran_filename, "-m", \
                  self.module_name]

    def compile_loewner(self):

        # Compile the module with f2py
        try:
            check_output(self.compile_command)
        except CalledProcessError:
            print(self.compile_command)
            print("Error: Could not compile module.")
            exit()

    def import_loewner(self):

        # Try to import the corresponding module
        return import_module(self.module_name)

    def set_resolution_parameters(self):

        while True:

            # Ask for the run parameters
            values = input(self.driving_string() + "Please enter the star" \
                       + "t time, end time, and number of points seperated b" \
                       + "y a space: ")
            try:

                # Split the input
                values = values.split()

                # Ensure that three values were entered
                if len(values) != 3:
                    continue

                self.start_time = float(values[0])

                # Check that the start time >= 0
                if self.start_time < 0:
                    continue

                self.final_time = float(values[1])

                # Check that final time is greater than the start time
                if self.final_time <= self.start_time:
                    continue

                self.total_points = int(values[2])

                # Check that the number of points is >= 1
                if self.total_points < 1:
                    continue

                return

            except ValueError:
                # Repeat if input had incorrect format
                continue

    def perform_loewner(self):

        try:

            # Check if the module can be imported successfully
            NumericalLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.set_compile_command()
            self.compile_loewner()
            NumericalLoewner = self.import_loewner()

        self.results = empty(self.total_points, dtype=complex)
        print(self.results.shape)
        NumericalLoewner.loewners_equation(self.start_time, self.final_time, self.results)

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

        self.results = empty(self.total_points, dtype=complex)
        NumericalLoewner.loewners_equation(self.start_time, self.final_time, self.results, sqrt_driving=self.sqrt_param)

class ExactLoewnerRun(LoewnerRun):

    def __init__(self, driving_function):

        LoewnerRun.__init__(self, driving_function, "ExactLoewner")
        self.module_name = "modules.ExactLoewner"

    def driving_string(self):

        # Return a string containing the name of the driving function in square
        # brackets
        return "[" + Constants.EXACT_INFO[self.driving_function] + "] "

    def set_compile_command(self):

        self.compile_command = Constants.F2PY_FIRST \
               + [self.fortran_filename, "-m", \
               self.module_name]

    def set_resolution_parameters(self):

        query = ["Please enter the start time and number of intervals seperated by a space: "]

        while True:

            # Ask for the run parameters
            values = input(self.driving_string() + query[self.driving_function])

            try:

                # Split the input
                values = values.split()

                if self.driving_function == 0:

                    # Ensure that three values were entered
                    if len(values) != 2:
                        continue

                    self.start_time = float(values[0])

                    # Check that the start time >= 0
                    if self.start_time < 0:
                        continue

                    self.total_points = int(values[1])

                    # Check that the number of points is >= 1
                    if self.total_points < 1:
                        continue

                    return

                else:
                    # Not yet implemented
                    pass

            except ValueError:
                    # Repeat if input had incorrect format
                    continue

    def perform_loewner(self):

        try:

            # Check that the module can be imported successfully
            ExactLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.set_compile_command()
            self.compile_loewner()
            ExactLoewner = self.import_loewner()

        self.results = empty(self.total_points, dtype=complex)

        if self.driving_function == 1:
            ExactLoewner.asymptotic_linear_driving(final_time=self.final_time,n_points=self.total_points,g_arr=self.results)

        else:
            # Not yet implemented
            pass

    def root_mean_squared_error(self,approx_sol):

        rms_error = 0

        for i in range(self.total_points):
            rms_error += (approx_sol[i] - exact_sol[i]) ** 2

        return sqrt(rms_error / n)
