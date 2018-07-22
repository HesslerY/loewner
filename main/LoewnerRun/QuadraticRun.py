import Constants
from subprocess import check_output, call, CalledProcessError
from numpy import empty, column_stack, savetxt, complex128
from importlib import import_module

class QuadraticRun:

    def __init__(self, driving_function):

        # Assign the driving function index
        self.driving_function = driving_function

        # Assign the module code
        self.module_code = str(driving_function)

        # Determine the filename of the relevant Fortran file
        self.forward_filename = "../" + Constants.FOR_LOEWNER + "/" + Constants.FOR_LOEWNER + Constants.FORTRAN_EXT
        self.inverse_filename = "../" + Constants.INV_LOEWNER + "/" + Constants.INV_LOEWNER + Constants.FORTRAN_EXT

        # Set a filename for the compiled module
        self.forward_module_name = "modules." + Constants.FOR_LOEWNER + "_"  + self.module_code
        self.inverse_module_name = "modules." + Constants.INV_LOEWNER + "_"  + self.module_code

        # Set the output directory for the data files - Constant?
        self.forward_output_data = "../Output/Data/Quadratic/Forward/"
        self.inverse_output_data = "../Output/Data/Quadratic/Inverse/"

        # Set the parameter name in the case of square-root driving
        if driving_function == Constants.KAPPA_IDX: 
            self.param_name = "kappa"

        if driving_function == Constants.C_ALPHA_IDX: 
            self.param_name = "calpha"

    def sqrt_filename_string(self):

        return str(self.sqrt_param)[:3].replace(".","point")

    def shift(self):

        offset = self.forward_results[0].real

        for i in range(self.outer_points): 
            self.forward_results[i] -= offset

    def generate_properties_string(self):

        # Place the parameters of the run into a list

        if self.driving_function not in [Constants.KAPPA_IDX, Constants.C_ALPHA_IDX]:
            properties = [self.driving_function, self.start_time, self.final_time, self.outer_points, self.inner_points]
        else:
            properties = [self.driving_function, self.sqrt_filename_string(), self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename
        return "-".join(desc)

    def set_compile_commands(self):

        # Create a string that is used to compile the forward fortran file with f2py
        self.compile_forward = Constants.F2PY_FIRST + ["-DCASE=" + self.module_code] \
               + [self.forward_filename, "-m", \
                  self.forward_module_name]

        # Create a string that is used to compile the inverse fortran file with f2py
        self.compile_inverse = Constants.F2PY_FIRST \
               + [self.inverse_filename, "-m", \
                  self.module_name]

    def compile_module(self, algorithm):

        if algorithm == "Forward":
            command == self.compile_forward

        if algorithm == "Inverse":
            comand = self.compile_inverse

        try:
            check_output(command)

        except CalledProcessError:
            
            print(command)
            call(["ls","-l"])
            print("Error: Could not compile module.")
            exit()

    def import_loewner(self, algorithm):

        if algorithm == "Forward":
            return import_module(self.forward_module_name)
        
        if algorithm == "Inverse":
            return import_module(self.inverse_module_name)

    def perform_forward_loewner(self):

        ForwardLoewner = self.import_loewner("Forward")

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        if self.driving_function == 0:
            ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.forward_results, constantdrivingarg=self.constantParam)

        else if not Constants.squareroot_driving(self.driving_function):
            ForwardLoewner.quadraticloewner(self.start_time, self.final_time, self.inner_points, self.forward_results)
        
        else: 
            ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.forward_results, sqrtantdrivingarg=self.sqrt_param)

    def perform_inverse_loewner(self):

        # Check if the module can be imported successfully
        InverseLoewner = self.import_loewner("Inverse")

        # Declare an empty complex array for the results
        self.inverse_results = empty(self.outer_points, dtype=complex128)

        self.driving_arr = empty(self.forward_run.outer_points, dtype=float)
        self.time_arr = empty(self.forward_run.outer_points, dtype=float)

        InverseLoewner.inverseloewner(self.forward_results, self.driving_arr, self.time_arr, self.outer_points)

    def prepare_file(self, algorithm):

        if algorithm == "Forward":
            return column_stack((self.forward_results.real,self.forward_results.imag))

        if algorithm == "Inverse":
            return column_stack((self.time_arr,self.driving_arr))

    def array_to_file(self, array, filename):

        savetxt(filename, array, fmt=Constants.DAT_PREC)

    def forward_save_to_dat(self):

        # Create a filename for the dat file
        filename = self.forward_output_dir + self.generate_properties_string() + Constants.DATA_EXT

        # Shift the real values for the case of kappa-driving
        if self.driving_function == 10:
            self.shift()

        # Create a 2D array from the real and imaginary values of the results
        self.array_to_file(self.prepare_file("Forward"), filename)

    def inverse_save_to_dat(self):

        # Create a filename for the dat file
        filename = self.inverse_output_dir + self.generate_properties_string() + Constants.DATA_EXT

        # Create a 2D array from the real and imaginary values of the results
        self.aray_to_file(self.prepare_file("Inverse"), filename)

    def forward_run(self):

class CubicRun(ForwardRun):

    def __init__(self, driving_function):

        ForwardRun.__init__(self, driving_function, "ForwardLoewner")
        self.module_name = "modules.ForwardLoewner"
        
        # Set the output directory for the data files
        self.output_dir = "../Output/Data/Cubic/Forward/"

    def perform_loewner(self):

        try:

            # Check if the module can be imported successfully
            ForwardLoewner = self.import_loewner()

        except ModuleNotFoundError:

            # Compile and import the module if it does not already exist
            self.set_compile_command()
            self.compile_loewner()
            ForwardLoewner = self.import_loewner()

        # Declare empty complex arrays for the results
        self.resultsA = empty(self.outer_points, dtype=complex128)
        self.resultsB = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        if self.driving_function == 0:
            ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.resultsA, gresultb=self.resultsB, constdrivingarg=self.constantParam)
        else:
            ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.resultsA, gresultb=self.resultsB)

    def save_to_dat(self):

        # Create filenames for the data files
        filenameA = self.output_dir + self.generate_properties_string() + "-A" + Constants.DATA_EXT
        filenameB = self.output_dir + self.generate_properties_string() + "-B" + Constants.DATA_EXT

        # Create 2D arrays from the real and imaginary values of the results
        combinedA = column_stack((self.resultsA.real,self.resultsA.imag))
        combinedB = column_stack((self.resultsB.real,self.resultsB.imag))

        # Convert the 2D arrays to files
        savetxt(filenameA, combinedA, fmt="%.18f")
        savetxt(filenameB, combinedB, fmt="%.18f")
