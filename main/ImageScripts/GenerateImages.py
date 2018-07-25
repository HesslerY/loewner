import sys
sys.path.append('../PythonTools')
import Constants
from LoewnerRunFactory import LoewnerRunFactory

# Declare final time for Loewner runs
start_time = 0
final_time = 25
outer_points = 1000
inner_points = 10
compile_modules = False
save_plot = True
save_data = True

# Create a list of LoewnerRun objects for the different driving functions
def create_loewner_runs():

    # Create an empty list for LoewnerRun objects
    loewner_runs = []

    # Iterate through the driving functions
    for index in range(1,Constants.TOTAL_DRIVING_FUNCTIONS):

        # Check that the driving function is not kappa or c_alpha
        if not Constants.SQUAREROOT_DRIVING(index):

            # Add a LoewnerRun object to the list that corresponds with the current driving function
            loewner_runs.append(LoewnerRunFactory(index,start_time,final_time,outer_points,inner_points,compile_modules,save_plot,save_data))

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
        loewner_runs.append(LoewnerRunFactory(index=kappa_driving,start_time=start_time,final_time=final_time,outer_points=outer_points,inner_points=inner_points,compile_modules=compile_modules,save_plot=save_plot,save_data=save_data,kappa=kappa))

    # Return the list
    return loewner_runs

# Create a list of SqrtLoewnerRun objects for calpha-driving
def create_calpha_runs():

    calpha_driving = 11

    loewner_runs = []
    alphas = [i * 0.1 for i in range(1,10)]

    for alpha in alphas:
        loewner_runs.append(LoewnerRunFactory(index=11,start_time=start_time,final_time=final_time,outer_points=outer_points,inner_points=inner_points,compile_modules=compile_modules,save_plot=save_plot,save_data=save_data,alpha=alpha))

    return loewner_runs

def create_constant_example_runs():

    constant_final_times = [1,4,9,16]

    loewner_runs = []

    for final_time in constant_final_times:

        loewner_runs.append(LoewnerRunFactory(index=0,start_time=start_time,final_time=final_time,outer_points=outer_points,inner_points=inner_points,compile_modules=compile_modules,save_plot=save_plot,save_data=save_data))

    return loewner_runs

# Create three lists of LoewnerRuns
loewner_runs = create_loewner_runs()
kappa_runs = create_kappa_runs()
calpha_runs = create_calpha_runs()
constant_example_runs = create_constant_example_runs()

for run in loewner_runs:

    run.quadratic_forward_loewner()
    run.quadratic_inverse_loewner()

    print("Finished driving function " + str(run.name))

exit()

exact_sol_res = [5,50,100,200,300,400,500]
run = loewner_runs[1]

for res in exact_sol_res:

    run.inner_points = res
    run.run("Forward")

for run in kappa_runs:

    run.run("Forward")
    run.run("Inverse")

for run in calpha_runs:

    run.run("Forward")
    run.run("Inverse")

