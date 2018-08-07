from Constants import *
import matplotlib.pyplot as plt
from subprocess import check_output, CalledProcessError
import matlab.engine
from mpmath import findroot
from cmath import log, sqrt
from cmath import cos as ccos
from cmath import sin as csin
from math import pi, sin, floor, cos
from numpy import empty, column_stack, savetxt, complex128, zeros, linspace, copy, roots, array
from importlib import import_module
plt.style.use('ggplot')

class LoewnerRun:

    def __init__(self, index, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Assign the driving function index
        self.index = index

        # Assign the module code
        self.module_code = str(index)

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

        # Declare constants used in special driving function cases
        self.constant = 0
        self.kappa = 0
        self.alpha = 0

        # Obtain the names and lambda function for the given driving function
        if index == 2:

            self.name = "cos(t)"
            self.latex_name = "$\\xi (t) = \cos(t)$"
            self.xi = lambda t: cos(t)

        elif index == 3:

            self.name = "t * cos(t)"
            self.latex_name = "$\\xi (t) = t \ \cos(t)$"
            self.xi = lambda t: t * cos(t)

        elif index == 4:

            self.name = "cos(t * pi)"
            self.latex_name = "$\\xi (t) = \cos(\pi t)$"
            self.xi = lambda t: cos(pi * t)

        elif index == 5:

            self.name = "t * cos(t * pi)"
            self.latex_name = "$\\xi (t) = t \ \cos(\pi t)$"
            self.xi = lambda t: t * cos(pi * t)

        elif index == 6:

            self.name = "sin(t)"
            self.latex_name = "$\\xi (t) = \sin(t)$"
            self.xi = lambda t: sin(t)

        elif index == 7:

            self.name = "t * sin(t)"
            self.latex_name = "$\\xi (t) = t \ \sin(t)$"
            self.xi = lambda t: t * sin(t)

        elif index == 8:

            self.name = "sin(t * pi)"
            self.latex_name = "$\\xi (t) = \sin(\pi t)$"
            self.xi = lambda t: sin(pi * t)

        elif index == 9:

            self.name = "t * sin(t * pi)"
            self.latex_name = "$\\xi (t) = t \ \sin(\pi t)$"
            self.xi = lambda t: t * sin(pi * t)

        elif index == 12:

            self.name = "floor(t)"
            self.latex_name = "$\\xi (t) = \lfloor t \\rfloor $"
            self.xi = lambda t: floor(t)

        elif index == 13:

            self.name = "floot(t) % 2"
            self.latex_name = "$\\xi (t) = \lfloor t \\rfloor \ \\mathrm{mod} \ 2$"
            self.xi = lambda t: floor(t) % 2

        # Create the properties string (Used for creating filenames)
        if not SQUAREROOT_DRIVING(index):
            self.set_properties_string()
            self.set_short_properties_string()

        # Construct the exact solution for time
        self.exact_time_sol = linspace(self.start_time, self.final_time, self.outer_points)

    def set_properties_string(self):

        # Place the parameters of the run into a list
        properties = [self.index, self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.properties_string = "-".join(desc)

    def set_short_properties_string(self):

        # Place the parameters of the run into a list
        properties = [self.index, self.start_time, self.final_time, self.outer_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.short_properties_string = "-".join(desc)

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
        for command in [self.compile_forward, self.compile_inverse]:

            # Attempt to compile the module
            try:
                check_output(command)

            # Display an error if the module could not be compiled (Typically means there is a problem in the Fortran code)
            except CalledProcessError:
                print("Error: Could not compile module " + " ".join(command))
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

        # Set the lower limit of the y-axis
        plt.ylim(bottom=0)

        # Save the plot to the filesystem
        plt.savefig(FORWARD_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

    def quadratic_inverse_plot(self):

        # Plot the values
        plt.plot(self.time_arr, self.driving_arr, color='crimson')

        # Set the axes labels
        plt.xlabel(INV_PLOT_XL)
        plt.ylabel(INV_PLOT_YL)

        # Set the lower limit of the x-axis
        plt.xlim(left=self.start_time)

        # Save the plot to the filesystem
        plt.savefig(INVERSE_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

    def cubic_forward_plot(self):

        # Plot the values
        plt.plot(self.cubic_results_a.real, self.cubic_results_a.imag, color='crimson')
        plt.plot(self.cubic_results_b.real, self.cubic_results_b.imag, color='crimson')

        # Set the axes labels
        plt.xlabel(FOR_PLOT_XL)
        plt.ylabel(FOR_PLOT_YL)

        # Set the lower limit of the y-axis
        plt.ylim(bottom=0)

        # Save the plot to the filesystem
        plt.savefig(CUBIC_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

    def finger_growth_plot(self):

        # Plot the values
        plt.plot(self.finger_results_a.real, self.finger_results_a.imag, color='crimson')
        plt.plot(self.finger_results_b.real, self.finger_results_b.imag, color='crimson')

        # Set the axes labels
        plt.xlabel(FOR_PLOT_XL)
        plt.ylabel(FOR_PLOT_YL)

        # Set the lower limit of the y-axis
        plt.ylim(bottom=0)

        # Save the plot to the filesystem
        plt.savefig(FINGER_PLOT_OUTPUT + self.short_properties_string + PLOT_EXT, bbox_inches='tight')

    def wedge_growth_plot(self, wedge_properties_string):

        # Plot the values
        plt.plot(self.wedge_results.real, self.wedge_results.imag, color='crimson')

        # Set the axes labels
        plt.xlabel(FOR_PLOT_XL)
        plt.ylabel(FOR_PLOT_YL)

        # Set the lower limit of the y-axis
        plt.ylim(bottom=0)

        # Save the plot to the filesystem
        plt.savefig(WEDGE_PLOT_OUTPUT + wedge_properties_string + PLOT_EXT, bbox_inches='tight')

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
        if self.forward_results is None:

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

        # Import the compiled Forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare empty complex arrays for the results
        self.cubic_results_a = empty(self.outer_points, dtype=complex128)
        self.cubic_results_b = empty(self.outer_points, dtype=complex128)

        # Carry out the Cubic algorithm
        ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_a, gresultb=self.cubic_results_b)

        if self.save_data:

            # Create filenames for the data files
            filename_a = CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filename_b = CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            array_a = column_stack((self.cubic_results_a.real,self.cubic_results_a.imag))
            array_b = column_stack((self.cubic_results_b.real,self.cubic_results_b.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename_a, array_a)
            self.save_to_dat(filename_b, array_b)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.cubic_forward_plot()

    def finger_growth(self):

        # Declare empty complex arrays for the results
        self.finger_results_a = empty(self.outer_points, dtype=complex128)
        self.finger_results_b = empty(self.outer_points, dtype=complex128)

        # Find all the values of the driving function
        xi_sol = [self.xi(t) for t in self.exact_time_sol]

        # Set the first values of the solution
        self.finger_results_a[0] = xi_sol[0]
        self.finger_results_b[0] = -xi_sol[0]

        # Define a 'weight' for the equation
        d = 1

        # Obtain the value of delta t
        delta_t = self.exact_time_sol[1]

        # Set an increment for obtaining an initial guess for the nonlinear solver
        increment = delta_t * 1j

        # Define a non-linear function for obtaining the fingered growth solution
        def f(g_current, g_previous, xi_t):
            return delta_t * d * HALF_PI * ccos(HALF_PI * g_current) + (g_current - g_previous)*(csin(HALF_PI * g_current) - csin(HALF_PI * xi_t))

        # Use the Secant method for finding the finger solution
        self.finger_results_a[1] = findroot(lambda g: f(g, self.finger_results_a[0],  xi_sol[0]), self.finger_results_a[0] + increment, solver='secant', tol=TOL)
        self.finger_results_b[1] = findroot(lambda g: f(g, self.finger_results_b[0], -xi_sol[0]), self.finger_results_b[0] + increment, solver='secant', tol=TOL)

        # Iterate through the exact time values
        for i in range(2,self.outer_points):

            # Use the Secant method for finding the finger solution
            self.finger_results_a[i] = findroot(lambda g: f(g, self.finger_results_a[i - 1],  xi_sol[i]), self.finger_results_a[i - 1], solver='secant', tol=TOL)
            self.finger_results_b[i] = findroot(lambda g: f(g, self.finger_results_b[i - 1], -xi_sol[i]), self.finger_results_b[i - 1], solver='secant', tol=TOL)

        if self.save_data:

            # Create filenames for the dat files
            filename_a = FINGER_DATA_OUTPUT + self.short_properties_string + "-A" + DATA_EXT
            filename_b = FINGER_DATA_OUTPUT + self.short_properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            array_a = column_stack((self.finger_results_a.real, self.finger_results_a.imag))
            array_b = column_stack((self.finger_results_b.real, self.finger_results_b.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename_a, array_a)
            self.save_to_dat(filename_b, array_b)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.finger_growth_plot()

    def wedge_growth(self, wedge_alpha):

        # Declare empty complex arrays for the results
        self.wedge_results = empty(self.outer_points, dtype=complex128)

        # Start the Matlab engine
        eng = matlab.engine.start_matlab()

        # Declare variables in the Matlab workspace for solving Loewner's equation
        eng.workspace['index'] = self.index
        eng.workspace['start_time'] = self.start_time
        eng.workspace['final_time'] = self.final_time
        eng.workspace['outer_points'] = self.outer_points
        eng.workspace['inner_points'] = self.inner_points
        eng.workspace['wedge_alpha'] = wedge_alpha
        eng.workspace['fast'] = 0 # Use the 'slow' mode because parfor loops don't seem to work within the Matlab engine for Python :(

        # Declare parameters for the 'special' driving functions
        eng.workspace['constant'] = self.constant
        eng.workspace['kappa'] = self.kappa
        eng.workspace['drive_alpha'] = self.alpha

        # Instruct the workspace to look for files in the Wedge directory
        eng.eval('addpath("../WedgeLoewner/")')

        # Carry out the algorithm for solving the wedge case of Loewner's equation
        wedge_result = eng.eval('SolveWedgeLoewner(index,start_time,final_time,inner_points,outer_points,wedge_alpha,fast,constant,kappa,drive_alpha)',nargout=1)

        # Stop the Matlab engine once the function returns
        eng.quit()

        # Convert the Matlab data to a numpy array
        for i in range(self.outer_points):
            self.wedge_results[i] = wedge_result[0][i]

        # Represent the alpha value as a string
        alpha_string = str(wedge_alpha)[:6].replace(".","point")

        # Create a properties sring for the run
        wedge_properties_string = "-".join([str(attr) for attr in [self.index, alpha_string, self.start_time, self.final_time, self.outer_points, self.inner_points]])

        if self.save_data:

            # Create  a filename for the dat file
            filename = WEDGE_DATA_OUTPUT + wedge_properties_string + DATA_EXT

            # Create a 2D array from the real and imaginary values of the results
            array = column_stack((self.wedge_results.real, self.wedge_results.imag))

            # Save the array to the filesystem
            self.save_to_dat(filename, array)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.wedge_growth_plot(wedge_properties_string)

class ConstantLoewnerRun(LoewnerRun):

    def __init__(self, constant, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Invoke the superclass initialiser
        LoewnerRun.__init__(self, CONST_IDX, start_time, final_time, outer_points, inner_points, compile_modules, save_data, save_plot)

        # Set the constant value
        self.constant = constant

        # Set the names and lambda function for the given driving function
        self.name = "Constant"
        self.latex_name = "$\\xi (t) = " + str(self.constant) + "$"
        self.xi = lambda t: self.constant

        # Set the latex name for the exact cubic case
        self.exact_cubic_latex_name = "$\\xi (t) = " + str(EXACT_CUBIC_CONSTANT) + "$"

    def quadratic_forward_loewner(self):

        # Import the compiled Forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, zresult=self.forward_results, constantdrivingarg=self.constant)

        if self.save_data:

            # Create a filenames for the dat files
            filename = FORWARD_DATA_OUTPUT + self.properties_string + DATA_EXT

            # Create a 2D array from the real and imaginary values of the raw results and translated results
            results_array = column_stack((self.forward_results.real, self.forward_results.imag))

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

        # Import the compiled Forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare empty complex arrays for the results
        self.cubic_results_a = empty(self.outer_points, dtype=complex128)
        self.cubic_results_b = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_a, gresultb=self.cubic_results_b, constdrivingarg=self.constant)

        if self.save_data:

            # Create filenames for the data files
            filename_a = CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filename_b = CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            array_a = column_stack((self.cubic_results_a.real,self.cubic_results_a.imag))
            array_b = column_stack((self.cubic_results_b.real,self.cubic_results_b.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename_a, array_a)
            self.save_to_dat(filename_b, array_b)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.cubic_forward_plot()

    def exact_cubic_forward_loewner(self):

        # Declare empty complex arrays for the exact results
        self.exact_cubic_sol_a = zeros(self.outer_points, dtype = complex128)
        self.exact_cubic_sol_b = zeros(self.outer_points, dtype = complex128)

        # Define a function for generating an initial guess to be used by the non-linear solver
        def initial_guess(t):
            return 1 + 1j * sqrt(2*t) - (1./3) * t

        # Define the non-linear function for obtaining the exact solution
        def exact_solution(g,t):
            return g**2 - 2*log(g) - 1 + 4*t

        # Iterate through the exact time values
        for i in range(self.outer_points):

            # Use Muller's method for finding the exact solution
            self.exact_cubic_sol_a[i] = findroot(lambda g: exact_solution(g, self.exact_time_sol[i]), initial_guess(self.exact_time_sol[i]), solver='muller', tol=TOL)

            # Obtain the solution to the second trace by changing the sign of the real component
            self.exact_cubic_sol_b[i] = -self.exact_cubic_sol_a[i].real + self.exact_cubic_sol_a[i].imag * 1j

        if self.save_data:

            # Create filenames for the dat files
            filename_a = EXACT_CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filename_b = EXACT_CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            array_a = column_stack((self.exact_cubic_sol_a.real, self.exact_cubic_sol_a.imag))
            array_b = column_stack((self.exact_cubic_sol_b.real, self.exact_cubic_sol_b.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename_a, array_a)
            self.save_to_dat(filename_b, array_b)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set a new plot title for the exact solution case (Uses a particular constant)
            plt.title(self.exact_cubic_latex_name, fontsize = 19, color = "black", y = 1.02, usetex = True)

            # Plot the values
            plt.plot(self.exact_cubic_sol_a.real, self.exact_cubic_sol_a.imag, color='crimson')
            plt.plot(self.exact_cubic_sol_b.real, self.exact_cubic_sol_b.imag, color='crimson')

            # Set the axes labels
            plt.xlabel(FOR_PLOT_XL)
            plt.ylabel(FOR_PLOT_YL)

            # Set the lower limit of the y-axis
            plt.ylim(bottom=0)

            # Save the plot to the filesystem
            plt.savefig(EXACT_CUBIC_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

class LinearLoewnerRun(LoewnerRun):

    def __init__(self, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Invoke the superclass initialiser
        LoewnerRun.__init__(self, LINR_IDX, start_time, final_time, outer_points, inner_points, compile_modules, save_data, save_plot)

        # Set the names and lambda function for the given driving function
        self.name = "t"
        self.latex_name = "$\\xi (t) = t$"
        self.xi = lambda t: t

    def exact_quadratic_forward_loewner(self):

        # Declare an empty complex array for the exact results
        self.exact_quadratic_forward = zeros(self.outer_points,dtype = complex128)

        # Define a function for generating an initial guess to be used by the non-linear solver
        def initial_guess(t):
            return 2 * 1j * sqrt(t) + (2./3) * t

        # Define the non-linear function for obtaining the exact solution
        def exact_solution(g,t):
            return g + 2 * log(2 - g) - 2 * log(2) - t

        # Iterate through the exact time values
        for i in range(self.outer_points):

            # Use Muller's method for finding the exact solution
            self.exact_quadratic_forward[i] = findroot(lambda g: exact_solution(g, self.exact_time_sol[i]), initial_guess(self.exact_time_sol[i]), solver='muller', tol=TOL)

        if self.save_data:

            # Create a filename for the dat file
            filename = EXACT_FORWARD_DATA_OUTPUT + self.properties_string + DATA_EXT

            # Create a 2D array from the real and imaginary values of the results
            array = column_stack((self.exact_quadratic_forward.real, self.exact_quadratic_forward.imag))

            # Save the array to the filesystem
            self.save_to_dat(filename, array)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plo the values
            plt.plot(self.exact_quadratic_forward.real, self.exact_quadratic_forward.imag, color='crimson')

            # Set the lower limit of the y-axis
            plt.ylim(bottom=0)

            # Save the plot to the filesystem
            plt.savefig(EXACT_FORWARD_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

class KappaLoewnerRun(LoewnerRun):

    def __init__(self, kappa, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Invoke the superclass initialiser
        LoewnerRun.__init__(self, KAPPA_IDX, start_time, final_time, outer_points, inner_points, compile_modules, save_data, save_plot)

        # Set the kappa value
        self.kappa = kappa

        # Generate a properties string for the kappa case (Used for creating filenames)
        self.set_properties_string()
        self.set_short_properties_string()

        # Create the names and lambda function for the given driving function
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

    def set_short_properties_string(self):

        # Convert the kappa parameter to a string
        sqrt_string = str(self.kappa)[:3].replace(".","point")

        # Create a list from the run parameters
        properties = [self.index, sqrt_string, self.start_time, self.final_time, self.outer_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.short_properties_string = "-".join(desc)

    def quadratic_forward_loewner(self):

        # Import the compiled forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, zresult=self.forward_results, sqrtdrivingarg=self.kappa)

        # Create a copy of the results
        self.translated_results = copy(self.forward_results)

        # Determine the distance from the first point to the origin
        offset = self.translated_results[0].real

        # Shift the copy so that the trace begins at the origin
        for i in range(self.outer_points):
            self.translated_results[i] -= offset

        if self.save_data:

            # Obtain the filenames for both the raw and translated results
            filename = FORWARD_DATA_OUTPUT + self.properties_string + DATA_EXT
            translated_filename = FORSHIFT_DATA_OUTPUT + self.properties_string + DATA_EXT

            # Create an array for the combined filenames and combined results
            combined_filenames = [filename, translated_filename]
            combined_results = [self.forward_results, self.translated_results]

            for result, filename in zip(combined_results, combined_filenames):

                # Convert the result to a 2D array
                results_array = column_stack((result.real, result.imag))

                # Save the array to the filesystem
                self.save_to_dat(filename, results_array)

        if self.save_plot:

            # Obtain the filenames for both the raw and translated results
            filename = FORWARD_PLOT_OUTPUT + self.properties_string + PLOT_EXT
            translated_filename = FORSHIFT_PLOT_OUTPUT + self.properties_string + PLOT_EXT

            # Create an array for the combined filenames and combined results
            combined_filenames = [filename, translated_filename]
            combined_results = [self.forward_results, self.translated_results]

            for result, filename in zip(combined_results, combined_filenames):

                # Clear any preexisting plots to be safe
                plt.cla()

                # Set the plot title
                self.set_plot_title()

                # Plot the values
                plt.plot(result.real, result.imag, color='crimson')

                # Set the axes labels
                plt.xlabel(FOR_PLOT_XL)
                plt.ylabel(FOR_PLOT_YL)

                # Set the lower limit of the y-axis
                plt.ylim(bottom=0)

                # Save the plot to the filesystem
                plt.savefig(filename, bbox_inches='tight')

    def cubic_forward_loewner(self):

        # Import the compiled Forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare empty complex arrays for the results
        self.cubic_results_a = empty(self.outer_points, dtype=complex128)
        self.cubic_results_b = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_a, gresultb=self.cubic_results_b, sqrtdrivingarg=self.kappa)

        if self.save_data:

            # Create filenames for the data files
            filename_a = CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filename_b = CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            array_a = column_stack((self.cubic_results_a.real,self.cubic_results_a.imag))
            array_b = column_stack((self.cubic_results_b.real,self.cubic_results_b.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename_a, array_a)
            self.save_to_dat(filename_b, array_b)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.cubic_forward_plot()

class CAlphaLoewnerRun(LoewnerRun):

    def __init__(self, alpha, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Invoke the superclass initialiser
        LoewnerRun.__init__(self, CALPHA_IDX, start_time, final_time, outer_points, inner_points, compile_modules, save_data, save_plot)

        # Set the value for alpha
        self.alpha = alpha

        # Obtain the value for calpha
        self.calpha = (2 - 4 * alpha) / sqrt(alpha - alpha**2)

        # Create a properties string for the calpha case (Used for creating filenames)
        self.set_properties_string()
        self.set_short_properties_string()

        # Create the names and lambda function for the given driving function
        self.name = "dsqrt(t) * c_alpha"
        self.latex_name = "$\\xi (t) = c_{" + str(self.alpha)[:3] + "} \sqrt{t}$"
        self.xi = lambda t: self.calpha * sqrt(t)

    def set_properties_string(self):

        # Convert the alpha parameter to a string
        sqrt_string = str(self.alpha)[:3].replace(".","point")

        # Create a list from the run parameters
        properties = [self.index, sqrt_string, self.start_time, self.final_time, self.outer_points, self.inner_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.properties_string = "-".join(desc)

    def set_short_properties_string(self):

        # Convert the alpha parameter to a string
        sqrt_string = str(self.alpha)[:3].replace(".","point")

        # Create a list from the run parameters
        properties = [self.index, sqrt_string, self.start_time, self.final_time, self.outer_points]

        # Convert the parameters to strings
        desc = [str(attr) for attr in properties]

        # Create a single string to use as a filename template
        self.short_properties_string = "-".join(desc)

    def quadratic_forward_loewner(self):

        # Import the compiiled Forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare an empty complex array for the results
        self.forward_results = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.quadraticloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, zresult=self.forward_results, sqrtdrivingarg=self.alpha)

    def cubic_forward_loewner(self):

        # Import the compiled Forward Loewner module
        ForwardLoewner = import_module(self.forward_module_name)

        # Declare empty complex arrays for the results
        self.cubic_results_a = empty(self.outer_points, dtype=complex128)
        self.cubic_results_b = empty(self.outer_points, dtype=complex128)

        # Solve Loewner's equation with the given parameters
        ForwardLoewner.cubicloewner(outerstarttime=self.start_time, outerfinaltime=self.final_time, innern=self.inner_points, gresulta=self.cubic_results_a, gresultb=self.cubic_results_b, sqrtdrivingarg=self.alpha)

        if self.save_data:

            # Create filenames for the data files
            filename_a = CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filename_b = CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            array_a = column_stack((self.cubic_results_a.real,self.cubic_results_a.imag))
            array_b = column_stack((self.cubic_results_b.real,self.cubic_results_b.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename_a, array_a)
            self.save_to_dat(filename_b, array_b)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the data and save it to the filesystem
            self.cubic_forward_plot()

class SqrtTPlusOneLoewnerRun(LoewnerRun):

    def __init__(self, start_time, final_time, outer_points, inner_points, compile_modules = True, save_data = True, save_plot = True):

        # Invoke the superclass initialiser
        LoewnerRun.__init__(self, SQRTPLUS_IDX, start_time, final_time, outer_points, inner_points, compile_modules, save_data, save_plot)

        # Create the names and lambda function for the given driving function
        self.name = "sqrt(1 + t)"
        self.latex_name = "$\\xi (t) = \sqrt{1 + t}$"
        self.xi = lambda t: sqrt(1 + t)

    def exact_cubic_forward_loewner(self):

        # Declare empty complex arrays for the exact results
        self.exact_cubic_sol_a = zeros(self.outer_points, dtype = complex128)
        self.exact_cubic_sol_b = zeros(self.outer_points, dtype = complex128)

        # Set the 'weights' of the exact solution
        a0 = 1
        d0 = 1

        # Define functions for generating the coefficients of the polynomial to be solved
        def get_coeffs_a(t):
            return [-1, 0, 10*a0**2, 0, -25*a0**4, 16*(a0**2 + d0 * t)**(5./2)]
        def get_coeffs_b(t):
            return [-1, 0, 10*a0**2, 0, -25*a0**4, -16*(a0**2 + d0 * t)**(5./2)]

        # Iterate through the exact time values
        for i in range(self.outer_points):

            # Find the roots of the polynomials at the given time value
            exact_roots_a = roots(get_coeffs_a(self.exact_time_sol[i]))
            exact_roots_b = roots(get_coeffs_b(self.exact_time_sol[i]))

            # Select the third root (this one has the positive imaginary component)
            self.exact_cubic_sol_a[i] = exact_roots_a[3]
            self.exact_cubic_sol_b[i] = exact_roots_b[3]

        if self.save_data:

            # Create filenames for the dat file
            filename_a = EXACT_CUBIC_DATA_OUTPUT + self.properties_string + "-A" + DATA_EXT
            filename_b = EXACT_CUBIC_DATA_OUTPUT + self.properties_string + "-B" + DATA_EXT

            # Create 2D arrays from the real and imaginary values of the results
            array_a = column_stack((self.exact_cubic_sol_a.real, self.exact_cubic_sol_a.imag))
            array_b = column_stack((self.exact_cubic_sol_b.real, self.exact_cubic_sol_b.imag))

            # Save the arrays to the filesystem
            self.save_to_dat(filename_a, array_a)
            self.save_to_dat(filename_b, array_b)

        if self.save_plot:

            # Clear any preexisting plots to be safe
            plt.cla()

            # Set the plot title
            self.set_plot_title()

            # Plot the results
            plt.plot(self.exact_cubic_sol_a.real, self.exact_cubic_sol_a.imag, color='crimson')
            plt.plot(self.exact_cubic_sol_b.real, self.exact_cubic_sol_b.imag, color='crimson')

            # Set the lower limit of the y-axis
            plt.ylim(bottom=0)

            # Save the plot to the filesystem
            plt.savefig(EXACT_CUBIC_PLOT_OUTPUT + self.properties_string + PLOT_EXT, bbox_inches='tight')

