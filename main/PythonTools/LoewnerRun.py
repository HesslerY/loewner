from Constants import *
import matplotlib.pyplot as plt
from subprocess import check_output, call, CalledProcessError
from DrivingFunction import DrivingFunction
from mpmath import findroot
from cmath import log, sqrt
from numpy import empty, column_stack, savetxt, complex128, zeros, linspace, copy, roots
from importlib import import_module
plt.style.use('ggplot')

class LoewnerRun:

    def __init__(self, index, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Assign the driving function index
        self.index = index

        # Assign the module code
        self.module_code = str(driving_function)

        # Determine the filename of the relevant Fortran file
        self.forward_filename = "../" + FOR_LOEWNER + "/" + FOR_LOEWNER + FORTRAN_EXT
        self.inverse_filename = "../" + INV_LOEWNER + "/" + INV_LOEWNER + FORTRAN_EXT

        # Set a filename for the compiled module
        self.forward_module_name = "modules." + FOR_LOEWNER + "_"  + self.module_code
        self.inverse_module_name = "modules." + INV_LOEWNER + "_"  + self.module_code

        # Set the data-saving parameters
        self.save_data = save_data
        self.save_plot = save_plot

        # Set the time and resolution parameters
        self.start_time = start_time
        self.final_time = final_time
        self.outer_points = outer_points
        self.inner_points = inner_points

        # Create a null variable for the quadratic forward results (Used to check if the quadratic forward algorithm has been executed)
        self.forward_resuls = None

        # Compile the modules (Not necessary unless the Fortran files have changed since last compilation)
        if compile_modules:
            self.compile_modules()

        # Obtain the name, plot title, and function for the given driving function
        if index == 2:

            self.name = "cos(t)"
            self.latex_name = "$\\xi (t) = \cos(t)$"
            self.xi = lambda t: cos(t)

        if index == 3:

            self.name = "t * cos(t)"
            self.latex_name = "$\\xi (t) = t \ \cos(t)$"
            self.xi = lambda t: t * cos(t)

        if index == 4:

            self.name = "cos(t * pi)"
            self.latex_name = "$\\xi (t) = \cos(\pi t)$"
            self.xi = lambda t: cos(pi * t)

        if index == 5:

            self.name = "t * cos(t * pi)"
            self.latex_name = "$\\xi (t) = t \ \cos(\pi t)$"
            self.xi = lambda t: t * cos(pi * t)

        if index == 6:

            self.name = "sin(t)"
            self.latex_name = "$\\xi (t) = \sin(t)$"
            self.xi = lambda t: sin(t)

        if index == 7:

            self.name = "t * sin(t)"
            self.latex_name = "$\\xi (t) = t \ \sin(t)$"
            self.xi = lambda t: t * sin(t)

        if index == 8:

            self.name = "sin(t * pi)"
            self.latex_name = "$\\xi (t) = \sin(\pi t)$"
            self.xi = lambda t: sin(pi * t)

        if index == 9:

            self.name = "t * sin(t * pi)"
            self.latex_name = "$\\xi (t) = t \ \sin(\pi t)$"
            self.xi = lambda t: t * sin(pi * t)

        if index == 12:

            self.name = "floor(t)"
            self.latex_name = "$\\xi (t) = \lfloor t \\rfloor $"
            self.xi = lambda t: floor(t)

        if index == 13:

            self.name = "floot(t) % 2"
            self.latex_name = "$\\xi (t) = \lfloor t \\rfloor \ \\mathrm{mod} \ 2$"
            self.xi = lambda t: floor(t) % 2

        # Create the properties string (Used for creating filenames)
        self.set_properties_string()

        # Construct the exact solution for time
        self.exact_time_sol = linspace(self.start_time, self.final_time, self.outer_points)

    def set_properties_string(self):

        # Place the parameters of the run into a list
        properties = [self.index, self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.properties_string = "-".join(desc)

    def compile_modules(self):

        # Create a string that is used to compile the forward fortran file with f2py
        self.compile_forward = F2PY_FIRST + ["-DCASE=" + self.module_code] \
               + [self.forward_filename, "-m", \
                  self.forward_module_name]

        # Create a string that is used to compile the inverse fortran file with f2py
        self.compile_inverse = F2PY_FIRST \
               + [self.inverse_filename, "-m", \
                  self.inverse_module_name]

        # Iterate through the modules
        for command in [FOR_RUN_STR, CBC_RUN_STR]:

            # Attempt to compile the module
            try:
                check_output(command)

            # Display an error if the module could not be compiled (Typically means there is a problem in the Fortran code)
            except CalledProcessError:
                print("Error: Could not compile module " + command)
                exit()

    def save_to_dat(self, filename, results_array):

        # Save the results to a dat file
        savetxt(filename, results_array, fmt=DATA_PREC)

    def set_plot_title(self):

        # Prepare the plot title
        plt.title(self.latex_name, fontsize = 19, color = "black", y = 1.02, usetex = True)

    def quadratic_forward_plot(self):

        # Plot the values
        plt.plot(self.forward_results.real, self.forward_results.imag, color='crimson')

        # Set the axes labels
        plt.xlabel(FOR_PLOT_XL)
        plt.ylabel(FOR_PLOT_YL)

        # Set the lower limit for the y-axis
        plt.ylim(bottom=0)

        # Save the plot to the filesystem
        plt.savefig(FORWARD_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

    def quadratic_inverse_plot(self):

        # Plot the values
        plt.plot(self.time_arr, self.driving_arr, color='crimson')

        # Set the axes labels
        plt.xlabel(INV_PLOT_XL)
        plt.ylabel(INV_PLOT_YL)

        # Set the lower limit for the x-axis
        plt.xlim(left=self.start_time)

        # Save the plot to the filesystem
        plt.savefig(INVERSE_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

    def cubic_forward_plot(self):

        # Plot the values
        plt.plot(self.cubic_results_A.real, self.cubic_results_A.imag, color='crimson')
        plt.plot(self.cubic_results_B.real, self.cubic_results_B.imag, color='crimson')

        # Set the axes labels
        plt.xlabel(FOR_PLOT_XL)
        plt.ylabel(FOR_PLOT_YL)

        # Set the lower limit for the y-axis
        plt.ylim(bottom=0)

        # Save the plot to the filesystem
        plt.savefig(CUBIC_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

    def quadratic_forward_loewner(self):

        # Import the compiled Forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.quadraticloewner(self.start_time, self.final_time, self.inner_points, self.forward_results)

        if self.save_data:

            # Convert the results to a 2D array
            results_array = column_stack((self.forward_results.real, self.forward_results.imag))

            # Create a filename for the dat file
            filename = FORWARD_DATA_OUTPUT + self.properties_string + DATA_EXT

            # Save the array to the filesystem
            self.save_to_dat(filename, results_array)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.quadratic_forward_plot()

    def quadratic_inverse_loewner(self):

        # Check if the quadratic forward function has been executed
        if self.forward_resuls is None:

            print("Error: No quadratic forward results to use for inverse algorithm.")
            exit()

        # Import the compiled Inverse Loewner module
        InverseLoewner = import_module(self.inverse_module_name)

        # Declare empty arrays for the time and driving function values
        self.driving_arr = empty(self.outer_points, dtype=float)
        self.time_arr = empty(self.outer_points, dtype=float)

        # Carry out the Inverse algorithm using the results of the forward run
        InverseLoewner.inverseloewner(self.forward_results, self.driving_arr, self.time_arr, self.outer_points)

        if self.save_data:

            # Convert the results to a 2D array
            results_array = column_stack((self.time_arr, self.driving_arr))

            # Create a filename for the dat file
            filename = INVERSE_DATA_OUTPUT + self.properties_string + DATA_EXT

            # Save the array to the filesystem
            self.save_to_dat(filename, results_array)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.quadratic_inverse_plot()

    def cubic_forward_loewner(self):

        # Import the module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare empty complex arrays for the results
        self.cubic_results_A = empty(self.outer_points, dtype=complex128)
        self.cubic_results_B = empty(self.outer_points, dtype=complex128)

        # Carry out the Cubic algorithm
        ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_A, gresultb=self.cubic_results_B)

        if self.save_data:

            # Create filenames for the data files
            filenameA = CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filenameB = CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            combinedA = column_stack((self.cubic_results_A.real,self.cubic_results_A.imag))
            combinedB = column_stack((self.cubic_results_B.real,self.cubic_results_B.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filenameA, combinedA)
            self.save_to_dat(filenameB, combinedB)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.cubic_forward_plot()

def ConstantLoewnerRun(LoewnerRun):

    def __init__(self, constant, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Invoke the superclass initialiser
        LoewnerRun.__init__(CONST_IDX, start_time, final_time, outer_points, inner_points, compile_modules, save_data, save_plot)

        # Set the constant value
        self.constant = constant

        # Set the name, plot title, and function for the given driving function
        self.name = "Constant"
        self.latex_name = "$\\xi (t) = " + str(self.constant) + "$"
        self.xi = lambda t: self.constant

    def quadratic_forward_loewner(self):

        # Import the module
        ForwardLoewner = self.import_loewner(FOR_RUN_STR)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.forward_results, constantdrivingarg=self.constant)

        if self.save_data:

            # Create a filenames for the dat files
            filename = FORWARD_DATA_OUTPUT + self.properties_string + DATA_EXT

            # Create a 2D array from the real and imaginary values of the raw results and translated results
            results_array = self.column_stack((self.forward_results.real, self.forward_results.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename, results_array)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.quadratic_forward_plot()

    def cubic_forward_loewner(self):

        # Improt the module
        ForwardLoewner = self.import_loewner(FOR_RUN_STR)

        # Declare empty complex arrays for the results
        self.cubic_results_A = empty(self.outer_points, dtype=complex128)
        self.cubic_results_B = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_A, gresultb=self.cubic_results_B, constdrivingarg=self.constant_param)

        if self.save_data:

            # Create filenames for the data files
            filenameA = CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filenameB = CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            combinedA = column_stack((self.cubic_results_A.real,self.cubic_results_A.imag))
            combinedB = column_stack((self.cubic_results_B.real,self.cubic_results_B.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filenameA, combinedA)
            self.save_to_dat(filenameB, combinedB)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.cubic_forward_plot()

    def exact_cubic_forward_loewner(self):

        # Declare empty complex arrays for the exact results
        self.exact_cubic_sol_A = zeros(self.outer_points,dtype = complex128)
        self.exact_cubic_sol_B = zeros(self.outer_points,dtype = complex128)

        # Define the constant term for the exact solution
        exact_constant = 1

        # Define a function for generating an initial guess to be used by the non-linear solver
        def initial_guess(t):
            return 1 + 1j * sqrt(2*t) - (1./3) * t

        # Define the non-linear function for obtaining the exact solution
        def exact_solution(g,t):
            return g**2 - 2*log(g) - 1 + 4*t

        # Iterate through the exact time values
        for i in range(self.outer_points):

            # Use Muller's method for finding the exact solution
            self.exact_cubic_sol_A[i] = findroot(lambda g: f(g,self.exact_time_sol[i], initial_guess(self.exact_time_sol[i]),solver='muller')

            # Obatain the solution to the second trace by changing the sign of the real component
            self.exact_cubic_sol_B[i] = -self.exact_cubic_sol_A[i].real + self.exact_cubic_sol_A[i].imag * 1j

        if save_data:

            # Create a filename for the dat file
            filename = EXACT_CUBIC_DATA_OUTPUT + properties_string

            # Create 2D arrays from the real and imaginary values of the results
            array_A = column_stack((self.cubic_exact_sol_A.real, self.cubic_exact_sol_A.imag))
            array_B = column_stack((self.cubic_exact_sol_B.real, self.cubic_exact_sol_B.imag))

        if save_plot:

            plt.cla()
            plt.title(MAKE_CONSTANT_TITLE(constant), fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.plot(self.cubic_exact_sol_A.real, self.cubic_exact_sol_A.imag, color='crimson')
            plt.plot(self.cubic_exact_sol_B.real, self.cubic_exact_sol_B.imag, color='crimson')
            plt.ylim(bottom=0)
            plt.savefig(EXACT_CUBIC_PLOT_OUTPUT + properties_string + PLOT_EXT, bbox_inches='tight')

def LinearLoewnerRun(LoewnerRun):

    def __init__(self):

        LoewnerRun.__init__(LINR_IDX)

        self.name = "t"
        self.latex_name = "$\\xi (t) = t$"
        self.xi = lambda t: t

    def exact_quadratic_forward(self):

        self.exact_quad_for = zeros(self.outer_points,dtype = complex128)

        def initial_guess(t):
            return 2 * 1j * sqrt(t) + (2./3) * t

        for i in range(self.outer_points):

            self.exact_quadfor[i] = findroot(lambda z: z + 2 * log(2 - z) - 2 * log(2) - self.exact_time_sol[i], initial_guess(self.exact_time_sol[i]),solver='muller')

        if save_data:

            filename = EXACT_FORWARD_DATA_OUTPUT + properties_string + DATA_EXT
            array = column_stack((exact_linear.real, exact_linear.imag))
            savetxt(filename, array, fmt=DATA_PREC)

        if save_plot:

            plt.cla()

            plt.ylim(bottom=0)

            plt.title(PLOT_TITLE[LINR_IDX], fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.plot(exact_linear.real, exact_linear.imag, color='crimson')
            plt.savefig(EXACT_FORWARD_PLOT_OUTPUT + properties_string + PLOT_EXT, bbox_inches='tight')


def KappaLoewnerRun(LoewnerRun):

    def __init__(self, kappa):

        LoewnerRun.__init__(KAPPA_IDX)

        # Set the kappa value
        self.kappa = kappa

        # Generate a properties string
        self.set_properties_string()

        self.name = "2 * dsqrt(kappa * (1 - t))"
        self.latex_name = "$\\xi (t) = 2 \ \sqrt{" + str(self.kappa)[:3] + "\ (1 - t)}$"
        self.xi = lambda t: sqrt(self.kappa * (1 - t))

    def set_properties_string(self):

        # Convert the kappa parameter to a string
        sqrt_string = str(self.kappa)[:3].replace(".","point")

        # Create a list from the run parameters
        properties = [self.index, sqrt_string, self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.properties_string = "-".join(desc)

    def shift(self):

        self.copy_answer = copy(self.forward_results)
        offset = self.copy_answer[0].real

        for i in range(self.outer_points):
            self.copy_answer[i] -= offset

        shifted_array = column_stack((self.copy_answer.real, self.copy_answer.imag))
        filename = FORSHIFT_DATA_OUTPUT + self.properties_string + DATA_EXT
        self.array_to_file(shifted_array, filename)

    def quadratic_forward_loewner(self):

        # Import the module
        ForwardLoewner = self.import_loewner(FOR_RUN_STR)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.forward_results, sqrtdrivingarg=self.kappa)

        if self.save_data:

            # Create a filename for the dat file
            filename = FORWARD_DATA_OUTPUT + self.properties_string + DATA_EXT

            # Create a 2D array from the real and imaginary values of the results
            self.array_to_file(self.prepare_file(FOR_RUN_STR), filename)

            # Translate the real values so the plot starts at the origin
            self.shift()

        if self.save_plot:
            pass

def CAlphaLoewnerRun(LoewnerRun):

    def __init__(self, alpha):

        LoewnerRun.__init__(CALPHA_IDX)

        # Set the value for alpha
        self.alpha = alpha

        # Obtain the value for calpha
        self.calpha = (2 - 4 * alpha) / sqrt(alpha - alpha**2)

        self.name = "dsqrt(t) * c_alpha"
        self.alpha = alpha
        self.calpha = (2 - 4 * alpha) / sqrt(alpha - alpha**2)
        self.latex_name = "$\\xi (t) = c_{" + str(self.alpha)[:3] + "} \sqrt{t}$"
        self.xi = lambda t: self.calpha * sqrt(t)

        self.set_properties_string()

    def set_properties_string(self):

        sqrt_string = str(self.alpha)[:3].replace(".","point")
        properties = [self.index, sqrt_string, self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.properties_string = "-".join(desc)

    def quadratic_forward_loewner(self):

        ForwardLoewner = self.import_loewner(FOR_RUN_STR)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresult=self.forward_results, sqrtdrivingarg=self.alpha)

def SqrtTPlusOneLoewnerRun(LoewnerRun):

    def __init__(self):

        LoewnerRun.__init__(SQRTPLUS_IDX)

        self.name = "sqrt(1 + t)"
        self.latex_name = "$\\xi (t) = \sqrt{1 + t}$"
        self.xi = lambda t: sqrt(1 + t)

    def sqrtplusone_cubic_exact(self, save_plot, save_data):

        self.cubic_exact_sol_A = zeros(self.outer_points,dtype = complex128)
        self.cubic_exact_sol_B = zeros(self.outer_points,dtype = complex128)

        driving_function = 14

        a0 = 1
        d0 = 1

        def get_coeffs(t):
            return [-1, 0, 10*a0**2, 0, -25*a0**4, 16*(a0**2 + d0 * t)**(5./2)]

        for i in range(self.outer_points):

            exact_roots = roots(get_coeffs(self.exact_time_sol[i]))
            self.cubic_exact_sol_A[i] = exact_roots[3]
            self.cubic_exact_sol_B[i] = -self.cubic_exact_sol_A[i].real + self.cubic_exact_sol_A[i].imag * 1j

        properties_string = "-".join([str(prop) for prop in [driving_function, self.start_time, self.final_time, self.outer_points]])

        if save_data:

            filename = EXACT_CUBIC_DATA_OUTPUT + properties_string

            array_A = column_stack((self.cubic_exact_sol_A.real, self.cubic_exact_sol_A.imag))
            array_B = column_stack((self.cubic_exact_sol_B.real, self.cubic_exact_sol_B.imag))

            savetxt(filename + "-A" + DATA_EXT, array_A, fmt=DATA_PREC)
            savetxt(filename + "-B" + DATA_EXT, array_B, fmt=DATA_PREC)

        if save_plot:

            plt.cla()

            plt.title(self.latex_name, fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.plot(self.cubic_exact_sol_A.real, self.cubic_exact_sol_A.imag, color='crimson')
            plt.plot(self.cubic_exact_sol_B.real, self.cubic_exact_sol_B.imag, color='crimson')
            plt.ylim(bottom=0)
            plt.savefig(EXACT_CUBIC_PLOT_OUTPUT + properties_string + PLOT_EXT, bbox_inches='tight')

