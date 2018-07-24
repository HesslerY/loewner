import Constants
import matplotlib.pyplot as plt
from subprocess import check_output, call, CalledProcessError
from mpmath import findroot
from cmath import log, sqrt
from numpy import empty, column_stack, savetxt, complex128, zeros, linspace, copy
from importlib import import_module
plt.style.use('ggplot')

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

        if self.driving_function not in [Constants.KAPPA_IDX, Constants.CALPHA_IDX]:
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

        savetxt(filename, array, fmt=Constants.DATA_PREC)

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

    def quadratic_forward_plot(self):

        # Plot the values
        plt.plot(self.forward_results.real, self.forward_results.imag, color='crimson')

        plt.xlabel(Constants.FOR_PLOT_XL)
        plt.ylabel(Constants.FOR_PLOT_YL)

        plt.ylim(bottom=0)

        if self.save_plot:
            plt.savefig(Constants.FORWARD_PLOT_OUTPUT + self.generate_properties_string() + Constants.PLOT_EXT, bbox_inches='tight')

    def quadratic_inverse_plot(self):

        # Plot the values
        plt.plot(self.time_arr, self.driving_arr, color='crimson')

        plt.xlabel(Constants.INV_PLOT_XL)
        plt.ylabel(Constants.INV_PLOT_YL)

        plt.xlim(left=self.start_time)

        if self.save_plot:
            plt.savefig(Constants.INVERSE_PLOT_OUTPUT + self.generate_properties_string() + Constants.PLOT_EXT, bbox_inches='tight')

    def cubic_plot(self):

        # Plot the values
        plt.plot(self.cubic_results_A.real, self.cubic_results_A.imag, color='crimson')
        plt.plot(self.cubic_results_B.real, self.cubic_results_B.imag, color='crimson')

        plt.xlabel(Constants.FOR_PLOT_XL)
        plt.ylabel(Constants.FOR_PLOT_YL)

        plt.ylim(bottom=0)

        if self.save_plot:
            plt.savefig(Constants.CUBIC_PLOT_OUTPUT + self.generate_properties_string() + Constants.PLOT_EXT, bbox_inches='tight')

    def set_plot_title(self):

        if self.driving_function == Constants.CONST_IDX:
            self.plot_title = Constants.MAKE_CONSTANT_TITLE(self.constant_param)

        elif self.driving_function == Constants.CALPHA_IDX:
            self.plot_title = Constants.MAKE_CALPHA_TITLE(self.sqrt_param)

        elif self.driving_function == Constants.KAPPA_IDX:
            self.plot_title = Constants.MAKE_KAPPA_TITLE(self.sqrt_param)

        else:
            self.plot_title = Constants.PLOT_TITLE[self.driving_function]

        plt.title(self.plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

    def plot_results(self, algorithm):

        plt.cla()
        self.set_plot_title()

        if algorithm == Constants.FOR_RUN_STR:
            return self.quadratic_forward_plot()

        if algorithm == Constants.INV_RUN_STR:
            return self.quadratic_inverse_plot()

        if algorithm == Constants.CBC_RUN_STR:
            return self.cubic_plot()

    def run(self, algorithm):

        self.set_compile_commands()
        self.compile_module(algorithm)
        self.import_loewner(algorithm)
        self.perform_loewner(algorithm)

        if self.save_data:
            self.save_to_dat(algorithm)

        if self.save_plot:
            self.plot_results(algorithm)

    def negative_real(self, complex_arr):

        for i in range(len(complex_arr)):
            complex_arr[i] = -complex_arr[i].real + complex_arr[i].imag

    def perform_linear_quad_exact(self,save_plot,save_data):

        exact_linear = zeros(self.outer_points,dtype = complex128)
        self.exact_time_sol = linspace(self.start_time, self.final_time, self.outer_points)

        def initial_guess(t):
            return 2 * 1j * sqrt(t) + (2./3) * t

        for i in range(self.outer_points):
            exact_linear[i] = findroot(lambda z: z + 2 * log(2 - z) - 2 * log(2) - self.exact_time_sol[i], initial_guess(self.exact_time_sol[i]),solver='muller')

        properties_string = "-".join([str(prop) for prop in [Constants.LINR_IDX, self.start_time, self.final_time, self.outer_points]])

        if save_data:

            filename = Constants.EXACT_FORWARD_DATA_OUTPUT + properties_string + Constants.DATA_EXT
            array = column_stack((exact_linear.real, exact_linear.imag))
            savetxt(filename, array, fmt=Constants.DATA_PREC)

        if save_plot:

            plt.cla()
            plt.ylim(bottom=0)

            plt.title(Constants.PLOT_TITLE[Constants.LINR_IDX], fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.plot(exact_linear.real, exact_linear.imag, color='crimson')
            plt.savefig(Constants.EXACT_FORWARD_PLOT_OUTPUT + properties_string + Constants.PLOT_EXT, bbox_inches='tight')

    def perform_constant_cubic_exact(self,save_plot,save_data):

        self.cubic_exact_sol_A = zeros(self.outer_points,dtype = complex128)
        self.cubic_exact_sol_B = zeros(self.outer_points,dtype = complex128)
        self.exact_time_sol = linspace(self.start_time, self.final_time, self.outer_points)

        def initial_guess(t):
            return 1 + 1j * sqrt(2*t) - (1./3) * t

        for i in range(self.outer_points):
            self.cubic_exact_sol_A[i] = findroot(lambda z: z**2 - 2*log(z) - 1 + 4*self.exact_time_sol[i], initial_guess(self.exact_time_sol[i]),solver='muller')
            self.cubic_exact_sol_B[i] = -self.cubic_exact_sol_A[i].real + self.cubic_exact_sol_A[i].imag * 1j

        properties_string = "-".join([str(prop) for prop in [Constants.CONST_IDX, self.start_time, self.final_time, self.outer_points]])

        if save_data:

            filename = Constants.EXACT_CUBIC_DATA_OUTPUT + properties_string

            array_A = column_stack((self.cubic_exact_sol_A.real, self.cubic_exact_sol_A.imag))
            array_B = column_stack((self.cubic_exact_sol_B.real, self.cubic_exact_sol_B.imag))

            savetxt(filename + "-A" + Constants.DATA_EXT, array_A, fmt=Constants.DATA_PREC)
            savetxt(filename + "-B" + Constants.DATA_EXT, array_B, fmt=Constants.DATA_PREC)

        if save_plot:

            plt.cla()
            plt.ylim(bottom=0)
            plt.title(Constants.MAKE_CONSTANT_TITLE(1), fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.plot(self.cubic_exact_sol_A.real, self.cubic_exact_sol_A.imag, color='crimson')
            plt.plot(self.cubic_exact_sol_B.real, self.cubic_exact_sol_B.imag, color='crimson')
            plt.savefig(Constants.EXACT_CUBIC_PLOT_OUTPUT + properties_string + Constants.PLOT_EXT, bbox_inches='tight')

    def sqrtplusone_cubic_exact(self):
        pass

