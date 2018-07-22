import sys
sys.path.append('../LoewnerRun')

from importlib import import_module
from numpy import savetxt, column_stack, full_like, linspace, empty, absolute, complex128, copy
from math import sqrt
import matplotlib.pyplot as plt
import subprocess

start_time = 0
final_time = 10
outer_n = 1000
inner_n = 10

kappas = [i + 0.5 for i in range(10)]
alphas = [i * 0.1 for i in range(1,10)]
nonSquareRootDriving = [i for i in range(1,10)] + [i for i in range(12,13)]

# Create a list of CubicRun objects for the different driving functions
def create_cubic_runs():

    # Create an empty list for ForwardRun objects
    loewner_runs = []

    # Iterate through the driving functions
    for driving_function in range(Constants.TOTAL_DRIVING_FUNCTIONS):

        # Check that the driving function is not kappa or c_alpha
        if not Constants.squareroot_driving(driving_function):

            # Add a ForwardRun object to the list that corresponds with the current driving function
            loewner_runs.append(CubicRun(driving_function))

            # Set the properties of the ForwardRun
            loewner_runs[-1].final_time = final_time
            loewner_runs[-1].start_time = start_time
            loewner_runs[-1].outer_points = outer_n
            loewner_runs[-1].inner_points = inner_n

    # Return list
    return loewner_runs

# Create a list of SqrtForwardRun objects for kappa-driving
def create_kappa_runs():

    # Define the kappa driving index
    kappa_driving = 10

    # Create an empty list for ForwardRun objects
    loewner_runs = []

    # Create a list of different kappa values
    kappas = [i + 0.5 for i in range(1,10)]

    # Ireate through the possible kappa values
    for kappa in kappas:

        # Add a new ForwardRun object to the list
        loewner_runs.append(SqrtCubicRun(kappa_driving))

        # Set the ForwardRun properties
        loewner_runs[-1].final_time = 1
        loewner_runs[-1].start_time = 0
        loewner_runs[-1].outer_points = 1000
        loewner_runs[-1].inner_points = 10

        # Set the kappa value for the ForwardRun
        loewner_runs[-1].sqrt_param = kappa

    # Return the list
    return loewner_runs

