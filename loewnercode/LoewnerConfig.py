import Constants
from Plot import Plot
from subprocess import call
from numpy import f2py

class LoewnerConfig:

    def __init__(self, driving_function, exact_mode):

        # Assign the driving function index
        self.driving_function = driving_function

        # Assign the exact solutions mode parameter
        self.exact_mode = exact_mode

        # Set squareroot parameter to None
        self.sqrt_param = None

        if exact_mode:
            self.compile_command = Constants.f2py_first + Constands.f2py_second + ["NumericalLoewner"]

        else:
            # Assign the corresponding compilation command
            self.compile_command = Constants.f2py_first + self.generate_compile_command() + Constants.f2py_second + self.generate_f2p_last()

        # Determine the execute command
        self.execute_command = self.obtain_execute_command()

    def driving_string(self):

        # Return a string containing the name of the driving function in square brackets
        return "[" + Constants.DRIVING_INFO[self.driving_function][0] + "] "

    def case_string(self):

        # Generate a string for the CASE conditional compilation option
        return ["-DCASE=" + str(self.driving_function)]

    def sqrt_param_string(self, param_name, param_val):

        # Generate a string for the KAPPA/C_ALPHA conditional compilation option
        return [param_name + str(param_val)]

    def generate_compile_command(self):

        # Compile string for a driving function that does not require any additional parameters
        if self.driving_function not in [Constants.KAPPA_IDX, Constants.C_ALPHA_IDX]:
            self.create_module_code()
            return self.case_string()

        # Compile string for kappa driving function
        elif self.driving_function == Constants.KAPPA_IDX:
            self.sqrt_param = self.obtain_sqrt_parameter("Please enter the desired kappa value: ")
            self.create_module_code()
            return self.case_string() + self.sqrt_param_string("-DKAPPA=", self.sqrt_param)

        # Compile string for c_alpha driving function
        elif self.driving_func_index == Constants.C_ALPHA_IDX:
            self.sqrt_param = self.obtain_sqrt_parameter("Please enter the desired c_alpha value: ")
            self.create_module_code()
            return self.case_string() + self.sqrt_param_string("-DC_ALPHA=", self.sqrt_param)

        else:
            # Error
            pass

    def create_module_code(self):

        # Set the module code to the driving function index
        self.module_code = str(self.driving_function)

    def generate_f2p_last(self):

        # Create the string that defines the module name
        return ["modules.NumericalLoewner_" + self.module_code]

    def obtain_sqrt_parameter(self, query):

        while True:

            # Ask for the square root parameter
            sqrt_parameter = input(query)

            try:

                # Return if parameter is positive
                if float(sqrt_parameter) > 0:
                    return sqrt_parameter

            except ValueError:
                # Repeat if input could not be converted to float
                continue

    def obtain_execute_command(self):

        while True:

            # Ask for the run parameters
            values = input(self.driving_string() + "Please enter the start time, end time, and number of points seperated by a space: ")

            try:

                # Split the input
                values = values.split()

                # Ensure that three values were entered
                if len(values) != 3:
                    continue

                start_time = float(values[0])

                # Check that the start time >= 0
                if start_time < 0:
                    continue

                # Check that final time is greater than the start time
                if float(values[1]) <= start_time:
                    continue

                # Check that the number of points is >= 1
                if int(values[2]) < 1:
                    continue

                # Create the execution command
                self.run_params = [start_time, float(values[1]), int(values[2])]
                return

            except ValueError:
                # Repeat if input had incorrect format
                continue

    def compile_loewner(self):

        # Compile the module with f2py
        call(self.compile_command)
