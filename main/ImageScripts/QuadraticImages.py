import sys
sys.path.append('../LoewnerRun')

import Constants
from QuadraticRun import QuadraticRun, SqrtQuadraticRun, ExactQuadraticRun
from InverseRun import InverseRun
from LoewnerPlot import LoewnerPlot, MultiLoewnerPlot, InverseLoewnerPlot, MiniLoewnerPlot, InverseMultiLoewnerPlot
from numpy import savetxt, column_stack, full_like, linspace

# Declare final time for Loewner runs
final_time = 25

# Create a list of QuadraticRun objects for the different driving functions
def create_loewner_runs():

    # Create an empty list for QuadraticRun objects
    loewner_runs = []

    # Iterate through the driving functions
    for driving_function in range(Constants.TOTAL_DRIVING_FUNCTIONS):

        # Check that the driving function is not kappa or c_alpha
        if not Constants.squareroot_driving(driving_function):

            # Add a QuadraticRun object to the list that corresponds with the current driving function
            loewner_runs.append(QuadraticRun(driving_function))

            # Set the properties of the QuadraticRun
            loewner_runs[-1].final_time = 25
            loewner_runs[-1].start_time = 0
            loewner_runs[-1].outer_points = 1000
            loewner_runs[-1].inner_points = 10

    # Return list
    return loewner_runs

# Create a list of SqrtQuadraticRun objects for kappa-driving
def create_kappa_runs():

    # Define the kappa driving index
    kappa_driving = 10

    # Create an empty list for QuadraticRun objects
    loewner_runs = []

    # Create a list of different kappa values
    kappas = [i + 0.5 for i in range(1,10)]

    # Ireate through the possible kappa values
    for kappa in kappas:

        # Add a new QuadraticRun object to the list
        loewner_runs.append(SqrtQuadraticRun(kappa_driving))

        # Set the QuadraticRun properties
        loewner_runs[-1].final_time = 1
        loewner_runs[-1].start_time = 0
        loewner_runs[-1].outer_points = 1000
        loewner_runs[-1].inner_points = 10

        # Set the kappa value for the QuadraticRun
        loewner_runs[-1].sqrt_param = kappa

    # Return the list
    return loewner_runs

# Create a list of SqrtQuadraticRun objects for calpha-driving
def create_calpha_runs():

    calpha_driving = 11

    loewner_runs = []
    alphas = [i * 0.1 for i in range(1,10)]

    for alpha in alphas:
        loewner_runs.append(SqrtQuadraticRun(11))
        loewner_runs[-1].final_time = 25
        loewner_runs[-1].start_time = 0
        loewner_runs[-1].outer_points = 1000
        loewner_runs[-1].inner_points = 10
        loewner_runs[-1].sqrt_param = alpha

    return loewner_runs

# Create three lists of QuadraticRuns
loewner_runs = create_loewner_runs()
kappa_runs = create_kappa_runs()
calpha_runs = create_calpha_runs()

for run in loewner_runs:

    run.perform_loewner()
    run.save_to_dat()

    inverse_loewner = InverseRun(run)
    inverse_loewner.perform_inverse()
    inverse_loewner.save_to_dat()

    print("Finished driving function " + str(run.driving_function))

exact_sol_res = [5,50,100,200,300,400,500]
run = loewner_runs[1]

for res in exact_sol_res:

    run.inner_points = res
    run.perform_loewner()
    run.save_to_dat()

constant_final_times = [1,4,9,16]
constant_run = loewner_runs[0]

for final in constant_final_times:

    constant_run.final_time = final
    constant_run.perform_loewner()
    constant_run.save_to_dat() 

for run in kappa_runs:

    run.perform_loewner()
    
    run.save_to_dat()

    inverse_loewner = InverseRun(run)
    inverse_loewner.perform_inverse()

    inverse_loewner.save_to_dat() 

for run in calpha_runs:

    run.perform_loewner()
   
    run.save_to_dat()

    inverse_loewner = InverseRun(run)
    inverse_loewner.perform_inverse()

    inverse_loewner.save_to_dat() 

