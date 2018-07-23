import Constants
import matplotlib.pyplot as plt
from subprocess import check_output, call, CalledProcessError
from numpy import empty, column_stack, savetxt, complex128
from importlib import import_module

class LoewnerRun:

    def __init__(self, driving_function, save_data = True, save_plot = True):

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

        self.save_data = save_data
        self.save_plot = save_plot

        self.compile_forward = None
        self.compile_inverse = None
        self.compile_cubic = None

    def shift(self):

        offset = self.forward_results[0].real

        for i in range(self.outer_points): 
            self.forward_results[i] -= offset

    def generate_properties_string(self):

        # Place the parameters of the run into a list

        if self.driving_function not in [Constants.KAPPA_IDX, Constants.C_ALPHA_IDX]:
            properties = [self.driving_function, self.start_time, self.final_time, self.outer_points, self.inner_points]

        else:

            sqrt_string = str(self.sqrt_param)[:3].replace(".","point")
            properties = [self.driving_function, sqrt_string, self.start_time, self.final_time, self.outer_points, self.inner_points]

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
                  self.inverse_module_name]

    def compile_module(self, algorithm):

        if algorithm in [Constants.FOR_RUN_STR, Constants.CBC_RUN_STR]:
            command = self.compile_forward

        if algorithm == Constants.INV_RUN_STR:
            command = self.compile_inverse

        try:
            check_output(command)

        except CalledProcessError:
            
            print(command)
            call(["ls","-l"])
            print("Error: Could not compile module.")
            exit()

    def import_loewner(self, algorithm):

        if algorithm in [Constants.FOR_RUN_STR, Constants.CBC_RUN_STR]:
            return import_module(self.forward_module_name)
        
        if algorithm == Constants.INV_RUN_STR:
            return import_module(self.inverse_module_name)

    def perform_forward_loewner(self):

        ForwardLoewner = self.import_loewner(Constants.FOR_RUN_STR)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        if self.driving_function == Constants.CONST_IDX:
            ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.forward_results, constantdrivingarg=self.constant_param)

        elif not Constants.SQUAREROOT_DRIVING(self.driving_function):
            ForwardLoewner.quadraticloewner(self.start_time, self.final_time, self.inner_points, self.forward_results)
        
        else: 
            ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.forward_results, sqrtdrivingarg=self.sqrt_param)

    def perform_inverse_loewner(self):

        # Check if the module can be imported successfully
        InverseLoewner = self.import_loewner(Constants.INV_RUN_STR)

        # Declare an empty complex array for the results
        self.inverse_results = empty(self.outer_points, dtype=complex128)

        self.driving_arr = empty(self.outer_points, dtype=float)
        self.time_arr = empty(self.outer_points, dtype=float)

        InverseLoewner.inverseloewner(self.forward_results, self.driving_arr, self.time_arr, self.outer_points)

    def perform_cubic_loewner(self):

        ForwardLoewner = self.import_loewner(Constants.FOR_RUN_STR)

        # Declare empty complex arrays for the results
        self.cubic_results_A = empty(self.outer_points, dtype=complex128)
        self.cubic_results_B = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        if self.driving_function == Constants.CONST_IDX:
            ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_A, gresultb=self.cubic_results_B, constdrivingarg=self.constant_param)
        else:
            ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_A, gresultb=self.cubic_results_B)

    def perform_loewner(self, algorithm):

        if algorithm == Constants.FOR_RUN_STR:
            return self.perform_forward_loewner()

        if algorithm == Constants.INV_RUN_STR:
            return self.perform_inverse_loewner()

        if algorithm == Constants.CBC_RUN_STR:
            return self.perform_cubic_loewner()

    def prepare_file(self, algorithm):

        if algorithm == Constants.FOR_RUN_STR:
            return column_stack((self.forward_results.real, self.forward_results.imag))

        if algorithm == Constants.INV_RUN_STR:
            return column_stack((self.time_arr, self.driving_arr))

    def array_to_file(self, array, filename):

        savetxt(filename, array, fmt=Constants.DAT_PREC)

    def forward_save_to_dat(self):

        # Create a filename for the dat file
        filename = Constants.FORWARD_DATA_OUTPUT + self.generate_properties_string() + Constants.DATA_EXT

        # Shift the real values for the case of kappa-driving
        if self.driving_function == Constants.KAPPA_IDX:
            self.shift()

        # Create a 2D array from the real and imaginary values of the results
        self.array_to_file(self.prepare_file(Constants.FOR_RUN_STR), filename)

    def inverse_save_to_dat(self):

        # Create a filename for the dat file
        filename = Constants.INVERSE_DATA_OUTPUT + self.generate_properties_string() + Constants.DATA_EXT

        # Create a 2D array from the real and imaginary values of the results
        self.array_to_file(self.prepare_file(Constants.INV_RUN_STR), filename)

    def cubic_save_to_dat(self):

        # Create filenames for the data files
        filenameA = Constants.CUBIC_DATA_OUTPUT + self.generate_properties_string() + "-A" + Constants.DATA_EXT
        filenameB = Constants.CUBIC_DATA_OUTPUT + self.generate_properties_string() + "-B" + Constants.DATA_EXT

        # Create 2D arrays from the real and imaginary values of the results
        combinedA = column_stack((self.cubic_results_A.real,self.cubic_results_A.imag))
        combinedB = column_stack((self.cubic_results_B.real,self.cubic_results_B.imag))

        # Convert the 2D arrays to files
        savetxt(filenameA, combinedA, fmt=Constants.DATA_PREC)
        savetxt(filenameB, combinedB, fmt=Constants.DATA_PREC)

    def save_to_dat(self, algorithm):

        if algorithm == Constants.FOR_RUN_STR:
            return self.forward_save_to_dat() 

        if algorithm == Constants.INV_RUN_STR:
            return self.inverse_save_to_dat() 

        if algorithm == Constants.CBC_RUN_STR:
            return self.cubic_save_to_dat() 

    def algorithm_run(self, algorithm):

        self.set_compile_commands()
        
        self.compile_module(algorithm)
        self.import_loewner(algorithm)
        self.perform_loewner(algorithm)

        if self.save_data:
            self.save_to_dat(algorithm)

        if self.save_plot or self.display_plot:
            self.plot_results(algorithm)

    def forward_run(self):
        self.algorithm_run(Constants.FOR_RUN_STR)

    def inverse_run(self):
        self.algorithm_run(Constants.INV_RUN_STR)

    def cubic_run(self):
        self.algorithm_run(Constants.CBC_RUN_STR)

    def forward_plot(self):

        # Plot the values
        plt.plot(self.forward_results.real, self.forward_results.imag, color='crimson')
        
        plt.title(Constants.PLOT_TITLE[self.driving_function], fontsize = 19, color = "black", y = 1.02, usetex = True)

        plt.xlabel(Constants.FOR_PLOT_XL)
        plt.ylabel(Constants.FOR_PLOT_YL)

        plt.ylim(bottom=0)

        if self.save_plot:
            plt.savefig(Constants.FORWARD_PLOT_OUTPUT + self.generate_properties_string() + Constants.PLOT_EXT, bbox_inches='tight')

        if self.display_plot:
            plt.draw()
                
    def inverse_plot(self):

        # Plot the values
        plt.plot(self.time_arr, self.driving_arr, color='crimson')
        
        plt.title(Constants.PLOT_TITLE[self.driving_function], fontsize = 19, color = "black", y = 1.02, usetex = True)

        plt.xlabel(Constants.INV_PLOT_XL)
        plt.ylabel(Constants.INV_PLOT_YL)

        plt.xlim(left=self.start_time)

        if self.save_plot:
            plt.savefig(Constants.INVERSE_PLOT_OUTPUT + self.generate_properties_string() + Constants.PLOT_EXT, bbox_inches='tight')

        if self.display_plot:
            plt.show()
                
    def cubic_plot(self):

        # Plot the values
        plt.plot(self.cubic_results_A.real, self.cubic_results_A.imag, color='crimson')
        plt.plot(self.cubic_results_B.real, self.cubic_results_B.imag, color='crimson')
        
        plt.title(Constants.PLOT_TITLE[self.driving_function], fontsize = 19, color = "black", y = 1.02, usetex = True)

        plt.xlabel(Constants.FOR_PLOT_XL)
        plt.ylabel(Constants.FOR_PLOT_YL)

        plt.ylim(bottom=0)

        if self.save_plot:
            plt.savefig(Constants.CUBIC_PLOT_OUTPUT + self.generate_properties_string() + Constants.PLOT_EXT, bbox_inches='tight')

    def plot_results(self, algorithm):
      
        plt.cla()
        
        if self.driving_function == Constants.CONST_IDX:
            Constants.PLOT_TITLE[self.driving_function] += str(self.constant_param) + "$"

        if self.driving_function == Constants.KAPPA_IDX:
            Constants.PLOT_TITLE[self.driving_function] = "$\\xi (t) = 2 \ \sqrt{"+str(self.sqrt_param)[:3]+"\ (1 - t)}$"

        if self.driving_function == Constants.C_ALPHA_IDX:
            Constants.PLOT_TITLE[self.driving_function] = "$\\xi (t) = c_{"+str(self.sqrt_param)[:3]+"} \sqrt{t}$"

        if algorithm == Constants.FOR_RUN_STR:
            return self.forward_plot() 

        if algorithm == Constants.INV_RUN_STR:
            return self.inverse_plot() 

        if algorithm == Constants.CBC_RUN_STR:
            return self.cubic_plot() 

