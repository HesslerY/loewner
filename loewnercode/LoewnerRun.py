import Constants
from subprocess import call
from numpy import empty
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
        self.resolution_parameters = None

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
        call(self.compile_command)
        
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
    
                start_time = float(values[0])
    
                # Check that the start time >= 0
                if start_time < 0:
                    continue
   
                final_time = float(values[1])

                # Check that final time is greater than the start time
                if final_time <= start_time:
                    continue
   
                total_points = int(values[2])

                # Check that the number of points is >= 1
                if total_points < 1:
                    continue
    
                # Create the execution command
                self.resolution_parameters = [start_time, final_time, total_points]
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

class ExactLoewnerRun(LoewnerRun):

    def __init__(self, driving_function):

        LoewnerRun.__init__(self, driving_function, "ExactLoewner")
        
    def driving_string(self):

        # Return a string containing the name of the driving function in square 
        # brackets
        return "[" + Constants.EXACT_INFO[self.driving_function][0] + "] "
    
    def set_compile_command(self):
    
        self.compile_command = Constants.F2PY_FIRST \
               + [self.fortran_filename, "-m", "modules." \
               + self.module_name] 
