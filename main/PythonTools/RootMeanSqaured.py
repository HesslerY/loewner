from Constants import QUADRATIC_FORWARD_RMS, DATA_EXT, DATA_PREC
from LoewnerRunFactory import LoewnerRunFactory
from numpy import square, mean, array, savetxt
from math import sqrt

class RootMeanSquared:

    def __init__(self, start_time, final_time, outer_points, inner_points, resolutions):

        # Set the time parameters for the root mean squared comparisons
        self.start_time = start_time
        self.final_time = final_time

        # Set the resolution for the root mean sqaured comparisons
        self.outer_points = outer_points
        self.inner_points = inner_points

        # Set the different resolutions that will be used to calculate the RMS
        self.resolutions = resolutions

        # Prevent the individual runs from compiling and saving plots and data
        dont_compile = False
        dont_save_data = False
        dont_save_plot = False

        # Create a LoewneRun factory for generaring LoewnerRuns that can be used to determine RMS
        self.rms_factory = LoewnerRunFactory(start_time,final_time,outer_points,inner_points,dont_compile,dont_save_plot,dont_save_data)

    def calculate_rms(self, array_a, array_b):

        diff = array_a - array_b
        return sqrt(mean(square(diff)))

    def quadratic_forward_error(self, points=None):

        # Create a list of driving functions that have an exact solution for the quadratic forward case
        exact_solutions = self.rms_factory.create_exact_quadratic_forward()

        # Use the resolutions that were created during class initialisation if no others are given
        if points == None:
            points = self.resolutions

        # Iterate through the exact solutions
        for exact_sol in exact_solutions:

            # Declare an empty list for the error values
            rms_list = []

            # Carry out the exact solution
            exact_sol.exact_quadratic_forward_loewner()

            # Create a list of LoewnerRuns corresponding with exact solution that have different inner resolutions
            approx_solutions = self.rms_factory.vary_inner_res(exact_sol.index, points)

            # Iterate through the approx solutions
            for approx_sol in approx_solutions:

                # Execute the approx solutions
                approx_sol.quadratic_forward_loewner()

                # Calculate the root mean squared error
                rms = self.calculate_rms(exact_sol.exact_quadratic_forward, approx_sol.forward_solution)

                # Add the RMS value to the list
                rms_list.append([approx_sol.inner_points, rms])

            # Create a filename for the error values
            filename = str(exact_sol.index) + "-" + QUADRATIC_FORWARD_RMS + DATA_EXT

            # Save the error values to the filesystem
            savetxt(filename, array(rms_list), fmt=DATA_PREC)
