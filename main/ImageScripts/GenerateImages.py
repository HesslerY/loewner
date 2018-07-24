import sys
sys.path.append('../PythonTools')

import Constants
from LoewnerRun import LoewnerRun
from numpy import savetxt, column_stack, full_like, linspace

# Declare final time for Loewner runs
final_time = 25

# Create a list of LoewnerRun objects for the different driving functions
def create_loewner_runs():

    # Create an empty list for LoewnerRun objects
    loewner_runs = []

    # Iterate through the driving functions
    for driving_function in range(Constants.TOTAL_DRIVING_FUNCTIONS):

        # Check that the driving function is not kappa or c_alpha
        if not Constants.SQUAREROOT_DRIVING(driving_function):

            # Add a LoewnerRun object to the list that corresponds with the current driving function
            loewner_runs.append(LoewnerRun(driving_function))

            # Set the properties of the LoewnerRun
            loewner_runs[-1].final_time = 25
            loewner_runs[-1].start_time = 0
            loewner_runs[-1].outer_points = 1000
            loewner_runs[-1].inner_points = 10

    loewner_runs[0].constant_param = 0

    # Return list
    return loewner_runs

# Create a list of SqrtLoewnerRun objects for kappa-driving
def create_kappa_runs():

    # Define the kappa driving index
    kappa_driving = 10

    # Create an empty list for LoewnerRun objects
    loewner_runs = []

    # Create a list of different kappa values
    kappas = [i + 0.5 for i in range(1,10)]

    # Ireate through the possible kappa values
    for kappa in kappas:

        # Add a new LoewnerRun object to the list
        loewner_runs.append(LoewnerRun(kappa_driving))

        # Set the LoewnerRun properties
        loewner_runs[-1].final_time = 1
        loewner_runs[-1].start_time = 0
        loewner_runs[-1].outer_points = 1000
        loewner_runs[-1].inner_points = 10

        # Set the kappa value for the LoewnerRun
        loewner_runs[-1].sqrt_param = kappa

    # Return the list
    return loewner_runs

# Create a list of SqrtLoewnerRun objects for calpha-driving
def create_calpha_runs():

    calpha_driving = 11

    loewner_runs = []
    alphas = [i * 0.1 for i in range(1,10)]

    for alpha in alphas:
        loewner_runs.append(LoewnerRun(11))
        loewner_runs[-1].final_time = 25
        loewner_runs[-1].start_time = 0
        loewner_runs[-1].outer_points = 1000
        loewner_runs[-1].inner_points = 10
        loewner_runs[-1].sqrt_param = alpha

    return loewner_runs

# Create three lists of LoewnerRuns
loewner_runs = create_loewner_runs()
kappa_runs = create_kappa_runs()
calpha_runs = create_calpha_runs()

loewner_runs[1].perform_linear_quad_exact(True,True)
loewner_runs[0].final_time = 10
loewner_runs[0].perform_constant_cubic_exact(True,True)
loewner_runs[0].final_time = 25

for run in loewner_runs:

    run.run("Forward")
    run.run("Inverse")

    run.final_time = 10

    if run.driving_function == 0:
        run.constant_param = 1

    run.run("Cubic")

    print("Finished driving function " + str(run.driving_function))

exact_sol_res = [5,50,100,200,300,400,500]
run = loewner_runs[1]

for res in exact_sol_res:

    run.inner_points = res
    run.run("Forward")

constant_final_times = [1,4,9,16]
constant_run = loewner_runs[0]

for final in constant_final_times:

    constant_run.final_time = final
    run.run("Forward")

for run in kappa_runs:

    run.run("Forward")
    run.run("Inverse")

for run in calpha_runs:

    run.run("Forward")
    run.run("Inverse")

